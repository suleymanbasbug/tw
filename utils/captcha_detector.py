import time
import random
from seleniumbase import BaseCase

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
