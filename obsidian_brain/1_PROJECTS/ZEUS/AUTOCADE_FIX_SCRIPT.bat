@echo off
:: =========================================================
:: AutoCAD 2024 Licensing Service Recovery Script
:: =========================================================

:: 1. Ensure script runs as Administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This script requires administrative privileges. Please run as Administrator.
    pause
    exit /b 1
)

:: 2. Stop any Autodesk services
sc stop AdskLicensingService >nul 2>&1
sc stop AutodeskGenuineService >nul 2>&1
sc stop AutodeskIdentityManager >nul 2>&1

:: 3. Remove leftover files and folders
rd /s /q "C:\Program Files (x86)\Common Files\Autodesk Shared\AdskLicensing"
rd /s /q "C:\ProgramData\Autodesk\AdskLicensingService"
rd /s /q "C:\Program Files (x86)\Autodesk\Identity Manager"

:: 4. Clean registry entries (if they exist)
reg delete "HKLM\SOFTWARE\Autodesk\AdskLicensing" /f >nul 2>&1
reg delete "HKLM\SOFTWARE\WOW6432Node\Autodesk\AdskLicensing" /f >nul 2>&1

:: 5. Install Autodesk Identity Manager (if installer is present)
set "IDM_PATH=C:\AUTODESK\Installers\IdentityManager\IdentityManagerSetup.exe"
if exist "%IDM_PATH%" (
    echo Installing Autodesk Identity Manager...
    "%IDM_PATH%" /quiet
) else (
    echo Identity Manager installer not found at %IDM_PATH% – you may need to download it manually.
)

:: 6. Install Desktop Licensing Service (if installer is present)
set "LIC_PATH=C:\AUTODESK\Installers\Licensing\AdskLicensing-installer.exe"
if exist "%LIC_PATH%" (
    echo Installing Autodesk Desktop Licensing Service...
    "%LIC_PATH%" /quiet
) else (
    echo Licensing installer not found at %LIC_PATH% – you may need to download it manually.
)

:: 7. Verify service is running
sc query AdskLicensingService | find "RUNNING" >nul
if %errorlevel% equ 0 (
    echo AutoCAD licensing service is now running.
) else (
    echo Failed to start the licensing service. Check Event Viewer for details.
)

:: 8. Launch AutoCAD 2024 (optional)
set "ACAD_PATH=C:\Program Files\Autodesk\AutoCAD 2024\acad.exe"
if exist "%ACAD_PATH%" (
    echo Starting AutoCAD 2024 for final verification...
    start "" "%ACAD_PATH%"
) else (
    echo AutoCAD executable not found at %ACAD_PATH%.
)

pause
