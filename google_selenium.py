import time
from seleniumbase import BaseCase

class TwitterSignup(BaseCase):
    def test_signup(self):
        # İngilizce locale ile başlat
        self.open("https://x.com/i/flow/signup")
        time.sleep(6)

        # Create account butonuna tıkla
        self.click('button:contains("Create account")')
        print("Create account butonuna tıklandı!")

        # Sayfanın yüklenmesini bekle
        time.sleep(3)

        # Use email instead butonuna tıkla
        self.click('button:contains("Use email instead")')
        print("Use email instead butonuna tıklandı!")

        # Sayfanın yüklenmesini bekle
        time.sleep(3)

        # Name input'una "süleyman" yaz
        self.type('input[name="name"]', "süleyman")
        time.sleep(1)
        print("Name input'una 'süleyman' yazıldı!")

        # Email input'una "sede@sede.com" yaz
        self.type('input[name="email"]', "sede@sede.com")
        time.sleep(1)
        print("Email input'una 'sede@sede.com' yazıldı!")

        # Ay seçimi - June (6. ay) seç
        self.select_option_by_text('select[id="SELECTOR_1"]', "June")
        time.sleep(1)
        print("Ay olarak 'June' seçildi!")

        # Gün seçimi - 30. gün seç
        self.select_option_by_text('select[id="SELECTOR_2"]', "30")
        time.sleep(1)
        print("Gün olarak '30' seçildi!")

        # Yıl seçimi - 1994 seç
        self.select_option_by_text('select[id="SELECTOR_3"]', "1994")
        time.sleep(1)
        print("Yıl olarak '1994' seçildi!")

        # Next butonuna tıkla
        self.click('button:contains("Next")')
        time.sleep(1)
        print("Next butonuna tıklandı!")

        # Enter'a basılmasını bekle
        input("Çıkmak için Enter'a basın...")

if __name__ == "__main__":
    # Proxy, İngilizce locale ve headed mode ile çalıştır
    BaseCase.main(__name__, __file__, "--proxy=3ed492ea9d26670b06c1__cr.us:4e17d20cd644f516@gw.dataimpulse.com:823", "--locale=en", "--headed")