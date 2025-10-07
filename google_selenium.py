import time
from seleniumbase import BaseCase
from mail_password import get_verification_code
import random

class TwitterSignup(BaseCase):
    def test_signup(self):
        email_address = "fvlqmsnt@fringmail.com"
        password = "zpclajahY!2326"
        # Stealth mode için ek ayarlar
        self.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
        self.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
        
        # İngilizce locale ile başlat (insan davranışı)
        self.open("https://x.com/i/flow/signup")
        time.sleep(random.uniform(5.0, 8.0))  # Sayfa yükleme süresi (insan benzeri)

        # Create account butonuna hover yap ve yavaşça tıkla (insan davranışı)
        time.sleep(random.uniform(1.0, 2.0))  # Sayfa yüklenmesini bekle
        self.hover_and_click(
            'button:contains("Create account")', 
            'button:contains("Create account")',
            hover_by="css selector", 
            click_by="css selector"
        )
        time.sleep(random.uniform(0.5, 1.0))  # Tıklama sonrası bekleme
        print("Create account butonuna hover yapıldı ve tıklandı!")

        # Sayfanın yüklenmesini bekle (insan davranışı)
        time.sleep(random.uniform(2.0, 4.0))

        # Use email instead butonuna hover yap ve yavaşça tıkla (insan davranışı)
        time.sleep(random.uniform(0.5, 1.5))  # Butonu görme süresi
        self.hover_and_click(
            'button:contains("Use email instead")', 
            'button:contains("Use email instead")',
            hover_by="css selector", 
            click_by="css selector"
        )
        time.sleep(random.uniform(0.5, 1.0))  # Tıklama sonrası bekleme
        print("Use email instead butonuna hover yapıldı ve tıklandı!")

        # Sayfanın yüklenmesini bekle (insan davranışı)
        time.sleep(random.uniform(2.0, 4.0))

        # Name input'una "hasan" yaz (insan davranışı simülasyonu)
        time.sleep(random.uniform(0.5, 1.5))  # Formu görme süresi
        self.hover_and_click(
            'input[name="name"]', 
            'input[name="name"]',
            hover_by="css selector", 
            click_by="css selector"
        )  # Input'a hover yap ve tıkla
        time.sleep(random.uniform(0.3, 0.8))  # Input'a odaklanma süresi
        
        # Karakter karakter yaz (insan davranışı)
        for char in "hasan":
            self.send_keys('input[name="name"]', char)
            time.sleep(random.uniform(0.15, 0.4))  # Daha gerçekçi yazma hızı
        
        time.sleep(random.uniform(0.5, 1.5))  # Yazma sonrası kontrol süresi
        print("Name input'una 'hasan' yazıldı!")

        # Email input'una email yaz (insan davranışı simülasyonu)
        time.sleep(random.uniform(0.5, 1.5))  # Bir sonraki alana geçme süresi
        self.hover_and_click(
            'input[name="email"]', 
            'input[name="email"]',
            hover_by="css selector", 
            click_by="css selector"
        )  # Input'a hover yap ve tıkla
        time.sleep(random.uniform(0.3, 0.8))  # Input'a odaklanma süresi
        
        # Karakter karakter yaz (insan davranışı)
        for char in email_address:
            self.send_keys('input[name="email"]', char)
            time.sleep(random.uniform(0.1, 0.3))  # Email yazma hızı
        
        time.sleep(random.uniform(0.5, 1.5))  # Yazma sonrası kontrol süresi
        print(f"Email input'una '{email_address}' yazıldı!")

        # Ay seçimi - June (6. ay) seç (insan davranışı)
        time.sleep(random.uniform(0.5, 1.5))  # Dropdown'u görme süresi
        self.select_option_by_text('select[id="SELECTOR_1"]', "June")
        time.sleep(random.uniform(0.5, 1.0))  # Seçim sonrası bekleme
        print("Ay olarak 'June' seçildi!")

        # Gün seçimi - 27. gün seç (insan davranışı)
        time.sleep(random.uniform(0.3, 0.8))  # Bir sonraki dropdown'a geçme
        self.select_option_by_text('select[id="SELECTOR_2"]', "27")
        time.sleep(random.uniform(0.5, 1.0))  # Seçim sonrası bekleme
        print("Gün olarak '27' seçildi!")

        # Yıl seçimi - 1984 seç (insan davranışı)
        time.sleep(random.uniform(0.3, 0.8))  # Son dropdown'a geçme
        self.select_option_by_text('select[id="SELECTOR_3"]', "1984")
        time.sleep(random.uniform(0.5, 1.0))  # Seçim sonrası bekleme
        print("Yıl olarak '1984' seçildi!")

        # Next butonuna hover yap ve yavaşça tıkla (insan davranışı)
        time.sleep(random.uniform(1.0, 2.5))  # Formu kontrol etme süresi
        self.hover_and_click(
            'button:contains("Next")', 
            'button:contains("Next")',
            hover_by="css selector", 
            click_by="css selector"
        )
        time.sleep(random.uniform(0.5, 1.0))  # Tıklama sonrası bekleme
        print("Next butonuna hover yapıldı ve tıklandı!")

        # E-posta doğrulama sayfasını bekle (insan davranışı)
        time.sleep(random.uniform(3.0, 5.0))  # Sayfa geçiş süresi
        
        print("Doğrulama kodu gönderildi!")
        
        # Doğrulama kodunu al (insan davranışı)
        time.sleep(random.uniform(1.0, 2.0))  # E-posta kontrol etme süresi
        print("E-posta doğrulama kodu bekleniyor...")
        verification_code = get_verification_code(email_address, password)
        
        if verification_code:
            print(f"Doğrulama kodu alındı: {verification_code}")
            
            # Doğrulama kodunu input'a yaz (insan davranışı simülasyonu)
            time.sleep(random.uniform(0.5, 1.5))  # Kodu görme ve hazırlanma süresi
            self.hover_and_click(
                'input[name="verfication_code"]', 
                'input[name="verfication_code"]',
                hover_by="css selector", 
                click_by="css selector"
            )  # Input'a hover yap ve tıkla
            time.sleep(random.uniform(0.3, 0.8))  # Input'a odaklanma süresi
            
            # Kodu karakter karakter yaz (insan davranışı)
            for char in verification_code:
                self.send_keys('input[name="verfication_code"]', char)
                time.sleep(random.uniform(0.2, 0.5))  # Kod yazma hızı (daha yavaş)
            
            time.sleep(random.uniform(0.5, 1.5))  # Kod kontrol süresi
            print("Doğrulama kodu yazıldı!")
            
            # Next butonuna hover yap ve yavaşça tıkla (insan davranışı)
            time.sleep(random.uniform(1.0, 2.0))  # Kod kontrol etme süresi
            self.hover_and_click(
                'span:contains("Next")', 
                'span:contains("Next")',
                hover_by="css selector", 
                click_by="css selector"
            )
            time.sleep(random.uniform(0.5, 1.0))  # Tıklama sonrası bekleme
            print("Doğrulama kodu ile Next butonuna hover yapıldı ve tıklandı!")
            
            # Hesap oluşturma tamamlanmasını bekle (insan davranışı)
            time.sleep(random.uniform(3.0, 5.0))  # İşlem tamamlanma süresi
            print("Hesap oluşturma işlemi tamamlandı!")
            
        else:
            print("Doğrulama kodu alınamadı!")

        # Enter'a basılmasını bekle
        input("Çıkmak için Enter'a basın...")

if __name__ == "__main__":
    # Proxy, İngilizce locale, headed mode ve stealth mode ile çalıştır
    BaseCase.main(__name__, __file__, "--proxy=3ed492ea9d26670b06c1__cr.us:4e17d20cd644f516@gw.dataimpulse.com:823", "--locale=en", "--headed", "--uc", "--disable-csp")