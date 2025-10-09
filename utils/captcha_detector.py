"""
Captcha Detector Modülü
CDP Mode ile Arkose Labs captcha tespit sistemi
"""

import time
import random

class CaptchaDetector:
    """CDP Mode ile captcha tespitini yöneten sınıf"""
    
    def __init__(self, cdp_instance):
        """CDP instance'ını al"""
        self.cdp = cdp_instance
        self.captcha_detected = False
        self.listener_active = False
        self.arkose_pattern = "client-api.arkoselabs.com/fc/init-load/"
    
    def setup_network_listener(self):
        """Network listener'ı kurarak Arkose Labs isteklerini izle"""
        print("🔍 Captcha network listener kuruluyor...")
        
        try:
            # JavaScript interceptor ile fetch ve XMLHttpRequest'i yakala
            self.cdp.evaluate("""
                (function() {
                    // Global flag'leri tanımla
                    window.captchaDetector = {
                        arkoseRequestDetected: false,
                        arkoseRequestCompleted: false,
                        requestUrl: null,
                        requestType: null,
                        iframeDetected: false
                    };
                    
                    // Original fetch'i sakla
                    const originalFetch = window.fetch;
                    
                    // Fetch interceptor
                    window.fetch = function(url, options) {
                        const urlString = url.toString();
                        
                        // Arkose Labs URL pattern kontrolü - tüm domain
                        if (urlString.includes('arkoselabs.com')) {
                            const timestamp = new Date().toISOString();
                            const urlType = urlString.includes('iframe') ? 'iframe' : 
                                          urlString.includes('client-api') ? 'api' : 'other';
                            console.log(`🔍 Arkose Labs captcha isteği tespit edildi [${urlType}]:`, urlString);
                            console.log(`⏰ Zaman: ${timestamp}`);
                            window.captchaDetector.arkoseRequestDetected = true;
                            window.captchaDetector.requestUrl = urlString;
                            window.captchaDetector.requestType = urlType;
                            
                            // Promise'i wrap et ve tamamlanma durumunu takip et
                            return originalFetch.apply(this, arguments)
                                .then(response => {
                                    console.log('✅ Arkose Labs captcha isteği tamamlandı:', response.status);
                                    window.captchaDetector.arkoseRequestCompleted = true;
                                    return response;
                                })
                                .catch(error => {
                                    console.log('❌ Arkose Labs captcha isteği hatası:', error);
                                    window.captchaDetector.arkoseRequestCompleted = true;
                                    throw error;
                                });
                        }
                        
                        return originalFetch.apply(this, arguments);
                    };
                    
                    // Original XMLHttpRequest'i sakla
                    const originalXHROpen = XMLHttpRequest.prototype.open;
                    const originalXHRSend = XMLHttpRequest.prototype.send;
                    
                    // XMLHttpRequest interceptor
                    XMLHttpRequest.prototype.open = function(method, url, async, user, password) {
                        this._url = url;
                        return originalXHROpen.apply(this, arguments);
                    };
                    
                    XMLHttpRequest.prototype.send = function(data) {
                        if (this._url && this._url.includes('arkoselabs.com')) {
                            const timestamp = new Date().toISOString();
                            const urlType = this._url.includes('iframe') ? 'iframe' : 
                                          this._url.includes('client-api') ? 'api' : 'other';
                            console.log(`🔍 Arkose Labs captcha XHR isteği tespit edildi [${urlType}]:`, this._url);
                            console.log(`⏰ Zaman: ${timestamp}`);
                            window.captchaDetector.arkoseRequestDetected = true;
                            window.captchaDetector.requestUrl = this._url;
                            window.captchaDetector.requestType = urlType;
                            
                            // Event listener'ları ekle
                            this.addEventListener('loadend', function() {
                                console.log('✅ Arkose Labs captcha XHR isteği tamamlandı:', this.status);
                                window.captchaDetector.arkoseRequestCompleted = true;
                            });
                            
                            this.addEventListener('error', function() {
                                console.log('❌ Arkose Labs captcha XHR isteği hatası');
                                window.captchaDetector.arkoseRequestCompleted = true;
                            });
                        }
                        
                        return originalXHRSend.apply(this, arguments);
                    };
                    
                    console.log('🎯 Captcha network listener aktif!');
                })();
            """)
            
            self.listener_active = True
            print("✅ Captcha network listener başarıyla kuruldu!")
            
        except Exception as e:
            print(f"❌ Network listener kurulumunda hata: {e}")
            self.listener_active = False
    
    def check_if_captcha_loaded(self):
        """Captcha yüklenme durumunu kontrol et - hem network hem iframe"""
        if not self.listener_active:
            print("⚠️ Network listener aktif değil!")
            return False
        
        try:
            # JavaScript'ten captcha durumunu al
            captcha_status = self.cdp.evaluate("""
                (function() {
                    if (window.captchaDetector) {
                        return {
                            detected: window.captchaDetector.arkoseRequestDetected,
                            completed: window.captchaDetector.arkoseRequestCompleted,
                            url: window.captchaDetector.requestUrl,
                            type: window.captchaDetector.requestType,
                            iframeDetected: window.captchaDetector.iframeDetected
                        };
                    }
                    return { detected: false, completed: false, url: null, type: null, iframeDetected: false };
                })();
            """)
            
            # Network isteği kontrolü
            network_detected = captcha_status.get('detected', False)
            network_completed = captcha_status.get('completed', False)
            request_url = captcha_status.get('url', 'Bilinmiyor')
            request_type = captcha_status.get('type', 'unknown')
            
            # Iframe varlığı kontrolü
            iframe_detected = self.check_iframe_presence()
            
            # Herhangi bir yöntemle captcha tespit edildi mi? (kullanıcı tercihi: ikisinden biri yeterli)
            if network_detected or iframe_detected:
                print(f"🔍 Arkose Labs captcha tespit edildi!")
                
                if network_detected:
                    print(f"📡 Network İstek: {request_type} - {request_url}")
                    if network_completed:
                        print("✅ Network isteği tamamlandı!")
                    else:
                        print("⏳ Network isteği devam ediyor...")
                
                if iframe_detected:
                    print("🖼️ Iframe element DOM'da tespit edildi!")
                
                # Captcha tamamen yüklendi mi? (kullanıcı tercihi: tam yüklendikten sonra manuel çözüm)
                # Network tamamlandıysa VEYA iframe görünürse captcha yüklendi sayılır
                captcha_fully_loaded = network_completed or iframe_detected
                
                if captcha_fully_loaded:
                    print("✅ Captcha yükleme işlemi tamamlandı!")
                    self.captcha_detected = True
                    return True
                else:
                    print("⏳ Captcha yükleme işlemi devam ediyor...")
                    return False
            else:
                print("ℹ️ Henüz captcha tespit edilmedi.")
                return False
                
        except Exception as e:
            print(f"❌ Captcha durumu kontrol edilirken hata: {e}")
            return False
    
    def wait_for_captcha_completion(self, timeout=30):
        """Captcha yüklenmesini bekle"""
        print(f"⏳ Captcha yüklenmesi bekleniyor (timeout: {timeout}s)...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.check_if_captcha_loaded():
                return True
            
            # Kısa bekleme
            time.sleep(0.5)
        
        print(f"⏰ Captcha yükleme timeout ({timeout}s) aşıldı!")
        return False
    
    def wait_for_manual_solve(self):
        """Manuel captcha çözümü için kullanıcıyı bekle"""
        print("\n" + "="*60)
        print("🚨 CAPTCHA TESPİT EDİLDİ!")
        print("="*60)
        print("📋 Captcha çözümü için:")
        print("1. Tarayıcıda captcha'yı manuel olarak çözün")
        print("2. Çözüm tamamlandıktan sonra Enter'a basın")
        print("3. Bot otomatik olarak devam edecek")
        print("="*60)
        
        try:
            input("Captcha çözümü tamamlandıktan sonra Enter'a basın...")
            print("✅ Manuel captcha çözümü tamamlandı!")
            return True
        except EOFError:
            print("⚠️ Test ortamında manuel captcha çözümü atlandı...")
            return True
    
    def get_captcha_status(self):
        """Captcha durumu hakkında detaylı bilgi al"""
        try:
            status = self.cdp.evaluate("""
                (function() {
                    if (window.captchaDetector) {
                        return {
                            listenerActive: true,
                            detected: window.captchaDetector.arkoseRequestDetected,
                            completed: window.captchaDetector.arkoseRequestCompleted,
                            url: window.captchaDetector.requestUrl,
                            type: window.captchaDetector.requestType,
                            iframeDetected: window.captchaDetector.iframeDetected
                        };
                    }
                    return { 
                        listenerActive: false, 
                        detected: false, 
                        completed: false, 
                        url: null,
                        type: null,
                        iframeDetected: false
                    };
                })();
            """)
            
            return status
            
        except Exception as e:
            print(f"❌ Captcha durumu alınırken hata: {e}")
            return {
                'listenerActive': False,
                'detected': False,
                'completed': False,
                'url': None,
                'type': None,
                'iframeDetected': False
            }
    
    def reset_detector(self):
        """Detector'ı sıfırla"""
        print("🔄 Captcha detector sıfırlanıyor...")
        self.captcha_detected = False
        
        try:
            self.cdp.evaluate("""
                (function() {
                    if (window.captchaDetector) {
                        window.captchaDetector.arkoseRequestDetected = false;
                        window.captchaDetector.arkoseRequestCompleted = false;
                        window.captchaDetector.requestUrl = null;
                        window.captchaDetector.requestType = null;
                        window.captchaDetector.iframeDetected = false;
                    }
                })();
            """)
            print("✅ Captcha detector sıfırlandı!")
        except Exception as e:
            print(f"❌ Detector sıfırlanırken hata: {e}")
    
    def check_iframe_presence(self):
        """DOM'da ArkoLabs iframe'ini kontrol et"""
        try:
            iframe_status = self.cdp.evaluate("""
                (function() {
                    // ArkoLabs iframe'lerini ara
                    const iframes = document.querySelectorAll('iframe[src*="arkoselabs.com"]');
                    const iframeCount = iframes.length;
                    
                    if (iframeCount > 0) {
                        console.log(`🔍 ArkoLabs iframe tespit edildi: ${iframeCount} adet`);
                        for (let i = 0; i < iframes.length; i++) {
                            const iframe = iframes[i];
                            console.log(`📋 Iframe ${i + 1}:`, {
                                src: iframe.src,
                                visible: iframe.offsetWidth > 0 && iframe.offsetHeight > 0,
                                loaded: iframe.contentDocument !== null
                            });
                        }
                        return {
                            detected: true,
                            count: iframeCount,
                            iframes: Array.from(iframes).map(iframe => ({
                                src: iframe.src,
                                visible: iframe.offsetWidth > 0 && iframe.offsetHeight > 0,
                                loaded: iframe.contentDocument !== null
                            }))
                        };
                    }
                    
                    return { detected: false, count: 0, iframes: [] };
                })();
            """)
            
            if iframe_status.get('detected'):
                print(f"🔍 ArkoLabs iframe tespit edildi: {iframe_status.get('count')} adet")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"❌ Iframe kontrolü sırasında hata: {e}")
            return False
    
    def cleanup(self):
        """Temizlik işlemleri"""
        print("🧹 Captcha detector temizleniyor...")
        self.listener_active = False
        self.captcha_detected = False