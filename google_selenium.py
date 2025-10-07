import time
from seleniumbase import Driver

driver = Driver(headless=False, proxy="3ed492ea9d26670b06c1__cr.us:4e17d20cd644f516@gw.dataimpulse.com:823", locale="en")
driver.get("https://x.com/i/flow/signup")
time.sleep(6)

# Create account butonuna tıkla
print("Create account butonuna tıklanıyor...")
driver.click('button:contains("Create account")')
print("Butona tıklandı!")

# Enter'a basılmasını bekle
input("Çıkmak için Enter'a basın...")

driver.quit()