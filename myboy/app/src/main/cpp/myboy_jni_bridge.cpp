#include <jni.h>
#include <android/log.h>

#include <algorithm>
#include <atomic>
#include <cstdint>
#include <fstream>
#include <memory>
#include <mutex>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>

#include "core_bridge.hpp"

#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR, "MyBoyArm64", __VA_ARGS__)
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO,  "MyBoyArm64", __VA_ARGS__)

namespace {

struct LinkContext {
    jobject linkGlobal = nullptr;
    std::string biosPath;
    std::string romPath;
    bool autoPatch = false;
    std::vector<jint> handles;
    std::shared_ptr<LinkCableBridge> cable;
};

std::mutex gMutex;
std::unordered_map<jint, std::shared_ptr<CoreBridge>> gCores;
std::vector<std::unique_ptr<LinkContext>> gLinks;
std::atomic<jint> gNextHandle{1};

jfieldID gNativeConsoleField = nullptr;
jobject gGameSaveListener = nullptr;
jmethodID gOnGameSaved = nullptr;

std::string jstr(JNIEnv* env, jstring s) {
    if (!s) return {};
    const char* p = env->GetStringUTFChars(s, nullptr);
    std::string out = p ? p : "";
    if (p) env->ReleaseStringUTFChars(s, p);
    return out;
}

jbyteArray toByteArray(JNIEnv* env, const std::vector<std::uint8_t>& v) {
    jbyteArray out = env->NewByteArray(static_cast<jsize>(v.size()));
    if (out && !v.empty()) {
        env->SetByteArrayRegion(out, 0, static_cast<jsize>(v.size()),
                                reinterpret_cast<const jbyte*>(v.data()));
    }
    return out;
}

LinkContext* findLinkLocked(JNIEnv* env, jobject link) {
    for (auto& ctx : gLinks) {
        if (ctx->linkGlobal && env->IsSameObject(ctx->linkGlobal, link)) {
            return ctx.get();
        }
    }
    return nullptr;
}

LinkContext* getOrCreateLink(JNIEnv* env, jobject link) {
    std::lock_guard<std::mutex> lock(gMutex);
    if (auto* found = findLinkLocked(env, link)) return found;

    auto ctx = std::make_unique<LinkContext>();
    ctx->linkGlobal = env->NewGlobalRef(link);
    ctx->cable = makeLinkCableBridge();
    LinkContext* raw = ctx.get();
    gLinks.emplace_back(std::move(ctx));
    return raw;
}

std::shared_ptr<CoreBridge> coreForHandle(jint h) {
    std::lock_guard<std::mutex> lock(gMutex);
    auto it = gCores.find(h);
    return it == gCores.end() ? nullptr : it->second;
}

jint handleFromConsole(JNIEnv* env, jobject console) {
    if (!console || !gNativeConsoleField) return 0;
    return env->GetIntField(console, gNativeConsoleField);
}

std::shared_ptr<CoreBridge> coreForConsole(JNIEnv* env, jobject console) {
    return coreForHandle(handleFromConsole(env, console));
}

void removeHandleFromLinkLocked(LinkContext* ctx, jint h) {
    if (!ctx) return;
    ctx->handles.erase(std::remove(ctx->handles.begin(), ctx->handles.end(), h),
                       ctx->handles.end());
}

void notifyGameSaved(JNIEnv* env, bool ok) {
    std::lock_guard<std::mutex> lock(gMutex);
    if (gGameSaveListener && gOnGameSaved) {
        env->CallVoidMethod(gGameSaveListener, gOnGameSaved, ok ? JNI_TRUE : JNI_FALSE);
        if (env->ExceptionCheck()) {
            env->ExceptionClear();
        }
    }
}

bool fileReadable(const std::string& path) {
    if (path.empty()) return false;
    std::ifstream f(path, std::ios::binary);
    return static_cast<bool>(f);
}

} // namespace

extern "C" JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM*, void*) {
    return JNI_VERSION_1_6;
}

extern "C" JNIEXPORT void JNICALL
Java_com_fastemulator_gba_Console_nativeInitIds(JNIEnv* env, jclass clazz) {
    gNativeConsoleField = env->GetFieldID(clazz, "nativeConsole", "I");
    if (!gNativeConsoleField) LOGE("Console.nativeConsole:I not found");
}

