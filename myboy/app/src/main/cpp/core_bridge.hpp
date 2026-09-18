#pragma once
#include <cstddef>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

class CoreBridge {
public:
    virtual ~CoreBridge() = default;
    virtual bool loadBios(const std::string& path) = 0;
    virtual std::string loadRom(const std::string& path, bool autoPatch) = 0;
    virtual void unloadRom(const std::string& path) = 0;
    virtual void runFrame(bool render) = 0;
    virtual void setKeys(std::uint32_t keys) = 0;
    virtual bool setScreenBuffer(void* address, std::size_t bytes) = 0;
    virtual int getAudioSamples(std::int16_t* out, int maxShorts) = 0;
    virtual void enableSound(bool enabled) = 0;
    virtual void reset(bool hard) = 0;
    virtual int saveState(const std::string& path) = 0;
    virtual int loadState(const std::string& path) = 0;
    virtual std::vector<std::uint8_t> saveStateToMemory() = 0;
    virtual int loadStateFromMemory(const std::uint8_t* data, std::size_t size) = 0;
    virtual void loadBattery(const std::string& path, const std::string& auxPath) = 0;
    virtual bool saveBattery() = 0;
    virtual std::vector<std::uint8_t> romCode() = 0;
    virtual std::string romHash() = 0;
    virtual int addCheat(const std::string& name, const std::string& code, bool enabled) = 0;
    virtual void clearCheats() = 0;
    virtual void enableCheat(int index, bool enabled) = 0;
    virtual void enableRumble(bool enabled) = 0;
    virtual bool getRumblePattern(std::vector<std::int64_t>& patternMs) = 0;
    virtual void setGyroValue(int value) = 0;
    virtual void setSolarValue(int value) = 0;
    virtual void setTiltValue(int x, int y) = 0;
    virtual void setOption(const std::string& key, const std::string& value) = 0;
};

class LinkCableBridge {
public:
    virtual ~LinkCableBridge() = default;
    virtual bool attach(const std::shared_ptr<CoreBridge>& core, int preferredId) = 0;
    virtual void detach(const std::shared_ptr<CoreBridge>& core) = 0;
    virtual bool runFrame(bool render) = 0;
    virtual std::size_t size() const = 0;
};

std::shared_ptr<CoreBridge> makeCoreBridge();
std::shared_ptr<LinkCableBridge> makeLinkCableBridge();

int applyLegacyPatchFile(const std::string& outputPath, const std::string& romPath);
