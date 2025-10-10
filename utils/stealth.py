"""
Stealth Helper Modülü
CDP Mode ile fingerprinting bypass ve stealth ayarları
"""

import random

class StealthHelper:
    """CDP Mode ile stealth ayarlarını yöneten sınıf"""
    
    def __init__(self, cdp_instance):
        """CDP instance'ını al"""
        self.cdp = cdp_instance
        # Session için tutarlı fingerprint değerleri üret
        self.session_seed = random.random()
        self.session_canvas_noise = random.randint(1, 1000)
        self.session_webgl_noise = random.randint(1, 1000)
        self.session_audio_noise = random.randint(1, 1000)
    
    def setup_canvas_fingerprint_bypass(self):
        """Canvas fingerprinting bypass - Session tutarlı"""
        print("Canvas fingerprinting bypass ayarlanıyor...")
        canvas_noise = self.session_canvas_noise
        self.cdp.evaluate(f"""
            const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
            const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
            
            // Session boyunca tutarlı canvas noise
            const sessionCanvasNoise = {canvas_noise};
            
            HTMLCanvasElement.prototype.toDataURL = function(type) {{
                if (type === 'image/png' && this.width === 280 && this.height === 60) {{
                    return 'data:image/png;base64,iVBORw0KGg==';
                }}
                return originalToDataURL.apply(this, arguments);
            }};
            
            CanvasRenderingContext2D.prototype.getImageData = function(sx, sy, sw, sh) {{
                const imageData = originalGetImageData.apply(this, arguments);
                // Canvas fingerprint'e session-specific noise ekle
                for (let i = 0; i < imageData.data.length; i += 4) {{
                    imageData.data[i] = (imageData.data[i] + sessionCanvasNoise) % 256;
                }}
                return imageData;
            }};
        """)
        print("✅ Canvas fingerprinting bypass aktif! (Session tutarlı)")
    
    def setup_webgl_fingerprint_bypass(self):
        """WebGL fingerprinting bypass - Session tutarlı"""
        print("WebGL fingerprinting bypass ayarlanıyor...")
        webgl_noise = self.session_webgl_noise
        self.cdp.evaluate(f"""
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            const getParameter2 = WebGL2RenderingContext.prototype.getParameter;
            
            // Session boyunca tutarlı WebGL noise
            const sessionWebGLNoise = {webgl_noise};
            
            WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                if (parameter === 37445) {{
                    return 'Intel Inc.';
                }}
                if (parameter === 37446) {{
                    return 'Intel Iris OpenGL Engine';
                }}
                if (parameter === 7936) {{ // VENDOR
                    return 'Intel Inc.';
                }}
                if (parameter === 7937) {{ // RENDERER
                    return 'Intel Iris OpenGL Engine';
                }}
                if (parameter === 7938) {{ // VERSION
                    return 'OpenGL ES 2.0';
                }}
                // Session-specific noise ekle
                const result = getParameter.apply(this, arguments);
                if (typeof result === 'string') {{
                    return result + sessionWebGLNoise.toString().slice(0, 2);
                }}
                return result;
            }};
            
            WebGL2RenderingContext.prototype.getParameter = function(parameter) {{
                if (parameter === 37445) {{
                    return 'Intel Inc.';
                }}
                if (parameter === 37446) {{
                    return 'Intel Iris OpenGL Engine';
                }}
                if (parameter === 7936) {{ // VENDOR
                    return 'Intel Inc.';
                }}
                if (parameter === 7937) {{ // RENDERER
                    return 'Intel Iris OpenGL Engine';
                }}
                if (parameter === 7938) {{ // VERSION
                    return 'OpenGL ES 3.0';
                }}
                // Session-specific noise ekle
                const result = getParameter.apply(this, arguments);
                if (typeof result === 'string') {{
                    return result + sessionWebGLNoise.toString().slice(0, 2);
                }}
                return result;
            }};
        """)
        print("✅ WebGL fingerprinting bypass aktif! (Session tutarlı)")
    
    def setup_audio_fingerprint_bypass(self):
        """Audio fingerprinting bypass - Session tutarlı"""
        print("Audio fingerprinting bypass ayarlanıyor...")
        audio_noise = self.session_audio_noise
        self.cdp.evaluate(f"""
            const audioContext = window.AudioContext || window.webkitAudioContext;
            if (audioContext) {{
                const OriginalAudioContext = audioContext;
                
                // Session boyunca tutarlı audio noise
                const sessionAudioNoise = {audio_noise};
                
                window.AudioContext = function() {{
                    const context = new OriginalAudioContext();
                    const originalCreateOscillator = context.createOscillator;
                    const originalCreateAnalyser = context.createAnalyser;
                    const originalCreateGain = context.createGain;
                    
                    context.createOscillator = function() {{
                        const oscillator = originalCreateOscillator.apply(this, arguments);
                        const originalStart = oscillator.start;
                        const originalStop = oscillator.stop;
                        
                        oscillator.start = function() {{
                            // Session-specific audio fingerprint değiştir
                            this.frequency.value = this.frequency.value + (sessionAudioNoise % 100);
                            return originalStart.apply(this, arguments);
                        }};
                        
                        oscillator.stop = function() {{
                            return originalStop.apply(this, arguments);
                        }};
                        
                        return oscillator;
                    }};
                    
                    context.createAnalyser = function() {{
                        const analyser = originalCreateAnalyser.apply(this, arguments);
                        const originalGetFloatFrequencyData = analyser.getFloatFrequencyData;
                        
                        analyser.getFloatFrequencyData = function(array) {{
                            originalGetFloatFrequencyData.apply(this, arguments);
                            // Session-specific noise ekle
                            for (let i = 0; i < array.length; i++) {{
                                array[i] = array[i] + (sessionAudioNoise % 10) - 5;
                            }}
                        }};
                        
                        return analyser;
                    }};
                    
                    context.createGain = function() {{
                        const gain = originalCreateGain.apply(this, arguments);
                        const originalSetValueAtTime = gain.gain.setValueAtTime;
                        
                        gain.gain.setValueAtTime = function(value, startTime) {{
                            // Session-specific gain değişikliği
                            const modifiedValue = value + (sessionAudioNoise % 100) / 10000;
                            return originalSetValueAtTime.apply(this, [modifiedValue, startTime]);
                        }};
                        
                        return gain;
                    }};
                    
                    return context;
                }};
            }}
        """)
        print("✅ Audio fingerprinting bypass aktif! (Session tutarlı)")
    
    def setup_webdriver_stealth(self):
        """WebDriver tespitini engelle"""
        print("WebDriver stealth ayarları yapılıyor...")
        self.cdp.evaluate("""
            // WebDriver tespitini engelle
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            // Plugin sayısını artır
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            // Language ayarları
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            // Permissions API bypass
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
        """)
        print("✅ WebDriver stealth ayarları aktif!")
    
    def setup_consistent_fingerprints(self):
        """Session boyunca tutarlı fingerprint ayarları"""
        print("🔒 Session tutarlı fingerprint ayarları kuruluyor...")
        print(f"Session Seed: {self.session_seed}")
        print(f"Canvas Noise: {self.session_canvas_noise}")
        print(f"WebGL Noise: {self.session_webgl_noise}")
        print(f"Audio Noise: {self.session_audio_noise}")
        
        # Tüm fingerprint bypass'larını çalıştır
        self.setup_canvas_fingerprint_bypass()
        self.setup_webgl_fingerprint_bypass()
        self.setup_audio_fingerprint_bypass()
        self.setup_webdriver_stealth()
        
        print("🎯 Session tutarlı fingerprint ayarları tamamlandı!")
    
    def setup_all_stealth(self):
        """Tüm stealth ayarlarını çalıştır (geriye uyumluluk için)"""
        print("🔒 Tüm stealth ayarları kuruluyor...")
        self.setup_canvas_fingerprint_bypass()
        self.setup_webgl_fingerprint_bypass()
        self.setup_audio_fingerprint_bypass()
        self.setup_webdriver_stealth()
        print("🎯 Tüm stealth ayarları başarıyla kuruldu!")
