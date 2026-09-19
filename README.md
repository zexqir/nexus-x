# NEXUS-X

**Security Assessment Framework** by **ZEXQIR**  
GitHub: **zexqir** — `https://github.com/zexqir/nexus-x`

NEXUS-X is a modular, Rich-based Python framework for authorized defensive security assessment on Kali Linux and Debian-based systems.

## Features
- Network intelligence and local snapshots
- Wireless/Bluetooth inventory where the OS permits discovery
- Static APK inspection
- Redacted secret scanning
- Authorization-first asset discovery
- Defensive Linux security audit
- Evidence-based correlation
- Dashboard and JSON/CSV/HTML reporting
- Configuration and future plugin architecture
- Unit tests and structured logging

## Safety
NEXUS-X does **not** implement credential phishing, session/cookie theft, camera/microphone hijacking, password attacks, jamming, deauthentication, malware deployment, persistence, stealth/evasion, unauthorized exploitation, destructive operations, or data exfiltration.

Active assessment requires an explicit authorization confirmation in the CLI. Use only against systems and data you are authorized to assess.

## Installation
```bash
git clone https://github.com/zexqir/nexus-x.git
cd nexus-x
chmod +x install.sh
./install.sh
source .venv/bin/activate
python3 -m nexus.cli
```

## CLI
```bash
python3 -m nexus.cli --help
python3 -m nexus.cli --version
```
