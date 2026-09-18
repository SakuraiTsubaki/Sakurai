#include "core_bridge.hpp"

#include <mgba/core/cheats.h>
#include <mgba/core/core.h>
#include <mgba/core/lockstep.h>
#include <mgba/core/serialize.h>
#include <mgba/gba/interface.h>
#include <mgba/internal/gba/sio/lockstep.h>
#include <mgba-util/audio-buffer.h>
#include <mgba-util/patch.h>
#include <mgba-util/vfs.h>

#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fcntl.h>
#include <fstream>
#include <iomanip>
#include <iterator>
#include <limits>
#include <memory>
#include <sstream>
#include <string>
#include <utility>
#include <vector>

namespace {

constexpr unsigned kWidth = 240;
constexpr unsigned kHeight = 160;
constexpr std::size_t kScreenBytes = kWidth * kHeight * 2;
constexpr std::uint32_t kGbaKeyMask = 0x3FF;
constexpr std::size_t kMaxGbaRom = 32u * 1024u * 1024u;
constexpr int kMaxLinkPlayers = 4;
constexpr int kLinkSchedulerPassLimit = 4096;

std::string withoutExtension(const std::string& path) {
    const std::size_t slash = path.find_last_of("/\\");
    const std::size_t dot = path.find_last_of('.');
    if (dot == std::string::npos || (slash != std::string::npos && dot < slash)) {
        return path;
    }
    return path.substr(0, dot);
}

bool fileExists(const std::string& path) {
    std::ifstream in(path, std::ios::binary);
    return static_cast<bool>(in);
}

std::string findLegacyPatchPath(const std::string& romPath) {
    const std::string base = withoutExtension(romPath);
    const std::string ups = base + ".ups";
    if (fileExists(ups)) return ups;
    const std::string ips = base + ".ips";
    if (fileExists(ips)) return ips;
    return {};
}

bool readWholeFile(const std::string& path, std::vector<std::uint8_t>& out) {
    std::ifstream in(path, std::ios::binary);
    if (!in) return false;
    in.seekg(0, std::ios::end);
    const std::streamoff len = in.tellg();
    if (len < 0 || static_cast<std::uint64_t>(len) > kMaxGbaRom) return false;
    in.seekg(0, std::ios::beg);
    out.resize(static_cast<std::size_t>(len));
    if (!out.empty()) {
        in.read(reinterpret_cast<char*>(out.data()), static_cast<std::streamsize>(out.size()));
        if (!in) return false;
    }
    return true;
}

bool writeWholeFile(const std::string& path, const std::vector<std::uint8_t>& data) {
    std::ofstream out(path, std::ios::binary | std::ios::trunc);
    if (!out) return false;
    if (!data.empty()) {
        out.write(reinterpret_cast<const char*>(data.data()),
                  static_cast<std::streamsize>(data.size()));
    }
    return static_cast<bool>(out);
}

std::uint32_t be24(const std::uint8_t* p) {
    return (static_cast<std::uint32_t>(p[0]) << 16) |
           (static_cast<std::uint32_t>(p[1]) << 8) |
           static_cast<std::uint32_t>(p[2]);
}

std::uint16_t be16(const std::uint8_t* p) {
    return static_cast<std::uint16_t>((static_cast<std::uint16_t>(p[0]) << 8) | p[1]);
}

bool exactIpsOutputSize(const std::string& patchPath, std::size_t inputSize, std::size_t& result) {
    std::vector<std::uint8_t> bytes;
    std::ifstream in(patchPath, std::ios::binary);
    if (!in) return false;
    bytes.assign(std::istreambuf_iterator<char>(in), std::istreambuf_iterator<char>());
    if (bytes.size() < 8 || std::memcmp(bytes.data(), "PATCH", 5) != 0) return false;

    std::size_t pos = 5;
    std::size_t maxEnd = inputSize;
    while (true) {
        if (pos + 3 > bytes.size()) return false;
        if (bytes[pos] == 'E' && bytes[pos + 1] == 'O' && bytes[pos + 2] == 'F') {
            pos += 3;
            if (bytes.size() - pos == 3) {
                const std::size_t explicitSize = be24(bytes.data() + pos);
                if (explicitSize > kMaxGbaRom) return false;
                result = explicitSize;
            } else if (bytes.size() != pos) {
                return false;
            } else {
                result = maxEnd;
            }
            return result <= kMaxGbaRom;
        }

        const std::size_t offset = be24(bytes.data() + pos);
        pos += 3;
        if (pos + 2 > bytes.size()) return false;
        const std::uint16_t size = be16(bytes.data() + pos);
        pos += 2;

        std::size_t chunkSize = size;
        if (size == 0) {
            if (pos + 3 > bytes.size()) return false;
            chunkSize = be16(bytes.data() + pos);
            pos += 3;
        } else {
            if (pos + size > bytes.size()) return false;
            pos += size;
        }
        if (offset > kMaxGbaRom || chunkSize > kMaxGbaRom - offset) return false;
        maxEnd = std::max(maxEnd, offset + chunkSize);
    }
}

class MgbaLinkCableBridge;

class MgbaCoreBridge final : public CoreBridge {
public:
    MgbaCoreBridge() {
        core_ = mCoreCreate(mPLATFORM_GBA);
        if (!core_) return;

        mCoreInitConfig(core_, "myboy-arm64");
        if (!core_->init(core_)) {
            mCoreConfigDeinit(&core_->config);
            core_ = nullptr;
            return;
        }

        core_->setAudioBufferSize(core_, 4096);

        rotation_.owner = this;
        rotation_.d.sample = &rotationSample;
        rotation_.d.readTiltX = &readTiltX;
        rotation_.d.readTiltY = &readTiltY;
        rotation_.d.readGyroZ = &readGyroZ;
        core_->setPeripheral(core_, mPERIPH_ROTATION, &rotation_.d);

        luminance_.owner = this;
        luminance_.d.sample = &luminanceSample;
        luminance_.d.readLuminance = &readLuminance;
        core_->setPeripheral(core_, mPERIPH_GBA_LUMINANCE, &luminance_.d);

        rumble_.owner = this;
        mRumbleIntegratorInit(&rumble_.d);
        rumble_.d.setRumble = &rumbleChanged;
        core_->setPeripheral(core_, mPERIPH_RUMBLE, &rumble_.d.d);

        core_->setVideoBuffer(core_, fallbackVideo_.data(), kWidth);
        valid_ = true;
    }

