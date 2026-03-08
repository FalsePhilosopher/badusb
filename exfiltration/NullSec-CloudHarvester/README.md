# NullSec-CloudHarvester

**Cloud Service Credential & Configuration Extractor**

## Description

Extracts saved cloud CLI credentials, API tokens, and configuration files from a Windows target. Targets developers and DevOps engineers who use cloud CLIs.

## Targeted Services

| Service | Files Extracted |
|---------|----------------|
| **AWS CLI** | `~/.aws/credentials`, `~/.aws/config` |
| **Azure CLI** | `~/.azure/azureProfile.json`, `clouds.config` |
| **Google Cloud** | `application_default_credentials.json`, `properties`, `credentials.db` path |
| **Docker** | `~/.docker/config.json` (registry auth tokens) |
| **Kubernetes** | `~/.kube/config` (cluster creds + certs) |
| **SSH** | Key file inventory from `~/.ssh/` |
| **Git** | `~/.git-credentials`, `~/.gitconfig` |
| **Terraform** | `~/.terraformrc`, `credentials.tfrc.json` |
| **npm** | `~/.npmrc` (registry tokens) |
| **pip** | `pip.ini` (index credentials) |

## Setup

1. Edit `payload.txt` and replace `YOUR_DISCORD_WEBHOOK_URL` with your Discord webhook
2. Copy to Flipper Zero SD: `SD/badusb/NullSec-CloudHarvester/`
3. Run via BadUSB app

## Exfiltration

Data is sent to a Discord webhook in chunked messages (1900 char limit per message). Each cloud service section is clearly labeled.

## Target

- **OS:** Windows 10/11
- **Requirements:** PowerShell (default on Windows)
- **Best against:** Developer workstations, CI/CD machines, DevOps laptops

## OPSEC Notes

- Runs in hidden PowerShell window
- Clears PSReadLine history on exit
- No files written to disk
- No persistent modifications

## Legal

**For authorized penetration testing and security assessments only.**

## Author

NullSec ([@bad-antics](https://github.com/bad-antics))
