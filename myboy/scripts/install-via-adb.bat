@echo off
setlocal
if "%~1"=="" (
  echo Usage: install-via-adb.bat MyBoy-1.8.0-arm64-v2v3.apk
  exit /b 2
)
where adb >nul 2>nul || (
  echo ERROR: adb not found. Install Android SDK Platform-Tools first.
  exit /b 3
)
echo.
echo === Connected devices ===
adb devices
echo.
echo === Package check ===
adb shell pm path com.fastemulator.gba 2>nul
echo.
echo === Installing APK directly via adb ===
adb install --no-incremental "%~1"
echo.
echo If installation failed, copy the exact "Failure [INSTALL_FAILED_...]" line.
endlocal