    ~MgbaCoreBridge() override {
        if (!core_) return;
        if (romLoaded_) core_->unloadROM(core_);
        mCoreConfigDeinit(&core_->config);
        core_->deinit(core_);
        core_ = nullptr;
    }

    bool loadBios(const std::string& path) override {
        if (!valid_ || path.empty()) return false;
        VFile* vf = VFileOpen(path.c_str(), O_RDONLY);
        if (!vf) return false;
        const bool ok = core_->loadBIOS(core_, vf, 0);
        if (!ok) vf->close(vf);
        if (ok) biosPath_ = path;
        return ok;
    }

    std::string loadRom(const std::string& path, bool autoPatch) override {
        if (!valid_ || path.empty()) return {};
        if (romLoaded_) {
            core_->unloadROM(core_);
            romLoaded_ = false;
        }

        if (!mCoreLoadFile(core_, path.c_str())) return {};

        if (autoPatch) {
            const std::string patchPath = findLegacyPatchPath(path);
            if (!patchPath.empty()) {
                if (VFile* patch = VFileOpen(patchPath.c_str(), O_RDONLY)) {
                    core_->loadPatch(core_, patch);
                    patch->close(patch);
                }
            }
        }

        core_->setVideoBuffer(core_, externalVideo_ ? externalVideo_ : fallbackVideo_.data(), kWidth);
        core_->reset(core_);
        romLoaded_ = true;
        romPath_ = path;
        return path;
    }

    void unloadRom(const std::string&) override {
        if (core_ && romLoaded_) {
            core_->unloadROM(core_);
            romLoaded_ = false;
            romPath_.clear();
        }
    }

    void runFrame(bool) override {
        runOneCoreSlice();
    }

    void setKeys(std::uint32_t keys) override {
        if (core_) core_->setKeys(core_, keys & kGbaKeyMask);
    }

