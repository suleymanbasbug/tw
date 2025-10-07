import time
from seleniumbase import BaseCase
from mail_password import get_verification_code
import random

class TwitterSignup(BaseCase):
    
    def human_like_page_load(self):
        """İnsan benzeri sayfa yükleme davranışı"""
        # Sayfa yüklenirken gerçekçi bekleme
        time.sleep(random.uniform(3.0, 6.0))
        
        # Basit scroll hareketleri
        for _ in range(random.randint(2, 4)):
            scroll_amount = random.randint(50, 200)
            self.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.3, 0.8))
        
        # Başa dön
        self.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(0.5, 1.0))
    
    def human_like_scroll(self):
        """İnsan benzeri scroll davranışı"""
        scroll_steps = random.randint(3, 6)
        for i in range(scroll_steps):
            scroll_amount = random.randint(100, 400)
            self.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.8, 2.5))
            
            # Bazen geri scroll
            if random.random() < 0.3:
                back_scroll = random.randint(50, scroll_amount // 2)
                self.execute_script(f"window.scrollBy(0, -{back_scroll});")
                time.sleep(random.uniform(0.5, 1.2))
        
        # Başa dön
        self.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(1.0, 2.0))
    
    def human_like_typing(self, selector, text, typing_speed="normal"):
        """İnsan benzeri yazma davranışı"""
        speed_ranges = {
            "slow": (0.2, 0.6),
            "normal": (0.1, 0.3),
            "fast": (0.05, 0.15)
        }
        
        min_delay, max_delay = speed_ranges.get(typing_speed, speed_ranges["normal"])
        
        # Elemente odaklan
        self.focus(selector)
        time.sleep(random.uniform(0.2, 0.5))
        
        # Karakter karakter yazma
        for char in text:
            base_delay = random.uniform(min_delay, max_delay)
            
            # Özel karakterler için daha yavaş yazma
            if char in "!@#$%^&*()_+-=[]{}|;':\",./<>?":
                base_delay *= random.uniform(1.5, 2.5)
            
            # Büyük harfler için yavaş yazma
            if char.isupper():
                base_delay *= random.uniform(1.2, 1.8)
            
            # Gerçek karakteri yaz
            self.send_keys(selector, char)
            time.sleep(base_delay)
            
            # Bazen düşünme molası
            if random.random() < 0.1:
                time.sleep(random.uniform(0.5, 1.5))
    
    def human_like_form_interaction(self, selector, text, field_type="text"):
        """Form alanı ile insan benzeri etkileşim"""
        # Elemente tıklama
        self.hover_and_click(selector, selector)
        time.sleep(random.uniform(0.3, 0.8))
        
        # Yazma öncesi bekleme
        time.sleep(random.uniform(0.2, 0.5))
        
        # Alan tipine göre yazma hızı
        if field_type == "email":
            typing_speed = "fast"
        elif field_type == "password":
            typing_speed = "slow"
        elif field_type == "verification":
            typing_speed = "slow"
        else:
            typing_speed = "normal"
        
        # İnsan benzeri yazma
        self.human_like_typing(selector, text, typing_speed)
        
        # Yazma sonrası kontrol süresi
        time.sleep(random.uniform(0.5, 1.5))
    
    def test_signup(self):
        email_address = "xscmfwnu@vargosmail.com"
        password = "bnycmoflS!4565"
        
        # Minimal stealth mode (sadece temel ayarlar)
        self.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # İngilizce locale ile başlat
        self.open("https://x.com/i/flow/signup")
        
        # İnsan benzeri sayfa yükleme davranışı
        self.human_like_page_load()
        
        # İnsan benzeri scroll davranışı
        self.human_like_scroll()
        
        # Create account butonunu bul ve tıkla
        self.wait_for_element('button:contains("Create account")', timeout=10)
        time.sleep(random.uniform(2.0, 4.0))
        
        self.hover_and_click(
            'button:contains("Create account")', 
            'button:contains("Create account")',
            hover_by="css selector", 
            click_by="css selector"
        )
        time.sleep(random.uniform(0.5, 1.5))
        print("Create account butonuna tıklandı!")

        # Sayfanın yüklenmesini bekle
        time.sleep(random.uniform(2.0, 4.0))

        # Use email instead butonunu bul ve tıkla
        self.wait_for_element('button:contains("Use email instead")', timeout=10)
        time.sleep(random.uniform(1.0, 2.5))
        
        self.hover_and_click(
            'button:contains("Use email instead")', 
            'button:contains("Use email instead")',
            hover_by="css selector", 
            click_by="css selector"
        )
        time.sleep(random.uniform(0.5, 1.5))
        print("Use email instead butonuna tıklandı!")

        # Sayfanın yüklenmesini bekle
        time.sleep(random.uniform(2.0, 4.0))

        # Name input'una "hasan" yaz
        time.sleep(random.uniform(1.0, 2.0))
        self.human_like_form_interaction('input[name="name"]', "hasan", "text")
        print("Name input'una 'hasan' yazıldı!")

        # Email input'una email yaz
        time.sleep(random.uniform(0.8, 1.8))
        self.human_like_form_interaction('input[name="email"]', email_address, "email")
        print(f"Email input'una '{email_address}' yazıldı!")

        # Ay seçimi - June seç
        time.sleep(random.uniform(0.8, 1.8))
        self.hover_and_click('select[id="SELECTOR_1"]', 'select[id="SELECTOR_1"]')
        time.sleep(random.uniform(0.3, 0.8))
        time.sleep(random.uniform(0.5, 1.2))
        
        self.select_option_by_text('select[id="SELECTOR_1"]', "June")
        time.sleep(random.uniform(0.5, 1.2))
        print("Ay olarak 'June' seçildi!")

        # Gün seçimi - 27 seç
        time.sleep(random.uniform(0.5, 1.2))
        self.hover_and_click('select[id="SELECTOR_2"]', 'select[id="SELECTOR_2"]')
        time.sleep(random.uniform(0.3, 0.8))
        time.sleep(random.uniform(0.5, 1.2))
        
        self.select_option_by_text('select[id="SELECTOR_2"]', "27")
        time.sleep(random.uniform(0.5, 1.2))
        print("Gün olarak '27' seçildi!")

        # Yıl seçimi - 1984 seç
        time.sleep(random.uniform(0.5, 1.2))
        self.hover_and_click('select[id="SELECTOR_3"]', 'select[id="SELECTOR_3"]')
        time.sleep(random.uniform(0.3, 0.8))
        time.sleep(random.uniform(0.5, 1.2))
        
        self.select_option_by_text('select[id="SELECTOR_3"]', "1984")
        time.sleep(random.uniform(0.5, 1.2))
        print("Yıl olarak '1984' seçildi!")

        # Next butonuna tıkla
        time.sleep(random.uniform(1.5, 3.0))
        self.hover_and_click(
            'button:contains("Next")', 
            'button:contains("Next")',
            hover_by="css selector", 
            click_by="css selector"
        )
        time.sleep(random.uniform(0.5, 1.5))
        print("Next butonuna tıklandı!")

        # E-posta doğrulama sayfasını bekle
        time.sleep(random.uniform(4.0, 7.0))
        print("Doğrulama kodu gönderildi!")
        
        # Doğrulama kodunu al
        time.sleep(random.uniform(2.0, 4.0))
        print("E-posta doğrulama kodu bekleniyor...")
        verification_code = get_verification_code(email_address, password)
        
        if verification_code:
            print(f"Doğrulama kodu alındı: {verification_code}")
            
            # Doğrulama kodunu input'a yaz
            time.sleep(random.uniform(1.0, 2.0))
            self.human_like_form_interaction('input[name="verfication_code"]', verification_code, "verification")
            print("Doğrulama kodu yazıldı!")
            
            # Next butonuna tıkla
            time.sleep(random.uniform(1.5, 2.5))
            self.hover_and_click(
                'span:contains("Next")', 
                'span:contains("Next")',
                hover_by="css selector", 
                click_by="css selector"
            )
            time.sleep(random.uniform(0.5, 1.5))
            print("Doğrulama kodu ile Next butonuna tıklandı!")
            
            # Hesap oluşturma tamamlanmasını bekle
            time.sleep(random.uniform(5.0, 8.0))
            print("Hesap oluşturma işlemi tamamlandı!")
            
        else:
            print("Doğrulama kodu alınamadı!")

        # Enter'a basılmasını bekle
        input("Çıkmak için Enter'a basın...")

if __name__ == "__main__":
    # Minimal ayarlarla çalıştır
    BaseCase.main(
        __name__, 
        __file__, 
        "--proxy=3ed492ea9d26670b06c1__cr.us:4e17d20cd644f516@gw.dataimpulse.com:823",
        "--locale=en", 
        "--headed", 
        "--uc"  # Sadece UC Mode
    )