extern "C" JNIEXPORT void JNICALL
Java_com_fastemulator_gba_Console_setGameSaveListener(JNIEnv* env, jclass, jobject listener) {
    std::lock_guard<std::mutex> lock(gMutex);
    if (gGameSaveListener) {
        env->DeleteGlobalRef(gGameSaveListener);
        gGameSaveListener = nullptr;
    }
    gOnGameSaved = nullptr;

    if (listener) {
        gGameSaveListener = env->NewGlobalRef(listener);
        jclass cls = env->GetObjectClass(listener);
        gOnGameSaved = env->GetMethodID(cls, "onGameSaved", "(Z)V");
        env->DeleteLocalRef(cls);
    }
}

extern "C" JNIEXPORT jint JNICALL
Java_com_fastemulator_gba_Link_nativeOpenConsole(
        JNIEnv* env, jobject self, jstring path, jint order) {
    const std::string rom = jstr(env, path);
    if (rom.empty()) return 0;

    LinkContext* link = getOrCreateLink(env, self);
    auto core = makeCoreBridge();
    if (!core) return 0;

    std::string bios;
    bool autoPatch = false;
    std::shared_ptr<LinkCableBridge> cable;
    {
        std::lock_guard<std::mutex> lock(gMutex);
        bios = link->biosPath;
        autoPatch = link->autoPatch;
        cable = link->cable;
    }
    if (!bios.empty()) core->loadBios(bios);
    if (core->loadRom(rom, autoPatch).empty()) return 0;

    if (!cable || !cable->attach(core, order)) return 0;

    jint h = gNextHandle.fetch_add(1);
    if (h <= 0) h = gNextHandle.fetch_add(1);
    {
        std::lock_guard<std::mutex> lock(gMutex);
        gCores[h] = core;
        link->handles.push_back(h);
    }
    return h;
}

extern "C" JNIEXPORT void JNICALL
Java_com_fastemulator_gba_Link_nativeCloseConsole(
        JNIEnv* env, jobject self, jobject console) {
    if (!console || !gNativeConsoleField) return;
    const jint h = env->GetIntField(console, gNativeConsoleField);

    std::shared_ptr<CoreBridge> core;
    std::shared_ptr<LinkCableBridge> cable;
    {
        std::lock_guard<std::mutex> lock(gMutex);
        LinkContext* link = findLinkLocked(env, self);
        if (link) cable = link->cable;
        auto it = gCores.find(h);
        if (it != gCores.end()) core = it->second;
    }
    if (cable && core) cable->detach(core);

    {
        std::lock_guard<std::mutex> lock(gMutex);
        LinkContext* link = findLinkLocked(env, self);
        removeHandleFromLinkLocked(link, h);
        gCores.erase(h);
    }
    env->SetIntField(console, gNativeConsoleField, 0);
}

extern "C" JNIEXPORT jboolean JNICALL
Java_com_fastemulator_gba_Link_loadBios(JNIEnv* env, jobject self, jstring path) {
    std::string p = jstr(env, path);
    if (!fileReadable(p)) return JNI_FALSE;

    auto probe = makeCoreBridge();
    if (!probe || !probe->loadBios(p)) return JNI_FALSE;

    LinkContext* link = getOrCreateLink(env, self);
    {
        std::lock_guard<std::mutex> lock(gMutex);
        link->biosPath = p;
    }
    return JNI_TRUE;
}

extern "C" JNIEXPORT jstring JNICALL
Java_com_fastemulator_gba_Link_loadRom(
        JNIEnv* env, jobject self, jstring path, jboolean autoPatch) {
    std::string p = jstr(env, path);
    if (!fileReadable(p)) return nullptr;

    auto probe = makeCoreBridge();
    if (!probe) return nullptr;

    LinkContext* link = getOrCreateLink(env, self);
    std::string bios;
    {
        std::lock_guard<std::mutex> lock(gMutex);
        bios = link->biosPath;
    }
    if (!bios.empty()) probe->loadBios(bios);

    const bool doAutoPatch = autoPatch == JNI_TRUE;
    std::string result = probe->loadRom(p, doAutoPatch);
    if (result.empty()) return nullptr;

    {
        std::lock_guard<std::mutex> lock(gMutex);
        link->romPath = result;
        link->autoPatch = doAutoPatch;
    }
    return env->NewStringUTF(result.c_str());
}

extern "C" JNIEXPORT void JNICALL
Java_com_fastemulator_gba_Link_unloadRom(JNIEnv* env, jobject self, jstring /*path*/) {
    LinkContext* link = getOrCreateLink(env, self);
    std::lock_guard<std::mutex> lock(gMutex);
    link->romPath.clear();
    link->autoPatch = false;
}