    bool setScreenBuffer(void* address, std::size_t bytes) override {
        if (!core_) return false;
        if (!address) {
            externalVideo_ = nullptr;
            externalVideoBytes_ = 0;
            core_->setVideoBuffer(core_, fallbackVideo_.data(), kWidth);
            return true;
        }
        if (bytes < kScreenBytes) return false;
        externalVideo_ = reinterpret_cast<mColor*>(address);
        externalVideoBytes_ = bytes;
        core_->setVideoBuffer(core_, externalVideo_, kWidth);
        return true;
    }

    int getAudioSamples(std::int16_t* out, int maxShorts) override {
        if (!core_ || !out || maxShorts < 2 || !soundEnabled_) return 0;
        mAudioBuffer* b = core_->getAudioBuffer(core_);
        if (!b) return 0;
        const std::size_t maxFrames = static_cast<std::size_t>(maxShorts / 2);
        const std::size_t frames = std::min(maxFrames, mAudioBufferAvailable(b));
        if (!frames) return 0;
        const std::size_t produced = mAudioBufferRead(b, out, frames);
        return static_cast<int>(produced * 2);
    }

    void enableSound(bool enabled) override {
        soundEnabled_ = enabled;
        if (!enabled && core_) {
            if (mAudioBuffer* b = core_->getAudioBuffer(core_)) mAudioBufferClear(b);
        }
    }

    void reset(bool) override {
        if (core_ && romLoaded_) core_->reset(core_);
    }

    int saveState(const std::string& path) override {
        if (!core_ || !romLoaded_ || path.empty()) return -1;
        VFile* vf = VFileOpen(path.c_str(), O_CREAT | O_TRUNC | O_RDWR);
        if (!vf) return -1;
        const bool ok = mCoreSaveStateNamed(core_, vf, SAVESTATE_SAVEDATA | SAVESTATE_RTC);
        vf->close(vf);
        return ok ? 0 : -1;
    }

    int loadState(const std::string& path) override {
        if (!core_ || !romLoaded_ || path.empty()) return -1;
        VFile* vf = VFileOpen(path.c_str(), O_RDONLY);
        if (!vf) return -1;
        const bool ok = mCoreLoadStateNamed(core_, vf, SAVESTATE_SAVEDATA | SAVESTATE_RTC);
        vf->close(vf);
        return ok ? 0 : -1;
    }

    std::vector<std::uint8_t> saveStateToMemory() override {
        std::vector<std::uint8_t> out;
        if (!core_ || !romLoaded_) return out;
        VFile* vf = VFileMemChunk(nullptr, 0);
        if (!vf) return out;
        if (!mCoreSaveStateNamed(core_, vf, SAVESTATE_SAVEDATA | SAVESTATE_RTC)) {
            vf->close(vf);
            return out;
        }
        const ssize_t size = vf->size(vf);
        if (size <= 0) {
            vf->close(vf);
            return out;
        }
        out.resize(static_cast<std::size_t>(size));
        vf->seek(vf, 0, SEEK_SET);
        const ssize_t got = vf->read(vf, out.data(), out.size());
        vf->close(vf);
        if (got != size) out.clear();
        return out;
    }

    int loadStateFromMemory(const std::uint8_t* data, std::size_t size) override {
        if (!core_ || !romLoaded_ || !data || !size) return -1;
        VFile* vf = VFileFromConstMemory(data, size);
        if (!vf) return -1;
        const bool ok = mCoreLoadStateNamed(core_, vf, SAVESTATE_SAVEDATA | SAVESTATE_RTC);
        vf->close(vf);
        return ok ? 0 : -1;
    }

    void loadBattery(const std::string& path, const std::string& auxPath) override {
        batteryPath_ = path;
        batteryAuxPath_ = auxPath;
        if (!core_ || !romLoaded_ || path.empty()) return;
        std::ifstream in(path, std::ios::binary);
        if (!in) return;
        std::vector<std::uint8_t> data((std::istreambuf_iterator<char>(in)),
                                       std::istreambuf_iterator<char>());
        if (!data.empty()) core_->savedataRestore(core_, data.data(), data.size(), true);
    }

