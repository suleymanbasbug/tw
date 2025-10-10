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
                // 1. Object.getOwnPropertyDescriptor override
                const originalGetOwnPropertyDescriptor = Object.getOwnPropertyDescriptor;
                Object.getOwnPropertyDescriptor = function(obj, prop) {
                    // Chrome automation kontrollerini bypass et
                    if (prop === 'webdriver' || prop === '$cdc_' || prop === '$chrome_asyncScriptInfo') {
                        return undefined;
                    }
                    return originalGetOwnPropertyDescriptor.apply(this, arguments);
                };
                
                // 2. Function.toString override (anti-override detection)
                const originalToString = Function.prototype.toString;
                Function.prototype.toString = function() {
                    if (this === Object.getOwnPropertyDescriptor) {
                        return 'function getOwnPropertyDescriptor() { [native code] }';
                    }
                    return originalToString.apply(this, arguments);
                };
                
                // 3. Chrome runtime detection bypass
                if (window.chrome && window.chrome.runtime) {
                    // Chrome extension API'yi maskele
                    delete window.chrome.runtime.sendMessage;
                    delete window.chrome.runtime.connect;
                }
                
                // 4. Error stack trace sanitization (bot detection'dan kaçınmak için)
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
                
                // 5. Navigator properties sanitization
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
                
                // 6. Performance timing fingerprint bypass
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
                
                // 7. Console debug detection bypass
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
                                
                                // js_instrumentation kontrolü
                                if (body.subtask_inputs) {
                                    body.subtask_inputs.forEach(input => {
                                        if (input.sign_up && input.sign_up.js_instrumentation) {
                                            console.log('🔍 js_instrumentation bulundu, manipüle ediliyor...');
                                            
                                            // Response'u parse et
                                            try {
                                                const jsInst = JSON.parse(input.sign_up.js_instrumentation.response);
                                                
                                                // RF değerlerini gerçekçi değerlerle değiştir
                                                if (jsInst.rf) {
                                                    // Tüm rf değerlerini 0 yap (en güvenli yöntem)
                                                    Object.keys(jsInst.rf).forEach(key => {
                                                        jsInst.rf[key] = 0;
                                                    });
                                                    
                                                    console.log('✅ RF değerleri temizlendi (hepsi 0)');
                                                }
                                                
                                                // Güncellenmiş response'u geri yaz
                                                input.sign_up.js_instrumentation.response = JSON.stringify(jsInst);
                                            } catch (e) {
                                                console.log('⚠️ js_instrumentation parse hatası:', e);
                                            }
                                        }
                                    });
                                }
                                
                                // Güncellenmiş body'yi options'a geri yaz
                                options.body = JSON.stringify(body);
                                
                            } catch (e) {
                                console.log('⚠️ Request body parse hatası:', e);
                            }
                        }
                    }
                    
                    // Orijinal fetch'i çağır
                    return originalFetch.apply(this, arguments);
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

