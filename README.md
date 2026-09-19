# NEXUS-X

### Security Assessment Framework

NEXUS-X is a modular, terminal-based security assessment framework designed for authorized security testing, defensive analysis, system visibility, and security auditing.

Built with Python 3 and a Rich-powered interactive terminal interface, NEXUS-X brings multiple defensive security assessment capabilities together inside a single structured framework. The project focuses on making security assessment workflows easier to organize, understand, automate, and report while maintaining a clear authorization-first approach.

NEXUS-X provides a unified command-line environment for network intelligence, wireless analysis, APK security analysis, secret detection, asset discovery, security auditing, finding correlation, dashboards, and report generation.

The framework is designed around a modular architecture, allowing individual security modules to operate independently while also sharing structured findings through the correlation and reporting layers.

---

## Core Capabilities

### Network Intelligence

Collect useful information about the local networking environment, including public IP information, network interfaces, active connections, listening services, routing information, DNS configuration, ARP/neighbor information, and complete network snapshots.

Results can be structured and exported for later analysis and reporting.

### Wireless Analyzer

Inspect available Wi-Fi interfaces and Bluetooth adapters and collect defensive inventory information.

The wireless module is intended for visibility and authorized assessment only and does not implement wireless jamming, deauthentication, or denial-of-service functionality.

### APK Security Lab

Analyze Android APK files from a defensive and static-analysis perspective.

The module can inspect application metadata, permissions, components, resources, DEX information, URLs, certificate metadata, and potentially exposed secrets without performing exploitative behavior.

### Secret Scanner

Search authorized files and project directories for potentially exposed credentials and sensitive configuration material such as API keys, tokens, passwords, cloud credentials, private keys, `.env` values, and configuration secrets.

Detected secrets are redacted in displayed and generated reports to reduce accidental exposure.

### Asset Discovery

Provide authorization-first asset discovery capabilities for approved environments.

The module can assist with host discovery, DNS information, connectivity checks, service identification, and asset classification.

### Security Audit

Review security-relevant configuration and system posture, including exposed services, local configuration issues, file permissions, TLS/security-header observations, dependency information, Linux security posture, and common configuration mistakes.

### Correlation Engine

Connect assets, observations, and security findings into a structured view so that related issues can be analyzed together instead of being treated as isolated results.

### Security Dashboard

Present assessment information through a consistent terminal interface, making it easier to review discovered assets, findings, statistics, and assessment status from one location.

### Report Center

Generate structured security assessment output in formats such as JSON, CSV, HTML, and PDF-compatible report workflows.

Reports are organized by assessment category:

- Network
- Wireless
- APK
- Secrets
- Assets
- Audits

Sensitive values are redacted before being written to reports.

---

## Installation

### Requirements

Before installing NEXUS-X, make sure your system has:

- Python 3.10 or newer
- Git
- Linux, Kali Linux, or another Debian-based distribution
- Internet connection for installing Python dependencies
- Recommended: Python virtual environment

### Clone Repository

Clone the official NEXUS-X repository:

```bash
git clone https://github.com/zexqir/nexus-x.git
cd nexus-x
