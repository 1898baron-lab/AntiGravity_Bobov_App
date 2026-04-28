$folder = Get-ChildItem "C:\Users\Sasha  Baron\Documents\1.*" | Select-Object -First 1
$sub = Get-ChildItem -Path "$($folder.FullName)\15.03.05*" | Select-Object -First 1
$file = Get-ChildItem $sub.FullName | Where-Object { $_.Name -match "grok" } | Select-Object -First 1
if ($file) {
    Copy-Item $file.FullName "c:\ANTIGRAVITY\1\scratch\grok_report.pdf" -Force
    Write-Host "Success: $($file.Name)"
} else {
    Write-Host "Grok report not found"
}