    bool saveBattery() override {
        if (!core_ || !romLoaded_ || batteryPath_.empty()) return false;
        void* sram = nullptr;
        const std::size_t size = core_->savedataClone(core_, &sram);
        if (!sram || !size) {
            std::free(sram);
            return false;
        }
        std::ofstream out(batteryPath_, std::ios::binary | std::ios::trunc);
        if (!out) {
            std::free(sram);
            return false;
        }
        out.write(reinterpret_cast<const char*>(sram), static_cast<std::streamsize>(size));
        const bool ok = static_cast<bool>(out);
        std::free(sram);
        return ok;
    }

    std::vector<std::uint8_t> romCode() override {
        std::vector<std::uint8_t> out;
        if (!core_ || !romLoaded_) return out;
        mGameInfo info{};
        core_->getGameInfo(core_, &info);
        out.assign(reinterpret_cast<std::uint8_t*>(info.code),
                   reinterpret_cast<std::uint8_t*>(info.code) + 4);
        return out;
    }

    std::string romHash() override {
        if (!core_ || !romLoaded_) return {};
        std::array<std::uint8_t, 16> md5{};
        core_->checksum(core_, md5.data(), mCHECKSUM_MD5);
        std::ostringstream ss;
        ss << std::hex << std::setfill('0');
        for (const std::uint8_t b : md5) ss << std::setw(2) << static_cast<unsigned>(b);
        return ss.str();
    }

    int addCheat(const std::string& name, const std::string& code, bool enabled) override {
        if (!core_ || !romLoaded_) return -1;
        mCheatDevice* device = core_->cheatDevice(core_);
        if (!device) return -1;
        const int index = static_cast<int>(mCheatSetsSize(&device->cheats));
        mCheatSet* set = device->createSet(device, name.empty() ? nullptr : name.c_str());
        if (!set) return -1;

        bool any = false;
        std::istringstream input(code);
        std::string line;
        while (std::getline(input, line)) {
            if (!line.empty() && mCheatAddLine(set, line.c_str(), 0)) any = true;
        }
        if (!any && !code.empty()) any = mCheatAddLine(set, code.c_str(), 0);
        if (!any) {
            mCheatSetDeinit(set);
            return -1;
        }
        set->enabled = enabled;
        mCheatAddSet(device, set);
        if (set->refresh) set->refresh(set, device);
        return index;
    }

    void clearCheats() override {
        if (core_) {
            if (mCheatDevice* d = core_->cheatDevice(core_)) mCheatDeviceClear(d);
        }
    }

    void enableCheat(int index, bool enabled) override {
        if (!core_ || index < 0) return;
        mCheatDevice* d = core_->cheatDevice(core_);
        if (!d || static_cast<std::size_t>(index) >= mCheatSetsSize(&d->cheats)) return;
        mCheatSet* set = *mCheatSetsGetPointer(&d->cheats, static_cast<std::size_t>(index));
        if (!set) return;
        set->enabled = enabled;
        if (set->refresh) set->refresh(set, d);
    }

    void enableRumble(bool enabled) override {
        rumbleEnabled_ = enabled;
        if (!enabled) {
            rumblePattern_.clear();
            mRumbleIntegratorReset(&rumble_.d);
        }
    }

    bool getRumblePattern(std::vector<std::int64_t>& patternMs) override {
        patternMs.swap(rumblePattern_);
        return !patternMs.empty();
    }

    void setGyroValue(int value) override { gyro_ = value; }
    void setSolarValue(int value) override {
        solar_ = static_cast<std::uint8_t>(std::clamp(value, 0, 255));
    }
    void setTiltValue(int x, int y) override {
        tiltX_ = x;
        tiltY_ = y;
    }

    void setOption(const std::string& key, const std::string& value) override {
        if (key == "enableCheats") cheatsEnabled_ = (value == "true" || value == "1");
    }

private:
    friend class MgbaLinkCableBridge;

    void runOneCoreSlice() {
        if (!core_ || !romLoaded_) return;
        core_->runFrame(core_);
        if (!soundEnabled_) {
            if (mAudioBuffer* b = core_->getAudioBuffer(core_)) mAudioBufferClear(b);
        }
    }

    std::uint32_t frameCounter() const {
        return core_ ? core_->frameCounter(core_) : 0;
    }

