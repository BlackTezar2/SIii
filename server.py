import socket
import sys

# گوش دادن روی پورت 443
HOST = '0.0.0.0'
PORT = 443

print(f"سرور در حال گوش دادن روی پورت {PORT}...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    
    conn, addr = s.accept()
    with conn:
        print(f"اتصال از {addr} برقرار شد.")
        
        # دریافت داده
        data = conn.recv(4096)
        if data:
            print(f"دریافت شد: {len(data)} بایت")
            print(f"بایت‌های اول: {data[:50].hex()}")
            
            # بررسی نوع Handshake
            # بایت اول نوع پروتکل (16 = Handshake)
            # بایت پنجم نوع Handshake (1 = Client Hello)
            if len(data) > 5:
                proto = data[0]
                handshake_type = data[5]
                
                if proto == 0x16 and handshake_type == 0x01:
                    print("✅ این یک Client Hello است!")
                    print("شبیه‌سازی با موفقیت انجام شد.")
                else:
                    print("❌ این یک Client Hello استاندارد نیست.")
            else:
                print("داده دریافتی خیلی کوتاه است.")
                
            # ارسال یک پاسخ ساده (اختیاری - برای تست)
            # اگر می‌خواهید چرخه کامل شود، می‌توانید یک Server Hello بسازید
            # اما برای تست دریافت، همین کافی است.
            conn.send(b"\x16\x03\x03\x00\x01\x01") # یک پاسخ کوچک
            print("پاسخ کوچک ارسال شد.")