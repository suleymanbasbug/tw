"""
Form Handler Modülü
Twitter kayıt formu işlemlerini yöneten sınıf
"""

import random
import math

class FormHandler:
    """Twitter kayıt formu işlemlerini yöneten sınıf"""
    
    def __init__(self, selenium_instance):
        """Selenium instance'ını al"""
        self.selenium = selenium_instance
        # Human behavior modülünü import et
        from utils.human_behavior import HumanBehavior
        self.human = HumanBehavior(selenium_instance)
    
    def gaussian_random(self, mean, std_dev):
        """Gauss dağılımından rastgele sayı üret"""
        # Box-Muller transformasyonu
        u1 = random.random()
        u2 = random.random()
        z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        return mean + z0 * std_dev
    
    def cdp_human_type(self, selector, text, speed="normal"):
        """CDP Mode ile insan benzeri yazma + form validasyonu"""
        # Önce element'e hover yap
        self.human.hover_element(selector)
        
        # Input'a odaklan
        self.selenium.cdp.click(selector)
        
        # Gauss dağılımı ile bekleme
        focus_delay = self.gaussian_random(0.75, 0.25)
        focus_delay = max(0.3, min(1.5, focus_delay))
        self.selenium.sleep(focus_delay)
        
        # Yazma işlemi - human behavior ile
        if speed == "slow":
            # Yavaş yazma için karakter karakter - human typing rhythm kullan
            for char, delay in self.human.typing_rhythm(text, "slow"):
                if char is None:
                    # Pause
                    self.selenium.sleep(delay)
                else:
                    self.selenium.cdp.press_keys(selector, char)
                    self.selenium.sleep(delay)
        else:
            # Normal ve hızlı yazma için human typing rhythm kullan
            for char, delay in self.human.typing_rhythm(text, speed):
                if char is None:
                    # Pause
                    self.selenium.sleep(delay)
                else:
                    self.selenium.cdp.press_keys(selector, char)
                    self.selenium.sleep(delay)
        
        # Form validasyonunu tetikle - Focus/blur cycle + event dispatch
        self.selenium.cdp.evaluate(f"""
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
        
        # Validasyon işleminin tamamlanmasını bekle - Gauss dağılımı
        validation_delay = self.gaussian_random(0.75, 0.25)
        validation_delay = max(0.3, min(1.5, validation_delay))
        self.selenium.sleep(validation_delay)
        
        return True
    
    def fill_name(self, name):
        """Name alanını doldur"""
        print(f"Name alanına CDP Mode ile '{name}' yazılıyor...")
        # Düşünme süresi ekle
        self.human.thinking_pause("form_fill")
        self.cdp_human_type('input[name="name"]', name, "normal")
        print("✅ Name alanı CDP Mode ile dolduruldu!")
    
    def fill_email(self, email):
        """Email alanını doldur"""
        print(f"Email alanına CDP Mode ile '{email}' yazılıyor...")
        # Düşünme süresi ekle
        self.human.thinking_pause("form_fill")
        self.cdp_human_type('input[name="email"]', email, "fast")
        print("✅ Email alanı CDP Mode ile dolduruldu!")
    
    def fill_birthdate(self, month, day, year):
        """Doğum tarihi seç"""
        print(f"Doğum tarihi seçiliyor: {month}/{day}/{year}")
        
        # Düşünme süresi ekle
        self.human.thinking_pause("decision")
        
        # Ay seçimi
        print("Ay seçimi CDP Mode ile yapılıyor...")
        month_select = 'select[id="SELECTOR_1"]'
        # Önce hover yap
        self.human.hover_element(month_select)
        self.selenium.cdp.select_option_by_text(month_select, month)
        
        # Ay seçimi validasyonu tetikle
        self.selenium.cdp.evaluate(f"""
            const monthElement = document.querySelector('{month_select}');
            if (monthElement) {{
                monthElement.dispatchEvent(new Event('change', {{ bubbles: true }}));
                monthElement.dispatchEvent(new Event('input', {{ bubbles: true }}));
                if (monthElement.form) {{
                    monthElement.form.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }}
        """)
        month_validation_delay = self.gaussian_random(0.75, 0.25)
        month_validation_delay = max(0.3, min(1.5, month_validation_delay))
        self.selenium.sleep(month_validation_delay)
        print("✅ Ay seçimi CDP Mode ile tamamlandı!")

        # Gün seçimi
        print("Gün seçimi CDP Mode ile yapılıyor...")
        day_select = 'select[id="SELECTOR_2"]'
        # Önce hover yap
        self.human.hover_element(day_select)
        self.selenium.cdp.select_option_by_text(day_select, day)
        
        # Gün seçimi validasyonu tetikle
        self.selenium.cdp.evaluate(f"""
            const dayElement = document.querySelector('{day_select}');
            if (dayElement) {{
                dayElement.dispatchEvent(new Event('change', {{ bubbles: true }}));
                dayElement.dispatchEvent(new Event('input', {{ bubbles: true }}));
                if (dayElement.form) {{
                    dayElement.form.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }}
        """)
        day_validation_delay = self.gaussian_random(0.75, 0.25)
        day_validation_delay = max(0.3, min(1.5, day_validation_delay))
        self.selenium.sleep(day_validation_delay)
        print("✅ Gün seçimi CDP Mode ile tamamlandı!")

        # Yıl seçimi
        print("Yıl seçimi CDP Mode ile yapılıyor...")
        year_select = 'select[id="SELECTOR_3"]'
        # Önce hover yap
        self.human.hover_element(year_select)
        self.selenium.cdp.select_option_by_text(year_select, year)
        
        # Yıl seçimi validasyonu tetikle
        self.selenium.cdp.evaluate(f"""
            const yearElement = document.querySelector('{year_select}');
            if (yearElement) {{
                yearElement.dispatchEvent(new Event('change', {{ bubbles: true }}));
                yearElement.dispatchEvent(new Event('input', {{ bubbles: true }}));
                if (yearElement.form) {{
                    yearElement.form.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }}
        """)
        year_validation_delay = self.gaussian_random(0.75, 0.25)
        year_validation_delay = max(0.3, min(1.5, year_validation_delay))
        self.selenium.sleep(year_validation_delay)
        print("✅ Yıl seçimi CDP Mode ile tamamlandı!")
    
    def validate_form(self):
        """Form validasyonunu tetikle"""
        print("Form validasyonu kontrol ediliyor...")
        
        # Tüm form alanlarını tekrar tetikle
        self.selenium.cdp.evaluate("""
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
        
        # Validasyon işleminin tamamlanmasını bekle - Gauss dağılımı
        validation_delay = self.gaussian_random(1.5, 0.5)
        validation_delay = max(0.5, min(3.0, validation_delay))
        self.selenium.sleep(validation_delay)
        print("✅ Form validasyonu tetiklendi!")
    
    def check_next_button_status(self):
        """Next buton durumunu kontrol et"""
        print("Next buton durumu kontrol ediliyor...")
        
        # Next butonunun durumunu kontrol et
        next_button_status = self.selenium.cdp.evaluate("""
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
            print("✅ Next butonu aktif!")
            return True
        else:
            print("❌ Next butonu hala disabled!")
            return False
    
    def get_form_debug_info(self):
        """Form alanlarının durumunu kontrol et"""
        print("Form debug bilgisi alınıyor...")
        
        form_debug = self.selenium.cdp.evaluate("""
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
        return form_debug
    
    def click_next_button(self):
        """Next butonuna tıkla"""
        print("CDP Mode ile Next butonuna tıklanıyor...")
        
        next_button = '//span[contains(text(), "Next")]'
        # İnsan benzeri tıklama kullan
        self.human.human_click(next_button)
        print("✅ Next butonu insan benzeri tıklama ile tıklandı!")
        return True
    
    def fill_verification_code(self, verification_code):
        """Doğrulama kodunu gir"""
        print("CDP Mode ile doğrulama kodu giriliyor...")
        # Düşünme süresi ekle - doğrulama kodu için daha uzun
        self.human.thinking_pause("reading")
        
        # CDP Mode ile yavaşça ve dikkatli yaz (robot tespitini bypass et)
        self.cdp_human_type('input[name="verfication_code"]', verification_code, "slow")
        
        print("✅ Doğrulama kodu CDP Mode ile başarıyla girildi!")
        return True
