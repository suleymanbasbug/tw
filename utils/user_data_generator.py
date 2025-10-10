"""
Kullanıcı Veri Üretici Modülü
Twitter hesap oluşturma için rastgele kullanıcı bilgileri üretir
"""

import random
from typing import Tuple

# İngilizce isim havuzları
FIRST_NAMES = [
    "John", "Michael", "David", "James", "Robert", "William", "Richard", "Thomas",
    "Christopher", "Daniel", "Matthew", "Anthony", "Mark", "Donald", "Steven",
    "Paul", "Andrew", "Joshua", "Kenneth", "Kevin", "Brian", "George", "Timothy",
    "Ronald", "Jason", "Edward", "Jeffrey", "Ryan", "Jacob", "Gary", "Nicholas",
    "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott", "Brandon",
    "Benjamin", "Samuel", "Gregory", "Alexander", "Patrick", "Jack", "Dennis",
    "Jerry", "Tyler", "Aaron", "Jose", "Henry", "Adam", "Douglas", "Nathan",
    "Peter", "Zachary", "Kyle", "Noah", "Alan", "Ethan", "Jeremy", "Christian",
    "Sean", "Bryan", "Austin", "Mason", "Carl", "Arthur", "Wayne", "Roy",
    "Eugene", "Louis", "Philip", "Bobby", "Johnny", "Terry", "Lawrence",
    "Jesse", "Albert", "Willie", "Ralph", "Joe", "Harold", "Gerald", "Keith",
    "Roger", "Arthur", "Juan", "Frank", "Raymond", "Ralph", "Eugene", "Wayne",
    "Louis", "Roy", "Carl", "Bobby", "Johnny", "Terry", "Lawrence", "Jesse",
    "Albert", "Willie", "Ralph", "Joe", "Harold", "Gerald", "Keith", "Roger"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
    "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill",
    "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell",
    "Mitchell", "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner",
    "Diaz", "Parker", "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris",
    "Morales", "Murphy", "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan",
    "Cooper", "Peterson", "Bailey", "Reed", "Kelly", "Howard", "Ramos", "Kim",
    "Cox", "Ward", "Richardson", "Watson", "Brooks", "Chavez", "Wood", "James",
    "Bennett", "Gray", "Mendoza", "Ruiz", "Hughes", "Price", "Alvarez", "Castillo",
    "Sanders", "Patel", "Myers", "Long", "Ross", "Foster", "Jimenez", "Powell",
    "Jenkins", "Perry", "Russell", "Sullivan", "Bell", "Coleman", "Butler",
    "Henderson", "Barnes", "Gonzales", "Fisher", "Vasquez", "Simmons", "Romero",
    "Jordan", "Patterson", "Alexander", "Hamilton", "Graham", "Reynolds", "Griffin",
    "Wallace", "Moreno", "West", "Cole", "Hayes", "Bryant", "Herrera", "Gibson",
    "Ellis", "Tran", "Medina", "Aguilar", "Stevens", "Murray", "Ford", "Castro",
    "Marshall", "Owens", "Harrison", "Fernandez", "McDonald", "Woods", "Washington",
    "Kennedy", "Wells", "Vargas", "Henry", "Chen", "Freeman", "Webb", "Tucker",
    "Guzman", "Burns", "Crawford", "Olson", "Simpson", "Porter", "Hunter",
    "Gordon", "Mendez", "Silva", "Shaw", "Snyder", "Mason", "Dixon", "Munoz",
    "Hunt", "Hicks", "Holmes", "Palmer", "Wagner", "Black", "Robertson", "Boyd",
    "Rose", "Stone", "Salazar", "Fox", "Warren", "Mills", "Meyer", "Rice",
    "Schmidt", "Garza", "Daniels", "Ferguson", "Nichols", "Stephens", "Soto",
    "Weaver", "Ryan", "Gardner", "Payne", "Grant", "Dunn", "Kelley", "Spencer",
    "Hawkins", "Arnold", "Pierce", "Vazquez", "Hansen", "Peters", "Santos",
    "Hart", "Bradley", "Knight", "Elliott", "Cunningham", "Duncan", "Armstrong",
    "Hudson", "Carroll", "Lane", "Riley", "Andrews", "Alvarado", "Ray", "Delgado",
    "Berry", "Perkins", "Hoffman", "Johnston", "Matthews", "Pena", "Richards",
    "Contreras", "Willis", "Carpenter", "Lawrence", "Sandoval", "Guerrero",
    "George", "Chapman", "Rios", "Estrada", "Ortega", "Watkins", "Greene",
    "Nunez", "Wheeler", "Valdez", "Harper", "Burke", "Larson", "Santiago",
    "Maldonado", "Morrison", "Franklin", "Carlson", "Austin", "Dominguez",
    "Carr", "Lawson", "Jacobs", "Obrien", "Lynch", "Singh", "Vega", "Blake",
    "Malone", "Summers", "Francis", "Atkins", "Ramsey", "Mccarthy", "Lynch",
    "Briggs", "Sharp", "Conway", "Tyler", "Logan", "Bowers", "Mueller", "Glover",
    "Floyd", "Hartman", "Buchanan", "Cody", "Burgess", "Swanson", "Schneider",
    "Maxwell", "Jenkins", "Tyler", "Logan", "Bowers", "Mueller", "Glover",
    "Floyd", "Hartman", "Buchanan", "Cody", "Burgess", "Swanson", "Schneider",
    "Maxwell", "Jenkins", "Tyler", "Logan", "Bowers", "Mueller", "Glover"
]

# Ay isimleri
MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

def get_random_name() -> str:
    """
    Rastgele bir isim üretir
    
    Returns:
        str: Rastgele seçilmiş tam isim (Ad Soyad)
    """
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    return f"{first_name} {last_name}"

def get_random_birthdate() -> Tuple[str, str, str]:
    """
    Rastgele bir doğum tarihi üretir (1980-2000 arası)
    
    Returns:
        Tuple[str, str, str]: (ay, gün, yıl) formatında doğum tarihi
    """
    # Yıl: 1980-2000 arası
    year = random.randint(1980, 2000)
    
    # Ay: 1-12 arası
    month_num = random.randint(1, 12)
    month_name = MONTHS[month_num - 1]
    
    # Gün: Ay'a göre uygun aralıkta
    if month_num in [1, 3, 5, 7, 8, 10, 12]:  # 31 günlük aylar
        day = random.randint(1, 31)
    elif month_num in [4, 6, 9, 11]:  # 30 günlük aylar
        day = random.randint(1, 30)
    else:  # Şubat
        # Basit yaklaşım: 28 gün (artık yıl kontrolü yapmıyoruz)
        day = random.randint(1, 28)
    
    return month_name, str(day), str(year)

def get_random_user_info() -> dict:
    """
    Tam kullanıcı bilgileri üretir
    
    Returns:
        dict: İsim ve doğum tarihi bilgilerini içeren sözlük
    """
    name = get_random_name()
    month, day, year = get_random_birthdate()
    
    return {
        "name": name,
        "birth_month": month,
        "birth_day": day,
        "birth_year": year
    }

# Test fonksiyonu
if __name__ == "__main__":
    print("=== Rastgele Kullanıcı Bilgileri Testi ===")
    
    for i in range(5):
        user_info = get_random_user_info()
        print(f"\n{i+1}. Kullanıcı:")
        print(f"   İsim: {user_info['name']}")
        print(f"   Doğum Tarihi: {user_info['birth_month']} {user_info['birth_day']}, {user_info['birth_year']}")
