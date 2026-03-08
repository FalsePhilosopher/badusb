# NullSec-PersistPlant

**Covert Persistence Mechanism Installer via BadUSB**

## Description

Installs multiple persistence mechanisms on a Windows target that beacon home to your C2/listener. Uses three independent methods for redundancy — if one is removed, the others continue operating.

## Persistence Methods

| Method | Mechanism | Admin Required | Survives |
|--------|-----------|---------------|----------|
| **Scheduled Task** | `WindowsHealthCheck` task at logon + every 4 hours | No (HKCU) | Reboot, user logoff |
| **Registry Run Key** | `HKCU\...\Run\WindowsHealthSvc` | No | Reboot |
| **Startup VBS** | `HealthCheck.vbs` in Startup folder | No | Reboot |

## Beacon Payload

Each persistence method executes a PowerShell beacon that sends:
```json
{
  "user": "targetuser",
  "host": "WORKSTATION-01",
  "ip": "192.168.1.50",
  "os": "Windows 11 Pro",
  "time": "2024-01-15 14:30:00"
}
```

## Setup

1. Set up a listener (simple webhook, Discord, or C2 framework)
2. Edit `payload.txt` and replace `YOUR_LISTENER_URL` with your endpoint
3. Copy to Flipper Zero SD: `SD/badusb/NullSec-PersistPlant/`

## Cleanup / Removal

To remove all persistence from a target:
```powershell
# Remove scheduled task
Unregister-ScheduledTask -TaskName 'WindowsHealthCheck' -Confirm:$false

# Remove registry key
Remove-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -Name 'WindowsHealthSvc'

# Remove startup VBS
Remove-Item "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\HealthCheck.vbs"
```

## OPSEC Notes

- All three methods use HKCU (no admin/UAC required)
- Task and registry names mimic Windows health services
- VBS wrapper hides the PowerShell window
- PowerShell history is cleared after execution
- Beacon uses encoded command to avoid command-line logging
- Reports back which methods were successfully installed

## Detection

Defenders can look for:
- Scheduled tasks with encoded PowerShell arguments
- `HKCU\Run` entries with `powershell -enc` commands
- `.vbs` files in Startup folder
- Network connections to unknown endpoints at regular intervals

## Legal

**For authorized penetration testing and red team engagements only. Always obtain written permission before deploying persistence mechanisms.**

## Author

NullSec ([@bad-antics](https://github.com/bad-antics))