extern "C" JNIEXPORT void JNICALL
Java_com_fastemulator_gba_Link_runFrame(JNIEnv* env, jobject self, jboolean render) {
    std::shared_ptr<LinkCableBridge> cable;
    {
        std::lock_guard<std::mutex> lock(gMutex);
        LinkContext* link = findLinkLocked(env, self);
        if (!link) return;
        cable = link->cable;
    }
    if (cable && !cable->runFrame(render == JNI_TRUE)) {
        LOGE("mGBA link lockstep scheduler did not complete a frame");
    }
}

extern "C" JNIEXPORT jint JNICALL
Java_com_fastemulator_gba_Link_patchRom(
        JNIEnv* env, jclass, jstring outputPath, jstring romPath) {
    return applyLegacyPatchFile(jstr(env, outputPath), jstr(env, romPath));
}

extern "C" JNIEXPORT void JNICALL
Java_com_fastemulator_gba_Console_setKeys(JNIEnv* env, jobject self, jint keys) {
    if (auto core = coreForConsole(env, self)) {
        core->setKeys(static_cast<std::uint32_t>(keys));
    }
}

extern "C" JNIEXPORT void JNICALL
Java_com_fastemulator_gba_Console_setScreenBuffer(JNIEnv* env, jobject self, jobject buffer) {
    auto core = coreForConsole(env, self);
    if (!core) return;

    if (!buffer) {
        core->setScreenBuffer(nullptr, 0);
        return;
    }

    void* address = env->GetDirectBufferAddress(buffer);
    jlong capacity = env->GetDirectBufferCapacity(buffer);
    if (!address || capacity < 0 ||
        !core->setScreenBuffer(address, static_cast<std::size_t>(capacity))) {
        LOGE("setScreenBuffer: expected direct RGB565 buffer >= 76800 bytes");
    }
}

extern "C" JNIEXPORT jint JNICALL
Java_com_fastemulator_gba_Console_getAudioSamples(
        JNIEnv* env, jobject self, jshortArray samples, jint maxShorts) {
    auto core = coreForConsole(env, self);
    if (!core || !samples || maxShorts <= 0) return 0;

    jsize arrayLen = env->GetArrayLength(samples);
    int cap = std::min<int>(arrayLen, maxShorts);
    std::vector<std::int16_t> temp(static_cast<std::size_t>(cap));
    int written = core->getAudioSamples(temp.data(), cap);
    written = std::clamp(written, 0, cap);

    if (written > 0) {
        env->SetShortArrayRegion(samples, 0, written,
                                 reinterpret_cast<const jshort*>(temp.data()));
    }
    return written;
}

extern "C" JNIEXPORT void JNICALL
Java_com_fastemulator_gba_Console_enableSound(JNIEnv* env, jobject self, jboolean enabled) {
    if (auto core = coreForConsole(env, self)) core->enableSound(enabled == JNI_TRUE);
}

extern "C" JNIEXPORT void JNICALL
Java_com_fastemulator_gba_Console_reset(JNIEnv* env, jobject self, jboolean hard) {
    if (auto core = coreForConsole(env, self)) core->reset(hard == JNI_TRUE);
}

extern "C" JNIEXPORT jint JNICALL
Java_com_fastemulator_gba_Console_saveState(JNIEnv* env, jobject self, jstring path) {
    auto core = coreForConsole(env, self);
    return core ? core->saveState(jstr(env, path)) : -1;
}

extern "C" JNIEXPORT jint JNICALL
Java_com_fastemulator_gba_Console_loadState(JNIEnv* env, jobject self, jstring path) {
    auto core = coreForConsole(env, self);
    return core ? core->loadState(jstr(env, path)) : -1;
}

extern "C" JNIEXPORT jbyteArray JNICALL
Java_com_fastemulator_gba_Console_saveStateToMemory(JNIEnv* env, jobject self) {
    auto core = coreForConsole(env, self);
    return core ? toByteArray(env, core->saveStateToMemory()) : nullptr;
}

extern "C" JNIEXPORT jint JNICALL
Java_com_fastemulator_gba_Console_loadStateFromMemory(
        JNIEnv* env, jobject self, jbyteArray data) {
    auto core = coreForConsole(env, self);
    if (!core || !data) return -1;

    jsize n = env->GetArrayLength(data);
    std::vector<std::uint8_t> temp(static_cast<std::size_t>(n));
    if (n > 0) {
        env->GetByteArrayRegion(data, 0, n, reinterpret_cast<jbyte*>(temp.data()));
    }
    return core->loadStateFromMemory(temp.data(), temp.size());
}

