# 🥷 Bug Bounty Toolkit - Termux Edition
> Built entirely on Android phone - No PC needed!

![Android](https://img.shields.io/badge/Android-Termux-black?style=for-the-badge&logo=android)
![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Bug Bounty](https://img.shields.io/badge/Bug%20Bounty-Ready-red?style=for-the-badge)

### 🔧 Tools Included
| Tool | Description |
|------|-------------|
| `subfinder.py` | Subdomain enumeration from crt.sh |
| `headers.py` | Security headers analysis & risk score |
| `mass_check.py` | Mass scan + Risk ranking |
| `report.py` | Professional HTML report |
| `xss.py` | Quick XSS payload tester |
| `hackerone.com_subs.txt` | Real target example |

### 🚀 Usage - On Termux
```bash
pkg install python git
git clone https://github.com/am5203847-stack/bugbounty-termux-toolkit.git
cd bugbounty-termux-toolkit
python subfinder.py hackerone.com
python mass_check.py hackerone.com_subs.txt
python report.py
