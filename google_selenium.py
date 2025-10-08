import time
from seleniumbase import BaseCase
from mail_password import get_verification_code
from user_agents import USER_AGENTS
import random

class TwitterSignup(BaseCase):
    
    def get_random_user_agent(self):
        """Random user agent seçimi"""
        return random.choice(USER_AGENTS)
    
    def human_like_page_load(self):
        """İnsan benzeri sayfa yükleme davranışı"""
        try:
            # Sayfa yüklenirken makul bekleme
            time.sleep(random.uniform(2.0, 4.0))
            
            # Sayfa yüklenme animasyonlarını taklit et
            self.execute_script("window.scrollTo(0, 0);")
            time.sleep(random.uniform(1.0, 2.0))
            
            # Çok detaylı sayfa keşfi
            scroll_count = random.randint(3, 5)  # Daha az scroll
            for i in range(scroll_count):
                scroll_amount = random.randint(50, 150)  # Daha büyük scroll
                self.execute_script(f"window.scrollBy(0, {scroll_amount});")
                time.sleep(random.uniform(0.8, 1.5))
                
                # Bazen çok küçük geri scroll
                if random.random() < 0.3:
                    # Güvenli geri scroll
                    back_scroll = max(10, scroll_amount // 3)
                    self.execute_script(f"window.scrollBy(0, -{back_scroll});")
                    time.sleep(random.uniform(0.5, 1.0))
            
            # Başa dön
            self.execute_script("window.scrollTo(0, 0);")
            time.sleep(random.uniform(1.0, 2.0))
            
        except Exception as e:
            print(f"human_like_page_load içinde hata: {e}")
            # Basit scroll yap
            self.execute_script("window.scrollTo(0, 100);")
            time.sleep(1)
            self.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)
    
    def human_like_scroll(self):
        """İnsan benzeri scroll davranışı - çok detaylı"""
        scroll_steps = random.randint(6, 10)
        for i in range(scroll_steps):
            scroll_amount = random.randint(50, 200)
            self.execute_script(f"window.scrollBy(0, {scroll_amount});")
            
            # Makul okuma süresi
            time.sleep(random.uniform(1.0, 2.5))
            
            # Sık geri scroll (insan davranışı)
            if random.random() < 0.6:
                # Güvenli aralık kontrolü
                max_back_scroll = max(10, scroll_amount // 3)
                min_back_scroll = min(10, max_back_scroll)
                back_scroll = random.randint(min_back_scroll, max_back_scroll)
                self.execute_script(f"window.scrollBy(0, -{back_scroll});")
                time.sleep(random.uniform(1.0, 2.0))
        
        # Başa dön
        self.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(1.5, 3.0))
    
    def human_like_typing(self, selector, text, typing_speed="normal"):
        """İnsan benzeri yazma davranışı - çok gerçekçi"""
        speed_ranges = {
            "slow": (0.5, 1.2),
            "normal": (0.3, 0.8),
            "fast": (0.2, 0.5)
        }
        
        min_delay, max_delay = speed_ranges.get(typing_speed, speed_ranges["normal"])
        
        # Elemente odaklan
        self.focus(selector)
        time.sleep(random.uniform(1.0, 2.0))
        
        # Karakter karakter yazma
        for i, char in enumerate(text):
            base_delay = random.uniform(min_delay, max_delay)
            
            # Özel karakterler için çok yavaş yazma
            if char in "!@#$%^&*()_+-=[]{}|;':\",./<>?":
                base_delay *= random.uniform(3.0, 5.0)
            
            # Büyük harfler için çok yavaş yazma
            if char.isupper():
                base_delay *= random.uniform(2.0, 4.0)
            
            # Gerçek karakteri yaz
            self.send_keys(selector, char)
            time.sleep(base_delay)
            
            # Makul düşünme molası
            if random.random() < 0.25:  # %25 düşünme molası şansı
                time.sleep(random.uniform(1.0, 2.0))
            
            # Yanlış tuş basma simülasyonu (daha sık)
            if random.random() < 0.05:  # %5 yanlış tuş basma şansı
                time.sleep(random.uniform(0.5, 1.0))
                # Geri silme simülasyonu
                self.press_keys(selector, "\b")
                time.sleep(random.uniform(0.3, 0.8))
                # Tekrar yazma
                self.send_keys(selector, char)
                time.sleep(random.uniform(0.5, 1.0))
            
            # Bazen kelime arası makul duraklama
            if char == " " and random.random() < 0.3:
                time.sleep(random.uniform(0.8, 1.5))
    
    def human_like_form_interaction(self, selector, text, field_type="text"):
        """Form alanı ile insan benzeri etkileşim - çok detaylı"""
        # Elemente yaklaşma süresi
        time.sleep(random.uniform(1.0, 3.0))
        
        # Elemente tıklama
        self.hover_and_click(selector, selector)
        time.sleep(random.uniform(1.0, 2.0))
        
        # Odaklanma süresi
        time.sleep(random.uniform(1.0, 2.0))
        
        # Yazma öncesi bekleme
        time.sleep(random.uniform(0.5, 1.5))
        
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
        
        # Çok sık geri dönüp kontrol etme
        if random.random() < 0.7:  # %70 kontrol etme şansı
            time.sleep(random.uniform(1.0, 2.0))
            # Küçük mouse hareketi simülasyonu
            self.execute_script("window.scrollBy(0, 5);")
            time.sleep(random.uniform(0.3, 0.8))
            self.execute_script("window.scrollBy(0, -5);")
            time.sleep(random.uniform(0.5, 1.0))
    
    def human_like_button_interaction(self, selector, button_name):
        """Buton ile insan benzeri etkileşim - çok detaylı"""
        # Butonu görme ve değerlendirme süresi
        time.sleep(random.uniform(1.5, 3.0))
        
        # Butona yaklaşma süresi
        time.sleep(random.uniform(1.0, 2.5))
        
        # Hover ve click
        self.hover_and_click(selector, selector, hover_by="css selector", click_by="css selector")
        
        # Tıklama sonrası bekleme
        time.sleep(random.uniform(1.0, 2.0))
        
        print(f"{button_name} butonuna insan benzeri etkileşim yapıldı!")
    
    def human_like_dropdown_interaction(self, selector, option_text, field_name):
        """Dropdown ile insan benzeri etkileşim - çok detaylı"""
        # Dropdown'u görme ve değerlendirme süresi
        time.sleep(random.uniform(1.0, 2.0))
        
        # Dropdown'a yaklaşma
        time.sleep(random.uniform(1.0, 2.0))
        
        # Dropdown'a tıklama
        self.hover_and_click(selector, selector)
        time.sleep(random.uniform(1.0, 2.0))
        
        # Seçenekleri görme süresi
        time.sleep(random.uniform(0.8, 1.5))
        
        # Seçim yapma
        self.select_option_by_text(selector, option_text)
        time.sleep(random.uniform(0.8, 1.5))
        
        print(f"{field_name} olarak '{option_text}' insan benzeri şekilde seçildi!")
    
    def simulate_human_reading(self):
        """İnsan okuma davranışı simülasyonu"""
        # Sayfayı okuma simülasyonu
        for _ in range(random.randint(3, 6)):
            scroll_amount = random.randint(20, 80)
            self.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(1.5, 3.0))
            
            # Bazen geri scroll
            if random.random() < 0.4:
                # Güvenli geri scroll
                back_scroll = max(5, scroll_amount // 2)
                self.execute_script(f"window.scrollBy(0, -{back_scroll});")
                time.sleep(random.uniform(1.0, 2.0))
        
        # Başa dön
        self.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(1.0, 2.0))
    
    def test_signup(self):
        try:
            email_address = "xscmfwnu@vargosmail.com"
            password = "bnycmoflS!4565"
            
            # Random user agent seçimi
            random_user_agent = self.get_random_user_agent()
            print(f"Seçilen User Agent: {random_user_agent}")
            
            # User agent ayarını yap
            self.execute_script(f"Object.defineProperty(navigator, 'userAgent', {{get: () => '{random_user_agent}'}})")
            
            # Minimal stealth mode
            self.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
            self.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
            
            print("Stealth mode ayarları yapıldı!")
            
            # Normal mode ile sayfayı aç
            print("Twitter signup sayfası açılıyor...")
            self.open("https://x.com/i/flow/signup")
            print("Sayfa başarıyla açıldı!")
            
            # Sayfa yüklenmesini bekle
            time.sleep(random.uniform(3.0, 5.0))
            
            # Sayfa yüklenmesini kısa bekle
            time.sleep(random.uniform(2.0, 3.0))
            
            # Create account butonunu bul ve UC Mode ile tıkla
            print("Create account butonu aranıyor...")
            self.wait_for_element('button:contains("Create account")', timeout=20)
            self.uc_click('button:contains("Create account")')
            print("Create account butonu UC Mode ile tıklandı!")

            # Sayfanın yüklenmesini bekle
            time.sleep(random.uniform(2.0, 4.0))

            # Use email instead butonunu bul ve tıkla
            print("Use email instead butonu aranıyor...")
            self.wait_for_element('button:contains("Use email instead")', timeout=20)
            self.human_like_button_interaction('button:contains("Use email instead")', "Use email instead")

            # Sayfanın yüklenmesini bekle
            time.sleep(random.uniform(2.0, 4.0))

            # Name input'una "hasan" yaz
            print("Name alanına yazılıyor...")
            self.human_like_form_interaction('input[name="name"]', "hasan", "text")

            # Email input'una email yaz
            time.sleep(random.uniform(2.0, 4.0))
            print("Email alanına yazılıyor...")
            self.human_like_form_interaction('input[name="email"]', email_address, "email")

            # Ay seçimi - June seç
            time.sleep(random.uniform(2.0, 4.0))
            print("Ay seçimi yapılıyor...")
            self.human_like_dropdown_interaction('select[id="SELECTOR_1"]', "June", "Ay")

            # Gün seçimi - 27 seç
            time.sleep(random.uniform(1.5, 3.0))
            print("Gün seçimi yapılıyor...")
            self.human_like_dropdown_interaction('select[id="SELECTOR_2"]', "27", "Gün")

            # Yıl seçimi - 1984 seç
            time.sleep(random.uniform(1.5, 3.0))
            print("Yıl seçimi yapılıyor...")
            self.human_like_dropdown_interaction('select[id="SELECTOR_3"]', "1984", "Yıl")

            # Next butonuna tıkla
            time.sleep(random.uniform(3.0, 6.0))
            print("Next butonuna tıklanıyor...")
            self.human_like_button_interaction('button:contains("Next")', "Next")

            # E-posta doğrulama sayfasını bekle
            time.sleep(random.uniform(3.0, 5.0))
            print("Doğrulama kodu gönderildi!")
            
            # Doğrulama kodunu al
            time.sleep(random.uniform(2.0, 4.0))
            print("E-posta doğrulama kodu bekleniyor...")
            verification_code = get_verification_code(email_address, password)
            
            if verification_code:
                print(f"Doğrulama kodu alındı: {verification_code}")
                
                # Doğrulama kodunu input'a yaz
                time.sleep(random.uniform(3.0, 5.0))
                self.human_like_form_interaction('input[name="verfication_code"]', verification_code, "verification")
                
                # Next butonuna tıkla
                time.sleep(random.uniform(3.0, 5.0))
                self.human_like_button_interaction('span:contains("Next")', "Doğrulama Next")
                
                # Hesap oluşturma tamamlanmasını bekle
                time.sleep(random.uniform(5.0, 8.0))
                print("Hesap oluşturma işlemi tamamlandı!")
                
            else:
                print("Doğrulama kodu alınamadı!")

            # Enter'a basılmasını bekle
            input("Çıkmak için Enter'a basın...")
            
        except Exception as e:
            print(f"Hata oluştu: {e}")
            print(f"Hata türü: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            
            # Hata durumunda da tarayıcıyı açık tut
            print("Hata nedeniyle tarayıcı açık tutuluyor...")
            input("Hata analizi için Enter'a basın...")

if __name__ == "__main__":
    # Minimal ayarlarla çalıştır
    BaseCase.main(
        __name__, 
        __file__, 
        "--proxy=3ed492ea9d26670b06c1__cr.us:4e17d20cd644f516@gw.dataimpulse.com:823",
        "--locale=en", 
        "--headed", 
        "--uc",  # UC Mode
        "--incognito"  # Incognito mode ile daha iyi gizlilik
    )