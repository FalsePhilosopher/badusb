# NullSec-LinuxRecon

**Comprehensive Linux System Reconnaissance via BadUSB**

## Description

Performs thorough system reconnaissance on Linux targets (Ubuntu, Debian, Fedora, Arch, etc.) and exfiltrates findings via webhook.

## Information Gathered

| Category | Details |
|----------|---------|
| **System** | Hostname, kernel, distro, uptime, CPU, RAM, disk |
| **User** | Current user, UID, groups, sudo privileges, shell, SSH keys |
| **Users** | All accounts with shell access |
| **Network** | Interfaces, IPs, gateway, DNS, ARP table |
| **Ports** | All listening TCP/UDP ports with process names |
| **Services** | Running systemd services |
| **Cron** | User and system cron jobs |
| **Security** | iptables/ufw rules, SELinux, AppArmor status |
| **SUID** | SUID binaries (privilege escalation candidates) |
| **Containers** | Docker/Podman running containers |
| **Files** | Cloud creds existence check (AWS, Kube, Docker) |

## Setup

1. Edit `payload.txt` and replace `YOUR_WEBHOOK_URL` with your Discord/Slack webhook
2. Copy to Flipper Zero SD: `SD/badusb/NullSec-LinuxRecon/`

## Terminal Launch

Uses `Ctrl+Alt+T` which works on most Linux desktop environments:
- GNOME, KDE, XFCE, MATE, Cinnamon, Unity

## OPSEC

- Runs entirely in background subshell
- Clears bash history after execution
- Unsets variables
- No files written to disk
- Terminal window closes automatically

## Legal

**For authorized penetration testing and security assessments only.**

## Author

NullSec ([@bad-antics](https://github.com/bad-antics))
