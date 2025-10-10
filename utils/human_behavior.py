"""
Human Behavior Modülü
Gerçekçi insan davranışlarını simüle eden sınıf
"""

import random
import math
import time

class HumanBehavior:
    """İnsan benzeri davranışları simüle eden sınıf"""
    
    def __init__(self, selenium_instance):
        """Selenium instance'ını al"""
        self.selenium = selenium_instance
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        
    def gaussian_random(self, mean, std_dev):
        """Gauss dağılımından rastgele sayı üret"""
        # Box-Muller transformasyonu
        u1 = random.random()
        u2 = random.random()
        z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        return mean + z0 * std_dev
    
    def bezier_curve(self, start_x, start_y, end_x, end_y, control_points=2):
        """Bezier eğrisi ile doğal mouse hareketi"""
        points = []
        
        # Kontrol noktaları oluştur
        for i in range(control_points):
            t = (i + 1) / (control_points + 1)
            # Rastgele sapma ekle
            offset_x = random.uniform(-50, 50)
            offset_y = random.uniform(-50, 50)
            
            control_x = start_x + (end_x - start_x) * t + offset_x
            control_y = start_y + (end_y - start_y) * t + offset_y
            
            points.append((control_x, control_y))
        
        # Bezier eğrisi boyunca noktalar hesapla
        curve_points = []
        steps = random.randint(10, 20)
        
        for i in range(steps + 1):
            t = i / steps
            x, y = self._bezier_point(start_x, start_y, end_x, end_y, points, t)
            curve_points.append((x, y))
        
        return curve_points
    
    def _bezier_point(self, start_x, start_y, end_x, end_y, control_points, t):
        """Bezier eğrisi üzerinde bir nokta hesapla"""
        # Basit cubic bezier
        if len(control_points) >= 2:
            cp1_x, cp1_y = control_points[0]
            cp2_x, cp2_y = control_points[1]
            
            # Cubic bezier formülü
            x = (1-t)**3 * start_x + 3*(1-t)**2*t * cp1_x + 3*(1-t)*t**2 * cp2_x + t**3 * end_x
            y = (1-t)**3 * start_y + 3*(1-t)**2*t * cp1_y + 3*(1-t)*t**2 * cp2_y + t**3 * end_y
        else:
            # Linear interpolation
            x = start_x + (end_x - start_x) * t
            y = start_y + (end_y - start_y) * t
        
        return x, y
    
    def random_mouse_movement(self, target_x=None, target_y=None):
        """Rastgele mouse hareketi"""
        print("🖱️ Rastgele mouse hareketi başlatılıyor...")
        
        # Mevcut mouse pozisyonunu al
        current_x = self.last_mouse_x if self.last_mouse_x > 0 else random.randint(100, 800)
        current_y = self.last_mouse_y if self.last_mouse_y > 0 else random.randint(100, 600)
        
        # Hedef pozisyon belirle
        if target_x is None:
            target_x = random.randint(100, 1200)
        if target_y is None:
            target_y = random.randint(100, 800)
        
        # Bezier eğrisi ile hareket
        curve_points = self.bezier_curve(current_x, current_y, target_x, target_y)
        
        # Mouse'u hareket ettir
        for x, y in curve_points:
            self.selenium.cdp.evaluate(f"""
                (function() {{
                    // Mouse'u belirtilen pozisyona hareket ettir
                    const event = new MouseEvent('mousemove', {{
                        clientX: {x},
                        clientY: {y},
                        bubbles: true,
                        cancelable: true
                    }});
                    document.dispatchEvent(event);
                }})();
            """)
            
            # Kısa bekleme
            time.sleep(random.uniform(0.01, 0.03))
        
        # Son pozisyonu kaydet
        self.last_mouse_x = target_x
        self.last_mouse_y = target_y
        
        print(f"✅ Mouse hareketi tamamlandı: ({current_x}, {current_y}) -> ({target_x}, {target_y})")
    
    def hover_element(self, selector):
        """Elementin üzerine hover yap"""
        print(f"🎯 Element hover: {selector}")
        
        # Element pozisyonunu al
        element_info = self.selenium.cdp.evaluate(f"""
            (function() {{
                const element = document.querySelector('{selector}');
                if (element) {{
                    const rect = element.getBoundingClientRect();
                    return {{
                        x: rect.left + rect.width / 2,
                        y: rect.top + rect.height / 2,
                        width: rect.width,
                        height: rect.height
                    }};
                }}
                return null;
            }})();
        """)
        
        if element_info:
            # Element merkezine hover yap
            center_x = element_info['x']
            center_y = element_info['y']
            
            # Rastgele sapma ekle (element içinde)
            offset_x = random.uniform(-element_info['width']/4, element_info['width']/4)
            offset_y = random.uniform(-element_info['height']/4, element_info['height']/4)
            
            hover_x = center_x + offset_x
            hover_y = center_y + offset_y
            
            # Mouse'u hareket ettir
            self.random_mouse_movement(hover_x, hover_y)
            
            # Hover eventi tetikle
            self.selenium.cdp.evaluate(f"""
                (function() {{
                    const element = document.querySelector('{selector}');
                    if (element) {{
                        const event = new MouseEvent('mouseenter', {{
                            clientX: {hover_x},
                            clientY: {hover_y},
                            bubbles: true,
                            cancelable: true
                        }});
                        element.dispatchEvent(event);
                    }}
                }})();
            """)
            
            # Hover süresi
            hover_duration = self.gaussian_random(0.5, 0.2)
            hover_duration = max(0.1, min(2.0, hover_duration))  # 0.1-2.0 saniye arası
            time.sleep(hover_duration)
            
            print(f"✅ Hover tamamlandı: ({hover_x:.1f}, {hover_y:.1f})")
        else:
            print(f"❌ Element bulunamadı: {selector}")
    
    def smooth_scroll(self, direction="down", distance=None):
        """Smooth scroll hareketi"""
        print(f"📜 Smooth scroll: {direction}")
        
        if distance is None:
            distance = random.randint(200, 800)
        
        # Scroll adımları
        steps = random.randint(5, 15)
        step_distance = distance / steps
        
        for i in range(steps):
            # Gauss dağılımı ile timing
            step_delay = self.gaussian_random(0.05, 0.02)
            step_delay = max(0.01, min(0.2, step_delay))
            
            # Scroll yönü
            scroll_delta = step_distance if direction == "down" else -step_distance
            
            self.selenium.cdp.evaluate(f"""
                window.scrollBy(0, {scroll_delta});
            """)
            
            time.sleep(step_delay)
        
        print(f"✅ Smooth scroll tamamlandı: {direction} {distance}px")
    
    def thinking_pause(self, context="general"):
        """Düşünme süresi - insan benzeri duraklama"""
        print(f"🤔 Düşünme süresi: {context}")
        
        # Context'e göre süre belirle
        if context == "form_fill":
            mean_time = 2.0
            std_dev = 0.8
        elif context == "reading":
            mean_time = 3.0
            std_dev = 1.2
        elif context == "decision":
            mean_time = 1.5
            std_dev = 0.6
        else:
            mean_time = 1.0
            std_dev = 0.4
        
        # Gauss dağılımı ile süre hesapla
        pause_time = self.gaussian_random(mean_time, std_dev)
        pause_time = max(0.2, min(5.0, pause_time))  # 0.2-5.0 saniye arası
        
        # Ara sıra micro-movements ekle
        if random.random() < 0.3:  # %30 ihtimal
            self.micro_movement()
        
        time.sleep(pause_time)
        print(f"✅ Düşünme süresi tamamlandı: {pause_time:.2f}s")
    
    def micro_movement(self):
        """Küçük düzeltici hareketler"""
        # Mevcut pozisyondan küçük sapma
        offset_x = random.uniform(-10, 10)
        offset_y = random.uniform(-10, 10)
        
        new_x = self.last_mouse_x + offset_x
        new_y = self.last_mouse_y + offset_y
        
        self.selenium.cdp.evaluate(f"""
            const event = new MouseEvent('mousemove', {{
                clientX: {new_x},
                clientY: {new_y},
                bubbles: true,
                cancelable: true
            }});
            document.dispatchEvent(event);
        """)
        
        # Kısa bekleme
        time.sleep(random.uniform(0.05, 0.15))
    
    def typing_rhythm(self, text, speed="normal"):
        """İnsan benzeri yazma ritmi"""
        print(f"⌨️ Yazma ritmi: {speed}")
        
        # Hız ayarları
        if speed == "slow":
            mean_delay = 0.15
            std_dev = 0.05
        elif speed == "fast":
            mean_delay = 0.08
            std_dev = 0.03
        else:  # normal
            mean_delay = 0.12
            std_dev = 0.04
        
        # Her karakter için timing
        for i, char in enumerate(text):
            # Karakter türüne göre timing ayarla
            if char.isalpha():
                # Harf - normal timing
                delay = self.gaussian_random(mean_delay, std_dev)
            elif char.isdigit():
                # Rakam - biraz daha hızlı
                delay = self.gaussian_random(mean_delay * 0.8, std_dev * 0.8)
            elif char in ' .,!?':
                # Noktalama - daha yavaş
                delay = self.gaussian_random(mean_delay * 1.5, std_dev * 1.2)
            else:
                # Diğer karakterler
                delay = self.gaussian_random(mean_delay, std_dev)
            
            # Ara sıra typo yap (çok nadir)
            if random.random() < 0.02:  # %2 ihtimal
                # Yanlış karakter yaz, sonra düzelt
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                yield wrong_char, delay * 0.5
                yield '\b', delay * 0.3  # Backspace
                yield char, delay
            else:
                yield char, delay
            
            # Ara sıra duraklama (kelime arası)
            if char == ' ' and random.random() < 0.1:  # %10 ihtimal
                pause = self.gaussian_random(0.3, 0.1)
                yield None, pause  # None = pause
    
    def human_click(self, selector, click_type="left"):
        """İnsan benzeri tıklama"""
        print(f"👆 İnsan benzeri tıklama: {selector}")
        
        # Önce hover yap
        self.hover_element(selector)
        
        # Kısa bekleme (tıklamadan önce)
        pre_click_delay = self.gaussian_random(0.1, 0.05)
        time.sleep(max(0.05, pre_click_delay))
        
        # Tıklama
        if click_type == "left":
            self.selenium.cdp.evaluate(f"""
                const element = document.querySelector('{selector}');
                if (element) {{
                    const rect = element.getBoundingClientRect();
                    const x = rect.left + rect.width / 2;
                    const y = rect.top + rect.height / 2;
                    
                    // Mouse down
                    const mouseDown = new MouseEvent('mousedown', {{
                        clientX: x,
                        clientY: y,
                        bubbles: true,
                        cancelable: true,
                        button: 0
                    }});
                    element.dispatchEvent(mouseDown);
                    
                    // Kısa bekleme
                    setTimeout(() => {{
                        // Mouse up
                        const mouseUp = new MouseEvent('mouseup', {{
                            clientX: x,
                            clientY: y,
                            bubbles: true,
                            cancelable: true,
                            button: 0
                        }});
                        element.dispatchEvent(mouseUp);
                        
                        // Click
                        const click = new MouseEvent('click', {{
                            clientX: x,
                            clientY: y,
                            bubbles: true,
                            cancelable: true,
                            button: 0
                        }});
                        element.dispatchEvent(click);
                    }}, {random.randint(50, 150)});
                }}
            """)
        
        # Tıklama sonrası bekleme
        post_click_delay = self.gaussian_random(0.2, 0.1)
        time.sleep(max(0.1, post_click_delay))
        
        print(f"✅ İnsan benzeri tıklama tamamlandı: {selector}")
    
    def random_idle_behavior(self):
        """Rastgele idle davranışları"""
        print("😴 Rastgele idle davranışı...")
        
        behaviors = [
            self._idle_scroll,
            self._idle_mouse_movement,
            self._idle_pause
        ]
        
        # Rastgele bir davranış seç
        behavior = random.choice(behaviors)
        behavior()
    
    def _idle_scroll(self):
        """Idle sırasında rastgele scroll"""
        direction = random.choice(["up", "down"])
        distance = random.randint(50, 200)
        self.smooth_scroll(direction, distance)
    
    def _idle_mouse_movement(self):
        """Idle sırasında rastgele mouse hareketi"""
        target_x = random.randint(100, 1200)
        target_y = random.randint(100, 800)
        self.random_mouse_movement(target_x, target_y)
    
    def _idle_pause(self):
        """Idle sırasında duraklama"""
        pause_time = self.gaussian_random(1.0, 0.5)
        pause_time = max(0.5, min(3.0, pause_time))
        time.sleep(pause_time)

# Test fonksiyonu
if __name__ == "__main__":
    print("=== Human Behavior Modülü Testi ===")
    
    # Mock selenium instance
    class MockSelenium:
        def __init__(self):
            self.cdp = self
        
        def evaluate(self, script):
            print(f"CDP Evaluate: {script[:50]}...")
            return {}
    
    mock_selenium = MockSelenium()
    human = HumanBehavior(mock_selenium)
    
    # Test fonksiyonları
    print("\n1. Gauss dağılımı testi:")
    for i in range(5):
        value = human.gaussian_random(1.0, 0.3)
        print(f"   {i+1}. {value:.3f}")
    
    print("\n2. Bezier eğrisi testi:")
    points = human.bezier_curve(100, 100, 500, 300)
    print(f"   {len(points)} nokta üretildi")
    
    print("\n3. Yazma ritmi testi:")
    for char, delay in human.typing_rhythm("Hello World!", "normal"):
        if char is None:
            print(f"   [PAUSE: {delay:.3f}s]")
        else:
            print(f"   '{char}' -> {delay:.3f}s")
    
    print("\n✅ Human Behavior modülü testi tamamlandı!")
