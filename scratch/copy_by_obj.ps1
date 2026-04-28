$folder = Get-ChildItem "C:\Users\Sasha  Baron\Documents\1.*" | Select-Object -First 1
$file = Get-ChildItem $folder.FullName | Where-Object { $_.Name -like "*Техническое*" -or $_.Name -like "*12-49-4750*" } | Select-Object -First 1
if ($file) {
    Copy-Item $file.FullName "c:\ANTIGRAVITY\1\scratch\main_tz.pdf" -Force
    Write-Host "Success: $($file.Name)"
} else {
    Write-Host "Still not found by name filter, trying index..."
    $file = (Get-ChildItem $folder.FullName)[-2] # Based on previous list, it was near the end
    Copy-Item $file.FullName "c:\ANTIGRAVITY\1\scratch\main_tz.pdf" -Force
    Write-Host "Copied by index: $($file.Name)"
}
