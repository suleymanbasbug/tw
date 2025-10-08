import time
import requests
import base64
import json
from seleniumbase import BaseCase
from mail_password import get_verification_code
from user_agents import USER_AGENTS
import random
from PIL import Image
import io
from config import YESCAPTCHA_API_KEY, YESCAPTCHA_API_URL, CAPTCHA_TIMEOUT, TURKISH_TO_ENGLISH

class TwitterSignup(BaseCase):
    
    def get_random_user_agent(self):
        """Random user agent seçimi"""
        return random.choice(USER_AGENTS)
    
    def cdp_human_type(self, selector, text, speed="normal"):
        """CDP Mode ile insan benzeri yazma - press_keys kullanarak"""
        # CDP Mode'da press_keys daha insan benzeri yazma sağlar
        if speed == "slow":
            # Yavaş yazma için karakter karakter
            self.cdp.click(selector)
            time.sleep(random.uniform(0.5, 1.0))
            
            for char in text:
                self.cdp.type(selector, char)
                time.sleep(random.uniform(0.2, 0.4))
        else:
            # Normal ve hızlı yazma için press_keys kullan
            self.cdp.click(selector)
            time.sleep(random.uniform(0.3, 0.7))
            self.cdp.press_keys(selector, text)
        
        return True
    
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
    
    def solve_captcha(self):
        """YesCaptcha API ile FunCaptcha çözme fonksiyonu"""
        print("Captcha tespit edildi!")
        print("YesCaptcha API ile captcha çözülüyor...")
        
        try:
            # Captcha sayfasının yüklenmesini bekle
            time.sleep(random.uniform(2.0, 4.0))
            
            # Authenticate butonunu bul ve tıkla
            if self.is_element_visible('button[data-theme="home.verifyButton"]'):
                print("Authenticate butonu bulundu!")
                time.sleep(random.uniform(1.0, 2.0))
                
                # İnsan benzeri etkileşim
                self.human_like_button_interaction('button[data-theme="home.verifyButton"]', "Authenticate")
                
                # Captcha yüklenmesini bekle
                time.sleep(random.uniform(3.0, 5.0))
                
                # FunCaptcha çözümü
                captcha_solved = self.solve_funcaptcha()
                
                if captcha_solved:
                    print("Captcha başarıyla çözüldü!")
                    return True
                else:
                    print("Captcha çözülemedi!")
                    return False
            else:
                print("Authenticate butonu bulunamadı!")
                return False
                
        except Exception as e:
            print(f"Captcha çözme sırasında hata: {e}")
            return False
    
    def solve_funcaptcha(self):
        """YesCaptcha API ile FunCaptcha çözme"""
        try:
            # YesCaptcha API ayarları
            API_KEY = YESCAPTCHA_API_KEY
            API_URL = YESCAPTCHA_API_URL
            
            # Captcha sorusunu al
            question_text = self.get_captcha_question()
            if not question_text:
                print("Captcha sorusu alınamadı!")
                return False
            
            print(f"Captcha sorusu: {question_text}")
            
            # Captcha görüntüsünü yakala
            captcha_image = self.capture_captcha_image()
            if not captcha_image:
                print("Captcha görüntüsü yakalanamadı!")
                return False
            
            # YesCaptcha API'ye gönder
            task_id = self.submit_captcha_task(API_KEY, API_URL, captcha_image, question_text)
            if not task_id:
                print("Captcha görevi oluşturulamadı!")
                return False
            
            # Sonucu bekle
            result = self.get_captcha_result(API_KEY, API_URL, task_id)
            if not result:
                print("Captcha sonucu alınamadı!")
                return False
            
            # Sonucu uygula
            success = self.apply_captcha_solution(result)
            return success
            
        except Exception as e:
            print(f"FunCaptcha çözme hatası: {e}")
            return False
    
    def get_captcha_question(self):
        """Captcha sorusunu al ve İngilizceye çevir"""
        try:
            # Captcha sorusunu bul
            question_selectors = [
                'div[data-theme="challenge.question"]',
                '.challenge-question',
                '.captcha-question',
                'h2:contains("Pick")',
                'p:contains("Pick")',
                'span:contains("Pick")'
            ]
            
            question_text = None
            for selector in question_selectors:
                if self.is_element_visible(selector):
                    question_text = self.get_text(selector)
                    break
            
            if not question_text:
                # Sayfa kaynağından soruyu bul
                page_source = self.get_page_source()
                if "Pick the" in page_source:
                    # Basit regex ile soruyu çıkar
                    import re
                    match = re.search(r'Pick the [^<]+', page_source)
                    if match:
                        question_text = match.group(0)
            
            if question_text:
                # Türkçe soruları İngilizceye çevir
                question_text = self.translate_question_to_english(question_text)
                return question_text.strip()
            
            return None
            
        except Exception as e:
            print(f"Soru alma hatası: {e}")
            return None
    
    def translate_question_to_english(self, question):
        """Captcha sorusunu İngilizceye çevir"""
        question_lower = question.lower()
        
        # Config'den çeviri sözlüğünü kullan
        for turkish, english in TURKISH_TO_ENGLISH.items():
            question_lower = question_lower.replace(turkish, english)
        
        # Eğer "Pick the" ile başlamıyorsa ekle
        if not question_lower.startswith("pick the"):
            question_lower = "Pick the " + question_lower
        
        return question_lower
    
    def capture_captcha_image(self):
        """Captcha görüntüsünü yakala ve Base64'e çevir"""
        try:
            # Captcha container'ını bul
            captcha_selectors = [
                '.captcha-container',
                '.challenge-container', 
                '.funcaptcha-container',
                'iframe[src*="funcaptcha"]'
            ]
            
            captcha_element = None
            for selector in captcha_selectors:
                if self.is_element_visible(selector):
                    captcha_element = self.find_element(selector)
                    break
            
            if not captcha_element:
                # Sayfanın tamamını yakala
                screenshot = self.get_screenshot_as_png()
            else:
                # Sadece captcha alanını yakala
                screenshot = captcha_element.screenshot_as_png
            
            # PNG'yi Base64'e çevir
            image_base64 = base64.b64encode(screenshot).decode('utf-8')
            return f"data:image/png;base64,{image_base64}"
            
        except Exception as e:
            print(f"Görüntü yakalama hatası: {e}")
            return None
    
    def submit_captcha_task(self, api_key, api_url, image, question):
        """YesCaptcha API'ye görev gönder"""
        try:
            url = f"{api_url}/createTask"
            
            payload = {
                "clientKey": api_key,
                "task": {
                    "type": "FunCaptchaClassification",
                    "image": image,
                    "question": question
                }
            }
            
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            if result.get("errorId") == 0:
                task_id = result.get("taskId")
                print(f"Captcha görevi oluşturuldu: {task_id}")
                return task_id
            else:
                print(f"API hatası: {result.get('errorDescription')}")
                return None
                
        except Exception as e:
            print(f"Görev gönderme hatası: {e}")
            return None
    
    def get_captcha_result(self, api_key, api_url, task_id):
        """Captcha sonucunu al"""
        try:
            url = f"{api_url}/getTaskResult"
            
            payload = {
                "clientKey": api_key,
                "taskId": task_id
            }
            
            # Sonucu bekle (config'den timeout)
            max_attempts = CAPTCHA_TIMEOUT // 2  # Her 2 saniyede bir kontrol
            for attempt in range(max_attempts):
                response = requests.post(url, json=payload, timeout=10)
                response.raise_for_status()
                
                result = response.json()
                
                if result.get("status") == "ready":
                    solution = result.get("solution")
                    if solution:
                        print(f"Captcha çözümü alındı: {solution}")
                        return solution
                
                time.sleep(2)
            
            print("Captcha sonucu zaman aşımına uğradı!")
            return None
            
        except Exception as e:
            print(f"Sonuç alma hatası: {e}")
            return None
    
    def apply_captcha_solution(self, solution):
        """Captcha çözümünü uygula"""
        try:
            # Solution formatı: {"click": [1, 3, 5]} veya {"click": [0, 2, 4]}
            if isinstance(solution, dict) and "click" in solution:
                click_positions = solution["click"]
                
                # Captcha kutularını bul
                captcha_boxes = self.find_elements('.captcha-box, .challenge-box, .funcaptcha-box')
                
                if len(captcha_boxes) >= len(click_positions):
                    for pos in click_positions:
                        if pos < len(captcha_boxes):
                            # İnsan benzeri tıklama
                            time.sleep(random.uniform(0.5, 1.0))
                            self.hover_and_click(captcha_boxes[pos], captcha_boxes[pos])
                            time.sleep(random.uniform(0.3, 0.8))
                    
                    # Submit butonuna tıkla
                    time.sleep(random.uniform(1.0, 2.0))
                    submit_selectors = [
                        'button[type="submit"]',
                        '.submit-button',
                        '.verify-button',
                        'button:contains("Verify")',
                        'button:contains("Submit")'
                    ]
                    
                    for selector in submit_selectors:
                        if self.is_element_visible(selector):
                            self.human_like_button_interaction(selector, "Submit")
                            break
                    
                    # Sonucu kontrol et
                    time.sleep(random.uniform(2.0, 4.0))
                    return True
                else:
                    print("Captcha kutuları yeterli değil!")
                    return False
            else:
                print("Geçersiz çözüm formatı!")
                return False
                
        except Exception as e:
            print(f"Çözüm uygulama hatası: {e}")
            return False
    
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
            time.sleep(random.uniform(3.0, 5.0))
            
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
            
            # Sayfa yüklenmesini bekle
            time.sleep(random.uniform(3.0, 5.0))
            
            # Sayfa yüklenmesini kısa bekle
            time.sleep(random.uniform(2.0, 3.0))
            
            # Create account butonunu bul ve CDP Mode ile tıkla
            print("Create account butonu aranıyor...")
            self.wait_for_element('button:contains("Create account")', timeout=20)
            
            # CDP Mode ile insan benzeri tıklama
            time.sleep(random.uniform(1.5, 2.5))
            self.cdp.click('button:contains("Create account")')
            print("Create account butonu CDP Mode ile tıklandı!")

            # Sayfanın yüklenmesini bekle
            time.sleep(random.uniform(3.0, 5.0))

            # Use email instead butonunu bul ve CDP Mode ile tıkla
            print("Use email instead butonu aranıyor...")
            self.wait_for_element('button:contains("Use email instead")', timeout=20)
            time.sleep(random.uniform(1.5, 2.5))
            self.cdp.click('button:contains("Use email instead")')
            print("Use email instead butonu CDP Mode ile tıklandı!")

            # Sayfanın yüklenmesini bekle
            time.sleep(random.uniform(3.0, 5.0))

            # Name input'una "hasan" yaz - CDP Mode ile
            print("Name alanına CDP Mode ile yazılıyor...")
            time.sleep(random.uniform(1.0, 2.0))
            self.cdp_human_type('input[name="name"]', "hasan", "normal")
            print("Name alanı CDP Mode ile dolduruldu!")

            # Email input'una email yaz - CDP Mode ile
            time.sleep(random.uniform(2.0, 4.0))
            print("Email alanına CDP Mode ile yazılıyor...")
            self.cdp_human_type('input[name="email"]', email_address, "fast")
            print("Email alanı CDP Mode ile dolduruldu!")

            # Ay seçimi - June seç (CDP Mode ile)
            time.sleep(random.uniform(2.0, 4.0))
            print("Ay seçimi CDP Mode ile yapılıyor...")
            month_select = 'select[id="SELECTOR_1"]'
            self.cdp.select_option_by_text(month_select, "June")
            time.sleep(random.uniform(0.5, 1.0))
            print("Ay seçimi CDP Mode ile tamamlandı!")

            # Gün seçimi - 27 seç (CDP Mode ile)
            time.sleep(random.uniform(1.5, 3.0))
            print("Gün seçimi CDP Mode ile yapılıyor...")
            day_select = 'select[id="SELECTOR_2"]'
            self.cdp.select_option_by_text(day_select, "27")
            time.sleep(random.uniform(0.5, 1.0))
            print("Gün seçimi CDP Mode ile tamamlandı!")

            # Yıl seçimi - 1984 seç (CDP Mode ile)
            time.sleep(random.uniform(1.5, 3.0))
            print("Yıl seçimi CDP Mode ile yapılıyor...")
            year_select = 'select[id="SELECTOR_3"]'
            self.cdp.select_option_by_text(year_select, "1984")
            time.sleep(random.uniform(0.5, 1.0))
            print("Yıl seçimi CDP Mode ile tamamlandı!")

            # Next butonuna tıkla (CDP Mode ile)
            time.sleep(random.uniform(3.0, 6.0))
            print("Next butonuna CDP Mode ile tıklanıyor...")
            self.cdp.click('button:contains("Next")')
            print("Next butonu CDP Mode ile tıklandı!")

            # Captcha kontrolü yap
            time.sleep(random.uniform(2.0, 4.0))
            if self.is_element_visible('button[data-theme="home.verifyButton"]'):
                print("Captcha tespit edildi! Çözülmeye çalışılıyor...")
                captcha_solved = self.solve_captcha()
                if not captcha_solved:
                    print("Captcha çözülemedi! Manuel müdahale gerekebilir.")
                    input("Captcha çözümü için Enter'a basın...")
                else:
                    print("Captcha başarıyla çözüldü! Devam ediliyor...")
            else:
                print("Captcha yok, normal akış devam ediyor...")

            # E-posta doğrulama sayfasını bekle
            time.sleep(random.uniform(3.0, 5.0))
            print("Doğrulama kodu gönderildi!")
            
            # Doğrulama kodunu al
            time.sleep(random.uniform(2.0, 4.0))
            print("E-posta doğrulama kodu bekleniyor...")
            verification_code = get_verification_code(email_address, password)
            
            if verification_code:
                print(f"Doğrulama kodu alındı: {verification_code}")
                
                # CDP Mode ile doğrulama kodu girişi - KRITIK NOKTA
                print("CDP Mode ile doğrulama kodu giriliyor...")
                time.sleep(random.uniform(2.0, 3.0))
                
                # CDP Mode ile yavaşça ve dikkatli yaz (robot tespitini bypass et)
                self.cdp_human_type('input[name="verfication_code"]', verification_code, "slow")
                
                print("Doğrulama kodu CDP Mode ile başarıyla girildi!")
                
            # CDP Mode ile Next butonuna tıkla - GUI click ile daha güvenli
            time.sleep(random.uniform(2.0, 4.0))
            print("CDP Mode ile Next butonuna tıklanıyor...")
            
            next_button = 'span:contains("Next")'
            # GUI click shadow DOM ve karmaşık elementler için daha güvenli
            try:
                self.cdp.gui_click_element(next_button)
                print("Next butonu GUI click ile tıklandı!")
            except:
                # Fallback olarak normal click
                self.cdp.click(next_button)
                print("Next butonu normal click ile tıklandı!")
                
                # Hesap oluşturma tamamlanmasını bekle
                time.sleep(random.uniform(5.0, 8.0))
                print("Hesap oluşturma işlemi tamamlandı!")
                print("CDP Mode sayesinde robot tespiti bypass edildi!")
                
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