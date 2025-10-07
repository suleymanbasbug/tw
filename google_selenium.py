import time
from seleniumbase import BaseCase
from mail_password import get_verification_code
import random

class TwitterSignup(BaseCase):
    
    def human_like_page_load(self):
        """İnsan benzeri sayfa yükleme davranışı"""
        # Sayfa yüklenirken gerçekçi bekleme
        time.sleep(random.uniform(5.0, 8.0))
        
        # Sayfa yüklenme animasyonlarını taklit et
        self.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(1.0, 2.0))
        
        # Küçük scroll hareketleri (sayfa keşfi)
        for _ in range(random.randint(3, 5)):
            scroll_amount = random.randint(50, 150)
            self.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.5, 1.2))
        
        # Başa dön
        self.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(1.0, 2.0))
    
    def human_like_scroll(self):
        """İnsan benzeri scroll davranışı"""
        scroll_steps = random.randint(4, 7)
        for i in range(scroll_steps):
            scroll_amount = random.randint(80, 300)
            self.execute_script(f"window.scrollBy(0, {scroll_amount});")
            
            # Scroll arası bekleme (insan okuma süresi)
            time.sleep(random.uniform(1.0, 3.0))
            
            # Bazen geri scroll (insan davranışı)
            if random.random() < 0.4:
                back_scroll = random.randint(30, scroll_amount // 2)
                self.execute_script(f"window.scrollBy(0, -{back_scroll});")
                time.sleep(random.uniform(0.8, 1.5))
        
        # Başa dön
        self.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(1.5, 3.0))
    
    def human_like_typing(self, selector, text, typing_speed="normal"):
        """İnsan benzeri yazma davranışı"""
        speed_ranges = {
            "slow": (0.3, 0.8),
            "normal": (0.15, 0.4),
            "fast": (0.08, 0.2)
        }
        
        min_delay, max_delay = speed_ranges.get(typing_speed, speed_ranges["normal"])
        
        # Elemente odaklan
        self.focus(selector)
        time.sleep(random.uniform(0.5, 1.0))
        
        # Karakter karakter yazma
        for i, char in enumerate(text):
            base_delay = random.uniform(min_delay, max_delay)
            
            # Özel karakterler için daha yavaş yazma
            if char in "!@#$%^&*()_+-=[]{}|;':\",./<>?":
                base_delay *= random.uniform(2.0, 3.0)
            
            # Büyük harfler için yavaş yazma
            if char.isupper():
                base_delay *= random.uniform(1.5, 2.5)
            
            # Gerçek karakteri yaz
            self.send_keys(selector, char)
            time.sleep(base_delay)
            
            # Bazen düşünme molası
            if random.random() < 0.15:  # %15 düşünme molası şansı
                time.sleep(random.uniform(1.0, 2.5))
            
            # Bazen yanlış tuş basma simülasyonu (çok nadir)
            if random.random() < 0.02:  # %2 yanlış tuş basma şansı
                time.sleep(random.uniform(0.3, 0.8))
                # Geri silme simülasyonu
                self.press_keys(selector, "\b")
                time.sleep(random.uniform(0.2, 0.5))
                # Tekrar yazma
                self.send_keys(selector, char)
                time.sleep(random.uniform(0.3, 0.6))
    
    def human_like_form_interaction(self, selector, text, field_type="text"):
        """Form alanı ile insan benzeri etkileşim"""
        # Elemente yaklaşma süresi
        time.sleep(random.uniform(0.5, 1.5))
        
        # Elemente tıklama
        self.hover_and_click(selector, selector)
        time.sleep(random.uniform(0.5, 1.2))
        
        # Odaklanma süresi
        time.sleep(random.uniform(0.5, 1.0))
        
        # Yazma öncesi bekleme
        time.sleep(random.uniform(0.3, 0.8))
        
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
        time.sleep(random.uniform(1.0, 2.0))
        
        # Bazen geri dönüp kontrol etme
        if random.random() < 0.4:  # %40 kontrol etme şansı
            time.sleep(random.uniform(0.5, 1.5))
            # Küçük mouse hareketi simülasyonu
            self.execute_script("window.scrollBy(0, 10);")
            time.sleep(random.uniform(0.2, 0.5))
            self.execute_script("window.scrollBy(0, -10);")
            time.sleep(random.uniform(0.3, 0.8))
    
    def human_like_button_interaction(self, selector, button_name):
        """Buton ile insan benzeri etkileşim"""
        # Butonu görme ve değerlendirme süresi
        time.sleep(random.uniform(2.0, 4.0))
        
        # Butona yaklaşma süresi
        time.sleep(random.uniform(0.5, 1.5))
        
        # Hover ve click
        self.hover_and_click(selector, selector, hover_by="css selector", click_by="css selector")
        
        # Tıklama sonrası bekleme
        time.sleep(random.uniform(1.0, 2.5))
        
        print(f"{button_name} butonuna insan benzeri etkileşim yapıldı!")
    
    def human_like_dropdown_interaction(self, selector, option_text, field_name):
        """Dropdown ile insan benzeri etkileşim"""
        # Dropdown'u görme ve değerlendirme süresi
        time.sleep(random.uniform(1.0, 2.0))
        
        # Dropdown'a yaklaşma
        time.sleep(random.uniform(0.5, 1.0))
        
        # Dropdown'a tıklama
        self.hover_and_click(selector, selector)
        time.sleep(random.uniform(0.5, 1.0))
        
        # Seçenekleri görme süresi
        time.sleep(random.uniform(0.8, 1.5))
        
        # Seçim yapma
        self.select_option_by_text(selector, option_text)
        time.sleep(random.uniform(0.8, 1.5))
        
        print(f"{field_name} olarak '{option_text}' insan benzeri şekilde seçildi!")
    
    def test_signup(self):
        email_address = "xscmfwnu@vargosmail.com"
        password = "bnycmoflS!4565"
        
        # Minimal stealth mode
        self.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
        self.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
        
        # İngilizce locale ile başlat
        self.open("https://x.com/i/flow/signup")
        
        # İnsan benzeri sayfa yükleme davranışı
        self.human_like_page_load()
        
        # İnsan benzeri scroll davranışı
        self.human_like_scroll()
        
        # Create account butonunu bul ve tıkla
        self.wait_for_element('button:contains("Create account")', timeout=15)
        self.human_like_button_interaction('button:contains("Create account")', "Create account")

        # Sayfanın yüklenmesini bekle
        time.sleep(random.uniform(3.0, 5.0))

        # Use email instead butonunu bul ve tıkla
        self.wait_for_element('button:contains("Use email instead")', timeout=15)
        self.human_like_button_interaction('button:contains("Use email instead")', "Use email instead")

        # Sayfanın yüklenmesini bekle
        time.sleep(random.uniform(3.0, 5.0))

        # Name input'una "hasan" yaz
        self.human_like_form_interaction('input[name="name"]', "hasan", "text")

        # Email input'una email yaz
        time.sleep(random.uniform(1.0, 2.0))
        self.human_like_form_interaction('input[name="email"]', email_address, "email")

        # Ay seçimi - June seç
        time.sleep(random.uniform(1.0, 2.0))
        self.human_like_dropdown_interaction('select[id="SELECTOR_1"]', "June", "Ay")

        # Gün seçimi - 27 seç
        time.sleep(random.uniform(0.8, 1.5))
        self.human_like_dropdown_interaction('select[id="SELECTOR_2"]', "27", "Gün")

        # Yıl seçimi - 1984 seç
        time.sleep(random.uniform(0.8, 1.5))
        self.human_like_dropdown_interaction('select[id="SELECTOR_3"]', "1984", "Yıl")

        # Next butonuna tıkla
        time.sleep(random.uniform(2.0, 4.0))
        self.human_like_button_interaction('button:contains("Next")', "Next")

        # E-posta doğrulama sayfasını bekle
        time.sleep(random.uniform(5.0, 8.0))
        print("Doğrulama kodu gönderildi!")
        
        # Doğrulama kodunu al
        time.sleep(random.uniform(3.0, 5.0))
        print("E-posta doğrulama kodu bekleniyor...")
        verification_code = get_verification_code(email_address, password)
        
        if verification_code:
            print(f"Doğrulama kodu alındı: {verification_code}")
            
            # Doğrulama kodunu input'a yaz
            time.sleep(random.uniform(2.0, 3.0))
            self.human_like_form_interaction('input[name="verfication_code"]', verification_code, "verification")
            
            # Next butonuna tıkla
            time.sleep(random.uniform(2.0, 3.0))
            self.human_like_button_interaction('span:contains("Next")', "Doğrulama Next")
            
            # Hesap oluşturma tamamlanmasını bekle
            time.sleep(random.uniform(6.0, 10.0))
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