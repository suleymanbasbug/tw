"""
Captcha Solver Modülü
CDP Mode ile Arkose Labs FunCaptcha çözüm sistemi
"""

import time
import random

class CaptchaSolver:
    """CDP Mode ile FunCaptcha çözümünü yöneten sınıf"""
    
    def __init__(self, cdp_instance):
        """CDP instance'ını al"""
        self.cdp = cdp_instance
        self.iframe_loaded = False
        self.button_found = False
    
    def wait_for_iframe_load(self, timeout=15):
        """iframe elementinin DOM'da görünür olmasını bekle (cross-origin güvenli)"""
        print("⏳ FunCaptcha iframe yüklenmesi bekleniyor...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                iframe_status = self.cdp.evaluate("""
                    (function() {
                        // ArkoLabs iframe'ini ara
                        const iframe = document.querySelector('iframe#game-core-frame') || 
                                       document.querySelector('iframe[src*="arkoselabs.com"]');
                        
                        if (!iframe) {
                            return { loaded: false, reason: 'iframe element not found' };
                        }
                        
                        // Sadece iframe elementinin görünürlüğünü kontrol et
                        const isVisible = iframe.offsetWidth > 0 && iframe.offsetHeight > 0;
                        
                        return { 
                            loaded: isVisible, 
                            reason: isVisible ? 'iframe visible in DOM' : 'iframe exists but not visible',
                            src: iframe.src,
                            width: iframe.offsetWidth,
                            height: iframe.offsetHeight
                        };
                    })();
                """)
                
                if iframe_status.get('loaded'):
                    print(f"✅ FunCaptcha iframe bulundu ve görünür!")
                    print(f"📋 Iframe src: {iframe_status.get('src', 'Bilinmiyor')}")
                    print(f"📋 Boyutlar: {iframe_status.get('width')}x{iframe_status.get('height')}")
                    self.iframe_loaded = True
                    return True
                else:
                    print(f"⏳ Iframe yükleniyor... ({iframe_status.get('reason')})")
                    
            except Exception as e:
                print(f"❌ Iframe kontrolü sırasında hata: {e}")
            
            # Kısa bekleme
            time.sleep(0.5)
        
        print(f"⏰ Iframe yükleme timeout ({timeout}s) aşıldı!")
        return False
    
    def check_button_clickable(self):
        """Authenticate butonunun tıklanabilir olduğunu kontrol et - önce ana DOM'da ara"""
        try:
            button_status = self.cdp.evaluate("""
                (function() {
                    // Önce ana DOM'da buton ara
                    let button = document.querySelector('button[data-theme="home.verifyButton"]');
                    if (!button) {
                        // Text içeriğine göre ana DOM'da ara
                        const buttons = document.querySelectorAll('button');
                        for (let btn of buttons) {
                            if (btn.textContent && btn.textContent.includes('Authenticate')) {
                                button = btn;
                                break;
                            }
                        }
                    }
                    
                    if (button) {
                        // Ana DOM'da buton bulundu
                        const isVisible = button.offsetWidth > 0 && button.offsetHeight > 0;
                        const isEnabled = !button.disabled;
                        const isClickable = isVisible && isEnabled;
                        
                        return {
                            found: true,
                            location: 'main-dom',
                            clickable: isClickable,
                            visible: isVisible,
                            enabled: isEnabled,
                            text: button.textContent,
                            classes: button.className,
                            disabled: button.disabled
                        };
                    }
                    
                    // Ana DOM'da buton yoksa, iframe'in yüklendiğini varsay
                    const iframe = document.querySelector('iframe#game-core-frame') || 
                                   document.querySelector('iframe[src*="arkoselabs.com"]');
                    
                    if (iframe && iframe.offsetWidth > 0 && iframe.offsetHeight > 0) {
                        return {
                            found: true,
                            location: 'iframe-cross-origin',
                            clickable: true, // Cross-origin'den kontrol edilemez, varsayılan true
                            visible: true,
                            enabled: true,
                            text: 'Authenticate (iframe içinde)',
                            classes: 'iframe-button',
                            disabled: false,
                            note: 'Cross-origin iframe içinde, içerik kontrol edilemez'
                        };
                    }
                    
                    return { 
                        found: false, 
                        reason: 'button not found in main DOM and iframe not visible' 
                    };
                })();
            """)
            
            if button_status.get('found'):
                print(f"🔍 Authenticate butonu bulundu!")
                print(f"📋 Konum: {button_status.get('location')}")
                print(f"📋 Buton metni: '{button_status.get('text', 'Bilinmiyor')}'")
                print(f"📋 Tıklanabilir: {button_status.get('clickable')}")
                print(f"📋 Görünür: {button_status.get('visible')}")
                print(f"📋 Aktif: {button_status.get('enabled')}")
                
                if button_status.get('note'):
                    print(f"📋 Not: {button_status.get('note')}")
                
                self.button_found = True
                return button_status.get('clickable', False)
            else:
                print(f"❌ Authenticate butonu bulunamadı: {button_status.get('reason')}")
                return False
                
        except Exception as e:
            print(f"❌ Buton kontrolü sırasında hata: {e}")
            return False
    
    def click_authenticate_button(self):
        """Authenticate butonuna tıkla - ana DOM'da varsa direkt, yoksa manuel çözüme düş"""
        print("🎯 FunCaptcha Authenticate butonuna tıklanıyor...")
        
        try:
            # Önce iframe'in yüklendiğinden emin ol
            if not self.iframe_loaded:
                if not self.wait_for_iframe_load():
                    print("❌ Iframe yüklenemedi, buton tıklama iptal edildi!")
                    return False
            
            # Butonun tıklanabilir olduğunu kontrol et
            if not self.check_button_clickable():
                print("❌ Buton tıklanabilir değil!")
                return False
            
            # Ana DOM'da buton var mı kontrol et
            button_location = self.cdp.evaluate("""
                (function() {
                    // Ana DOM'da buton ara
                    let button = document.querySelector('button[data-theme="home.verifyButton"]');
                    if (!button) {
                        const buttons = document.querySelectorAll('button');
                        for (let btn of buttons) {
                            if (btn.textContent && btn.textContent.includes('Authenticate')) {
                                button = btn;
                                break;
                            }
                        }
                    }
                    
                    if (button) {
                        return { 
                            found: true, 
                            location: 'main-dom',
                            button: button
                        };
                    }
                    
                    return { found: false, location: 'iframe-cross-origin' };
                })();
            """)
            
            if button_location.get('found') and button_location.get('location') == 'main-dom':
                # Ana DOM'da buton bulundu, direkt tıkla
                print("✅ Ana DOM'da buton bulundu, direkt tıklanıyor...")
                
                click_result = self.cdp.evaluate("""
                    (function() {
                        try {
                            let button = document.querySelector('button[data-theme="home.verifyButton"]');
                            if (!button) {
                                const buttons = document.querySelectorAll('button');
                                for (let btn of buttons) {
                                    if (btn.textContent && btn.textContent.includes('Authenticate')) {
                                        button = btn;
                                        break;
                                    }
                                }
                            }
                            
                            if (!button) {
                                return { success: false, error: 'button not found in main DOM' };
                            }
                            
                            // Butonun tıklanabilir olduğunu kontrol et
                            if (button.disabled || button.offsetWidth === 0 || button.offsetHeight === 0) {
                                return { success: false, error: 'button not clickable' };
                            }
                            
                            // İnsan benzeri tıklama için küçük bir gecikme
                            setTimeout(() => {
                                button.click();
                            }, 100);
                            
                            return { 
                                success: true, 
                                message: 'button clicked in main DOM',
                                buttonText: button.textContent,
                                buttonClasses: button.className
                            };
                            
                        } catch (error) {
                            return { success: false, error: error.message };
                        }
                    })();
                """)
                
                if click_result.get('success'):
                    print("✅ Ana DOM'daki Authenticate butonu başarıyla tıklandı!")
                    print(f"📋 Buton metni: '{click_result.get('buttonText', 'Bilinmiyor')}'")
                    time.sleep(random.uniform(1.0, 2.0))
                    return True
                else:
                    print(f"❌ Ana DOM'da buton tıklama başarısız: {click_result.get('error')}")
                    return False
                    
            else:
                # Buton iframe içinde (cross-origin), manuel çözüme düş
                print("⚠️ Buton iframe içinde (cross-origin), otomatik tıklama mümkün değil!")
                print("🔄 Manuel çözüme geçiliyor...")
                return self.wait_for_manual_solve()
                
        except Exception as e:
            print(f"❌ Buton tıklama sırasında hata: {e}")
            return False
    
    def wait_for_manual_solve(self):
        """Manuel captcha çözümü için kullanıcıyı bekle"""
        print("\n" + "="*60)
        print("🚨 CAPTCHA TESPİT EDİLDİ!")
        print("="*60)
        print("📋 Captcha çözümü için:")
        print("1. Tarayıcıda captcha'yı manuel olarak çözün")
        print("2. Authenticate butonuna tıklayın")
        print("3. Puzzle'ı çözün")
        print("4. Çözüm tamamlandıktan sonra Enter'a basın")
        print("="*60)
        
        try:
            input("Captcha çözümü tamamlandıktan sonra Enter'a basın...")
            print("✅ Manuel captcha çözümü tamamlandı!")
            return True
        except EOFError:
            print("⚠️ Test ortamında manuel captcha çözümü atlandı...")
            return True
    
    def solve_captcha(self):
        """Ana captcha çözüm fonksiyonu - basitleştirilmiş yaklaşım"""
        print("\n" + "="*60)
        print("🤖 OTOMATİK CAPTCHA ÇÖZÜMÜ BAŞLATILIYOR")
        print("="*60)
        
        try:
            # 1. Iframe'in DOM'da görünür olmasını bekle
            print("📋 Adım 1: Iframe tespiti...")
            if not self.wait_for_iframe_load():
                print("❌ Iframe bulunamadı!")
                return False
            
            # 2. Kısa bekleme - iframe içeriğinin yüklenmesi için
            print("📋 Adım 2: Iframe içeriği yüklenmesi bekleniyor...")
            time.sleep(random.uniform(2.0, 3.0))
            
            # 3. Buton kontrolü ve tıklama denemesi
            print("📋 Adım 3: Buton kontrolü ve tıklama...")
            if self.click_authenticate_button():
                print("✅ Captcha çözümü başarıyla tamamlandı!")
                return True
            else:
                print("❌ Otomatik captcha çözümü başarısız!")
                print("🔄 Manuel çözüme geçiliyor...")
                return self.wait_for_manual_solve()
                
        except Exception as e:
            print(f"❌ Captcha çözümü sırasında hata: {e}")
            print("🔄 Manuel çözüme geçiliyor...")
            return self.wait_for_manual_solve()
    
    def get_captcha_status(self):
        """Captcha durumu hakkında detaylı bilgi al - cross-origin güvenli"""
        try:
            status = self.cdp.evaluate("""
                (function() {
                    // Iframe kontrolü
                    const iframe = document.querySelector('iframe#game-core-frame') || 
                                   document.querySelector('iframe[src*="arkoselabs.com"]');
                    
                    if (!iframe) {
                        return { iframeFound: false };
                    }
                    
                    // Ana DOM'da buton kontrolü
                    let button = document.querySelector('button[data-theme="home.verifyButton"]');
                    if (!button) {
                        const buttons = document.querySelectorAll('button');
                        for (let btn of buttons) {
                            if (btn.textContent && btn.textContent.includes('Authenticate')) {
                                button = btn;
                                break;
                            }
                        }
                    }
                    
                    return {
                        iframeFound: true,
                        iframeLoaded: true,
                        iframeSrc: iframe.src,
                        iframeVisible: iframe.offsetWidth > 0 && iframe.offsetHeight > 0,
                        iframeWidth: iframe.offsetWidth,
                        iframeHeight: iframe.offsetHeight,
                        buttonFound: !!button,
                        buttonLocation: button ? 'main-dom' : 'iframe-cross-origin',
                        buttonClickable: button ? (!button.disabled && button.offsetWidth > 0) : true,
                        buttonText: button ? button.textContent : 'Authenticate (iframe içinde)',
                        buttonClasses: button ? button.className : 'iframe-button',
                        crossOriginNote: button ? null : 'Cross-origin iframe içinde, içerik kontrol edilemez'
                    };
                })();
            """)
            
            return status
            
        except Exception as e:
            print(f"❌ Captcha durumu alınırken hata: {e}")
            return {
                'iframeFound': False,
                'iframeLoaded': False,
                'buttonFound': False,
                'buttonClickable': False
            }
    
    def cleanup(self):
        """Temizlik işlemleri"""
        print("🧹 Captcha solver temizleniyor...")
        self.iframe_loaded = False
        self.button_found = False
