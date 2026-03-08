# NullSec Network Recon

Comprehensive network reconnaissance payload for Linux. Maps the local network, discovers live hosts, enumerates services, and identifies network topology — all using built-in system tools.

## Description

This payload performs a full network reconnaissance of the target Linux system's environment without requiring any third-party tools like nmap. It uses only utilities available on virtually every Linux distribution.

### What it collects:
- **Network interfaces** — All interfaces with IP addresses
- **Routing table** — Gateway and route information
- **DNS configuration** — Configured name servers
- **ARP neighbors** — Known hosts on local network segments
- **Listening services** — All services bound to ports with process info
- **Established connections** — Active outbound/inbound connections
- **Firewall rules** — iptables configuration (requires root)
- **Wireless networks** — Nearby WiFi networks (if wireless available)
- **Subnet ping sweep** — Discovers live hosts on the local /24 subnet
- **Hosts file** — Static hostname mappings

### Features:
- **No nmap needed** — uses ping, ss, ip, and other built-in tools
- **Parallel ping sweep** — scans /24 subnet in seconds using background jobs
- **Auto-detects subnet** — determines scan range from default gateway
- **Text report** — easy to grep and parse

## Target
Linux (tested on Ubuntu, Debian, Arch, Fedora)

## Output
Report saved to: `/tmp/netrecon_<hostname>_<timestamp>.txt`

## Author
[NullSec (bad-antics)](https://github.com/bad-antics)
