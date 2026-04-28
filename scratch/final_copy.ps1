$src = "C:\Users\Sasha  Baron\Documents\1. Рабочка_КО\1 Техническое задание 12-49-4750 от 11.06.2024-1.pdf"
$dest = "c:\ANTIGRAVITY\1\scratch\main_tz.pdf"
Copy-Item $src -Destination $dest -Force
Write-Host "Done"