    struct RotationAdapter {
        mRotationSource d{};
        MgbaCoreBridge* owner = nullptr;
    };
    struct LuminanceAdapter {
        GBALuminanceSource d{};
        MgbaCoreBridge* owner = nullptr;
    };
    struct RumbleAdapter {
        mRumbleIntegrator d{};
        MgbaCoreBridge* owner = nullptr;
    };

    static void rotationSample(mRotationSource*) {}
    static std::int32_t readTiltX(mRotationSource* p) {
        return reinterpret_cast<RotationAdapter*>(p)->owner->tiltX_;
    }
    static std::int32_t readTiltY(mRotationSource* p) {
        return reinterpret_cast<RotationAdapter*>(p)->owner->tiltY_;
    }
    static std::int32_t readGyroZ(mRotationSource* p) {
        return reinterpret_cast<RotationAdapter*>(p)->owner->gyro_;
    }
    static void luminanceSample(GBALuminanceSource*) {}
    static std::uint8_t readLuminance(GBALuminanceSource* p) {
        return reinterpret_cast<LuminanceAdapter*>(p)->owner->solar_;
    }
    static void rumbleChanged(mRumbleIntegrator* p, float value) {
        auto* a = reinterpret_cast<RumbleAdapter*>(p);
        if (a->owner->rumbleEnabled_ && value > 0.01f) {
            a->owner->rumblePattern_.assign({0, 16});
        }
    }

    mCore* core_ = nullptr;
    bool valid_ = false;
    bool romLoaded_ = false;
    bool soundEnabled_ = true;
    bool rumbleEnabled_ = false;
    bool cheatsEnabled_ = true;

    std::string romPath_;
    std::string biosPath_;
    std::string batteryPath_;
    std::string batteryAuxPath_;

    std::array<mColor, kWidth * kHeight> fallbackVideo_{};
    mColor* externalVideo_ = nullptr;
    std::size_t externalVideoBytes_ = 0;

    RotationAdapter rotation_{};
    LuminanceAdapter luminance_{};
    RumbleAdapter rumble_{};
    std::vector<std::int64_t> rumblePattern_;

    int tiltX_ = 0;
    int tiltY_ = 0;
    int gyro_ = 0;
    std::uint8_t solar_ = 0;
};

class MgbaLinkCableBridge final : public LinkCableBridge {
public:
    MgbaLinkCableBridge() {
        GBASIOLockstepCoordinatorInit(&coordinator_);
        coordinatorReady_ = true;
    }

    ~MgbaLinkCableBridge() override {
        while (!nodes_.empty()) detach(nodes_.back()->core);
        if (coordinatorReady_) GBASIOLockstepCoordinatorDeinit(&coordinator_);
    }

    bool attach(const std::shared_ptr<CoreBridge>& bridge, int preferredId) override {
        auto core = std::dynamic_pointer_cast<MgbaCoreBridge>(bridge);
        if (!core || !core->core_ || nodes_.size() >= kMaxLinkPlayers) return false;
        for (const auto& n : nodes_) {
            if (n->core == core) return true;
        }

        auto node = std::make_unique<Node>();
        node->core = std::move(core);
        node->preferredId = std::clamp(preferredId, 0, kMaxLinkPlayers - 1);
        node->user.node = node.get();
        node->user.d.sleep = &sleep;
        node->user.d.wake = &wake;
        node->user.d.requestedId = &requestedId;
        node->user.d.playerIdChanged = &playerIdChanged;
        GBASIOLockstepDriverCreate(&node->driver, &node->user.d);
        nodes_.push_back(std::move(node));

        if (nodes_.size() >= 2) {
            for (auto& n : nodes_) attachNode(*n);
        }
        return true;
    }

    void detach(const std::shared_ptr<CoreBridge>& bridge) override {
        auto core = std::dynamic_pointer_cast<MgbaCoreBridge>(bridge);
        if (!core) return;
        auto it = std::find_if(nodes_.begin(), nodes_.end(),
                               [&](const auto& n) { return n->core == core; });
        if (it == nodes_.end()) return;
        detachNode(**it);
        nodes_.erase(it);
    }

