# NullSec IR Triage

A rapid incident response triage payload for Linux systems. Collects volatile forensic artifacts and generates a self-contained HTML report for offline analysis.

## Description

When responding to a security incident on a Linux machine, time is critical. This payload automates the collection of the most important volatile artifacts into a styled HTML report that can be opened in any browser.

### What it collects:
- Running processes (full tree with command lines)
- Network connections (listening, established, with process info)
- Logged-in users and recent login history
- Scheduled tasks (cron, systemd timers)
- SUID binaries (privilege escalation vectors)
- Executable files in temp directories (malware indicators)
- SSH authorized keys (persistence check)
- Recently modified system files
- Loaded kernel modules

### Features:
- **Zero dependencies** — uses only built-in Linux utilities
- **No root required** — works with standard user privileges
- **HTML output** — styled report viewable in any browser
- **Single command** — entire triage runs as one bash command
- **Self-contained** — no network access or downloads needed

## Target
Linux (tested on Ubuntu, Debian, Arch, Fedora)

## Output
Report saved to: `/tmp/ir_triage_<hostname>_<timestamp>.html`

## Author
[NullSec (bad-antics)](https://github.com/bad-antics)
