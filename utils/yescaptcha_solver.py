import requests
import json
import re

def solve_funcaptcha(base64_image, question_text):
    """
    YesCaptcha API'sine FunCaptcha çözümü için istek gönderir.
    
    Args:
        base64_image (str): Captcha resmi (base64 string)
        question_text (str): Soru metni (örn: "Pick the bread")
    
    Returns:
        dict: API response'u (JSON formatında)
    """
    print("🚀 YesCaptcha API'sine FunCaptcha çözümü için istek gönderiliyor...")
    
    # API endpoint ve client key
    api_url = "https://api.yescaptcha.com/createTask"
    client_key = "3850773cda8581361a553b1f3712102c1dd44de179197"
    
    try:
        # Base64 image formatını kontrol et ve düzelt
        print("🔍 Base64 image formatı kontrol ediliyor...")
        
        # Eğer başında data:image prefix'i yoksa ekle
        if not re.match(r'^data:image/(jpeg|jpg|png);base64,', base64_image):
            print("⚠️ Base64 image'de data:image prefix'i bulunamadı, ekleniyor...")
            # PNG formatında ekle (daha yaygın)
            base64_image = f"data:image/png;base64,{base64_image}"
            print("✅ data:image/png;base64, prefix'i eklendi")
        else:
            print("✅ Base64 image formatı doğru")
        
        # Request body'yi hazırla
        request_body = {
            "clientKey": client_key,
            "task": {
                "type": "FunCaptchaClassification",
                "image": base64_image,
                "question": question_text
            }
        }
        
        print(f"📤 Request body hazırlandı:")
        print(f"   - Type: FunCaptchaClassification")
        print(f"   - Question: {question_text}")
        print(f"   - Image length: {len(base64_image)} karakter")
        
        # Headers
        headers = {
            "Content-Type": "application/json"
        }
        
        # POST isteği gönder
        print("🌐 API'ye POST isteği gönderiliyor...")
        response = requests.post(api_url, json=request_body, headers=headers, timeout=30)
        
        # Status code kontrolü
        print(f"📊 Response status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ API isteği başarılı!")
            
            # Response'u parse et
            try:
                response_data = response.json()
                
                # Response'u formatted olarak print et
                print("\n" + "="*60)
                print("📋 YESCAPTCHA API RESPONSE")
                print("="*60)
                print(json.dumps(response_data, indent=2, ensure_ascii=False))
                print("="*60)
                
                return response_data
                
            except json.JSONDecodeError as json_error:
                print(f"❌ Response JSON parse hatası: {json_error}")
                print(f"📄 Raw response: {response.text}")
                return {"error": "JSON parse hatası", "raw_response": response.text}
                
        else:
            print(f"❌ API isteği başarısız! Status code: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return {
                "error": f"HTTP {response.status_code}",
                "status_code": response.status_code,
                "response": response.text
            }
            
    except requests.exceptions.Timeout:
        print("❌ API isteği timeout! (30 saniye)")
        return {"error": "Timeout", "message": "API isteği 30 saniye içinde tamamlanamadı"}
        
    except requests.exceptions.ConnectionError:
        print("❌ Bağlantı hatası! İnternet bağlantınızı kontrol edin.")
        return {"error": "Connection Error", "message": "API'ye bağlanılamadı"}
        
    except requests.exceptions.RequestException as req_error:
        print(f"❌ Request hatası: {req_error}")
        return {"error": "Request Error", "message": str(req_error)}
        
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        return {"error": "Unexpected Error", "message": str(e)}


def test_yescaptcha_solver():
    """Test fonksiyonu - örnek base64 ve question ile API'yi test eder"""
    print("\n🧪 YesCaptcha Solver Test Fonksiyonu")
    print("="*50)
    
    # Test için örnek base64 (küçük bir test resmi)
    test_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    # Test question
    test_question = "Pick the bread"
    
    print(f"📝 Test parametreleri:")
    print(f"   - Question: {test_question}")
    print(f"   - Base64 length: {len(test_base64)} karakter")
    
    # API'yi test et
    result = solve_funcaptcha(test_base64, test_question)
    
    print(f"\n📊 Test sonucu:")
    print(f"   - Result type: {type(result)}")
    if isinstance(result, dict):
        print(f"   - Keys: {list(result.keys())}")
    
    return result


if __name__ == "__main__":
    print("🎯 YesCaptcha Solver - Bağımsız Test Modu")
    print("="*60)
    
    # Test fonksiyonunu çalıştır
    test_result = test_yescaptcha_solver()
    
    print(f"\n🏁 Test tamamlandı!")
    print(f"📋 Sonuç: {test_result}")
