$folder = Get-ChildItem "C:\Users\Sasha  Baron\Documents\1.*" | Select-Object -First 1
if ($folder) {
    Get-ChildItem $folder.FullName | Select-Object FullName | Out-File "c:\ANTIGRAVITY\1\scratch\file_list.txt"
    Write-Host "Listed files in: $($folder.FullName)"
} else {
    Write-Host "Folder not found"
}
