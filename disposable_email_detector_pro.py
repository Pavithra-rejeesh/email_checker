
import json
from pathlib import Path
import dns.resolver
import re
import requests
from email_validator import validate_email, EmailNotValidError 
from datetime import datetime

BASE_DIR = Path(__file__).parent
CONFIG_PATH = BASE_DIR / "config.json"
DOMAINS_PATH = BASE_DIR / "domains.json"
DEFAULT_URL = "https://cdn.jsdelivr.net/gh/disposable/disposable-email-domains@master/domains.json"

def load_config():
    if CONFIG_PATH.exists():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {"domains_url": DEFAULT_URL, "last_updated": None}

def save_config(cfg):
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2), encoding="utf-8")

def load_local_domains():
    if DOMAINS_PATH.exists():
        try:
            domains = json.loads(DOMAINS_PATH.read_text(encoding="utf-8"))
            print(f"✅ Loaded {len(domains)} disposable domains from local file")
            return set(domains)
        except Exception as e:
            print(f"Error reading local domains.json: {e}")

    return {"mailinator.com", "tempmail.com", "guerrillamail.com"}

def update_domains_from_cdn(timeout=10):
    cfg = load_config()
    url = cfg.get("domains_url", DEFAULT_URL)
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        domains = resp.json()

        tmp = DOMAINS_PATH.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(domains, indent=2), encoding="utf-8")
        tmp.replace(DOMAINS_PATH)
        cfg["last_updated"] = datetime.utcnow().isoformat() + "Z"
        save_config(cfg)
        print(f"✅ Updated local domains.json with {len(domains)} entries")
        return True
    except Exception as e:
        print(f"Failed to update domains from CDN: {e}")
        return False


DISPOSABLE_DOMAINS = load_local_domains()

def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def get_domain(email):
    return email.split("@")[-1].lower() if "@" in email else ""

def is_disposable_local(email):
    domain = get_domain(email)
    return domain in DISPOSABLE_DOMAINS

def check_disposable_api(email):
    
    API_KEY = "YOUR_API_KEY"
    API_URL = "https://api.yourprovider.com/v1/check"
    if "YOUR_API_KEY" in API_KEY:
        return False
    try:
        response = requests.get(
            API_URL,
            params={"email": email},
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("disposable", False)
        return False
    except Exception as e:
        print(f"API check failed: {e}")
        return False

def has_mx_record(domain):
    if not domain:
        return False
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return len(records) > 0
    except Exception:
        return False

def looks_suspicious(email):
    username = email.split("@")[0] if "@" in email else ""
    domain = get_domain(email)
    if re.search(r'[0-9]{3,}', username):
        return True
    if any(word in domain for word in 
           ['tempmail', 'mailinator', '10minutemail', 'guerrillamail']):
        return True
    return False
def calculate_risk(email, new_domain=False, vpn_detected=False, accounts_from_ip=1):
    risk_score = 0
    domain = get_domain(email)

   
    email_valid = True
    try:
        validate_email(email, check_deliverability=False)
    except EmailNotValidError:
        email_valid = False

    mx_valid = has_mx_record(domain)
    local_disposable = is_disposable_local(email)
    api_disposable = check_disposable_api(email)

    if not email_valid:
        risk_score += 40

    if local_disposable:
        risk_score += 50

    if api_disposable:
        risk_score += 50

    if looks_suspicious(email):
        risk_score += 20

    if new_domain:
        risk_score += 20

    if vpn_detected:
        risk_score += 20

    if accounts_from_ip > 3:
        risk_score += 30

    if not mx_valid:
        risk_score += 30

    return risk_score, local_disposable, api_disposable, email_valid

def assess_email(email, new_domain=False, vpn_detected=False, accounts_from_ip=1):
    risk, local_disp, api_disp, email_valid = calculate_risk(
        email,
        new_domain,
        vpn_detected,
        accounts_from_ip
    )
    if risk >= 50:
        action = "BLOCK"
    elif 20 <= risk < 50:
        action = "FLAG"
    else:
        action = "ALLOW"
    return {
        "email": email,
        "domain": get_domain(email),
        "valid_email": email_valid,  
        "local_disposable": local_disp,
        "api_disposable": api_disp,
        "risk_score": risk,
        "action": action
    }

if __name__ == "__main__":
    print("=== Advanced Disposable Email Detector ===")
    while True:
        user_input = input("\nEnter email (or type 'exit'): ").strip()
        if user_input.lower() == "exit":
            print("Exiting...")
            break
        result = assess_email(user_input)
        print("\n--- Result ---")
        print(f"Email:            {result['email']}")
        print(f"Domain:           {result['domain']}")
        print(f"Valid Email:      {'Yes' if result['valid_email'] else 'No'}")
        print(f"Local Disposable: {'Yes' if result['local_disposable'] else 'No'}")
        print(f"API Disposable:   {'Yes' if result['api_disposable'] else 'No'}")
        print(f"Risk Score:       {result['risk_score']}")
        print(f"Recommended Action: {result['action']}")