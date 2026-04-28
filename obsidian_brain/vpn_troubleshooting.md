# 🛠 Восстановление работы VPN (AirLink / Tun)

## Описание проблемы
VPN-клиенты (особенно использующие `tun`-интерфейсы, такие как AirLink, sing-box, Xray) могут перестать работать и выдавать ошибки таймаута (например, `i/o timeout` или `ws closed`). 

Чаще всего это происходит, если в Windows были глобально заданы **прокси-переменные** или включен **системный прокси**. Это приводит к возникновению «мертвой петли» (routing loop): VPN пытается выйти в интернет, но система заворачивает его трафик обратно в локальный прокси, который этот же VPN и должен был поднять.

## Как проверить наличие проблемы

Откройте PowerShell и выполните следующие команды:

1. **Проверка переменных среды:**
   ```powershell
   Get-ChildItem Env: | Where-Object Name -match 'proxy'
   ```
   *Если в выдаче есть `HTTP_PROXY` или `HTTPS_PROXY` — это причина проблемы.*

2. **Проверка системного прокси Windows:**
   ```powershell
   Get-ItemProperty -Path 'Registry::HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings' | Select-Object ProxyEnable, ProxyServer
   ```
   *Если `ProxyEnable` равно `1`, значит включен системный прокси.*

---

## 🚀 Решение (Скрипт очистки)

Чтобы исправить проблему, скопируйте и выполните этот скрипт в PowerShell (лучше от имени Администратора). Он удалит конфликтующие переменные и выключит системный прокси:

```powershell
# 1. Удаляем переменные среды (для текущего пользователя)
[System.Environment]::SetEnvironmentVariable('HTTP_PROXY', $null, 'User')
[System.Environment]::SetEnvironmentVariable('HTTPS_PROXY', $null, 'User')

# 2. Удаляем переменные среды (для всей системы)
[System.Environment]::SetEnvironmentVariable('HTTP_PROXY', $null, 'Machine')
[System.Environment]::SetEnvironmentVariable('HTTPS_PROXY', $null, 'Machine')

# 3. Отключаем системный прокси Windows в реестре
Set-ItemProperty -Path 'Registry::HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings' -Name ProxyEnable -Value 0

# 4. Сброс сетевых сокетов (опционально, если проблема сохраняется)
# netsh winsock reset
# netsh int ip reset

Write-Host "✅ Прокси успешно очищены! Пожалуйста, перезагрузите ПК." -ForegroundColor Green
```

## Последующие шаги
После выполнения скрипта **обязательно перезагрузите компьютер**. Запустите VPN-клиент заново — соединение должно восстановиться.