    bool runFrame(bool) override {
        if (nodes_.empty()) return false;
        if (nodes_.size() == 1 && !nodes_[0]->attached) {
            nodes_[0]->core->runOneCoreSlice();
            return true;
        }

        std::array<std::uint32_t, kMaxLinkPlayers> start{};
        for (std::size_t i = 0; i < nodes_.size(); ++i) {
            start[i] = nodes_[i]->core->frameCounter();
        }

        for (int pass = 0; pass < kLinkSchedulerPassLimit; ++pass) {
            bool allDone = true;
            bool runnable = false;
            for (std::size_t i = 0; i < nodes_.size(); ++i) {
                Node& node = *nodes_[i];
                if (node.core->frameCounter() != start[i]) continue;
                allDone = false;
                if (node.asleep) continue;
                runnable = true;
                node.core->runOneCoreSlice();
            }
            if (allDone) return true;
            if (!runnable) return false;
        }
        return false;
    }

    std::size_t size() const override { return nodes_.size(); }

private:
    struct Node;
    struct User {
        mLockstepUser d{};
        Node* node = nullptr;
    };
    struct Node {
        std::shared_ptr<MgbaCoreBridge> core;
        GBASIOLockstepDriver driver{};
        User user{};
        bool attached = false;
        bool asleep = false;
        int preferredId = 0;
        int actualId = -1;
    };

    static Node* nodeFromUser(mLockstepUser* user) {
        return reinterpret_cast<User*>(user)->node;
    }
    static void sleep(mLockstepUser* user) { nodeFromUser(user)->asleep = true; }
    static void wake(mLockstepUser* user) { nodeFromUser(user)->asleep = false; }
    static int requestedId(mLockstepUser* user) { return nodeFromUser(user)->preferredId; }
    static void playerIdChanged(mLockstepUser* user, int id) { nodeFromUser(user)->actualId = id; }

    void attachNode(Node& node) {
        if (node.attached) return;
        GBASIOLockstepCoordinatorAttach(&coordinator_, &node.driver);
        node.core->core_->setPeripheral(node.core->core_, mPERIPH_GBA_LINK_PORT, &node.driver.d);
        node.attached = true;
        node.asleep = false;
    }

    void detachNode(Node& node) {
        if (!node.attached || !node.core->core_) return;
        node.core->core_->setPeripheral(node.core->core_, mPERIPH_GBA_LINK_PORT, nullptr);
        GBASIOLockstepCoordinatorDetach(&coordinator_, &node.driver);
        node.attached = false;
        node.asleep = false;
    }

    GBASIOLockstepCoordinator coordinator_{};
    bool coordinatorReady_ = false;
    std::vector<std::unique_ptr<Node>> nodes_;
};

} // namespace

std::shared_ptr<CoreBridge> makeCoreBridge() {
    return std::make_shared<MgbaCoreBridge>();
}

std::shared_ptr<LinkCableBridge> makeLinkCableBridge() {
    return std::make_shared<MgbaLinkCableBridge>();
}

int applyLegacyPatchFile(const std::string& outputPath, const std::string& romPath) {
    const std::string patchPath = findLegacyPatchPath(romPath);
    if (patchPath.empty()) return -1;

    std::vector<std::uint8_t> input;
    if (!readWholeFile(romPath, input)) return -2;

    VFile* patchVf = VFileOpen(patchPath.c_str(), O_RDONLY);
    if (!patchVf) return -2;

    Patch patch{};
    if (!loadPatch(patchVf, &patch)) {
        patchVf->close(patchVf);
        return -3;
    }

    std::size_t outputSize = 0;
    const bool ips = patchPath.size() >= 4 &&
                     patchPath.compare(patchPath.size() - 4, 4, ".ips") == 0;
    if (ips) {
        if (!exactIpsOutputSize(patchPath, input.size(), outputSize)) {
            patchVf->close(patchVf);
            return -3;
        }
    } else {
        outputSize = patch.outputSize(&patch, input.size());
        if (!outputSize) {
            patchVf->close(patchVf);
            return -4;
        }
    }

    if (!outputSize || outputSize > kMaxGbaRom) {
        patchVf->close(patchVf);
        return -3;
    }

    std::vector<std::uint8_t> output(outputSize, 0);
    const bool ok = patch.applyPatch(&patch, input.data(), input.size(),
                                     output.data(), output.size());
    patchVf->close(patchVf);
    if (!ok) return -4;
    if (!writeWholeFile(outputPath, output)) return -2;
    return 0;
}
