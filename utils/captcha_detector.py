import time
import random
import re
from seleniumbase import BaseCase
from utils.yescaptcha_solver import solve_funcaptcha


class CaptchaDetector:
    """ArkoseLabs Captcha Tespit Utility"""
    
    def __init__(self, selenium_instance):
        self.selenium = selenium_instance
        self.remote_entry_loaded = False
        self.captcha_detected = False
        
    def setup_network_monitoring(self):
        """CDP ile network izleme kurulumu"""
        print("🔍 Network izleme kuruluyor...")
        
        try:
            # Network monitoring'i aktif et (CDP için gerekli)
            self.selenium.cdp.execute_cdp_cmd("Network.enable", {})
            print("✅ Network.enable komutu çalıştırıldı!")
            
            # Event handler tanımla
            def on_response_received(event):
                url = event.get('response', {}).get('url', '')
                
                # remoteEntry.js isteğini kontrol et (tüm ArkoseLabs domain'leri)
                if 'remoteEntry.js' in url and 'arkoselabs.com' in url:
                    print(f"✅ remoteEntry.js yüklendi: {url}")
                    print(f"⏰ Yükleme zamanı: {time.strftime('%H:%M:%S')}")
                    self.remote_entry_loaded = True
                    
                    # remoteEntry.js yüklendikten sonra captcha DOM'a render edilmesi için bekle
                    print("⏳ Captcha DOM'a render edilmesi bekleniyor (3 saniye)...")
                    self.selenium.sleep(3)
                    
                    # Captcha elementlerini kontrol etmeye başla
                    self.check_captcha_elements()
            
            # Handler'ı ekle
            self.selenium.cdp.add_handler("Network.responseReceived", on_response_received)
            print("✅ Network monitoring aktif!")
            
        except Exception as e:
            print(f"❌ Network monitoring kurulumunda hata: {e}")
            print("🔄 DOM polling moduna geçiliyor...")
    
    def check_captcha_elements(self):
        """Captcha elementlerinin DOM'da olup olmadığını kontrol et (retry mekanizması ile)"""
        print("🔍 Captcha elementleri kontrol ediliyor (retry mekanizması ile)...")
        
        max_retries = 30  # 15 saniye boyunca her 0.5 saniyede kontrol
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                print(f"🔍 Kontrol denemesi {retry_count + 1}/{max_retries}")
                
                # Ana captcha iframe'ini kontrol et (#arkoseFrame)
                if self.selenium.is_element_visible("#arkoseFrame"):
                    print("✅ Ana captcha iframe (#arkoseFrame) bulundu!")
                    
                    # iframe src attribute'unu kontrol et
                    iframe_src = self.selenium.get_attribute("#arkoseFrame", "src")
                    if iframe_src and "arkoselabs.com" in iframe_src:
                        print(f"✅ iframe src doğrulandı: {iframe_src}")
                        
                        # iframe boyutlarını kontrol et
                        try:
                            iframe_size = self.selenium.get_element_size("#arkoseFrame")
                            print(f"✅ iframe boyutu: {iframe_size['width']}x{iframe_size['height']}")
                            
                            # Captcha başarıyla tespit edildi
                            self.captcha_detected = True
                            self.show_captcha_info()
                            return  # Başarılı tespit, döngüden çık
                            
                        except Exception as e:
                            print(f"⚠️ iframe boyut bilgisi alınamadı: {e}")
                            # Boyut bilgisi alınamasa da iframe var, devam et
                            self.captcha_detected = True
                            self.show_captcha_info()
                            return
                    else:
                        print(f"❌ iframe src beklenen formatta değil: {iframe_src}")
                else:
                    print("❌ Ana captcha iframe (#arkoseFrame) bulunamadı")
                    
                    # Alternatif selector'ları dene
                    if self.selenium.is_element_visible("iframe[id='arkoseFrame']"):
                        print("✅ Alternatif iframe selector bulundu (iframe[id='arkoseFrame'])")
                        self.captcha_detected = True
                        self.show_captcha_info()
                        return
                    elif self.selenium.is_element_visible("iframe[src*='arkoselabs.com']"):
                        print("✅ Genel ArkoseLabs iframe bulundu")
                        self.captcha_detected = True
                        self.show_captcha_info()
                        return
                    elif self.selenium.is_element_visible("iframe[title='arkoseFrame']"):
                        print("✅ Title-based iframe bulundu")
                        self.captcha_detected = True
                        self.show_captcha_info()
                        return
                
                # Başarısız deneme, 0.5 saniye bekle
                retry_count += 1
                if retry_count < max_retries:
                    # İlk 3 saniye hızlı kontrol (6 deneme), sonra yavaşlat
                    if retry_count <= 6:
                        print(f"⏳ 0.5 saniye bekleniyor... (hızlı kontrol - deneme {retry_count + 1}/{max_retries})")
                    else:
                        print(f"⏳ 0.5 saniye bekleniyor... (deneme {retry_count + 1}/{max_retries})")
                    self.selenium.sleep(0.5)
                
            except Exception as e:
                print(f"❌ Captcha element kontrolünde hata: {e}")
                retry_count += 1
                if retry_count < max_retries:
                    self.selenium.sleep(0.5)
        
        print("❌ Captcha elementleri 15 saniye boyunca tespit edilemedi!")
    
    def wait_for_iframe_content(self):
        """iframe içeriğinin yüklenmesini bekle (basitleştirilmiş versiyon)"""
        print("⏳ iframe içeriği kontrol ediliyor...")
        
        try:
            # iframe'e geçiş yap
            self.selenium.switch_to_frame("#arkoseFrame")
            print("✅ iframe'e geçiş yapıldı")
            
            # iframe içindeki herhangi bir elementin yüklenmesini bekle
            self.selenium.sleep(2)  # Basit bekleme
            
            # Ana frame'e geri dön
            self.selenium.switch_to_default_content()
            print("✅ Ana frame'e geri dönüldü")
            
            # Captcha başarıyla tespit edildi
            self.captcha_detected = True
            self.show_captcha_info()
                
        except Exception as e:
            print(f"❌ iframe içerik kontrolünde hata: {e}")
            # Ana frame'e geri dön
            try:
                self.selenium.switch_to_default_content()
            except:
                pass
            # Hata olsa da iframe var, captcha tespit edildi say
            self.captcha_detected = True
            self.show_captcha_info()
    
    def show_captcha_info(self):
        """Captcha hakkında detaylı bilgi göster"""
        print("\n" + "="*60)
        print("🎯 CAPTCHA TESPİT EDİLDİ!")
        print("="*60)
        print(f"⏰ Tespit zamanı: {time.strftime('%H:%M:%S')}")
        print(f"🌐 Sayfa URL: {self.selenium.get_current_url()}")
        print(f"📦 remoteEntry.js yüklendi: {'✅' if self.remote_entry_loaded else '❌'}")
        print(f"🎮 Captcha render edildi: {'✅' if self.captcha_detected else '❌'}")
        
        # iframe bilgilerini göster
        try:
            iframe_src = self.selenium.get_attribute("#arkoseFrame", "src")
            print(f"🔗 iframe src: {iframe_src}")
            
            # iframe boyutlarını göster
            iframe_size = self.selenium.get_element_size("#arkoseFrame")
            print(f"📏 iframe boyutu: {iframe_size['width']}x{iframe_size['height']}")
            
        except Exception as e:
            print(f"❌ iframe bilgileri alınamadı: {e}")
        
        print("="*60)
    
    def solve_captcha_with_yescaptcha(self, base64_image, question_text):
        """YesCaptcha API'sini kullanarak captcha'yı çöz"""
        print("\n🤖 YesCaptcha ile captcha çözülüyor...")
        print("="*50)
        
        try:
            # YesCaptcha API'sine istek gönder
            result = solve_funcaptcha(base64_image, question_text)
            
            # Sonucu kontrol et
            if isinstance(result, dict):
                if "error" in result:
                    print(f"❌ YesCaptcha API hatası: {result['error']}")
                    if "message" in result:
                        print(f"📝 Hata mesajı: {result['message']}")
                    return None
                elif "solution" in result:
                    print("✅ Captcha başarıyla çözüldü!")
                    print(f"🎯 Çözüm: {result['solution']}")
                    return result["solution"]
                elif "taskId" in result:
                    print(f"⏳ Task oluşturuldu, ID: {result['taskId']}")
                    print("ℹ️ Bu durumda task'ın tamamlanmasını beklemek gerekir")
                    return result
                else:
                    print("⚠️ Beklenmeyen response formatı")
                    print(f"📋 Response keys: {list(result.keys())}")
                    return result
            else:
                print(f"❌ Beklenmeyen response türü: {type(result)}")
                return None
                
        except Exception as e:
            print(f"❌ YesCaptcha çözme hatası: {e}")
            return None
    
    def apply_captcha_solution(self, solution):
        """Captcha çözümünü uygula (YesCaptcha API yanıtına göre)"""
        print(f"\n🖱️ Captcha çözümü uygulanıyor: {solution}")
        
        try:
            # YesCaptcha API yanıtını kontrol et - iki farklı format destekle
            if isinstance(solution, dict):
                # Format 1: {"solution": {"objects": [...]}} - tüm API yanıtı
                # Format 2: {"objects": [...]} - sadece solution kısmı (mevcut)
                
                objects = None
                if "solution" in solution and isinstance(solution["solution"], dict):
                    # Format 1: Tüm API yanıtı
                    print("✅ YesCaptcha API yanıtı tespit edildi (tüm yanıt formatı)")
                    objects = solution["solution"].get("objects", [])
                elif "objects" in solution:
                    # Format 2: Sadece solution kısmı
                    print("✅ YesCaptcha solution tespit edildi (solution formatı)")
                    objects = solution.get("objects", [])
                
                if objects is None:
                    print("❌ Objects dizisi bulunamadı!")
                    return False
                
                if not objects:
                    print("⚠️ Objects dizisi boş, hiç tıklama yapılmayacak")
                    click_count = 0
                else:
                    click_count = objects[0]  # İlk değeri al
                    print(f"🎯 Tıklama sayısı: {click_count}")
                
                # Right arrow butonunu bul ve tıkla
                if click_count > 0:
                    print(f"🔄 Right arrow butonuna {click_count} kez tıklanıyor...")
                    
                    # Right arrow butonunu bul (birden fazla selector dene)
                    right_arrow_selectors = [
                        'a[aria-label="Navigate to next image"]',
                        'a.right-arrow',
                        'a.sc-7csxyx-2.sc-7csxyx-4.ioYDmH.gOozvt.right-arrow'
                    ]
                    
                    right_arrow_element = None
                    for selector in right_arrow_selectors:
                        try:
                            if self.selenium.is_element_visible(selector):
                                right_arrow_element = selector
                                print(f"✅ Right arrow butonu bulundu: {selector}")
                                break
                        except:
                            continue
                    
                    if right_arrow_element:
                        # Belirtilen sayı kadar tıkla
                        for i in range(click_count):
                            print(f"🖱️ Tıklama {i+1}/{click_count}")
                            self.selenium.click(right_arrow_element)
                            self.selenium.sleep(0.8)  # Her tıklama arasında bekleme
                        print(f"✅ {click_count} kez tıklama tamamlandı!")
                    else:
                        print("❌ Right arrow butonu bulunamadı!")
                        return False
                else:
                    print("ℹ️ Tıklama gerekmiyor (objects: [0])")
                
                # Submit butonunu bul ve tıkla
                print("📤 Submit butonuna tıklanıyor...")
                submit_selectors = [
                    'button.sc-nkuzb1-0.yuVdl.button',
                    'button[class*="button"]',
                    'button:contains("Submit")'
                ]
                
                submit_element = None
                for selector in submit_selectors:
                    try:
                        if self.selenium.is_element_visible(selector):
                            submit_element = selector
                            print(f"✅ Submit butonu bulundu: {selector}")
                            break
                    except:
                        continue
                
                if submit_element:
                    self.selenium.click(submit_element)
                    print("✅ Submit butonu başarıyla tıklandı!")
                    self.selenium.sleep(1)  # Submit sonrası kısa bekleme
                else:
                    print("❌ Submit butonu bulunamadı!")
                    return False
                
                print("✅ Captcha çözümü başarıyla uygulandı!")
                return True
                
            elif isinstance(solution, str):
                # Metin tabanlı çözümler (eski format)
                print("⚠️ String format çözüm tespit edildi (eski format)")
                if "click" in solution.lower() or "tıkla" in solution.lower():
                    print("🖱️ Tıklama çözümü tespit edildi")
                elif "type" in solution.lower() or "yaz" in solution.lower():
                    print("⌨️ Metin girme çözümü tespit edildi")
                else:
                    print(f"ℹ️ Genel çözüm: {solution}")
                return True
                
            elif isinstance(solution, list):
                print(f"📋 Liste çözümü: {solution}")
                return True
                
            else:
                print(f"⚠️ Bilinmeyen çözüm türü: {type(solution)}")
                return False
                
        except Exception as e:
            print(f"❌ Captcha çözümü uygulama hatası: {e}")
            print(f"🔍 Hata detayı: {type(e).__name__}")
            return False
    
    def wait_for_captcha(self, max_wait_time=30):
        """Captcha'nın yüklenmesini bekle (network monitoring + DOM polling)"""
        print("⏳ Captcha yüklenmesi bekleniyor...")
        start_time = time.time()
        
        while not self.captcha_detected and (time.time() - start_time) < max_wait_time:
            self.selenium.sleep(1)
            
            # Her 5 saniyede bir durum raporu ver
            if int(time.time() - start_time) % 5 == 0:
                print(f"⏳ Bekleniyor... ({int(time.time() - start_time)}s)")
                
                # 10 saniye sonra DOM polling'e geç (network monitoring başarısızsa)
                if int(time.time() - start_time) >= 10 and not self.remote_entry_loaded:
                    print("🔄 Network monitoring başarısız, DOM polling'e geçiliyor...")
                    self.check_captcha_elements()
        
        if self.captcha_detected:
            print("🎉 Captcha başarıyla tespit edildi!")
            return True
        else:
            print("❌ Captcha tespit edilemedi (30 saniye timeout)")
            return False
    
    def click_captcha_authenticate_button(self):
        """FunCaptcha iframe içindeki Authenticate butonuna tıklama"""
        print("\n🎯 FunCaptcha Authenticate butonu tıklanıyor...")
        
        try:
            # 1. RECONNECT çağır (iframe geçişinden ÖNCE!)
            print("🔄 CDP Mode'dan standart Selenium'a geçiş yapılıyor...")
            self.selenium.reconnect()
            print("✅ Reconnect başarılı! Standart Selenium metodları aktif.")
            
            # 2. Ana captcha iframe'ine geçiş yap (#arkoseFrame)
            print("📱 Ana captcha iframe'ine (#arkoseFrame) geçiş yapılıyor...")
            self.selenium.wait_for_element("#arkoseFrame", timeout=10)
            self.selenium.switch_to_frame("#arkoseFrame")
            print("✅ #arkoseFrame'e geçiş başarılı!")
            
            # 3. Orta iframe'e geçiş yap (Verification challenge iframe)
            print("📱 Orta iframe'e (Verification challenge) geçiş yapılıyor...")
            self.selenium.wait_for_element('iframe[title="Verification challenge"]', timeout=10)
            self.selenium.switch_to_frame('iframe[title="Verification challenge"]')
            print("✅ Verification challenge iframe'e geçiş başarılı!")
            
            # 4. En iç iframe'e geçiş yap (game-core-frame)
            print("📱 En iç iframe'e (#game-core-frame) geçiş yapılıyor...")
            self.selenium.wait_for_element('#game-core-frame', timeout=10)
            self.selenium.switch_to_frame('#game-core-frame')
            print("✅ #game-core-frame'e geçiş başarılı!")
            
            # 5. Authenticate butonunun yüklenmesini bekle
            print("⏳ Authenticate butonu bekleniyor...")
            self.selenium.wait_for_element('button[data-theme="home.verifyButton"]', timeout=10)
            print("✅ Authenticate butonu bulundu!")
            self.selenium.sleep(2)
            
            # 6. Butona tıkla
            print("🖱️ Authenticate butonuna tıklanıyor...")
            self.selenium.click('button[data-theme="home.verifyButton"]')
            print("✅ Authenticate butonu başarıyla tıklandı!")
            self.selenium.sleep(2)
            
            # 7. Challenge text'ini al ve temizle
            print("📝 Challenge text'i alınıyor...")
            clean_text = "Pick the bread"  # Varsayılan değer
            try:
                # Challenge text elementini bekle ve al
                self.selenium.wait_for_element('span[role="text"]', timeout=10)
                challenge_text = self.selenium.get_text('span[role="text"]')
                print(f"📄 Ham challenge text: {challenge_text}")
                
                # HTML tag'lerini kaldır
                clean_text = re.sub(r'<[^>]+>', '', challenge_text)
                
                # Sondaki parantez içindeki sayıları kaldır (örn: (1 of 1), (2 of 3))
                clean_text = re.sub(r'\s*\(\d+\s+of\s+\d+\)\s*$', '', clean_text)
                
                # Gereksiz boşlukları temizle
                clean_text = clean_text.strip()
                
                print(f"✨ Temizlenmiş challenge text: {clean_text}")
                
            except Exception as text_error:
                print(f"⚠️ Challenge text alınamadı: {text_error}")
                print(f"🔄 Varsayılan challenge text kullanılıyor: {clean_text}")
            
            # 8. Captcha resminin background-image'ini base64'e dönüştür ve YesCaptcha ile çöz
            print("🖼️ Captcha resmi base64'e dönüştürülüyor...")
            try:
                # İlk captcha resmini bul
                img_element = self.selenium.find_element('img[aria-label*="Image 1"]')
                print("✅ Captcha resmi bulundu!")
                
                # Style attribute'unu al
                style_attr = img_element.get_attribute('style')
                print(f"📄 Style attribute: {style_attr}")
                
                # Background-image URL'ini extract et
                url_match = re.search(r'url\("([^"]+)"\)', style_attr)
                if url_match:
                    blob_url = url_match.group(1)
                    print(f"🔗 Blob URL: {blob_url}")
                    
                    # Aşama 1: Resmi geçici img elementine yükle
                    print("📥 Resim geçici elementine yükleniyor...")
                    load_img_js = """
                    var img = new Image();
                    img.id = 'temp-captcha-img';
                    img.crossOrigin = 'anonymous';
                    img.src = arguments[0];
                    document.body.appendChild(img);
                    return 'IMG_LOADED';
                    """
                    
                    self.selenium.execute_script(load_img_js, blob_url)
                    print("✅ Resim DOM'a eklendi, yüklenmesi bekleniyor...")
                    
                    # Resmin yüklenmesi için kısa bekleme
                    self.selenium.sleep(2)
                    
                    # Aşama 2: Canvas'a çiz ve base64'e dönüştür
                    print("🎨 Canvas'a çiziliyor ve base64'e dönüştürülüyor...")
                    canvas_js = """
                    try {
                        var img = document.getElementById('temp-captcha-img');
                        if (!img || !img.complete) {
                            return 'ERROR: Resim henüz yüklenmedi';
                        }
                        
                        var canvas = document.createElement('canvas');
                        canvas.width = img.naturalWidth;
                        canvas.height = img.naturalHeight;
                        var ctx = canvas.getContext('2d');
                        ctx.drawImage(img, 0, 0);
                        
                        var base64 = canvas.toDataURL('image/png');
                        
                        // Geçici img elementini temizle
                        document.body.removeChild(img);
                        
                        return base64;
                    } catch (error) {
                        return 'ERROR: ' + error.message;
                    }
                    """
                    
                    # Base64 string'i al
                    base64_string = self.selenium.execute_script(canvas_js)
                    
                    # Base64 string'inin geçerli olup olmadığını kontrol et
                    if base64_string and not base64_string.startswith('ERROR:'):
                        print(f"✅ Base64 resim başarıyla oluşturuldu!")
                        print(f"📏 Resim boyutu: {len(base64_string)} karakter")
                        
                        # YesCaptcha ile captcha'yı çöz
                        print("\n🤖 YesCaptcha ile captcha çözülüyor...")
                        captcha_solution = self.solve_captcha_with_yescaptcha(base64_string, clean_text)
                        
                        if captcha_solution:
                            print(f"🎯 Captcha çözümü alındı: {captcha_solution}")
                            
                            # Çözümü uygula
                            solution_applied = self.apply_captcha_solution(captcha_solution)
                            
                            if solution_applied:
                                print("✅ Captcha çözümü başarıyla uygulandı!")
                            else:
                                print("❌ Captcha çözümü uygulanamadı!")
                            
                        else:
                            print("❌ Captcha çözülemedi!")
                            
                    else:
                        print(f"❌ Base64 dönüştürme hatası: {base64_string}")
                    
                else:
                    print("❌ Background-image URL'i bulunamadı!")
                    
            except Exception as img_error:
                print(f"⚠️ Captcha resmi işlenirken hata: {img_error}")
            
            # 9. Ana frame'e geri dön
            self.selenium.switch_to_default_content()
            print("✅ Ana frame'e geri dönüldü")
            
            # 10. Kısa bekleme (captcha'nın yanıt vermesi için)
            self.selenium.sleep(2)
            print("🎉 FunCaptcha Authenticate işlemi tamamlandı!")
            
            return True
            
        except Exception as e:
            print(f"❌ FunCaptcha Authenticate butonu tıklama hatası: {e}")
            print(f"🔍 Hata türü: {type(e).__name__}")
            
            # Hata durumunda ana frame'e geri dönmeye çalış
            try:
                self.selenium.switch_to_default_content()
                print("✅ Hata durumunda ana frame'e geri dönüldü")
            except:
                print("⚠️ Ana frame'e geri dönüş başarısız")
            
            return False