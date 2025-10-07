# Selenium 3 ile Google'a Gitme

Bu proje Selenium 3 kullanarak Google'a gitmeyi ve temel web otomasyonu işlemlerini gösterir.

## Gereksinimler

- Python 3.6+
- Chrome tarayıcısı
- ChromeDriver

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. ChromeDriver'ı indirin ve PATH'e ekleyin:
   - [ChromeDriver indirme sayfası](https://chromedriver.chromium.org/downloads)
   - ChromeDriver'ı sistem PATH'ine ekleyin

## Kullanım

Scripti çalıştırın:
```bash
python google_selenium.py
```

## Özellikler

- Selenium 3.141.0 kullanır
- Google'a gider
- Arama kutusunu bulur ve test eder
- Hata yönetimi içerir
- Chrome tarayıcı seçenekleri ile optimize edilmiştir

## Notlar

- Script Chrome tarayıcısını kullanır
- Arka planda çalıştırmak için `chrome_options.add_argument("--headless")` satırının yorumunu kaldırın
- ChromeDriver'ın Chrome tarayıcısı ile uyumlu olduğundan emin olun
