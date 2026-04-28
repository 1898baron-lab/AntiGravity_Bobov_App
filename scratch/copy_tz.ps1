$file = Get-ChildItem "C:\Users\Sasha  Baron\Documents\1.*" | Get-ChildItem -Filter "*Техническое*" | Select-Object -First 1
if ($file) {
    Copy-Item $file.FullName "c:\ANTIGRAVITY\1\scratch\main_tz.pdf" -Force
    Write-Host "Success: $($file.FullName)"
} else {
    Write-Host "File not found"
}
