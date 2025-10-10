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
        """WebDriver tespitini engelle ve navigator properties'i güçlendir"""
        print("WebDriver stealth ayarları yapılıyor...")
        self.cdp.evaluate("""
            // WebDriver tespitini engelle
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            // Plugin sayısını artır ve gerçekçi plugin listesi
            Object.defineProperty(navigator, 'plugins', {
                get: () => {
                    const plugins = [];
                    // Chrome PDF Viewer
                    plugins.push({
                        name: 'Chrome PDF Plugin',
                        description: 'Portable Document Format',
                        filename: 'internal-pdf-viewer',
                        length: 1
                    });
                    // Chrome PDF Viewer
                    plugins.push({
                        name: 'Chrome PDF Viewer',
                        description: '',
                        filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai',
                        length: 1
                    });
                    // Native Client
                    plugins.push({
                        name: 'Native Client',
                        description: '',
                        filename: 'internal-nacl-plugin',
                        length: 2
                    });
                    return plugins;
                },
            });
            
            // Language ayarları - ABD odaklı
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
            
            Object.defineProperty(navigator, 'language', {
                get: () => 'en-US',
            });
            
            // Hardware concurrency (CPU çekirdek sayısı) - gerçekçi değer
            Object.defineProperty(navigator, 'hardwareConcurrency', {
                get: () => 8, // Yaygın CPU çekirdek sayısı
            });
            
            // Device memory (RAM bilgisi) - gerçekçi değer
            Object.defineProperty(navigator, 'deviceMemory', {
                get: () => 8, // 8GB RAM
            });
            
            // Connection type - gerçekçi değer
            if (navigator.connection) {
                Object.defineProperty(navigator.connection, 'effectiveType', {
                    get: () => '4g',
                });
                Object.defineProperty(navigator.connection, 'type', {
                    get: () => 'wifi',
                });
                Object.defineProperty(navigator.connection, 'downlink', {
                    get: () => 10,
                });
                Object.defineProperty(navigator.connection, 'rtt', {
                    get: () => 50,
                });
            }
            
            // Platform details - Windows 10
            Object.defineProperty(navigator, 'platform', {
                get: () => 'Win32',
            });
            
            Object.defineProperty(navigator, 'oscpu', {
                get: () => 'Windows NT 10.0; Win64; x64',
            });
            
            // Vendor information
            Object.defineProperty(navigator, 'vendor', {
                get: () => 'Google Inc.',
            });
            
            Object.defineProperty(navigator, 'vendorSub', {
                get: () => '',
            });
            
            // Product information
            Object.defineProperty(navigator, 'product', {
                get: () => 'Gecko',
            });
            
            Object.defineProperty(navigator, 'productSub', {
                get: () => '20030107',
            });
            
            // User agent consistency
            Object.defineProperty(navigator, 'appName', {
                get: () => 'Netscape',
            });
            
            Object.defineProperty(navigator, 'appCodeName', {
                get: () => 'Mozilla',
            });
            
            Object.defineProperty(navigator, 'appVersion', {
                get: () => '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            });
            
            // Permissions API bypass
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            
            // Battery API - gerçekçi değerler
            if (navigator.getBattery) {
                const originalGetBattery = navigator.getBattery;
                navigator.getBattery = function() {
                    return Promise.resolve({
                        charging: true,
                        chargingTime: 0,
                        dischargingTime: Infinity,
                        level: 0.85
                    });
                };
            }
            
            // Screen properties - gerçekçi değerler
            Object.defineProperty(screen, 'availWidth', {
                get: () => 1920,
            });
            Object.defineProperty(screen, 'availHeight', {
                get: () => 1040,
            });
            Object.defineProperty(screen, 'width', {
                get: () => 1920,
            });
            Object.defineProperty(screen, 'height', {
                get: () => 1080,
            });
            Object.defineProperty(screen, 'colorDepth', {
                get: () => 24,
            });
            Object.defineProperty(screen, 'pixelDepth', {
                get: () => 24,
            });
            
            // Window properties
            Object.defineProperty(window, 'outerWidth', {
                get: () => 1920,
            });
            Object.defineProperty(window, 'outerHeight', {
                get: () => 1080,
            });
            Object.defineProperty(window, 'innerWidth', {
                get: () => 1920,
            });
            Object.defineProperty(window, 'innerHeight', {
                get: () => 947,
            });
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
    
    def block_webrtc_leak(self):
        """WebRTC IP sızıntısını engelle"""
        print("WebRTC IP sızıntısı engelleniyor...")
        self.cdp.evaluate("""
            // WebRTC'yi tamamen devre dışı bırak
            const originalRTCPeerConnection = window.RTCPeerConnection;
            const originalRTCSessionDescription = window.RTCSessionDescription;
            const originalRTCIceCandidate = window.RTCIceCandidate;
            
            // RTCPeerConnection'ı override et
            window.RTCPeerConnection = function(configuration) {
                console.log('WebRTC blocked: RTCPeerConnection attempt');
                return {
                    createOffer: function() { return Promise.reject(new Error('WebRTC blocked')); },
                    createAnswer: function() { return Promise.reject(new Error('WebRTC blocked')); },
                    setLocalDescription: function() { return Promise.reject(new Error('WebRTC blocked')); },
                    setRemoteDescription: function() { return Promise.reject(new Error('WebRTC blocked')); },
                    addIceCandidate: function() { return Promise.reject(new Error('WebRTC blocked')); },
                    getStats: function() { return Promise.reject(new Error('WebRTC blocked')); },
                    close: function() {},
                    localDescription: null,
                    remoteDescription: null,
                    connectionState: 'closed',
                    iceConnectionState: 'closed',
                    signalingState: 'closed'
                };
            };
            
            // RTCSessionDescription'ı override et
            window.RTCSessionDescription = function(descriptionInitDict) {
                return {
                    type: descriptionInitDict.type || 'offer',
                    sdp: descriptionInitDict.sdp || ''
                };
            };
            
            // RTCIceCandidate'ı override et
            window.RTCIceCandidate = function(candidateInitDict) {
                return {
                    candidate: candidateInitDict.candidate || '',
                    sdpMid: candidateInitDict.sdpMid || null,
                    sdpMLineIndex: candidateInitDict.sdpMLineIndex || null
                };
            };
            
            // getUserMedia'yi engelle
            const originalGetUserMedia = navigator.mediaDevices.getUserMedia;
            navigator.mediaDevices.getUserMedia = function(constraints) {
                console.log('WebRTC blocked: getUserMedia attempt');
                return Promise.reject(new Error('getUserMedia blocked'));
            };
            
            // enumerateDevices'i engelle
            const originalEnumerateDevices = navigator.mediaDevices.enumerateDevices;
            navigator.mediaDevices.enumerateDevices = function() {
                console.log('WebRTC blocked: enumerateDevices attempt');
                return Promise.resolve([]);
            };
            
            // getDisplayMedia'yı engelle
            if (navigator.mediaDevices.getDisplayMedia) {
                navigator.mediaDevices.getDisplayMedia = function(constraints) {
                    console.log('WebRTC blocked: getDisplayMedia attempt');
                    return Promise.reject(new Error('getDisplayMedia blocked'));
                };
            }
            
            // Legacy getUserMedia'yi de engelle
            if (navigator.getUserMedia) {
                navigator.getUserMedia = function(constraints, success, error) {
                    console.log('WebRTC blocked: legacy getUserMedia attempt');
                    if (error) error(new Error('getUserMedia blocked'));
                };
            }
            
            // webkitGetUserMedia'yi de engelle
            if (navigator.webkitGetUserMedia) {
                navigator.webkitGetUserMedia = function(constraints, success, error) {
                    console.log('WebRTC blocked: webkitGetUserMedia attempt');
                    if (error) error(new Error('webkitGetUserMedia blocked'));
                };
            }
            
            // mozGetUserMedia'yi de engelle
            if (navigator.mozGetUserMedia) {
                navigator.mozGetUserMedia = function(constraints, success, error) {
                    console.log('WebRTC blocked: mozGetUserMedia attempt');
                    if (error) error(new Error('mozGetUserMedia blocked'));
                };
            }
            
            // STUN/TURN sunucularını engelle
            const originalFetch = window.fetch;
            window.fetch = function(url, options) {
                if (typeof url === 'string' && (url.includes('stun:') || url.includes('turn:'))) {
                    console.log('WebRTC blocked: STUN/TURN request blocked');
                    return Promise.reject(new Error('STUN/TURN blocked'));
                }
                return originalFetch.apply(this, arguments);
            };
            
            // XMLHttpRequest ile STUN/TURN isteklerini engelle
            const originalXHROpen = XMLHttpRequest.prototype.open;
            XMLHttpRequest.prototype.open = function(method, url, async, user, password) {
                if (typeof url === 'string' && (url.includes('stun:') || url.includes('turn:'))) {
                    console.log('WebRTC blocked: XHR STUN/TURN request blocked');
                    throw new Error('STUN/TURN blocked');
                }
                return originalXHROpen.apply(this, arguments);
            };
        """)
        print("✅ WebRTC IP sızıntısı engellendi!")

    def setup_timezone_locale(self):
        """Timezone ve locale tutarlılığını sağla"""
        print("Timezone ve locale tutarlılığı ayarlanıyor...")
        self.cdp.evaluate("""
            // ABD timezone'ları - rastgele seç
            const usTimezones = [
                'America/New_York',      // Eastern Time
                'America/Chicago',       // Central Time  
                'America/Denver',        // Mountain Time
                'America/Los_Angeles',   // Pacific Time
                'America/Phoenix',       // Mountain Time (no DST)
                'America/Anchorage',     // Alaska Time
                'Pacific/Honolulu'       // Hawaii Time
            ];
            
            // Rastgele bir US timezone seç
            const selectedTimezone = usTimezones[Math.floor(Math.random() * usTimezones.length)];
            console.log('Selected timezone:', selectedTimezone);
            
            // Date.prototype.getTimezoneOffset override
            const originalGetTimezoneOffset = Date.prototype.getTimezoneOffset;
            Date.prototype.getTimezoneOffset = function() {
                // Seçilen timezone'a göre offset döndür
                switch(selectedTimezone) {
                    case 'America/New_York':
                        return 300; // UTC-5 (EST) / UTC-4 (EDT)
                    case 'America/Chicago':
                        return 360; // UTC-6 (CST) / UTC-5 (CDT)
                    case 'America/Denver':
                        return 420; // UTC-7 (MST) / UTC-6 (MDT)
                    case 'America/Los_Angeles':
                        return 480; // UTC-8 (PST) / UTC-7 (PDT)
                    case 'America/Phoenix':
                        return 420; // UTC-7 (MST - no DST)
                    case 'America/Anchorage':
                        return 540; // UTC-9 (AKST) / UTC-8 (AKDT)
                    case 'Pacific/Honolulu':
                        return 600; // UTC-10 (HST - no DST)
                    default:
                        return 300; // Default to Eastern
                }
            };
            
            // Intl.DateTimeFormat override
            const originalDateTimeFormat = Intl.DateTimeFormat;
            Intl.DateTimeFormat = function(locales, options) {
                // Timezone'u zorla ayarla
                if (!options) options = {};
                options.timeZone = selectedTimezone;
                return new originalDateTimeFormat(locales, options);
            };
            
            // Intl.DateTimeFormat.prototype.resolvedOptions override
            const originalResolvedOptions = Intl.DateTimeFormat.prototype.resolvedOptions;
            Intl.DateTimeFormat.prototype.resolvedOptions = function() {
                const options = originalResolvedOptions.call(this);
                options.timeZone = selectedTimezone;
                return options;
            };
            
            // Date.prototype.toLocaleString override
            const originalToLocaleString = Date.prototype.toLocaleString;
            Date.prototype.toLocaleString = function(locales, options) {
                if (!options) options = {};
                options.timeZone = selectedTimezone;
                return originalToLocaleString.call(this, locales, options);
            };
            
            // Date.prototype.toLocaleDateString override
            const originalToLocaleDateString = Date.prototype.toLocaleDateString;
            Date.prototype.toLocaleDateString = function(locales, options) {
                if (!options) options = {};
                options.timeZone = selectedTimezone;
                return originalToLocaleDateString.call(this, locales, options);
            };
            
            // Date.prototype.toLocaleTimeString override
            const originalToLocaleTimeString = Date.prototype.toLocaleTimeString;
            Date.prototype.toLocaleTimeString = function(locales, options) {
                if (!options) options = {};
                options.timeZone = selectedTimezone;
                return originalToLocaleTimeString.call(this, locales, options);
            };
            
            // Navigator.language consistency
            Object.defineProperty(navigator, 'language', {
                get: () => 'en-US',
                configurable: true
            });
            
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
                configurable: true
            });
            
            // Intl.Locale override
            if (window.Intl && window.Intl.Locale) {
                const originalLocale = window.Intl.Locale;
                window.Intl.Locale = function(tag, options) {
                    if (!options) options = {};
                    options.region = 'US';
                    options.language = 'en';
                    return new originalLocale(tag, options);
                };
            }
            
            // Number format locale consistency
            const originalNumberFormat = Intl.NumberFormat;
            Intl.NumberFormat = function(locales, options) {
                if (!locales || locales.length === 0) {
                    locales = ['en-US'];
                }
                return new originalNumberFormat(locales, options);
            };
            
            // Collator locale consistency
            const originalCollator = Intl.Collator;
            Intl.Collator = function(locales, options) {
                if (!locales || locales.length === 0) {
                    locales = ['en-US'];
                }
                return new originalCollator(locales, options);
            };
            
            // RelativeTimeFormat locale consistency
            if (window.Intl && window.Intl.RelativeTimeFormat) {
                const originalRelativeTimeFormat = window.Intl.RelativeTimeFormat;
                window.Intl.RelativeTimeFormat = function(locales, options) {
                    if (!locales || locales.length === 0) {
                        locales = ['en-US'];
                    }
                    return new originalRelativeTimeFormat(locales, options);
                };
            }
            
            // ListFormat locale consistency
            if (window.Intl && window.Intl.ListFormat) {
                const originalListFormat = window.Intl.ListFormat;
                window.Intl.ListFormat = function(locales, options) {
                    if (!locales || locales.length === 0) {
                        locales = ['en-US'];
                    }
                    return new originalListFormat(locales, options);
                };
            }
        """)
        print("✅ Timezone ve locale tutarlılığı sağlandı!")

    def setup_browser_properties(self):
        """Browser properties spoofing"""
        print("Browser properties spoofing ayarlanıyor...")
        self.cdp.evaluate("""
            // Chrome specific properties
            if (!window.chrome) {
                window.chrome = {};
            }
            
            // Chrome runtime
            window.chrome.runtime = {
                onConnect: {
                    addListener: function() {},
                    removeListener: function() {},
                    hasListener: function() { return false; }
                },
                onMessage: {
                    addListener: function() {},
                    removeListener: function() {},
                    hasListener: function() { return false; }
                },
                connect: function() {
                    return {
                        postMessage: function() {},
                        onMessage: {
                            addListener: function() {},
                            removeListener: function() {},
                            hasListener: function() { return false; }
                        },
                        disconnect: function() {}
                    };
                },
                sendMessage: function() {},
                getManifest: function() {
                    return {
                        name: "Chrome",
                        version: "120.0.0.0"
                    };
                }
            };
            
            // Chrome app
            window.chrome.app = {
                isInstalled: false,
                InstallState: {
                    DISABLED: 'disabled',
                    INSTALLED: 'installed',
                    NOT_INSTALLED: 'not_installed'
                },
                RunningState: {
                    CANNOT_RUN: 'cannot_run',
                    READY_TO_RUN: 'ready_to_run',
                    RUNNING: 'running'
                }
            };
            
            // Chrome csi
            window.chrome.csi = function() {
                return {
                    onloadT: Date.now(),
                    startE: Date.now() - Math.random() * 1000,
                    tran: Math.floor(Math.random() * 20)
                };
            };
            
            // Chrome loadTimes
            window.chrome.loadTimes = function() {
                return {
                    commitLoadTime: Date.now() / 1000 - Math.random() * 2,
                    connectionInfo: 'h2',
                    finishDocumentLoadTime: Date.now() / 1000 - Math.random(),
                    finishLoadTime: Date.now() / 1000 - Math.random() * 0.5,
                    firstPaintAfterLoadTime: 0,
                    firstPaintTime: Date.now() / 1000 - Math.random() * 3,
                    navigationType: 'Other',
                    npnNegotiatedProtocol: 'h2',
                    requestTime: Date.now() / 1000 - Math.random() * 5,
                    startLoadTime: Date.now() / 1000 - Math.random() * 4,
                    wasAlternateProtocolAvailable: false,
                    wasFetchedViaSpdy: true,
                    wasNpnNegotiated: true
                };
            };
            
            // PDF viewer plugin
            Object.defineProperty(navigator, 'plugins', {
                get: () => {
                    const plugins = [];
                    // Chrome PDF Viewer
                    plugins.push({
                        name: 'Chrome PDF Plugin',
                        description: 'Portable Document Format',
                        filename: 'internal-pdf-viewer',
                        length: 1,
                        item: function(index) {
                            return {
                                name: 'Chrome PDF Viewer',
                                description: 'Portable Document Format',
                                filename: 'internal-pdf-viewer'
                            };
                        },
                        namedItem: function(name) {
                            return {
                                name: 'Chrome PDF Viewer',
                                description: 'Portable Document Format',
                                filename: 'internal-pdf-viewer'
                            };
                        }
                    });
                    // Chrome PDF Viewer (extension)
                    plugins.push({
                        name: 'Chrome PDF Viewer',
                        description: '',
                        filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai',
                        length: 1,
                        item: function(index) {
                            return {
                                name: 'Chrome PDF Viewer',
                                description: '',
                                filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai'
                            };
                        },
                        namedItem: function(name) {
                            return {
                                name: 'Chrome PDF Viewer',
                                description: '',
                                filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai'
                            };
                        }
                    });
                    // Native Client
                    plugins.push({
                        name: 'Native Client',
                        description: '',
                        filename: 'internal-nacl-plugin',
                        length: 2,
                        item: function(index) {
                            return {
                                name: index === 0 ? 'Native Client' : 'Native Client',
                                description: '',
                                filename: 'internal-nacl-plugin'
                            };
                        },
                        namedItem: function(name) {
                            return {
                                name: 'Native Client',
                                description: '',
                                filename: 'internal-nacl-plugin'
                            };
                        }
                    });
                    return plugins;
                },
            });
            
            // MIME types
            Object.defineProperty(navigator, 'mimeTypes', {
                get: () => {
                    const mimeTypes = [];
                    // PDF MIME type
                    mimeTypes.push({
                        type: 'application/pdf',
                        suffixes: 'pdf',
                        description: 'Portable Document Format',
                        enabledPlugin: {
                            name: 'Chrome PDF Plugin',
                            description: 'Portable Document Format',
                            filename: 'internal-pdf-viewer'
                        }
                    });
                    // NaCl MIME types
                    mimeTypes.push({
                        type: 'application/x-nacl',
                        suffixes: 'nexe',
                        description: 'Native Client Executable',
                        enabledPlugin: {
                            name: 'Native Client',
                            description: '',
                            filename: 'internal-nacl-plugin'
                        }
                    });
                    mimeTypes.push({
                        type: 'application/x-pnacl',
                        suffixes: 'pexe',
                        description: 'Portable Native Client Executable',
                        enabledPlugin: {
                            name: 'Native Client',
                            description: '',
                            filename: 'internal-nacl-plugin'
                        }
                    });
                    return mimeTypes;
                },
            });
            
            // Notification API consistency
            if (window.Notification) {
                const originalNotification = window.Notification;
                window.Notification = function(title, options) {
                    return new originalNotification(title, options);
                };
                window.Notification.permission = 'default';
                window.Notification.requestPermission = function() {
                    return Promise.resolve('default');
                };
            }
            
            // Permissions API realism
            if (navigator.permissions) {
                const originalQuery = navigator.permissions.query;
                navigator.permissions.query = function(parameters) {
                    return Promise.resolve({
                        state: 'prompt',
                        onchange: null
                    });
                };
            }
            
            // Battery API (if needed)
            if (navigator.getBattery) {
                const originalGetBattery = navigator.getBattery;
                navigator.getBattery = function() {
                    return Promise.resolve({
                        charging: true,
                        chargingTime: 0,
                        dischargingTime: Infinity,
                        level: 0.85,
                        addEventListener: function() {},
                        removeEventListener: function() {},
                        dispatchEvent: function() { return true; }
                    });
                };
            }
            
            // Vibration API
            if (navigator.vibrate) {
                const originalVibrate = navigator.vibrate;
                navigator.vibrate = function(pattern) {
                    return true;
                };
            }
            
            // Geolocation API
            if (navigator.geolocation) {
                const originalGetCurrentPosition = navigator.geolocation.getCurrentPosition;
                const originalWatchPosition = navigator.geolocation.watchPosition;
                
                navigator.geolocation.getCurrentPosition = function(success, error, options) {
                    if (error) {
                        error({
                            code: 1,
                            message: 'User denied geolocation'
                        });
                    }
                };
                
                navigator.geolocation.watchPosition = function(success, error, options) {
                    return 1;
                };
            }
            
            // MediaDevices API
            if (navigator.mediaDevices) {
                const originalGetUserMedia = navigator.mediaDevices.getUserMedia;
                navigator.mediaDevices.getUserMedia = function(constraints) {
                    return Promise.reject(new Error('Permission denied'));
                };
                
                const originalEnumerateDevices = navigator.mediaDevices.enumerateDevices;
                navigator.mediaDevices.enumerateDevices = function() {
                    return Promise.resolve([]);
                };
            }
            
            // Clipboard API
            if (navigator.clipboard) {
                const originalWriteText = navigator.clipboard.writeText;
                navigator.clipboard.writeText = function(text) {
                    return Promise.resolve();
                };
                
                const originalReadText = navigator.clipboard.readText;
                navigator.clipboard.readText = function() {
                    return Promise.resolve('');
                };
            }
        """)
        print("✅ Browser properties spoofing aktif!")

    def setup_request_headers(self):
        """Request headers tutarlılığını sağla"""
        print("Request headers tutarlılığı ayarlanıyor...")
        self.cdp.evaluate("""
            // Accept-Language tutarlılığı
            const originalFetch = window.fetch;
            window.fetch = function(url, options) {
                if (!options) options = {};
                if (!options.headers) options.headers = {};
                
                // Accept-Language header'ını zorla ayarla
                options.headers['Accept-Language'] = 'en-US,en;q=0.9';
                
                // Sec-CH-UA headers (Chrome User Agent Client Hints)
                options.headers['Sec-CH-UA'] = '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"';
                options.headers['Sec-CH-UA-Mobile'] = '?0';
                options.headers['Sec-CH-UA-Platform'] = '"Windows"';
                options.headers['Sec-CH-UA-Platform-Version'] = '"15.0.0"';
                options.headers['Sec-CH-UA-Arch'] = '"x86"';
                options.headers['Sec-CH-UA-Bitness'] = '"64"';
                options.headers['Sec-CH-UA-Model'] = '""';
                options.headers['Sec-CH-UA-Full-Version'] = '"120.0.6099.109"';
                options.headers['Sec-CH-UA-Full-Version-List'] = '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.109", "Google Chrome";v="120.0.6099.109"';
                
                // Fetch metadata headers
                options.headers['Sec-Fetch-Dest'] = 'document';
                options.headers['Sec-Fetch-Mode'] = 'navigate';
                options.headers['Sec-Fetch-Site'] = 'none';
                options.headers['Sec-Fetch-User'] = '?1';
                
                // Referer policy
                options.headers['Referer'] = 'https://www.google.com/';
                
                // Cache control
                options.headers['Cache-Control'] = 'max-age=0';
                
                // Upgrade-Insecure-Requests
                options.headers['Upgrade-Insecure-Requests'] = '1';
                
                return originalFetch.call(this, url, options);
            };
            
            // XMLHttpRequest headers
            const originalXHROpen = XMLHttpRequest.prototype.open;
            const originalXHRSend = XMLHttpRequest.prototype.send;
            
            XMLHttpRequest.prototype.open = function(method, url, async, user, password) {
                this._method = method;
                this._url = url;
                return originalXHROpen.call(this, method, url, async, user, password);
            };
            
            XMLHttpRequest.prototype.send = function(data) {
                // Accept-Language header'ını zorla ayarla
                this.setRequestHeader('Accept-Language', 'en-US,en;q=0.9');
                
                // Sec-CH-UA headers
                this.setRequestHeader('Sec-CH-UA', '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"');
                this.setRequestHeader('Sec-CH-UA-Mobile', '?0');
                this.setRequestHeader('Sec-CH-UA-Platform', '"Windows"');
                this.setRequestHeader('Sec-CH-UA-Platform-Version', '"15.0.0"');
                this.setRequestHeader('Sec-CH-UA-Arch', '"x86"');
                this.setRequestHeader('Sec-CH-UA-Bitness', '"64"');
                this.setRequestHeader('Sec-CH-UA-Model', '""');
                this.setRequestHeader('Sec-CH-UA-Full-Version', '"120.0.6099.109"');
                this.setRequestHeader('Sec-CH-UA-Full-Version-List', '"Not_A Brand";v="8.0.0.0", "Chromium";v="120.0.6099.109", "Google Chrome";v="120.0.6099.109"');
                
                // Fetch metadata headers
                this.setRequestHeader('Sec-Fetch-Dest', 'empty');
                this.setRequestHeader('Sec-Fetch-Mode', 'cors');
                this.setRequestHeader('Sec-Fetch-Site', 'same-origin');
                
                // Referer policy
                this.setRequestHeader('Referer', window.location.origin + '/');
                
                // Cache control
                this.setRequestHeader('Cache-Control', 'no-cache');
                
                return originalXHRSend.call(this, data);
            };
            
            // Navigator.sendBeacon headers
            const originalSendBeacon = navigator.sendBeacon;
            navigator.sendBeacon = function(url, data) {
                // sendBeacon için header ayarlama yapılamaz, ama URL'yi kontrol edebiliriz
                return originalSendBeacon.call(this, url, data);
            };
            
            // Document.referrer override
            Object.defineProperty(document, 'referrer', {
                get: () => 'https://www.google.com/',
                configurable: true
            });
            
            // Document.referrer (alternatif)
            Object.defineProperty(document, 'referer', {
                get: () => 'https://www.google.com/',
                configurable: true
            });
            
            // History API override
            const originalPushState = history.pushState;
            const originalReplaceState = history.replaceState;
            
            history.pushState = function(state, title, url) {
                // Referer'ı güncelle
                document._referrer = window.location.href;
                return originalPushState.call(this, state, title, url);
            };
            
            history.replaceState = function(state, title, url) {
                // Referer'ı güncelle
                document._referrer = window.location.href;
                return originalReplaceState.call(this, state, title, url);
            };
            
            // Link click tracking
            document.addEventListener('click', function(event) {
                const target = event.target;
                if (target.tagName === 'A' && target.href) {
                    // Link tıklamalarında referer'ı ayarla
                    target.setAttribute('data-referrer', window.location.href);
                }
            }, true);
            
            // Form submission tracking
            document.addEventListener('submit', function(event) {
                const form = event.target;
                if (form.tagName === 'FORM') {
                    // Form gönderimlerinde referer'ı ayarla
                    const hiddenInput = document.createElement('input');
                    hiddenInput.type = 'hidden';
                    hiddenInput.name = '_referrer';
                    hiddenInput.value = window.location.href;
                    form.appendChild(hiddenInput);
                }
            }, true);
            
            // Service Worker registration (if exists)
            if ('serviceWorker' in navigator) {
                const originalRegister = navigator.serviceWorker.register;
                navigator.serviceWorker.register = function(scriptURL, options) {
                    // Service Worker kayıtlarında referer'ı ayarla
                    if (!options) options = {};
                    options.scope = options.scope || '/';
                    return originalRegister.call(this, scriptURL, options);
                };
            }
            
            // WebSocket headers (if needed)
            const originalWebSocket = window.WebSocket;
            window.WebSocket = function(url, protocols) {
                // WebSocket bağlantılarında referer'ı ayarla
                const ws = new originalWebSocket(url, protocols);
                return ws;
            };
            
            // EventSource headers (if needed)
            if (window.EventSource) {
                const originalEventSource = window.EventSource;
                window.EventSource = function(url, eventSourceInitDict) {
                    // EventSource bağlantılarında referer'ı ayarla
                    if (!eventSourceInitDict) eventSourceInitDict = {};
                    eventSourceInitDict.withCredentials = false;
                    return new originalEventSource(url, eventSourceInitDict);
                };
            }
        """)
        print("✅ Request headers tutarlılığı sağlandı!")

    def setup_all_stealth(self):
        """Tüm stealth ayarlarını çalıştır (geriye uyumluluk için)"""
        print("🔒 Tüm stealth ayarları kuruluyor...")
        self.setup_canvas_fingerprint_bypass()
        self.setup_webgl_fingerprint_bypass()
        self.setup_audio_fingerprint_bypass()
        self.setup_webdriver_stealth()
        self.block_webrtc_leak()
        self.setup_timezone_locale()
        self.setup_browser_properties()
        self.setup_request_headers()
        print("🎯 Tüm stealth ayarları başarıyla kuruldu!")
