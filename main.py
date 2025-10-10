import random
import time
import math
from seleniumbase import BaseCase
from utils.mail_password import get_verification_code
from utils.user_agents import USER_AGENTS
from utils.stealth import StealthHelper
from utils.form_handler import FormHandler
from utils.captcha_detector import CaptchaDetector
from utils.user_data_generator import get_random_user_info

class TwitterSignup(BaseCase):
    
    def get_random_user_agent(self):
        """Random user agent seçimi"""
        return random.choice(USER_AGENTS)
    
    def gaussian_random(self, mean, std_dev):
        """Gauss dağılımından rastgele sayı üret"""
        # Box-Muller transformasyonu
        u1 = random.random()
        u2 = random.random()
        z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        return mean + z0 * std_dev
    
    
    def test_signup(self):
        try:
            email_address = "ekdkjkbq@fringmail.com"
            password = "kgmafqhkA!9074"
            
            # Random user agent seçimi
            random_user_agent = self.get_random_user_agent()
            print(f"Seçilen User Agent: {random_user_agent}")
            
            # CDP Mode ile Twitter signup sayfasını aç
            print("CDP Mode ile Twitter signup sayfası açılıyor...")
            self.activate_cdp_mode("https://x.com/i/flow/signup")
            print("CDP Mode aktif edildi!")
            print("CDP hazırlanıyor...")
            self.sleep(2)  # CDP'nin tamamen hazır olması için
            
            # Captcha tespit sistemini erken başlat (CDP aktif olduktan hemen sonra)
            print("\n🎯 Captcha tespit sistemi erken başlatılıyor...")
            captcha_detector = CaptchaDetector(self)
            captcha_detector.setup_network_monitoring()
            
            # Sayfa yüklenmesini bekle - Gauss dağılımı
            page_load_delay = self.gaussian_random(4.0, 1.0)
            page_load_delay = max(2.0, min(7.0, page_load_delay))
            self.sleep(page_load_delay)
            
            # Stealth ayarlarını kur
            print("Stealth ayarları kuruluyor...")
            stealth = StealthHelper(self.cdp)
            stealth.setup_consistent_fingerprints()  # Session tutarlı fingerprint'ler
            stealth.block_webrtc_leak()  # YENİ
            stealth.setup_timezone_locale()  # YENİ
            stealth.setup_browser_properties()  # YENİ
            stealth.setup_request_headers()  # YENİ
            
            # Human behavior ekle
            from utils.human_behavior import HumanBehavior
            human = HumanBehavior(self)
            human.random_mouse_movement()  # YENİ
            
            # Sayfa yüklenmesini bekle - Gauss dağılımı
            post_stealth_delay = self.gaussian_random(4.0, 1.0)
            post_stealth_delay = max(2.0, min(7.0, post_stealth_delay))
            self.sleep(post_stealth_delay)
            
            # Create account butonunu bul ve CDP Mode ile tıkla
            print("Create account butonu aranıyor...")
            self.wait_for_element('//button[contains(text(), "Create account")]', timeout=20)
            
            # CDP Mode ile insan benzeri tıklama
            pre_click_delay = self.gaussian_random(2.0, 0.5)
            pre_click_delay = max(1.0, min(3.5, pre_click_delay))
            self.sleep(pre_click_delay)
            self.cdp.click('//button[contains(text(), "Create account")]')
            print("Create account butonu CDP Mode ile tıklandı!")

            # Sayfanın yüklenmesini bekle - Gauss dağılımı
            page_load_delay = self.gaussian_random(4.0, 1.0)
            page_load_delay = max(2.0, min(7.0, page_load_delay))
            self.sleep(page_load_delay)

            # Use email instead butonunu bul ve CDP Mode ile tıkla
            print("Use email instead butonu aranıyor...")
            self.wait_for_element('//button[contains(text(), "Use email instead")]', timeout=20)
            pre_click_delay = self.gaussian_random(2.0, 0.5)
            pre_click_delay = max(1.0, min(3.5, pre_click_delay))
            self.sleep(pre_click_delay)
            self.cdp.click('//button[contains(text(), "Use email instead")]')
            print("Use email instead butonu CDP Mode ile tıklandı!")

            # Sayfanın yüklenmesini bekle - Gauss dağılımı
            page_load_delay = self.gaussian_random(4.0, 1.0)
            page_load_delay = max(2.0, min(7.0, page_load_delay))
            self.sleep(page_load_delay)

            # Form handler'ı başlat
            form = FormHandler(self)
            
            # Rastgele kullanıcı bilgileri üret
            print("🎲 Rastgele kullanıcı bilgileri üretiliyor...")
            user_info = get_random_user_info()
            print(f"Seçilen isim: {user_info['name']}")
            print(f"Seçilen doğum tarihi: {user_info['birth_month']} {user_info['birth_day']}, {user_info['birth_year']}")
            
            # Form alanlarını doldur
            form.fill_name(user_info['name'])
            form.fill_email(email_address)
            form.fill_birthdate(user_info['birth_month'], user_info['birth_day'], user_info['birth_year'])

            # Form validasyonunu tetikle
            form.validate_form()

            # Next buton durumunu kontrol et
            if form.check_next_button_status():
                print("Next butonu aktif! Tıklanıyor...")
                form.click_next_button()
                print("Next butonu CDP Mode ile tıklandı!")
                
                # Captcha'nın yüklenmesini bekle (zaten başlatılmış)
                print("\n🎯 Captcha yüklenmesi bekleniyor...")
                captcha_detected = captcha_detector.wait_for_captcha()
                
                if captcha_detected:
                    print("✅ Captcha başarıyla tespit edildi!")
                    
                    # FunCaptcha Authenticate butonuna tıkla
                    print("\n🎯 FunCaptcha Authenticate butonu tıklanıyor...")
                    authenticate_success = captcha_detector.click_captcha_authenticate_button()
                    
                    if authenticate_success:
                        print("🎉 FunCaptcha Authenticate işlemi başarılı!")
                        # Captcha çözümü sonrası devam edebilirsiniz
                        self.sleep(3)  # Captcha'nın işlenmesi için bekle
                    else:
                        print("❌ FunCaptcha Authenticate işlemi başarısız!")
                        print("🔄 Manuel müdahale gerekebilir...")
                        
                else:
                    print("❌ Captcha tespit edilemedi!")
                
            else:
                print("Next butonu hala disabled! Manuel müdahale gerekebilir.")
                form.get_form_debug_info()
                
                # Manuel müdahale için bekle
                try:
                    input("Next butonu aktif olmadı. Manuel kontrol için Enter'a basın...")
                except EOFError:
                    print("Test ortamında manuel müdahale atlandı...")


            # E-posta doğrulama sayfasını bekle - Gauss dağılımı
            email_delay = self.gaussian_random(4.0, 1.0)
            email_delay = max(2.0, min(7.0, email_delay))
            self.sleep(email_delay)
            print("Doğrulama kodu gönderildi!")
            
            # Doğrulama kodunu al - Gauss dağılımı
            code_delay = self.gaussian_random(3.0, 1.0)
            code_delay = max(1.0, min(6.0, code_delay))
            self.sleep(code_delay)
            print("E-posta doğrulama kodu bekleniyor...")
            verification_code = get_verification_code(email_address, password)
            
            if verification_code:
                print(f"Doğrulama kodu alındı: {verification_code}")
                
                # Doğrulama kodunu gir
                form.fill_verification_code(verification_code)
                
                # Next butonuna tıkla - Gauss dağılımı
                next_delay = self.gaussian_random(3.0, 1.0)
                next_delay = max(1.0, min(6.0, next_delay))
                self.sleep(next_delay)
                form.click_next_button()
                
                # Hesap oluşturma tamamlanmasını bekle - Gauss dağılımı
                completion_delay = self.gaussian_random(6.5, 1.5)
                completion_delay = max(3.0, min(12.0, completion_delay))
                self.sleep(completion_delay)
                print("Hesap oluşturma işlemi tamamlandı!")
                print("CDP Mode sayesinde robot tespiti bypass edildi!")
                
            else:
                print("Doğrulama kodu alınamadı!")

            
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