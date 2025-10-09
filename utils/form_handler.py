"""
Form Handler Modülü
Twitter kayıt formu işlemlerini yöneten sınıf
"""

import random

class FormHandler:
    """Twitter kayıt formu işlemlerini yöneten sınıf"""
    
    def __init__(self, selenium_instance):
        """Selenium instance'ını al"""
        self.selenium = selenium_instance
    
    def cdp_human_type(self, selector, text, speed="normal"):
        """CDP Mode ile insan benzeri yazma + form validasyonu"""
        # Input'a odaklan
        self.selenium.cdp.click(selector)
        self.selenium.sleep(random.uniform(0.5, 1.0))
        
        # Yazma işlemi
        if speed == "slow":
            # Yavaş yazma için karakter karakter - press_keys ile
            for char in text:
                self.selenium.cdp.press_keys(selector, char)
                self.selenium.sleep(random.uniform(0.2, 0.4))
        else:
            # Normal ve hızlı yazma için press_keys kullan
            self.selenium.cdp.press_keys(selector, text)
        
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
        
        # Validasyon işleminin tamamlanmasını bekle
        self.selenium.sleep(random.uniform(0.5, 1.0))
        
        return True
    
    def fill_name(self, name):
        """Name alanını doldur"""
        print(f"Name alanına CDP Mode ile '{name}' yazılıyor...")
        self.selenium.sleep(random.uniform(1.0, 2.0))
        self.cdp_human_type('input[name="name"]', name, "normal")
        print("✅ Name alanı CDP Mode ile dolduruldu!")
    
    def fill_email(self, email):
        """Email alanını doldur"""
        print(f"Email alanına CDP Mode ile '{email}' yazılıyor...")
        self.selenium.sleep(random.uniform(2.0, 4.0))
        self.cdp_human_type('input[name="email"]', email, "fast")
        print("✅ Email alanı CDP Mode ile dolduruldu!")
    
    def fill_birthdate(self, month, day, year):
        """Doğum tarihi seç"""
        print(f"Doğum tarihi seçiliyor: {month}/{day}/{year}")
        
        # Ay seçimi
        self.selenium.sleep(random.uniform(2.0, 4.0))
        print("Ay seçimi CDP Mode ile yapılıyor...")
        month_select = 'select[id="SELECTOR_1"]'
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
        self.selenium.sleep(random.uniform(0.5, 1.0))
        print("✅ Ay seçimi CDP Mode ile tamamlandı!")

        # Gün seçimi
        self.selenium.sleep(random.uniform(1.5, 3.0))
        print("Gün seçimi CDP Mode ile yapılıyor...")
        day_select = 'select[id="SELECTOR_2"]'
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
        self.selenium.sleep(random.uniform(0.5, 1.0))
        print("✅ Gün seçimi CDP Mode ile tamamlandı!")

        # Yıl seçimi
        self.selenium.sleep(random.uniform(1.5, 3.0))
        print("Yıl seçimi CDP Mode ile yapılıyor...")
        year_select = 'select[id="SELECTOR_3"]'
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
        self.selenium.sleep(random.uniform(0.5, 1.0))
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
        
        # Validasyon işleminin tamamlanmasını bekle
        self.selenium.sleep(random.uniform(1.0, 2.0))
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
        # GUI click shadow DOM ve karmaşık elementler için daha güvenli
        try:
            self.selenium.cdp.gui_click_element(next_button)
            print("✅ Next butonu GUI click ile tıklandı!")
            return True
        except:
            # Fallback olarak normal click
            self.selenium.cdp.click(next_button)
            print("✅ Next butonu normal click ile tıklandı!")
            return True
    
    def fill_verification_code(self, verification_code):
        """Doğrulama kodunu gir"""
        print("CDP Mode ile doğrulama kodu giriliyor...")
        self.selenium.sleep(random.uniform(2.0, 3.0))
        
        # CDP Mode ile yavaşça ve dikkatli yaz (robot tespitini bypass et)
        self.cdp_human_type('input[name="verfication_code"]', verification_code, "slow")
        
        print("✅ Doğrulama kodu CDP Mode ile başarıyla girildi!")
        return True
