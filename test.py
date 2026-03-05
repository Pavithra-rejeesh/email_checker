
import datetime
import re
import email
import requests
import json
import os

LOCAL_FILE = "domains.json"

def save_config():
    x = requests.get('https://cdn.jsdelivr.net/gh/disposable/disposable-email-domains@master/domains.json')

    domains = x.json()

    domain_document = {"last_updated": datetime.datetime.now().isoformat(), "domains": domains}

    open(LOCAL_FILE, 'w').write(json.dumps(domain_document, indent=2))
x = "buymeacoffee@gmail.com"

domain = x.split("@")[-1]
username = x.split("@")[0]

print(f"Username: {username}")
print(f"Domain: {domain}")


if (len(username) > 64):
    print("email is not valid")

    DISPOSABLE_URL = "https://cdn.jsdelivr.net/gh/disposable/disposable-email-domains@master/domains.json"

def load_disposable_domains():
    if os.path.exists(LOCAL_FILE):
        with open(LOCAL_FILE, "r") as f:
            try:
                data = json.load(f)   
                return set(data.get("domains", []))  
            except:
                pass 

    with open(LOCAL_FILE, "w") as f:
        json.dump(domain, f, indent=4)

    return set(domain)

disposable_domains = load_disposable_domains()

def is_disposable_email(email):
    domain = email.split("@")[-1].lower()
    return domain in disposable_domains



def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return (re.match(pattern, email))

test_emails = [
    "valid.email@example.com",
    "user123@sub.domain.org",
    "invalid-email.com",
    "user@.com",
    "another.valid+alias@example-domain.co.uk",
     "temp123@guerrillamail.com",
    "random@10minutemail.com",
    "someone@yopmail.com",
    "test@throwawaymail.com",
    "fakeuser@mailinator.com",
    "@missingusername.com",
    "plainaddress",
     "hello.world+alias@gmail.com",
    "user.name@subdomain.example.org",
    "contact123@mywebsite.io"]

for email in test_emails:
    print("\nChecking:", email)

    if not is_valid_email(email):
        print("INVALID FORMAT")
        continue

    if is_disposable_email(email):
        print("Disposable email detected")
    else:
        print("VALID email")

# for email in test_emails:
#     if is_valid_email(email):
#         print(f"'{email}' is a valid email address.")
#     else:
#         print(f"'{email}' is an invalid email address.")

#         def check_chars_in_email_loop(email,username):
#             for char in username:
#                 if char in email:
#                     return True    
#                 return False
            
#         username = "testuser"
#         email = "testuser@example.com"
#         result = check_chars_in_email_loop(username, email)
#         print(f"Are all characters in '{username}' present in '{email}'? {result}")
                      