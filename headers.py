import requests
import sys
from urllib.parse import urlparse

# الوان عشان الشكل يبقى جامد في ترمكس
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def check_headers(url):
    if not url.startswith("http"):
        url = "https://" + url
    
    print(f"\n{YELLOW}[*] بفحص: {url}{RESET}\n")

    try:
        r = requests.get(url, timeout=30, verify=False, headers={'User-Agent': 'BugBounty-Lab'})
    except Exception as e:
        print(f"{RED}[!] فشل الاتصال: {e}{RESET}")
        return

    print(f"URL: {url}")
    print(f"Status: {r.status_code}")
    for k,v in r.headers.items():
        print(f"{k}: {v}")

    print(f"\n{YELLOW}--- Security Check ---{RESET}")
    
    missing = []
    
    checks = {
        "X-Frame-Options": "يحمي من Clickjacking",
        "Content-Security-Policy": "يحمي من XSS",
        "X-Content-Type-Options": "يمنع تخمين نوع الملف",
        "Strict-Transport-Security": "يفرض HTTPS"
    }

    for header, desc in checks.items():
        if header in r.headers:
            print(f"{GREEN}[OK] {header} : {desc}{RESET}")
        else:
            print(f"{RED}[MISSING] {header} : {desc}{RESET}")
            missing.append(header)

    print(f"\n{YELLOW}--- التقرير النهائي ---{RESET}")
    if len(missing) == 0:
        print(f"{GREEN}[SECURE] الموقع ده متأمن كويس جدا!{RESET}")
    elif len(missing) == 1:
        print(f"{YELLOW}[LOW RISK] ناقص هيدر واحد: {', '.join(missing)}{RESET}")
    elif len(missing) == 2:
        print(f"{YELLOW}[MEDIUM RISK] ناقص هيدرين: {', '.join(missing)}{RESET}")
    else:
        print(f"{RED}[HIGH RISK] الموقع ضعيف! ناقص {len(missing)} هيدرز: {', '.join(missing)} - احتمالية وجود XSS عالية{RESET}")

url = input("ادخل لينك الموقع للفحص: ")
check_headers(url)
