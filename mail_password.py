import threading
from retrying import retry
import time
import logging
from queue import Queue, Empty
import imaplib
import email as em
import re
import urllib.parse
from multiprocessing import cpu_count
import os
import sys
import requests
from requests.exceptions import RequestException
from seleniumbase import BaseCase

file_write_lock = threading.Lock()

# Windows'ta ANSI renk kodlarını etkinleştir
if sys.platform == "win32":
    os.system('')

class Colors:
    SUCCESS = '\033[92m'  # Yeşil
    WARNING = '\033[93m'  # Sarı
    FAIL = '\033[91m'     # Kırmızı
    INFO = '\033[94m'      # Mavi
    ENDC = '\033[0m'

# Logging yapılandırmasını renkli ve sade hale getirelim
class SimpleColoredFormatter(logging.Formatter):
    def format(self, record):
        level = record.levelname
        message = record.getMessage()
        if level == 'INFO':
            return f"[{Colors.SUCCESS}BAŞARILI{Colors.ENDC}] {message}"
        elif level == 'WARNING':
            return f"[{Colors.WARNING}UYARI{Colors.ENDC}] {message}"
        elif level == 'ERROR':
            return f"[{Colors.FAIL}HATA{Colors.ENDC}] {message}"
        return message

logger = logging.getLogger()
logger.setLevel(logging.INFO)
if logger.hasHandlers():
    logger.handlers.clear()
ch = logging.StreamHandler()
ch.setFormatter(SimpleColoredFormatter())
logger.addHandler(ch)

def get_verification_code(email_address, password, timeout_seconds=90, check_interval=15, retry_attempts=10):
    """E-posta doğrulama kodunu al"""
    imap_server = 'imap.firstmail.ltd'
    attempt = 0

    while retry_attempts == -1 or attempt < retry_attempts:
        try:
            print(f"{email_address} için IMAP sunucusuna bağlanılıyor, {attempt + 1}. deneme...")
            mailbox = imaplib.IMAP4_SSL(imap_server, port=993)
            mailbox.login(email_address, password)
            print(f"{email_address} için giriş başarılı!")
            break
        except imaplib.IMAP4.error as e:
            attempt += 1
            print(f"IMAP bağlantı hatası: {e}. {attempt}. deneme")
            time.sleep(2)
            if retry_attempts != -1 and attempt >= retry_attempts:
                with file_write_lock:
                    with open('blocked_emails.txt', 'a') as f:
                        f.write(f'{email_address}:{password}\n')
                return False
        except OSError as e:
            attempt += 1
            print(f"Bağlantı hatası: {e}. {attempt}. deneme.")
            time.sleep(2)
            if retry_attempts != -1 and attempt >= retry_attempts:
                return False

    # Gelen kutusunu kontrol et
    start_time = time.time()
    while True:
        time.sleep(check_interval)
        current_time = time.time()
        elapsed_time = current_time - start_time
        
        if elapsed_time >= timeout_seconds:
            return None

        mailbox.select('inbox')
        status, email_ids = mailbox.search(None, 'UNSEEN')
        email_ids = email_ids[0].split()

        if not email_ids:
            continue
        
        latest_email_id = email_ids[-1]
        status, email_data = mailbox.fetch(latest_email_id, '(RFC822)')
        raw_email = email_data[0][1]
        email_message = em.message_from_bytes(raw_email)
        body = ""
        
        if email_message.is_multipart():
            for part in email_message.get_payload():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = email_message.get_payload(decode=True).decode()

        if "Please contact us!" in body:
            with file_write_lock:
                with open('blocked_emails.txt', 'a') as f:
                    f.write(f'{email_address}:{password}\n')
            return False

        code_match = re.search(r'\b\d{6}\b', body)
        if code_match:
            verification_code = code_match.group()
            print(f"Doğrulama kodu bulundu: {verification_code}")
            return verification_code

