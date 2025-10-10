"""
JS Instrumentation Bypass Modülü
Twitter'ın js_instrumentation fingerprint collection'ını bypass eder
"""

class JSInstrumentationBypass:
    """Twitter'ın fingerprint collection'ını bypass eden sınıf"""
    
    def __init__(self, cdp_instance):
        """CDP instance'ını al"""
        self.cdp = cdp_instance
    
    def setup_early_injection(self):
        """
        Sayfa yüklenmeden ÖNCE fingerprint bypass'ı inject et
        Twitter'ın js_instrumentation response'unu manipüle eder
        """
        print("🔒 JS Instrumentation bypass inject ediliyor (early injection)...")
        
        # Twitter'ın fingerprint collection fonksiyonlarını override et
        self.cdp.evaluate("""
            // Twitter fingerprint collection bypass
            (function() {
                console.log('🚀 JS Instrumentation bypass başlatılıyor...');
                
                // 1. RF hesaplama fonksiyonlarını TAMAMEN engelle
                const originalPerformanceNow = performance.now;
                performance.now = function() {
                    // Timing hesaplamalarını manipüle et
                    return originalPerformanceNow.call(this) + Math.random() * 10;
                };
                
                // 2. Coverage fonksiyonlarını engelle (__cov_*)
                const coverageFunctions = ['__cov_', '__coverage__', '__coverage'];
                coverageFunctions.forEach(funcName => {
                    if (window[funcName]) {
                        window[funcName] = {};
                        Object.freeze(window[funcName]);
                    }
                });
                
                // 3. Object.getOwnPropertyDescriptor override
                const originalGetOwnPropertyDescriptor = Object.getOwnPropertyDescriptor;
                Object.getOwnPropertyDescriptor = function(obj, prop) {
                    // Chrome automation kontrollerini bypass et
                    if (prop === 'webdriver' || prop === '$cdc_' || prop === '$chrome_asyncScriptInfo') {
                        return undefined;
                    }
                    return originalGetOwnPropertyDescriptor.apply(this, arguments);
                };
                
                // 4. Function.toString override (anti-override detection)
                const originalToString = Function.prototype.toString;
                Function.prototype.toString = function() {
                    if (this === Object.getOwnPropertyDescriptor) {
                        return 'function getOwnPropertyDescriptor() { [native code] }';
                    }
                    return originalToString.apply(this, arguments);
                };
                
                // 5. Chrome runtime detection bypass
                if (window.chrome && window.chrome.runtime) {
                    // Chrome extension API'yi maskele
                    delete window.chrome.runtime.sendMessage;
                    delete window.chrome.runtime.connect;
                }
                
                // 6. Error stack trace sanitization (bot detection'dan kaçınmak için)
                const OriginalError = window.Error;
                window.Error = function(...args) {
                    const error = new OriginalError(...args);
                    // Stack trace'den automation işaretlerini temizle
                    if (error.stack) {
                        error.stack = error.stack
                            .replace(/chrome-extension:\\/\\/[a-z]+\\//, '')
                            .replace(/\\$cdc_[a-zA-Z0-9_]+/g, '')
                            .replace(/webdriver/gi, '');
                    }
                    return error;
                };
                window.Error.prototype = OriginalError.prototype;
                
                // 7. Navigator properties sanitization
                const navigatorProps = {
                    webdriver: false,
                    plugins: {
                        length: 3,
                        0: { name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer' },
                        1: { name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai' },
                        2: { name: 'Native Client', filename: 'internal-nacl-plugin' }
                    },
                    languages: ['en-US', 'en'],
                    platform: 'MacIntel',
                    hardwareConcurrency: 8,
                    deviceMemory: 8,
                    maxTouchPoints: 0
                };
                
                for (const [key, value] of Object.entries(navigatorProps)) {
                    try {
                        Object.defineProperty(navigator, key, {
                            get: () => value,
                            configurable: true
                        });
                    } catch (e) {
                        // Bazı propertyler override edilemeyebilir
                    }
                }
                
                // 8. Performance timing fingerprint bypass
                if (window.performance && window.performance.timing) {
                    const originalGetEntries = performance.getEntries;
                    performance.getEntries = function() {
                        const entries = originalGetEntries.apply(this, arguments);
                        // Chrome extension ve webdriver işaretlerini filtrele
                        return entries.filter(entry => {
                            return !entry.name.includes('chrome-extension') && 
                                   !entry.name.includes('webdriver');
                        });
                    };
                }
                
                // 9. Console debug detection bypass
                const originalLog = console.log;
                const originalDebug = console.debug;
                console.log = function(...args) {
                    // Automation loglarını filtrele
                    const filtered = args.filter(arg => {
                        if (typeof arg === 'string') {
                            return !arg.includes('webdriver') && !arg.includes('$cdc_');
                        }
                        return true;
                    });
                    return originalLog.apply(console, filtered);
                };
                console.debug = function() {
                    // Debug mesajlarını tamamen sustur (fingerprinting önlemi)
                    return;
                };
                
                // 10. RF objelerini freeze et (değiştirilemez yap)
                const originalDefineProperty = Object.defineProperty;
                Object.defineProperty = function(obj, prop, descriptor) {
                    // RF objelerini koru
                    if (prop === 'rf' && descriptor && descriptor.value) {
                        console.log('🔒 RF objesi korunuyor, değerler 0 yapılıyor...');
                        if (typeof descriptor.value === 'object') {
                            Object.keys(descriptor.value).forEach(key => {
                                descriptor.value[key] = 0;
                            });
                        }
                    }
                    return originalDefineProperty.apply(this, arguments);
                };
                
                console.log('✅ JS Instrumentation bypass aktif!');
            })();
        """)
        
        print("✅ JS Instrumentation bypass başarıyla inject edildi!")
    
    def setup_rf_values_override(self):
        """
        Twitter'ın topladığı 'rf' (fingerprint) değerlerini override et
        Bu değerler js_instrumentation response'unda gönderiliyor
        """
        print("🔐 RF (fingerprint) değerleri override ediliyor...")
        
        self.cdp.evaluate("""
            // Twitter RF değerleri override
            (function() {
                console.log('🔐 RF değerleri override başlatılıyor...');
                
                // RF değerlerini toplayan fonksiyonları override et
                const originalFetch = window.fetch;
                window.fetch = function(url, options) {
                    // onboarding/task.json isteğini kontrol et
                    if (url.includes('/onboarding/task.json')) {
                        console.log('🎯 onboarding/task.json isteği yakalandı!');
                        
                        // Request body'yi kontrol et
                        if (options && options.body) {
                            try {
                                const body = JSON.parse(options.body);
                                console.log('📦 Orijinal payload alındı');
                                
                                // js_instrumentation kontrolü
                                if (body.subtask_inputs) {
                                    body.subtask_inputs.forEach((input, index) => {
                                        if (input.sign_up && input.sign_up.js_instrumentation) {
                                            console.log(`🔍 js_instrumentation bulundu (index: ${index}), manipüle ediliyor...`);
                                            
                                            // Response'u parse et
                                            try {
                                                const jsInst = JSON.parse(input.sign_up.js_instrumentation.response);
                                                console.log('📊 Orijinal js_instrumentation:', jsInst);
                                                
                                                // RF değerlerini MUTLAKA 0 yap
                                                if (jsInst.rf) {
                                                    const originalRf = { ...jsInst.rf };
                                                    console.log('🔢 Orijinal RF değerleri:', originalRf);
                                                    
                                                    // Tüm rf değerlerini 0 yap
                                                    Object.keys(jsInst.rf).forEach(key => {
                                                        jsInst.rf[key] = 0;
                                                    });
                                                    
                                                    console.log('✅ RF değerleri 0 yapıldı:', jsInst.rf);
                                                }
                                                
                                                // S değerini de temizle
                                                if (jsInst.s) {
                                                    jsInst.s = "";
                                                    console.log('🧹 S değeri temizlendi');
                                                }
                                                
                                                // Güncellenmiş response'u geri yaz
                                                input.sign_up.js_instrumentation.response = JSON.stringify(jsInst);
                                                console.log('📦 Güncellenmiş js_instrumentation response yazıldı');
                                                
                                            } catch (e) {
                                                console.log('⚠️ js_instrumentation parse hatası:', e);
                                            }
                                        }
                                    });
                                }
                                
                                // Güncellenmiş body'yi options'a geri yaz
                                options.body = JSON.stringify(body);
                                console.log('📦 Güncellenmiş payload hazırlandı');
                                
                            } catch (e) {
                                console.log('⚠️ Request body parse hatası:', e);
                            }
                        }
                    }
                    
                    // Orijinal fetch'i çağır
                    return originalFetch.apply(this, arguments);
                };
                
                // XHR override (backup)
                const originalXHROpen = XMLHttpRequest.prototype.open;
                const originalXHRSend = XMLHttpRequest.prototype.send;
                
                XMLHttpRequest.prototype.open = function(method, url) {
                    this._url = url;
                    this._method = method;
                    return originalXHROpen.apply(this, arguments);
                };
                
                XMLHttpRequest.prototype.send = function(body) {
                    if (this._url && this._url.includes('/onboarding/task.json')) {
                        console.log('🎯 XHR ile onboarding/task.json yakalandı!');
                        
                        if (body) {
                            try {
                                const parsed = JSON.parse(body);
                                console.log('📦 XHR Orijinal payload:', parsed);
                                
                                if (parsed.subtask_inputs) {
                                    parsed.subtask_inputs.forEach((input, index) => {
                                        if (input.sign_up && input.sign_up.js_instrumentation) {
                                            console.log(`🔍 XHR js_instrumentation bulundu (index: ${index})`);
                                            
                                            try {
                                                const jsInst = JSON.parse(input.sign_up.js_instrumentation.response);
                                                
                                                if (jsInst.rf) {
                                                    Object.keys(jsInst.rf).forEach(key => {
                                                        jsInst.rf[key] = 0;
                                                    });
                                                    console.log('✅ XHR RF değerleri 0 yapıldı');
                                                }
                                                
                                                input.sign_up.js_instrumentation.response = JSON.stringify(jsInst);
                                                
                                            } catch (e) {
                                                console.log('⚠️ XHR js_instrumentation parse hatası:', e);
                                            }
                                        }
                                    });
                                }
                                
                                body = JSON.stringify(parsed);
                                
                            } catch (e) {
                                console.log('⚠️ XHR Request body parse hatası:', e);
                            }
                        }
                    }
                    
                    return originalXHRSend.call(this, body);
                };
                
                // fetch.toString() override (anti-detection)
                window.fetch.toString = function() {
                    return 'function fetch() { [native code] }';
                };
                
                console.log('✅ RF değerleri override edildi!');
            })();
        """)
        
        print("✅ RF değerleri override başarıyla kuruldu!")
    
    def setup_complete_bypass(self):
        """Tüm bypass mekanizmalarını çalıştır"""
        print("\n🚀 JS Instrumentation Complete Bypass Başlatılıyor...\n")
        
        # 1. Early injection (en önemli - önce çalışmalı)
        self.setup_early_injection()
        
        # 2. RF değerleri override
        self.setup_rf_values_override()
        
        print("\n🎉 JS Instrumentation Complete Bypass Tamamlandı!\n")

