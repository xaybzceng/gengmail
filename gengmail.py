import requests
import time
import sys

API_URL = "https://api.mail.tm"

def get_domains():
    res = requests.get(f"{API_URL}/domains")
    return res.json()['hydra:member'][0]['domain']

def create_account(email, password):
    data = {"address": email, "password": password}
    res = requests.post(f"{API_URL}/accounts", json=data)
    return res.status_code == 201

def get_token(email, password):
    data = {"address": email, "password": password}
    res = requests.post(f"{API_URL}/token", json=data)
    return res.json().get('token')

# --- [ เริ่มขั้นตอนของ Adithep ] ---
domain = get_domains()
password = "Password12345!"
temp_accounts = []

print(f"📧 [SAN] กำลังเจนเมลทางเลือกให้มึง 5 เมล...")
for i in range(1, 6):
    email = f"adithep_san_{int(time.time())}{i}@{domain}"
    if create_account(email, password):
        temp_accounts.append(email)
        print(f"[{i}] {email}")

print("-" * 30)
choice = int(input("👉 เลือกเมลที่มึงจะใช้สมัครทวิต (1-5): "))
selected_email = temp_accounts[choice-1]
token = get_token(selected_email, password)

print(f"\n✅ มึงเลือก: {selected_email}")
print(f"🚀 เอาเมลนี้ไปใส่ในหน้าสมัคร Twitter เลยไอ้สัส! กูกำลังดัก OTP ให้...")

# --- [ ด่านดัก OTP ] ---
print("⏳ กำลังจ้องกล่องจดหมาย... (ถ้า OTP มามันจะเด้งตรงนี้)")
while True:
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get(f"{API_URL}/messages", headers=headers)
    messages = res.json().get('hydra:member')
    
    if messages:
        msg_id = messages[0]['id']
        # ดึงเนื้อหาเต็มเพื่อหาเลข
        full_msg = requests.get(f"{API_URL}/messages/{msg_id}", headers=headers).json()
        content = full_msg.get('text', '') or full_msg.get('intro', '')
        
        import re
        otp = re.findall(r'\b\d{6}\b', content)
        if otp:
            print("\n" + "🔥"*10)
            print(f"🎯 [OTP TWITTER]: {otp[0]}")
            print("🔥"*10)
            sys.stdout.write('\a') # เสียงเตือน
            break # เจอแล้วจบงาน
            
    time.sleep(3) # เช็คทุก 3 วินาที
