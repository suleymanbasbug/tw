"""
Stealth Helper Modülü
CDP Mode ile fingerprinting bypass ve stealth ayarları
"""

class StealthHelper:
    """CDP Mode ile stealth ayarlarını yöneten sınıf"""
    
    def __init__(self, cdp_instance):
        """CDP instance'ını al"""
        self.cdp = cdp_instance
    
    def setup_canvas_fingerprint_bypass(self):
        """Canvas fingerprinting bypass"""
        print("Canvas fingerprinting bypass ayarlanıyor...")
        self.cdp.evaluate("""
            const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
            HTMLCanvasElement.prototype.toDataURL = function(type) {
                if (type === 'image/png' && this.width === 280 && this.height === 60) {
                    return 'data:image/png;base64,iVBORw0KGg==';
                }
                return originalToDataURL.apply(this, arguments);
            };
        """)
        print("✅ Canvas fingerprinting bypass aktif!")
    
    def setup_webgl_fingerprint_bypass(self):
        """WebGL fingerprinting bypass"""
        print("WebGL fingerprinting bypass ayarlanıyor...")
        self.cdp.evaluate("""
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) {
                    return 'Intel Inc.';
                }
                if (parameter === 37446) {
                    return 'Intel Iris OpenGL Engine';
                }
                return getParameter.apply(this, arguments);
            };
        """)
        print("✅ WebGL fingerprinting bypass aktif!")
    
    def setup_audio_fingerprint_bypass(self):
        """Audio fingerprinting bypass"""
        print("Audio fingerprinting bypass ayarlanıyor...")
        self.cdp.evaluate("""
            const audioContext = window.AudioContext || window.webkitAudioContext;
            if (audioContext) {
                const OriginalAudioContext = audioContext;
                window.AudioContext = function() {
                    const context = new OriginalAudioContext();
                    const originalCreateOscillator = context.createOscillator;
                    context.createOscillator = function() {
                        const oscillator = originalCreateOscillator.apply(this, arguments);
                        const originalStart = oscillator.start;
                        oscillator.start = function() {
                            // Ses parmak izini değiştir
                            return originalStart.apply(this, arguments);
                        };
                        return oscillator;
                    };
                    return context;
                };
            }
        """)
        print("✅ Audio fingerprinting bypass aktif!")
    
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
    
    def setup_all_stealth(self):
        """Tüm stealth ayarlarını çalıştır"""
        print("🔒 Tüm stealth ayarları kuruluyor...")
        self.setup_canvas_fingerprint_bypass()
        self.setup_webgl_fingerprint_bypass()
        self.setup_audio_fingerprint_bypass()
        self.setup_webdriver_stealth()
        print("🎯 Tüm stealth ayarları başarıyla kuruldu!")
