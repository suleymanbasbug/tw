import time
from seleniumbase import BaseCase
from mail_password import get_verification_code

class TwitterSignup(BaseCase):
    def test_signup(self):
        email_address = "vmdbzggy@polosmail.com"
        password = "lfbsnkbmX!5753"
        # Stealth mode için ek ayarlar
        self.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
        self.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
        
        # İngilizce locale ile başlat
        self.open("https://x.com/i/flow/signup")
        time.sleep(6)

        # Create account butonuna tıkla
        self.click('button:contains("Create account")')
        print("Create account butonuna tıklandı!")

        # Sayfanın yüklenmesini bekle
        time.sleep(3)

        # Use email instead butonuna tıkla
        self.click('button:contains("Use email instead")')
        print("Use email instead butonuna tıklandı!")

        # Sayfanın yüklenmesini bekle
        time.sleep(3)

        # Name input'una "süleyman" yaz
        self.type('input[name="name"]', "hasan")
        time.sleep(1)
        print("Name input'una 'süleyman' yazıldı!")

        # Email input'una "sede@sede.com" yaz
        self.type('input[name="email"]', email_address)
        time.sleep(1)
        print("Email input'una 'sede@sede.com' yazıldı!")

        # Ay seçimi - June (6. ay) seç
        self.select_option_by_text('select[id="SELECTOR_1"]', "June")
        time.sleep(1)
        print("Ay olarak 'June' seçildi!")

        # Gün seçimi - 30. gün seç
        self.select_option_by_text('select[id="SELECTOR_2"]', "27")
        time.sleep(1)
        print("Gün olarak '30' seçildi!")

        # Yıl seçimi - 1994 seç
        self.select_option_by_text('select[id="SELECTOR_3"]', "1984")
        time.sleep(1)
        print("Yıl olarak '1994' seçildi!")

        # Next butonuna tıkla
        self.click('button:contains("Next")')
        time.sleep(1)
        print("Next butonuna tıklandı!")

        # E-posta doğrulama sayfasını bekle
        time.sleep(3)
        
        print("Doğrulama kodu gönderildi!")
        
        # Doğrulama kodunu al
        print("E-posta doğrulama kodu bekleniyor...")
        verification_code = get_verification_code(email_address, password)
        
        if verification_code:
            print(f"Doğrulama kodu alındı: {verification_code}")
            
            # Doğrulama kodunu input'a yaz
            self.type('input[name="verfication_code"]', verification_code)
            time.sleep(1)
            print("Doğrulama kodu yazıldı!")
            
            # Next butonuna tıkla
            self.click('span:contains("Next")')
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