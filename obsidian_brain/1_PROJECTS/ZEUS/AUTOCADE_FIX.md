# AutoCAD 2024 Licensing Service Recovery Guide

## Overview
This guide provides a repeatable, low‑risk procedure to restore the **Autodesk Desktop Licensing Service** (`AdskLicensingService`) for **AutoCAD 2024** when it fails to start or reports *"License manager is not functioning or is improperly installed"*.

## Prerequisites
1. **Administrator rights** on the machine.
2. **Revo Uninstaller Pro** (or an equivalent uninstall utility) – located in `C:\Users\Sasha  Baron\Desktop\SOFT\Revo Uninstaller Pro.lnk`.
3. **Microsoft Edge WebView2 Runtime** – already installed (`C:\Program Files (x86)\Microsoft\EdgeWebView\Application`).
4. **AutoCAD 2024 installer** (the full ISO or offline installer) and **Autodesk Identity Manager** installer (optional, but recommended).

## Step‑by‑Step Procedure

### 1. Stop any running Autodesk services
```powershell
# Open an elevated PowerShell console and run:
Stop-Service -Name "AdskLicensingService" -Force -ErrorAction SilentlyContinue
```
If the service does not exist, ignore the error.

### 2. Fully remove Autodesk licensing remnants
- Launch **Revo Uninstaller Pro** (run as administrator) and choose **"Advanced Uninstall"** for the following entries (if present):
  - Autodesk Desktop Licensing Service
  - Autodesk Identity Manager
  - Autodesk Genuine Service (GUID `{D207E870-6397-417E-B7DD-720BFBE589A3}`)
- After the normal uninstall, let Revo scan for leftover files/registry entries and **delete them**.

- Manually delete the folders (run each command in an elevated CMD):
```cmd
rd /s /q "C:\Program Files (x86)\Common Files\Autodesk Shared\AdskLicensing"
rd /s /q "C:\ProgramData\Autodesk\AdskLicensingService"
rd /s /q "C:\Program Files (x86)\Autodesk\Identity Manager"
```

### 3. Clean the registry (optional, but safe)
```powershell
Remove-Item -Path "HKLM:\SOFTWARE\Autodesk\AdskLicensing" -Recurse -ErrorAction SilentlyContinue
Remove-Item -Path "HKLM:\SOFTWARE\WOW6432Node\Autodesk\AdskLicensing" -Recurse -ErrorAction SilentlyContinue
```

### 4. Re‑install **Autodesk Identity Manager** (if you have the installer)
1. Download the latest version from Autodesk’s portal.
2. Right‑click the installer → **Run as administrator**.
3. Follow the wizard; it will automatically place the required service binaries.

### 5. Re‑install **Autodesk Desktop Licensing Service**
If the Identity Manager installer includes the licensing service, you can skip this step. Otherwise:
1. Locate `AdskLicensing-installer.exe` inside the AutoCAD offline media (usually under `\Setup\Licensing`).
2. Run it **as administrator**.
3. After installation, verify the service exists:
```powershell
Get-Service -Name "AdskLicensingService"
```
It should show `Running`.

### 6. Verify WebView2 Runtime (required for the sign‑in UI)
If the WebView2 folder already exists, you are good. If not, download the Evergreen installer from Microsoft and run it.

### 7. Launch AutoCAD 2024 and activate the license
1. Start **AutoCAD 2024** (right‑click → **Run as administrator** the first time).
2. When prompted, log in with your Autodesk account.
3. The software will contact the licensing service; you should see a *"License validated"* message.

## Troubleshooting Tips
- **"Access denied"** when deleting folders: ensure you are in an elevated command prompt and that no Autodesk processes are running.
- **Service fails to start**: open **Event Viewer → Windows Logs → Application** and look for `AdskLicensingService` errors – they often point to missing `WebView2` or corrupt registry keys.
- **License still invalid**: repeat steps 2‑5, making sure the Identity Manager is freshly installed; a stale token cache can be cleared by deleting `%LOCALAPPDATA%\Autodesk\IdentityManager`.

## Quick One‑Liner for Power Users
```cmd
powershell -Command "Stop-Service -Name AdskLicensingService -Force; rd /s /q 'C:\Program Files (x86)\Common Files\Autodesk Shared\AdskLicensing'; rd /s /q 'C:\ProgramData\Autodesk\AdskLicensingService'; "
```
Run the above, then reinstall the licensing service via the installer.

---
*Prepared by the Antigravity AI assistant – keep this note in your **ZEUS** project for future reference.*
