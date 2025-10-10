"""
Twitter API İstek Override Modülü
Twitter'ın /1.1/onboarding/task.json endpoint'ine giden istekleri yakalar ve js_instrumentation değerlerini değiştirir
"""

import json
import random
import string

class RequestInterceptor:
    """Twitter API isteklerini yakalayıp payload'ı değiştiren sınıf"""
    
    def __init__(self, driver):
        """Driver instance'ını al"""
        self.driver = driver
    
    def generate_fake_js_instrumentation(self):
        """Sahte js_instrumentation response'u üret"""
        # Gerçekçi görünen ama zararsız değerler
        fake_rf = {}
        for i in range(10):  # 10 adet fake rf değeri
            key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=64))
            fake_rf[key] = random.randint(0, 100)
        
        # Sahte s değeri (base64 benzeri)
        fake_s = ''.join(random.choices(string.ascii_letters + string.digits + '_-', k=200))
        
        return {
            "rf": fake_rf,
            "s": fake_s
        }
    
    def setup_twitter_request_override(self, custom_js_instrumentation=None, strategy="zero_rf"):
        """
        Twitter API isteklerini yakala ve js_instrumentation değerlerini değiştir
        
        Args:
            custom_js_instrumentation: Özel js_instrumentation değeri (dict)
            strategy: Değiştirme stratejisi
                - "zero_rf": RF değerlerini 0 yap
                - "fake": Sahte değerler üret
                - "empty": Boş değerler gönder
                - "custom": custom_js_instrumentation kullan
        """
        print("🎯 Twitter API Request Override kuruluyor...")
        
        # Stratejiye göre js_instrumentation değerini belirle
        if strategy == "custom" and custom_js_instrumentation:
            js_inst_data = custom_js_instrumentation
        elif strategy == "fake":
            js_inst_data = self.generate_fake_js_instrumentation()
        elif strategy == "empty":
            js_inst_data = {"rf": {}, "s": ""}
        else:  # default: zero_rf
            js_inst_data = None  # RF değerlerini 0 yapacağız
        
        js_override = f"""
        (function() {{
            console.log('🚀 Twitter API Request Override aktif!');
            
            // Fetch override
            const originalFetch = window.fetch;
            window.fetch = function(input, init) {{
                try {{
                    const url = (typeof input === 'string') ? input : (input && input.url) || '';
                    
                    // Twitter onboarding endpoint'ini yakala
                    if (url.includes('/1.1/onboarding/task.json')) {{
                        console.log('🎯 Twitter onboarding/task.json isteği yakalandı!');
                        
                        init = init || {{}};
                        
                        if (init.body) {{
                            try {{
                                const parsed = JSON.parse(init.body);
                                console.log('📦 Orijinal payload alındı');
                                
                                // js_instrumentation değerlerini değiştir
                                if (parsed.subtask_inputs) {{
                                    parsed.subtask_inputs.forEach((input, index) => {{
                                        if (input.sign_up && input.sign_up.js_instrumentation) {{
                                            console.log(`🔍 js_instrumentation bulundu (index: ${{index}}), manipüle ediliyor...`);
                                            
                                            try {{
                                                const jsInst = JSON.parse(input.sign_up.js_instrumentation.response);
                                                console.log('📊 Orijinal js_instrumentation:', jsInst);
                                                
                                                // RF değerlerini MUTLAKA 0 yap
                                                if (jsInst.rf) {{
                                                    const originalRf = {{ ...jsInst.rf }};
                                                    console.log('🔢 Orijinal RF değerleri:', originalRf);
                                                    
                                                    // Tüm rf değerlerini 0 yap
                                                    Object.keys(jsInst.rf).forEach(key => {{
                                                        jsInst.rf[key] = 0;
                                                    }});
                                                    
                                                    console.log('✅ RF değerleri 0 yapıldı:', jsInst.rf);
                                                }}
                                                
                                                // S değerini de temizle
                                                if (jsInst.s) {{
                                                    jsInst.s = "";
                                                    console.log('🧹 S değeri temizlendi');
                                                }}
                                                
                                                // Güncellenmiş response'u geri yaz
                                                input.sign_up.js_instrumentation.response = JSON.stringify(jsInst);
                                                console.log('✅ js_instrumentation güncellendi!');
                                                
                                            }} catch(e) {{
                                                console.log('⚠️ js_instrumentation parse hatası:', e);
                                            }}
                                        }}
                                    }});
                                }}
                                
                                // Güncellenmiş body'yi geri yaz
                                init.body = JSON.stringify(parsed);
                                console.log('📦 Güncellenmiş payload hazırlandı');
                                
                            }} catch(e) {{
                                console.log('⚠️ Request body parse hatası:', e);
                            }}
                        }}
                    }}
                }} catch(e) {{ 
                    console.error('🚨 fetch-override-error:', e); 
                }}
                
                return originalFetch.call(this, input, init);
            }};

            // XHR override (backup)
            const origOpen = XMLHttpRequest.prototype.open;
            const origSend = XMLHttpRequest.prototype.send;
            
            XMLHttpRequest.prototype.open = function(method, url) {{
                this._url = url;
                this._method = method;
                return origOpen.apply(this, arguments);
            }};
            
            XMLHttpRequest.prototype.send = function(body) {{
                try {{
                    if (this._url && this._url.includes('/1.1/onboarding/task.json')) {{
                        console.log('🎯 XHR ile Twitter onboarding/task.json yakalandı!');
                        
                        if (body) {{
                            try {{
                                const parsed = JSON.parse(body);
                                console.log('📦 XHR Orijinal payload alındı');
                                
                                // js_instrumentation değerlerini değiştir
                                if (parsed.subtask_inputs) {{
                                    parsed.subtask_inputs.forEach((input, index) => {{
                                        if (input.sign_up && input.sign_up.js_instrumentation) {{
                                            console.log(`🔍 XHR js_instrumentation bulundu (index: ${{index}}), manipüle ediliyor...`);
                                            
                                            try {{
                                                const jsInst = JSON.parse(input.sign_up.js_instrumentation.response);
                                                console.log('📊 XHR Orijinal js_instrumentation:', jsInst);
                                                
                                                // RF değerlerini MUTLAKA 0 yap
                                                if (jsInst.rf) {{
                                                    Object.keys(jsInst.rf).forEach(key => {{
                                                        jsInst.rf[key] = 0;
                                                    }});
                                                    console.log('✅ XHR RF değerleri 0 yapıldı:', jsInst.rf);
                                                }}
                                                
                                                // S değerini de temizle
                                                if (jsInst.s) {{
                                                    jsInst.s = "";
                                                    console.log('🧹 XHR S değeri temizlendi');
                                                }}
                                                
                                                // Güncellenmiş response'u geri yaz
                                                input.sign_up.js_instrumentation.response = JSON.stringify(jsInst);
                                                console.log('✅ XHR js_instrumentation güncellendi!');
                                                
                                            }} catch(e) {{
                                                console.log('⚠️ XHR js_instrumentation parse hatası:', e);
                                            }}
                                        }}
                                    }});
                                }}
                                
                                // Güncellenmiş body'yi geri yaz
                                body = JSON.stringify(parsed);
                                console.log('📦 XHR Güncellenmiş payload hazırlandı');
                                
                            }} catch(e) {{
                                console.log('⚠️ XHR Request body parse hatası:', e);
                            }}
                        }}
                    }}
                }} catch(e) {{ 
                    console.error('🚨 xhr-override-error:', e); 
                }}
                
                return origSend.call(this, body);
            }};

            // Anti-detection: toString override
            window.fetch.toString = function() {{
                return 'function fetch() {{ [native code] }}';
            }};
            
            XMLHttpRequest.prototype.open.toString = function() {{
                return 'function open() {{ [native code] }}';
            }};
            
            XMLHttpRequest.prototype.send.toString = function() {{
                return 'function send() {{ [native code] }}';
            }};
            
            console.log('✅ Twitter API Request Override kuruldu!');
        }})();
        """
        
        # CDP ile sayfa yüklenmeden önce inject et
        try:
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": js_override
            })
            print("✅ Twitter API Request Override başarıyla inject edildi!")
            print(f"📋 Strateji: {strategy}")
            
        except Exception as e:
            print(f"❌ Request Override inject hatası: {e}")
            raise
    
    def _get_js_modification_code(self, js_inst_data, strategy):
        """JS modification kodunu stratejiye göre üret"""
        if strategy == "custom" and js_inst_data:
            # Custom değerler kullan
            js_inst_json = json.dumps(js_inst_data)
            return f"""
                                                // Custom js_instrumentation değerleri kullan
                                                const customData = {js_inst_json};
                                                jsInst.rf = customData.rf;
                                                jsInst.s = customData.s;
                                                console.log('🎨 Custom js_instrumentation uygulandı:', customData);
            """
        elif strategy == "fake":
            # Sahte değerler üret
            return """
                                                // Sahte değerler üret
                                                const fakeRf = {};
                                                for (let i = 0; i < 10; i++) {
                                                    const key = Math.random().toString(36).substring(2, 66);
                                                    fakeRf[key] = Math.floor(Math.random() * 100);
                                                }
                                                jsInst.rf = fakeRf;
                                                jsInst.s = Math.random().toString(36).substring(2, 202);
                                                console.log('🎭 Sahte js_instrumentation uygulandı');
            """
        elif strategy == "empty":
            # Boş değerler
            return """
                                                // Boş değerler gönder
                                                jsInst.rf = {};
                                                jsInst.s = "";
                                                console.log('🧹 Boş js_instrumentation uygulandı');
            """
        else:  # default: zero_rf
            # RF değerlerini 0 yap
            return """
                                                // RF değerlerini 0 yap
                                                if (jsInst.rf) {
                                                    Object.keys(jsInst.rf).forEach(key => {
                                                        jsInst.rf[key] = 0;
                                                    });
                                                    console.log('🔢 RF değerleri sıfırlandı');
                                                }
                                                // S değerini de temizle
                                                jsInst.s = "";
                                                console.log('🧹 S değeri temizlendi');
            """
    
    def setup_advanced_interception(self):
        """Gelişmiş interception - tüm Twitter API endpoint'lerini yakala"""
        print("🔬 Gelişmiş Twitter API Interception kuruluyor...")
        
        js_advanced = """
        (function() {
            console.log('🔬 Gelişmiş Twitter API Interception aktif!');
            
            // Tüm Twitter API endpoint'lerini yakala
            const twitterEndpoints = [
                '/1.1/onboarding/task.json',
                '/1.1/account/verify_credentials.json',
                '/1.1/account/settings.json',
                '/1.1/users/lookup.json'
            ];
            
            const originalFetch = window.fetch;
            window.fetch = function(input, init) {
                try {
                    const url = (typeof input === 'string') ? input : (input && input.url) || '';
                    
                    // Twitter endpoint'lerini kontrol et
                    const isTwitterEndpoint = twitterEndpoints.some(endpoint => url.includes(endpoint));
                    
                    if (isTwitterEndpoint) {
                        console.log('🎯 Twitter API endpoint yakalandı:', url);
                        
                        // Request logging
                        if (init && init.body) {
                            try {
                                const body = JSON.parse(init.body);
                                console.log('📦 Request body:', JSON.stringify(body, null, 2));
                            } catch(e) {
                                console.log('📦 Request body (raw):', init.body);
                            }
                        }
                        
                        // Response logging için promise wrapper
                        const response = originalFetch.call(this, input, init);
                        
                        response.then(res => {
                            console.log('📡 Response status:', res.status);
                            if (res.ok) {
                                res.clone().text().then(text => {
                                    try {
                                        const jsonData = JSON.parse(text);
                                        console.log('📦 Response data:', JSON.stringify(jsonData, null, 2));
                                    } catch(e) {
                                        console.log('📦 Response data (raw):', text.substring(0, 500));
                                    }
                                });
                            }
                        }).catch(err => {
                            console.log('❌ Response error:', err);
                        });
                        
                        return response;
                    }
                } catch(e) { 
                    console.error('🚨 advanced-interception-error:', e); 
                }
                
                return originalFetch.call(this, input, init);
            };
            
            console.log('✅ Gelişmiş Twitter API Interception kuruldu!');
        })();
        """
        
        try:
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": js_advanced
            })
            print("✅ Gelişmiş Twitter API Interception başarıyla kuruldu!")
            
        except Exception as e:
            print(f"❌ Gelişmiş Interception kurulum hatası: {e}")
            raise