extern "C" JNIEXPORT void JNICALL
Java_com_fastemulator_gba_Console_loadBattery(
        JNIEnv* env, jobject self, jstring path, jstring auxPath) {
    if (auto core = coreForConsole(env, self)) {
        core->loadBattery(jstr(env, path), jstr(env, auxPath));
    }
}

extern "C" JNIEXPORT void JNICALL
Java_com_fastemulator_gba_Console_saveBattery(JNIEnv* env, jobject self) {
    bool ok = false;
    if (auto core = coreForConsole(env, self)) ok = core->saveBattery();
    notifyGameSaved(env, ok);
}

extern "C" JNIEXPORT jbyteArray JNICALL
Java_com_fastemulator_gba_Console_getRomCode(JNIEnv* env, jobject self) {
    auto core = coreForConsole(env, self);
    return core ? toByteArray(env, core->romCode()) : nullptr;
}

extern "C" JNIEXPORT jstring JNICALL
Java_com_fastemulator_gba_Console_getRomHash(JNIEnv* env, jobject self) {
    auto core = coreForConsole(env, self);
    if (!core) return nullptr;
    std::string hash = core->romHash();
    return hash.empty() ? nullptr : env->NewStringUTF(hash.c_str());
}

extern "C" JNIEXPORT jint JNICALL
Java_com_fastemulator_gba_Console_addCheat(
        JNIEnv* env, jobject self, jstring name, jstring code, jboolean enabled) {
    auto core = coreForConsole(env, self);
    return core ? core->addCheat(jstr(env, name), jstr(env, code), enabled == JNI_TRUE) : -1;
}

extern "C" JNIEXPORT void JNICALL
Java_com_fastemulator_gba_Console_clearCheats(JNIEnv* env, jobject self) {
    if (auto core = coreForConsole(env, self)) core->clearCheats();
}

extern "C" JNIEXPORT void JNICALL
Java_com_fastemulator_gba_Console_enableCheat(
        JNIEnv* env, jobject self, jint index, jboolean enabled) {
    if (auto core = coreForConsole(env, self)) core->enableCheat(index, enabled == JNI_TRUE);
}

extern "C" JNIEXPORT void JNICALL
Java_com_fastemulator_gba_Console_enableRumble(JNIEnv* env, jobject self, jboolean enabled) {
    if (auto core = coreForConsole(env, self)) core->enableRumble(enabled == JNI_TRUE);
}

extern "C" JNIEXPORT jboolean JNICALL
Java_com_fastemulator_gba_Console_getRumblePattern(
        JNIEnv* env, jobject self, jlongArray pattern) {
    auto core = coreForConsole(env, self);
    if (!core || !pattern) return JNI_FALSE;

    std::vector<std::int64_t> values;
    if (!core->getRumblePattern(values)) return JNI_FALSE;

    jsize cap = env->GetArrayLength(pattern);
    jsize n = std::min<jsize>(cap, static_cast<jsize>(values.size()));
    if (n > 0) {
        env->SetLongArrayRegion(pattern, 0, n,
                                reinterpret_cast<const jlong*>(values.data()));
    }
    return JNI_TRUE;
}

extern "C" JNIEXPORT void JNICALL
Java_com_fastemulator_gba_Console_setGyroValue(JNIEnv* env, jobject self, jint value) {
    if (auto core = coreForConsole(env, self)) core->setGyroValue(value);
}

extern "C" JNIEXPORT void JNICALL
Java_com_fastemulator_gba_Console_setSolarValue(JNIEnv* env, jobject self, jint value) {
    if (auto core = coreForConsole(env, self)) core->setSolarValue(value);
}

extern "C" JNIEXPORT void JNICALL
Java_com_fastemulator_gba_Console_setTiltValue(JNIEnv* env, jobject self, jint x, jint y) {
    if (auto core = coreForConsole(env, self)) core->setTiltValue(x, y);
}

extern "C" JNIEXPORT void JNICALL
Java_com_fastemulator_gba_Console_setOption(
        JNIEnv* env, jobject self, jstring key, jstring value) {
    if (auto core = coreForConsole(env, self)) {
        core->setOption(jstr(env, key), jstr(env, value));
    }
}
