import random
import time
from seleniumbase import BaseCase
from mail_password import get_verification_code
from user_agents import USER_AGENTS
from monitoring import NetworkMonitor

class TwitterSignup(BaseCase):
    
    def get_random_user_agent(self):
        """Random user agent seçimi"""
        return random.choice(USER_AGENTS)
    
    def cdp_human_type(self, selector, text, speed="normal"):
        """CDP Mode ile insan benzeri yazma + form validasyonu"""
        # Input'a odaklan
        self.cdp.click(selector)
        self.sleep(random.uniform(0.5, 1.0))
        
        # Yazma işlemi
        if speed == "slow":
            # Yavaş yazma için karakter karakter - press_keys ile
            for char in text:
                self.cdp.press_keys(selector, char)
                self.sleep(random.uniform(0.2, 0.4))
        else:
            # Normal ve hızlı yazma için press_keys kullan
            self.cdp.press_keys(selector, text)
        
        # Form validasyonunu tetikle - Focus/blur cycle + event dispatch
        self.cdp.evaluate(f"""
            (function() {{
                const inputElement = document.querySelector('{selector}');
                if (inputElement) {{
                    // Focus/blur cycle ile validasyonu tetikle
                    inputElement.focus();
                    inputElement.blur();
                    
                    // JavaScript eventleri tetikle
                    inputElement.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    inputElement.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    inputElement.dispatchEvent(new Event('blur', {{ bubbles: true }}));
                    
                    // Form validasyonunu zorla tetikle
                    if (inputElement.form) {{
                        inputElement.form.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    }}
                }}
            }})();
        """)
        
        # Validasyon işleminin tamamlanmasını bekle
        self.sleep(random.uniform(0.5, 1.0))
        
        return True
    
    def setup_network_monitoring(self):
        """Network isteklerini izlemek için CDP ayarları - NetworkMonitor sınıfını kullanır"""
        network_monitor = NetworkMonitor(self)
        return network_monitor.setup_network_monitoring()

    def monitor_console_logs(self):
        """Console loglarını izle - NetworkMonitor sınıfını kullanır"""
        network_monitor = NetworkMonitor(self)
        return network_monitor.monitor_console_logs()
    
    
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
            
            # CDP Mode ek stealth ayarları
            print("CDP Mode ile ek stealth ayarları yapılıyor...")
            
            # Canvas fingerprinting bypass
            self.cdp.evaluate("""
                const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
                HTMLCanvasElement.prototype.toDataURL = function(type) {
                    if (type === 'image/png' && this.width === 280 && this.height === 60) {
                        return 'data:image/png;base64,iVBORw0KGg==';
                    }
                    return originalToDataURL.apply(this, arguments);
                };
            """)
            
            # WebGL fingerprinting bypass
            self.cdp.evaluate("""
                const getParameter = WebGLRenderingContext.prototype.getParameter;
                WebGLRenderingContext.prototype.getParameter = function(parameter) {
                    if (parameter === 37445) {
                        return 'Intel Inc.';
                    }
                    if (parameter === 37446) {
                        return 'Intel Iris OpenGL Engine';
                    }
                    return getParameter.apply(this, arguments);
                };
            """)
            
            # Audio fingerprinting bypass
            self.cdp.evaluate("""
                const audioContext = window.AudioContext || window.webkitAudioContext;
                if (audioContext) {
                    const OriginalAudioContext = audioContext;
                    window.AudioContext = function() {
                        const context = new OriginalAudioContext();
                        const originalCreateOscillator = context.createOscillator;
                        context.createOscillator = function() {
                            const oscillator = originalCreateOscillator.apply(this, arguments);
                            const originalStart = oscillator.start;
                            oscillator.start = function() {
                                // Ses parmak izini değiştir
                                return originalStart.apply(this, arguments);
                            };
                            return oscillator;
                        };
                        return context;
                    };
                }
            """)
            
            # Ek stealth scriptleri - dokümantasyondan
            self.cdp.evaluate("""
                // WebDriver tespitini engelle
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                // Plugin sayısını artır
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                
                // Language ayarları
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en'],
                });
                
                // Permissions API bypass
                const originalQuery = window.navigator.permissions.query;
                window.navigator.permissions.query = (parameters) => (
                    parameters.name === 'notifications' ?
                        Promise.resolve({ state: Notification.permission }) :
                        originalQuery(parameters)
                );
            """)
            
            print("CDP Mode stealth ayarları tamamlandı!")
            
            # Network izlemeyi başlat
            print("Network izleme sistemi başlatılıyor...")
            self.setup_network_monitoring()
            
            # Console log izlemeyi başlat
            print("Console log izleme sistemi başlatılıyor...")
            self.monitor_console_logs()
            
            # Sayfa yüklenmesini bekle
            self.sleep(random.uniform(3.0, 5.0))
            
            # Sayfa yüklenmesini kısa bekle
            self.sleep(random.uniform(2.0, 3.0))
            
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

            # Name input'una "hasan" yaz - CDP Mode ile
            print("Name alanına CDP Mode ile yazılıyor...")
            self.sleep(random.uniform(1.0, 2.0))
            self.cdp_human_type('input[name="name"]', "hasan", "normal")
            print("Name alanı CDP Mode ile dolduruldu!")

            # Email input'una email yaz - CDP Mode ile
            self.sleep(random.uniform(2.0, 4.0))
            print("Email alanına CDP Mode ile yazılıyor...")
            self.cdp_human_type('input[name="email"]', email_address, "fast")
            print("Email alanı CDP Mode ile dolduruldu!")

            # Ay seçimi - June seç (CDP Mode ile)
            self.sleep(random.uniform(2.0, 4.0))
            print("Ay seçimi CDP Mode ile yapılıyor...")
            month_select = 'select[id="SELECTOR_1"]'
            self.cdp.select_option_by_text(month_select, "June")
            
            # Ay seçimi validasyonu tetikle
            self.cdp.evaluate(f"""
                const monthElement = document.querySelector('{month_select}');
                if (monthElement) {{
                    monthElement.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    monthElement.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    if (monthElement.form) {{
                        monthElement.form.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    }}
                }}
            """)
            self.sleep(random.uniform(0.5, 1.0))
            print("Ay seçimi CDP Mode ile tamamlandı!")

            # Gün seçimi - 27 seç (CDP Mode ile)
            self.sleep(random.uniform(1.5, 3.0))
            print("Gün seçimi CDP Mode ile yapılıyor...")
            day_select = 'select[id="SELECTOR_2"]'
            self.cdp.select_option_by_text(day_select, "27")
            
            # Gün seçimi validasyonu tetikle
            self.cdp.evaluate(f"""
                const dayElement = document.querySelector('{day_select}');
                if (dayElement) {{
                    dayElement.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    dayElement.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    if (dayElement.form) {{
                        dayElement.form.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    }}
                }}
            """)
            self.sleep(random.uniform(0.5, 1.0))
            print("Gün seçimi CDP Mode ile tamamlandı!")

            # Yıl seçimi - 1984 seç (CDP Mode ile)
            self.sleep(random.uniform(1.5, 3.0))
            print("Yıl seçimi CDP Mode ile yapılıyor...")
            year_select = 'select[id="SELECTOR_3"]'
            self.cdp.select_option_by_text(year_select, "1984")
            
            # Yıl seçimi validasyonu tetikle
            self.cdp.evaluate(f"""
                const yearElement = document.querySelector('{year_select}');
                if (yearElement) {{
                    yearElement.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    yearElement.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    if (yearElement.form) {{
                        yearElement.form.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    }}
                }}
            """)
            self.sleep(random.uniform(0.5, 1.0))
            print("Yıl seçimi CDP Mode ile tamamlandı!")

            # Next butonuna tıklamadan önce form validasyonunu kontrol et
            self.sleep(random.uniform(2.0, 4.0))
            print("Form validasyonu kontrol ediliyor...")
            
            # Tüm form alanlarını tekrar tetikle
            self.cdp.evaluate("""
                // Tüm input ve select alanlarını bul ve eventleri tetikle
                const inputs = document.querySelectorAll('input, select');
                inputs.forEach(input => {
                    // Focus/blur cycle
                    input.focus();
                    input.blur();
                    
                    // Eventleri tetikle
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                    input.dispatchEvent(new Event('blur', { bubbles: true }));
                });
                
                // Form validasyonunu zorla tetikle
                const forms = document.querySelectorAll('form');
                forms.forEach(form => {
                    form.dispatchEvent(new Event('input', { bubbles: true }));
                    form.dispatchEvent(new Event('change', { bubbles: true }));
                });
            """)
            
            # Validasyon işleminin tamamlanmasını bekle
            self.sleep(random.uniform(1.0, 2.0))
            
            # Next butonunun durumunu kontrol et
            next_button_status = self.cdp.evaluate("""
                (function() {
                    const buttons = document.querySelectorAll('button');
                    let nextButton = null;
                    
                    for (let button of buttons) {
                        if (button.textContent.includes('Next')) {
                            nextButton = button;
                            break;
                        }
                    }
                    
                    if (nextButton) {
                        return {
                            exists: true,
                            disabled: nextButton.disabled,
                            text: nextButton.textContent.trim(),
                            classes: nextButton.className
                        };
                    }
                    return { exists: false };
                })();
            """)
            
            print(f"Next buton durumu: {next_button_status}")
            
            if next_button_status.get('exists') and not next_button_status.get('disabled'):
                print("Next butonu aktif! Tıklanıyor...")
                self.cdp.click('//button[contains(text(), "Next")]')
                print("Next butonu CDP Mode ile tıklandı!")
            else:
                print("Next butonu hala disabled! Manuel müdahale gerekebilir.")
                print("Form alanlarını kontrol edin:")
                
                # Form alanlarının durumunu kontrol et
                form_debug = self.cdp.evaluate("""
                    (function() {
                        const debug = {};
                        
                        // Name kontrolü
                        const nameInput = document.querySelector('input[name="name"]');
                        debug.name = {
                            value: nameInput ? nameInput.value : 'not found',
                            valid: nameInput ? nameInput.validity.valid : false,
                            required: nameInput ? nameInput.required : false
                        };
                        
                        // Email kontrolü
                        const emailInput = document.querySelector('input[name="email"]');
                        debug.email = {
                            value: emailInput ? emailInput.value : 'not found',
                            valid: emailInput ? emailInput.validity.valid : false,
                            required: emailInput ? emailInput.required : false
                        };
                        
                        // Select kontrolleri
                        const monthSelect = document.querySelector('select[id="SELECTOR_1"]');
                        const daySelect = document.querySelector('select[id="SELECTOR_2"]');
                        const yearSelect = document.querySelector('select[id="SELECTOR_3"]');
                        
                        debug.month = {
                            value: monthSelect ? monthSelect.value : 'not found',
                            valid: monthSelect ? monthSelect.validity.valid : false
                        };
                        debug.day = {
                            value: daySelect ? daySelect.value : 'not found',
                            valid: daySelect ? daySelect.validity.valid : false
                        };
                        debug.year = {
                            value: yearSelect ? yearSelect.value : 'not found',
                            valid: yearSelect ? yearSelect.validity.valid : false
                        };
                        
                        return debug;
                    })();
                """)
                
                print(f"Form debug bilgisi: {form_debug}")
                
                # Manuel müdahale için bekle
                try:
                    input("Next butonu aktif olmadı. Manuel kontrol için Enter'a basın...")
                except EOFError:
                    print("Test ortamında manuel müdahale atlandı...")

            # Captcha kontrolü kaldırıldı - normal akış devam ediyor
            self.sleep(random.uniform(2.0, 4.0))
            print("Captcha kontrolü kaldırıldı, normal akış devam ediyor...")

            # E-posta doğrulama sayfasını bekle
            self.sleep(random.uniform(3.0, 5.0))
            print("Doğrulama kodu gönderildi!")
            
            # Doğrulama kodunu al
            self.sleep(random.uniform(2.0, 4.0))
            print("E-posta doğrulama kodu bekleniyor...")
            verification_code = get_verification_code(email_address, password)
            
            if verification_code:
                print(f"Doğrulama kodu alındı: {verification_code}")
                
                # CDP Mode ile doğrulama kodu girişi - KRITIK NOKTA
                print("CDP Mode ile doğrulama kodu giriliyor...")
                self.sleep(random.uniform(2.0, 3.0))
                
                # CDP Mode ile yavaşça ve dikkatli yaz (robot tespitini bypass et)
                self.cdp_human_type('input[name="verfication_code"]', verification_code, "slow")
                
                print("Doğrulama kodu CDP Mode ile başarıyla girildi!")
                
            # CDP Mode ile Next butonuna tıkla - GUI click ile daha güvenli
            self.sleep(random.uniform(2.0, 4.0))
            print("CDP Mode ile Next butonuna tıklanıyor...")
            
            next_button = '//span[contains(text(), "Next")]'
            # GUI click shadow DOM ve karmaşık elementler için daha güvenli
            try:
                self.cdp.gui_click_element(next_button)
                print("Next butonu GUI click ile tıklandı!")
            except:
                # Fallback olarak normal click
                self.cdp.click(next_button)
                print("Next butonu normal click ile tıklandı!")
                
                # Hesap oluşturma tamamlanmasını bekle
                self.sleep(random.uniform(5.0, 8.0))
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