# NullSec Security Audit

Quick security posture audit for Linux systems. Performs automated checks against common misconfigurations and security best practices, producing a pass/fail scorecard.

## Description

This payload runs a rapid security assessment of a Linux system, checking for common hardening issues that could leave the system vulnerable. It produces a simple PASS/FAIL scorecard that makes it easy to identify security gaps at a glance.

### Checks performed:

**Firewall**
- Firewall rules configured (iptables)
- UFW or Firewalld active

**SSH Hardening**
- Root login disabled
- Password authentication disabled (key-only)
- Protocol version 2 enforced

**User Security**
- Users with empty passwords
- Non-root UID 0 accounts (backdoor detection)

**File Permissions**
- /etc/passwd permissions (should be 644)
- /etc/shadow permissions (should be 640 or 600)
- World-writable files in /etc

**System Updates**
- Pending package updates (apt/dnf)

**Kernel Security**
- ASLR (Address Space Layout Randomization)
- SYN cookies (SYN flood protection)
- ICMP broadcast response

### Features:
- **Scorecard output** — Simple PASS/FAIL/WARN format
- **Zero dependencies** — built-in Linux tools only
- **Quick execution** — completes in seconds
- **No modifications** — read-only checks, doesn't change anything

## Target
Linux (tested on Ubuntu, Debian, Arch, Fedora)

## Output
Report saved to: `/tmp/secaudit_<hostname>_<timestamp>.txt`

## Author
[NullSec (bad-antics)](https://github.com/bad-antics)
