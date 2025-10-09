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
    
    def human_like_page_load(self):
        """İnsan benzeri sayfa yükleme davranışı"""
        try:
            # Sayfa yüklenirken makul bekleme
            self.sleep(random.uniform(2.0, 4.0))
            
            # Sayfa yüklenme animasyonlarını taklit et
            self.execute_script("window.scrollTo(0, 0);")
            self.sleep(random.uniform(1.0, 2.0))
            
            # Çok detaylı sayfa keşfi
            scroll_count = random.randint(3, 5)  # Daha az scroll
            for i in range(scroll_count):
                scroll_amount = random.randint(50, 150)  # Daha büyük scroll
                self.execute_script(f"window.scrollBy(0, {scroll_amount});")
                self.sleep(random.uniform(0.8, 1.5))
                
                # Bazen çok küçük geri scroll
                if random.random() < 0.3:
                    # Güvenli geri scroll
                    back_scroll = max(10, scroll_amount // 3)
                    self.execute_script(f"window.scrollBy(0, -{back_scroll});")
                    self.sleep(random.uniform(0.5, 1.0))
            
            # Başa dön
            self.execute_script("window.scrollTo(0, 0);")
            self.sleep(random.uniform(1.0, 2.0))
            
        except Exception as e:
            print(f"human_like_page_load içinde hata: {e}")
            # Basit scroll yap
            self.execute_script("window.scrollTo(0, 100);")
            self.sleep(1)
            self.execute_script("window.scrollTo(0, 0);")
            self.sleep(1)
    
    def human_like_scroll(self):
        """İnsan benzeri scroll davranışı - çok detaylı"""
        scroll_steps = random.randint(6, 10)
        for i in range(scroll_steps):
            scroll_amount = random.randint(50, 200)
            self.execute_script(f"window.scrollBy(0, {scroll_amount});")
            
            # Makul okuma süresi
            self.sleep(random.uniform(1.0, 2.5))
            
            # Sık geri scroll (insan davranışı)
            if random.random() < 0.6:
                # Güvenli aralık kontrolü
                max_back_scroll = max(10, scroll_amount // 3)
                min_back_scroll = min(10, max_back_scroll)
                back_scroll = random.randint(min_back_scroll, max_back_scroll)
                self.execute_script(f"window.scrollBy(0, -{back_scroll});")
                self.sleep(random.uniform(1.0, 2.0))
        
        # Başa dön
        self.execute_script("window.scrollTo(0, 0);")
        self.sleep(random.uniform(1.5, 3.0))
    
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
        self.sleep(random.uniform(1.0, 2.0))
        
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
            self.sleep(base_delay)
            
            # Makul düşünme molası
            if random.random() < 0.25:  # %25 düşünme molası şansı
                self.sleep(random.uniform(1.0, 2.0))
            
            # Yanlış tuş basma simülasyonu (daha sık)
            if random.random() < 0.05:  # %5 yanlış tuş basma şansı
                self.sleep(random.uniform(0.5, 1.0))
                # Geri silme simülasyonu
                self.press_keys(selector, "\b")
                self.sleep(random.uniform(0.3, 0.8))
                # Tekrar yazma
                self.send_keys(selector, char)
                self.sleep(random.uniform(0.5, 1.0))
            
            # Bazen kelime arası makul duraklama
            if char == " " and random.random() < 0.3:
                self.sleep(random.uniform(0.8, 1.5))
    
    def human_like_form_interaction(self, selector, text, field_type="text"):
        """Form alanı ile insan benzeri etkileşim - çok detaylı"""
        # Elemente yaklaşma süresi
        self.sleep(random.uniform(1.0, 3.0))
        
        # Elemente tıklama
        self.hover_and_click(selector, selector)
        self.sleep(random.uniform(1.0, 2.0))
        
        # Odaklanma süresi
        self.sleep(random.uniform(1.0, 2.0))
        
        # Yazma öncesi bekleme
        self.sleep(random.uniform(0.5, 1.5))
        
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
        self.sleep(random.uniform(1.0, 2.0))
        
        # Çok sık geri dönüp kontrol etme
        if random.random() < 0.7:  # %70 kontrol etme şansı
            self.sleep(random.uniform(1.0, 2.0))
            # Küçük mouse hareketi simülasyonu
            self.execute_script("window.scrollBy(0, 5);")
            self.sleep(random.uniform(0.3, 0.8))
            self.execute_script("window.scrollBy(0, -5);")
            self.sleep(random.uniform(0.5, 1.0))
    
    def human_like_button_interaction(self, selector, button_name):
        """Buton ile insan benzeri etkileşim - çok detaylı"""
        # Butonu görme ve değerlendirme süresi
        self.sleep(random.uniform(1.5, 3.0))
        
        # Butona yaklaşma süresi
        self.sleep(random.uniform(1.0, 2.5))
        
        # Hover ve click
        self.hover_and_click(selector, selector, hover_by="css selector", click_by="css selector")
        
        # Tıklama sonrası bekleme
        self.sleep(random.uniform(1.0, 2.0))
        
        print(f"{button_name} butonuna insan benzeri etkileşim yapıldı!")
    
    def human_like_dropdown_interaction(self, selector, option_text, field_name):
        """Dropdown ile insan benzeri etkileşim - çok detaylı"""
        # Dropdown'u görme ve değerlendirme süresi
        self.sleep(random.uniform(1.0, 2.0))
        
        # Dropdown'a yaklaşma
        self.sleep(random.uniform(1.0, 2.0))
        
        # Dropdown'a tıklama
        self.hover_and_click(selector, selector)
        self.sleep(random.uniform(1.0, 2.0))
        
        # Seçenekleri görme süresi
        self.sleep(random.uniform(0.8, 1.5))
        
        # Seçim yapma
        self.select_option_by_text(selector, option_text)
        self.sleep(random.uniform(0.8, 1.5))
        
        print(f"{field_name} olarak '{option_text}' insan benzeri şekilde seçildi!")
    
    def simulate_human_reading(self):
        """İnsan okuma davranışı simülasyonu"""
        # Sayfayı okuma simülasyonu
        for _ in range(random.randint(3, 6)):
            scroll_amount = random.randint(20, 80)
            self.execute_script(f"window.scrollBy(0, {scroll_amount});")
            self.sleep(random.uniform(1.5, 3.0))
            
            # Bazen geri scroll
            if random.random() < 0.4:
                # Güvenli geri scroll
                back_scroll = max(5, scroll_amount // 2)
                self.execute_script(f"window.scrollBy(0, -{back_scroll});")
                self.sleep(random.uniform(1.0, 2.0))
        
        # Başa dön
        self.execute_script("window.scrollTo(0, 0);")
        self.sleep(random.uniform(1.0, 2.0))
    
    def setup_network_monitoring(self):
        """Network isteklerini izlemek için CDP ayarları - NetworkMonitor sınıfını kullanır"""
        network_monitor = NetworkMonitor(self)
        return network_monitor.setup_network_monitoring()

    def on_network_request(self, event):
        """Network isteklerini yakala - NetworkMonitor sınıfını kullanır"""
        network_monitor = NetworkMonitor(self)
        return network_monitor.on_network_request(event)

    def on_network_response(self, event):
        """Network yanıtlarını yakala - NetworkMonitor sınıfını kullanır"""
        network_monitor = NetworkMonitor(self)
        return network_monitor.on_network_response(event)

    def wait_for_arkose_request(self, timeout=30):
        """Arkose Labs isteği gelene kadar bekle - NetworkMonitor sınıfını kullanır"""
        network_monitor = NetworkMonitor(self)
        return network_monitor.wait_for_arkose_request(timeout)


    def wait_for_specific_url(self, url_pattern, timeout=30):
        """Belirli bir URL pattern'i gelene kadar bekle - NetworkMonitor sınıfını kullanır"""
        network_monitor = NetworkMonitor(self)
        return network_monitor.wait_for_specific_url(url_pattern, timeout)

    def monitor_console_logs(self):
        """Console loglarını izle - NetworkMonitor sınıfını kullanır"""
        network_monitor = NetworkMonitor(self)
        return network_monitor.monitor_console_logs()

    def on_console_message(self, event):
        """Console mesajlarını yakala - NetworkMonitor sınıfını kullanır"""
        network_monitor = NetworkMonitor(self)
        return network_monitor.on_console_message(event)
    
    
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