import time
import random

class NetworkMonitor:
    """Network ve Console izleme sınıfı"""
    
    def __init__(self, selenium_instance):
        """Selenium instance'ını al"""
        self.selenium = selenium_instance
    
    def setup_network_monitoring(self):
        """Network isteklerini izlemek için CDP ayarları - Çok daha kapsamlı"""
        try:
            print("🌐 Network izleme sistemi kuruluyor...")
            
            # Network eventlerini dinle - Çok daha kapsamlı yaklaşım
            self.selenium.cdp.evaluate("""
                (function() {
                    // Global captcha tespit flagleri
                    window.captchaRequestDetected = false;
                    window.captchaResponseDetected = false;
                    window.captchaElementsDetected = [];
                    
                    // Network isteklerini yakala - Fetch API
                    const originalFetch = window.fetch;
                    window.fetch = function(...args) {
                        const url = args[0];
                        if (typeof url === 'string') {
                            const urlLower = url.toLowerCase();
                            if (urlLower.includes('arkoselabs.com') || 
                                urlLower.includes('funcaptcha') ||
                                urlLower.includes('arkose') ||
                                urlLower.includes('client-api.arkoselabs.com') ||
                                urlLower.includes('api.arkoselabs.com')) {
                                console.log('🚨 ARKOSE LABS FETCH İSTEĞİ TESPİT EDİLDİ:', url);
                                window.captchaRequestDetected = true;
                                window.captchaElementsDetected.push({
                                    type: 'fetch_request',
                                    url: url,
                                    timestamp: Date.now()
                                });
                            }
                        }
                        return originalFetch.apply(this, args);
                    };
                    
                    // XMLHttpRequest'i de yakala
                    const originalXHR = window.XMLHttpRequest.prototype.open;
                    window.XMLHttpRequest.prototype.open = function(method, url) {
                        if (typeof url === 'string') {
                            const urlLower = url.toLowerCase();
                            if (urlLower.includes('arkoselabs.com') || 
                                urlLower.includes('funcaptcha') ||
                                urlLower.includes('arkose') ||
                                urlLower.includes('client-api.arkoselabs.com') ||
                                urlLower.includes('api.arkoselabs.com')) {
                                console.log('🚨 ARKOSE LABS XHR İSTEĞİ TESPİT EDİLDİ:', url);
                                window.captchaRequestDetected = true;
                                window.captchaElementsDetected.push({
                                    type: 'xhr_request',
                                    url: url,
                                    timestamp: Date.now()
                                });
                            }
                        }
                        return originalXHR.apply(this, arguments);
                    };
                    
                    // Script yükleme olaylarını yakala
                    const originalCreateElement = document.createElement;
                    document.createElement = function(tagName) {
                        const element = originalCreateElement.apply(this, arguments);
                        
                        if (tagName.toLowerCase() === 'script') {
                            const originalSetSrc = Object.getOwnPropertyDescriptor(HTMLScriptElement.prototype, 'src').set;
                            Object.defineProperty(element, 'src', {
                                set: function(value) {
                                    if (value && (
                                        value.includes('arkoselabs.com') ||
                                        value.includes('funcaptcha') ||
                                        value.includes('arkose')
                                    )) {
                                        console.log('🚨 ARKOSE LABS SCRIPT TESPİT EDİLDİ:', value);
                                        window.captchaRequestDetected = true;
                                        window.captchaElementsDetected.push({
                                            type: 'script_load',
                                            url: value,
                                            timestamp: Date.now()
                                        });
                                    }
                                    return originalSetSrc.call(this, value);
                                },
                                get: function() {
                                    return this.getAttribute('src');
                                }
                            });
                        }
                        
                        return element;
                    };
                    
                    // Iframe oluşturma olaylarını yakala
                    const originalCreateElementNS = document.createElementNS;
                    document.createElementNS = function(namespaceURI, qualifiedName) {
                        const element = originalCreateElementNS.apply(this, arguments);
                        
                        if (qualifiedName.toLowerCase() === 'iframe') {
                            const originalSetSrc = Object.getOwnPropertyDescriptor(HTMLIFrameElement.prototype, 'src').set;
                            Object.defineProperty(element, 'src', {
                                set: function(value) {
                                    if (value && (
                                        value.includes('arkoselabs.com') ||
                                        value.includes('funcaptcha') ||
                                        value.includes('arkose')
                                    )) {
                                        console.log('🚨 ARKOSE LABS IFRAME TESPİT EDİLDİ:', value);
                                        window.captchaRequestDetected = true;
                                        window.captchaElementsDetected.push({
                                            type: 'iframe_load',
                                            url: value,
                                            timestamp: Date.now()
                                        });
                                    }
                                    return originalSetSrc.call(this, value);
                                },
                                get: function() {
                                    return this.getAttribute('src');
                                }
                            });
                        }
                        
                        return element;
                    };
                    
                    // MutationObserver ile DOM değişikliklerini izle
                    const observer = new MutationObserver(function(mutations) {
                        mutations.forEach(function(mutation) {
                            mutation.addedNodes.forEach(function(node) {
                                if (node.nodeType === 1) { // Element node
                                    const element = node;
                                    const className = element.className || '';
                                    const id = element.id || '';
                                    const src = element.src || '';
                                    const ariaLabel = element.getAttribute('aria-label') || '';
                                    
                                    // Arkose Labs elementlerini tespit et
                                    if (className.includes('arkose') || 
                                        className.includes('funcaptcha') ||
                                        className.includes('challenge') ||
                                        id.includes('arkose') ||
                                        id.includes('funcaptcha') ||
                                        src.includes('arkoselabs.com') ||
                                        src.includes('funcaptcha') ||
                                        ariaLabel.includes('challenge') ||
                                        ariaLabel.includes('verify')) {
                                        console.log('🚨 ARKOSE LABS DOM ELEMENT TESPİT EDİLDİ:', element);
                                        window.captchaRequestDetected = true;
                                        window.captchaElementsDetected.push({
                                            type: 'dom_element',
                                            element: element.outerHTML.substring(0, 200),
                                            timestamp: Date.now()
                                        });
                                    }
                                }
                            });
                        });
                    });
                    
                    observer.observe(document.body, {
                        childList: true,
                        subtree: true,
                        attributes: true,
                        attributeFilter: ['class', 'id', 'src', 'aria-label']
                    });
                    
                    console.log('✅ Network izleme sistemi aktif!');
                })();
            """)
            
            # Captcha tespit flagleri
            self.selenium.captcha_request_detected = False
            self.selenium.captcha_response_detected = False
            
            print("✅ Network izleme sistemi başarıyla kuruldu!")
            return True
            
        except Exception as e:
            print(f"Network izleme kurulum hatası: {e}")
            return False

    def on_network_request(self, event):
        """Network isteklerini yakala"""
        try:
            request = event.get('params', {}).get('request', {})
            url = request.get('url', '')
            method = request.get('method', '')
            
            # Arkose Labs API isteklerini tespit et
            arkose_patterns = [
                'client-api.arkoselabs.com',
                'arkoselabs.com',
                'funcaptcha',
                'arkose'
            ]
            
            for pattern in arkose_patterns:
                if pattern in url.lower():
                    print(f"🚨 ARKOSE LABS İSTEĞİ TESPİT EDİLDİ: {method} {url}")
                    self.selenium.captcha_request_detected = True
                    break
                    
        except Exception as e:
            print(f"Network request yakalama hatası: {e}")

    def on_network_response(self, event):
        """Network yanıtlarını yakala"""
        try:
            response = event.get('params', {}).get('response', {})
            url = response.get('url', '')
            status = response.get('status', 0)
            
            # Arkose Labs API yanıtlarını tespit et
            arkose_patterns = [
                'client-api.arkoselabs.com',
                'arkoselabs.com',
                'funcaptcha',
                'arkose'
            ]
            
            for pattern in arkose_patterns:
                if pattern in url.lower():
                    print(f"🚨 ARKOSE LABS YANITI TESPİT EDİLDİ: {status} {url}")
                    self.selenium.captcha_response_detected = True
                    break
                    
        except Exception as e:
            print(f"Network response yakalama hatası: {e}")

    def wait_for_specific_url(self, url_pattern, timeout=30):
        """Belirli bir URL pattern'i gelene kadar bekle"""
        print(f"'{url_pattern}' URL'si bekleniyor...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            # Network loglarını kontrol et - SeleniumBase'de farklı metod
            try:
                # JavaScript ile URL kontrolü yap
                url_found = self.selenium.cdp.evaluate(f"""
                    (function() {{
                        // Sayfa URL'sini kontrol et
                        if (window.location.href.includes('{url_pattern}')) {{
                            return true;
                        }}
                        
                        // Network isteklerini kontrol et (eğer yakalanmışsa)
                        if (window.captchaRequestDetected && '{url_pattern}'.includes('arkose')) {{
                            return true;
                        }}
                        
                        return false;
                    }})();
                """)
                
                if url_found:
                    print(f"✅ İstenen URL geldi: {url_pattern}")
                    return True
            except:
                pass
            
            time.sleep(0.5)
        
        print(f"❌ '{url_pattern}' URL'si zaman aşımına uğradı")
        return False

    def monitor_console_logs(self):
        """Console loglarını izle"""
        try:
            # Console loglarını dinle - JavaScript ile console.log'u yakala
            self.selenium.cdp.evaluate("""
                (function() {
                    const originalLog = console.log;
                    console.log = function(...args) {
                        const message = args.join(' ');
                        
                        // Captcha ile ilgili mesajları tespit et
                        const captchaKeywords = ['captcha', 'challenge', 'verify', 'authenticate', 'arkose'];
                        for (const keyword of captchaKeywords) {
                            if (message.toLowerCase().includes(keyword)) {
                                console.log('🚨 CONSOLE CAPTCHA MESAJI:', message);
                                window.captchaConsoleDetected = true;
                                break;
                            }
                        }
                        
                        // Orijinal log'u da çalıştır
                        return originalLog.apply(this, args);
                    };
                })();
            """)
            print("Console log izleme aktif!")
            
        except Exception as e:
            print(f"Console log izleme hatası: {e}")

    def on_console_message(self, event):
        """Console mesajlarını yakala - Artık JavaScript ile yapılıyor"""
        try:
            message = event.get('message', '')
            if message:
                # Captcha ile ilgili mesajları tespit et
                captcha_keywords = ['captcha', 'challenge', 'verify', 'authenticate', 'arkose']
                for keyword in captcha_keywords:
                    if keyword in message.lower():
                        print(f"🚨 CONSOLE CAPTCHA MESAJI: {message}")
                        # JavaScript flag'ini set et
                        self.selenium.cdp.evaluate("window.captchaConsoleDetected = true")
                        break
        except Exception as e:
            print(f"Console mesaj yakalama hatası: {e}")
            return False

    def get_network_status(self):
        """Network durumunu kontrol et"""
        try:
            # JavaScript ile tespit edilen flag'leri kontrol et
            captcha_request = self.selenium.cdp.evaluate("window.captchaRequestDetected || false")
            captcha_response = self.selenium.cdp.evaluate("window.captchaResponseDetected || false")
            captcha_elements = self.selenium.cdp.evaluate("window.captchaElementsDetected || []")
            
            return {
                'request_detected': captcha_request,
                'response_detected': captcha_response,
                'elements_detected': captcha_elements,
                'total_elements': len(captcha_elements) if captcha_elements else 0
            }
        except Exception as e:
            print(f"Network durum kontrolü hatası: {e}")
            return {
                'request_detected': False,
                'response_detected': False,
                'elements_detected': [],
                'total_elements': 0
            }

    def reset_monitoring_flags(self):
        """Monitoring flag'lerini sıfırla"""
        try:
            self.selenium.cdp.evaluate("""
                window.captchaRequestDetected = false;
                window.captchaResponseDetected = false;
                window.captchaElementsDetected = [];
                window.captchaConsoleDetected = false;
            """)
            print("✅ Monitoring flag'leri sıfırlandı!")
        except Exception as e:
            print(f"Flag sıfırlama hatası: {e}")

    def get_detailed_captcha_info(self):
        """Detaylı captcha bilgilerini al"""
        try:
            # JavaScript ile detaylı bilgi al
            detailed_info = self.selenium.cdp.evaluate("""
                (function() {
                    const info = {
                        request_detected: window.captchaRequestDetected || false,
                        response_detected: window.captchaResponseDetected || false,
                        console_detected: window.captchaConsoleDetected || false,
                        elements: window.captchaElementsDetected || [],
                        timestamp: Date.now()
                    };
                    
                    // Arkose Labs script'lerini kontrol et
                    const scripts = document.querySelectorAll('script[src*="arkoselabs"], script[src*="funcaptcha"]');
                    info.scripts_found = scripts.length;
                    
                    // Arkose Labs iframe'lerini kontrol et
                    const iframes = document.querySelectorAll('iframe[src*="arkoselabs"], iframe[src*="funcaptcha"]');
                    info.iframes_found = iframes.length;
                    
                    // Arkose Labs elementlerini kontrol et
                    const elements = document.querySelectorAll('[class*="arkose"], [class*="funcaptcha"], [id*="arkose"], [id*="funcaptcha"]');
                    info.dom_elements_found = elements.length;
                    
                    return info;
                })();
            """)
            
            return detailed_info
        except Exception as e:
            print(f"Detaylı captcha bilgisi alma hatası: {e}")
            return None
