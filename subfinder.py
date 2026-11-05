import requests, socket, urllib3
from concurrent.futures import ThreadPoolExecutor
urllib3.disable_warnings()

GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

def from_crtsh(domain):
    print(f"{YELLOW}[*] بجرب اجيب من crt.sh ...{RESET}")
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        r = requests.get(url, timeout=30, verify=False, headers={'User-Agent': 'Mozilla/5.0'})
        if r.status_code == 200:
            data = r.json()
            subs = set()
            for entry in data:
                name = entry.get('name_value','')
                for n in name.split('\n'):
                    if domain in n:
                        subs.add(n.strip())
            return list(subs)
    except Exception as e:
        print(f"{RED}[!] crt.sh فشل (النت واقع): {e}{RESET}")
    return []

def brute_force(domain):
    print(f"{YELLOW}[*] ببدأ Brute Force بكلمات مشهورة ...{RESET}")
    wordlist = ["www", "api", "admin", "test", "dev", "mail", "blog", "shop", "app", "beta", "staging", "vpn", "m", "mobile", "secure", "portal", "cpanel", "webmail", "support", "docs"]
    
    found = []
    def check(sub):
        full = f"{sub}.{domain}"
        try:
            socket.gethostbyname(full)
            print(f"{GREEN}[FOUND] {full}{RESET}")
            found.append(full)
        except:
            pass

    with ThreadPoolExecutor(max_workers=10) as ex:
        ex.map(check, wordlist)
    return found

domain = input("ادخل الدومين (مثال: hackerone.com): ").strip()

all_subs = set()

# 1
crt_result = from_crtsh(domain)
if crt_result:
    for s in crt_result:
        print(f"{GREEN}[CRT] {s}{RESET}")
        all_subs.add(s)

# 2
brute_result = brute_force(domain)
for s in brute_result:
    all_subs.add(s)

print(f"\n{YELLOW}--- خلصنا - لقينا {len(all_subs)} سابدومين ---{RESET}")
for s in sorted(all_subs):
    print(s)

# احفظهم في ملف
with open(f"{domain}_subs.txt", "w") as f:
    for s in all_subs:
        f.write(s + "\n")
print(f"\n{GREEN}حفظتهم في ملف: {domain}_subs.txt{RESET}")