class TwitterSignupWithMail(BaseCase):
    def test_signup_with_mail_verification(self):
        """Twitter kayıt akışı ve mail doğrulama"""
        # Stealth mode için ek ayarlar
        self.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
        self.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
        
        # Twitter kayıt sayfasına git
        self.open("https://x.com/i/flow/signup")
        time.sleep(6)

        # Create account butonuna tıkla
        self.click('button:contains("Create account")')
        print("Create account butonuna tıklandı!")
        time.sleep(3)

        # Use email instead butonuna tıkla
        self.click('button:contains("Use email instead")')
        print("Use email instead butonuna tıklandı!")
        time.sleep(3)

        # Name input'una "süleyman" yaz
        self.type('input[name="name"]', "süleyman")
        time.sleep(1)
        print("Name input'una 'süleyman' yazıldı!")

        # Email input'una email yaz
        email_address = "rigriahu@polosmail.com"
        self.type('input[name="email"]', email_address)
        time.sleep(1)
        print(f"Email input'una '{email_address}' yazıldı!")

        # Ay seçimi - June (6. ay) seç
        self.select_option_by_text('select[id="SELECTOR_1"]', "June")
        time.sleep(1)
        print("Ay olarak 'June' seçildi!")

        # Gün seçimi - 30. gün seç
        self.select_option_by_text('select[id="SELECTOR_2"]', "30")
        time.sleep(1)
        print("Gün olarak '30' seçildi!")

        # Yıl seçimi - 1994 seç
        self.select_option_by_text('select[id="SELECTOR_3"]', "1994")
        time.sleep(1)
        print("Yıl olarak '1994' seçildi!")

        # Next butonuna tıkla
        self.click('button:contains("Next")')
        time.sleep(1)
        print("Next butonuna tıklandı!")

        # Şifre sayfasında şifre oluştur
        time.sleep(3)
        
        # Şifre input'una şifre yaz
        password = "TestPassword123!"
        self.type('input[name="password"]', password)
        time.sleep(1)
        print("Şifre yazıldı!")

        # Next butonuna tıkla
        self.click('button:contains("Next")')
        time.sleep(1)
        print("Şifre ile Next butonuna tıklandı!")

        # E-posta doğrulama sayfasını bekle
        time.sleep(3)
        
        # E-posta doğrulama kodu gönder
        print("E-posta doğrulama kodu gönderiliyor...")
        
        # Doğrulama kodu gönder butonuna tıkla
        self.click('button:contains("Send code")')
        time.sleep(2)
        print("Doğrulama kodu gönderildi!")
        
        # E-posta şifresi (gerçek şifreyi buraya yazın)
        email_password = "your_email_password_here"
        
        # Doğrulama kodunu al
        print("E-posta doğrulama kodu bekleniyor...")
        verification_code = get_verification_code(email_address, email_password)
        
        if verification_code:
            print(f"Doğrulama kodu alındı: {verification_code}")
            
            # Doğrulama kodunu input'a yaz
            self.type('input[name="verification_code"]', verification_code)
            time.sleep(1)
            print("Doğrulama kodu yazıldı!")
            
            # Next butonuna tıkla
            self.click('button:contains("Next")')
            time.sleep(1)
            print("Doğrulama kodu ile Next butonuna tıklandı!")
            
            # Hesap oluşturma tamamlanmasını bekle
            time.sleep(3)
            print("Hesap oluşturma işlemi tamamlandı!")
            
        else:
            print("Doğrulama kodu alınamadı!")

        # Enter'a basılmasını bekle
        input("Çıkmak için Enter'a basın...")

if __name__ == "__main__":
    # Proxy, İngilizce locale, headed mode ve stealth mode ile çalıştır
    BaseCase.main(__name__, __file__, "--proxy=3ed492ea9d26670b06c1__cr.us:4e17d20cd644f516@gw.dataimpulse.com:823", "--locale=en", "--headed", "--uc", "--disable-csp")
