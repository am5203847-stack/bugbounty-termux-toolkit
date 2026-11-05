import requests, urllib3
urllib3.disable_warnings()

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

SECURITY_HEADERS = [
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Strict-Transport-Security",
    "X-XSS-Protection",
    "Referrer-Policy"
]

def check_one(domain):
    # نجرب https الاول
    for proto in ["https://", "http://"]:
        url = proto + domain
        try:
            r = requests.get(url, timeout=15, verify=False, headers={'User-Agent': 'Mozilla/5.0'})
            missing = []
            for h in SECURITY_HEADERS:
                if h not in r.headers:
                    missing.append(h)
            
            risk = len(missing)
            if risk >= 4:
                level = f"{RED}[HIGH RISK - {risk} missing]{RESET}"
            elif risk >= 2:
                level = f"{YELLOW}[MEDIUM - {risk} missing]{RESET}"
            else:
                level = f"{GREEN}[LOW - {risk} missing]{RESET}"
            
            print(f"{level} -> {domain} -> {url}")
            if missing:
                print(f"      ناقص: {', '.join(missing)}")
            return risk, domain
        except:
            continue
    print(f"{RED}[DOWN]{RESET} -> {domain}")
    return -1, domain

file_name = input("ادخل اسم ملف السابدومينات (مثال: hackerone.com_subs.txt): ").strip()

try:
    with open(file_name) as f:
        domains = [line.strip() for line in f if line.strip()]
except:
    print("الملف مش موجود، اتأكد من الاسم")
    exit()

print(f"\n{YELLOW}[*] هفحص {len(domains)} سابدومين ...{RESET}\n")

results = []
for d in domains:
    r = check_one(d)
    results.append(r)

# رتبهم من الاخطر للآمن
results.sort(reverse=True)

print(f"\n{YELLOW}--- الترتيب من الاخطر للأضعف ---{RESET}")
for risk, dom in results:
    if risk >= 0:
        print(f"{risk} -> {dom}")
