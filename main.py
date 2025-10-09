import random
import time
from seleniumbase import BaseCase
from utils.mail_password import get_verification_code
from utils.user_agents import USER_AGENTS
from utils.stealth import StealthHelper
from utils.form_handler import FormHandler
from utils.captcha_detector import CaptchaDetector

class TwitterSignup(BaseCase):
    
    def get_random_user_agent(self):
        """Random user agent seçimi"""
        return random.choice(USER_AGENTS)
    
    
    def test_signup(self):
        try:
            email_address = "xscmfwnu@vargosmail.com"
            password = "bnycmoflS!4565"
            
            # Random user agent seçimi
            random_user_agent = self.get_random_user_agent()
            print(f"Seçilen User Agent: {random_user_agent}")
            
            # CDP Mode ile Twitter signup sayfasını aç
            print("CDP Mode ile Twitter signup sayfası açılıyor...")
            self.activate_cdp_mode("https://x.com/i/flow/signup")
            print("CDP Mode aktif edildi!")
            
            # Sayfa yüklenmesini bekle
            self.sleep(random.uniform(3.0, 5.0))
            
            # Stealth ayarlarını kur
            print("Stealth ayarları kuruluyor...")
            stealth = StealthHelper(self.cdp)
            stealth.setup_all_stealth()
            
            # Captcha detector'ı başlat
            print("Captcha detector başlatılıyor...")
            captcha_detector = CaptchaDetector(self.cdp)
            captcha_detector.setup_network_listener()
            
            # Sayfa yüklenmesini bekle
            self.sleep(random.uniform(3.0, 5.0))
            
            # Create account butonunu bul ve CDP Mode ile tıkla
            print("Create account butonu aranıyor...")
            self.wait_for_element('//button[contains(text(), "Create account")]', timeout=20)
            
            # CDP Mode ile insan benzeri tıklama
            self.sleep(random.uniform(1.5, 2.5))
            self.cdp.click('//button[contains(text(), "Create account")]')
            print("Create account butonu CDP Mode ile tıklandı!")

            # Sayfanın yüklenmesini bekle
            self.sleep(random.uniform(3.0, 5.0))

            # Use email instead butonunu bul ve CDP Mode ile tıkla
            print("Use email instead butonu aranıyor...")
            self.wait_for_element('//button[contains(text(), "Use email instead")]', timeout=20)
            self.sleep(random.uniform(1.5, 2.5))
            self.cdp.click('//button[contains(text(), "Use email instead")]')
            print("Use email instead butonu CDP Mode ile tıklandı!")

            # Sayfanın yüklenmesini bekle
            self.sleep(random.uniform(3.0, 5.0))

            # Form handler'ı başlat
            form = FormHandler(self)
            
            # Form alanlarını doldur
            form.fill_name("hasan")
            form.fill_email(email_address)
            form.fill_birthdate("June", "27", "1984")

            # Form validasyonunu tetikle
            form.validate_form()

            # Next buton durumunu kontrol et
            if form.check_next_button_status():
                print("Next butonu aktif! Tıklanıyor...")
                form.click_next_button()
                print("Next butonu CDP Mode ile tıklandı!")
            else:
                print("Next butonu hala disabled! Manuel müdahale gerekebilir.")
                form.get_form_debug_info()
                
                # Manuel müdahale için bekle
                try:
                    input("Next butonu aktif olmadı. Manuel kontrol için Enter'a basın...")
                except EOFError:
                    print("Test ortamında manuel müdahale atlandı...")

            # Captcha kontrolü yap
            print("Captcha kontrolü yapılıyor...")
            self.sleep(random.uniform(2.0, 4.0))
            
            # Captcha yüklenme durumunu kontrol et
            if captcha_detector.check_if_captcha_loaded():
                print("🚨 Captcha tespit edildi! Manuel çözüm bekleniyor...")
                captcha_detector.wait_for_manual_solve()
                
                # Gelecekte captcha solver entegrasyonu için placeholder
                # TODO: Otomatik captcha çözüm servisi entegrasyonu
                # captcha_solver = CaptchaSolver()
                # solution = captcha_solver.solve_captcha()
                
            else:
                print("✅ Captcha tespit edilmedi, normal akış devam ediyor...")

            # E-posta doğrulama sayfasını bekle
            self.sleep(random.uniform(3.0, 5.0))
            print("Doğrulama kodu gönderildi!")
            
            # Doğrulama kodunu al
            self.sleep(random.uniform(2.0, 4.0))
            print("E-posta doğrulama kodu bekleniyor...")
            verification_code = get_verification_code(email_address, password)
            
            if verification_code:
                print(f"Doğrulama kodu alındı: {verification_code}")
                
                # Doğrulama kodunu gir
                form.fill_verification_code(verification_code)
                
                # Next butonuna tıkla
                self.sleep(random.uniform(2.0, 4.0))
                form.click_next_button()
                
                # Hesap oluşturma tamamlanmasını bekle
                self.sleep(random.uniform(5.0, 8.0))
                print("Hesap oluşturma işlemi tamamlandı!")
                print("CDP Mode sayesinde robot tespiti bypass edildi!")
                
            else:
                print("Doğrulama kodu alınamadı!")

            # Captcha detector'ı temizle
            captcha_detector.cleanup()
            
            # Enter'a basılmasını bekle
            try:
                input("Çıkmak için Enter'a basın...")
            except EOFError:
                print("Test ortamında çıkış atlandı...")
            
        except Exception as e:
            print(f"Hata oluştu: {e}")
            print(f"Hata türü: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            
            # Hata durumunda da tarayıcıyı açık tut
            print("Hata nedeniyle tarayıcı açık tutuluyor...")
            try:
                input("Hata analizi için Enter'a basın...")
            except EOFError:
                print("Test ortamında hata analizi atlandı...")

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