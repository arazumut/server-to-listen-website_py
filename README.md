  <a href="https://www.python.org" target="_blank" rel="noreferrer"> 
        <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> 
    </a> 
    <br>
Genel Bakış

Bu Python betiği, bir restoranın yemeklerini yönetmek ve bilgi sağlamak için API uç noktaları sunan basit bir HTTP sunucusu tanımlar. Betik, JSON dosyasından yemek verilerini okur, vejetaryen ve vegan filtreleri ile yemek listesini sağlar ve belirli bir yemeğin ID'si ile detaylarını getirir.
Ana Bileşenler

    Restaurant (Restoran) Sınıfı
        Başlatma: Yemek verilerini içeren JSON dosyasını (dataset_file) okur ve menu özelliğine yükler.
        Metodlar:
            list_meals: Vejetaryen ve vegan filtreleriyle tüm yemekleri listeler.
            get_meal: Bir yemeği ID'sine göre getirir.
            
            _is_meal_vegetarian: Bir yemeğin vejetaryen olup olmadığını kontrol eder.
            _is_meal_vegan: Bir yemeğin vegan olup olmadığını kontrol eder.
            _is_ingredient_vegetarian: Bir bileşenin vejetaryen olup olmadığını kontrol etmek için yer tutucu.
            _is_ingredient_vegan: Bir bileşenin vegan olup olmadığını kontrol etmek için yer tutucu.

    RequestHandler (İstek İşleyici) Sınıfı
        BaseHTTPRequestHandler sınıfından miras alarak HTTP isteklerini işler.
        Metodlar:
            _set_headers: Yanıtlar için HTTP başlıklarını ayarlar.
            do_GET: GET isteklerini işler. URL yolunu ve sorgu parametrelerini çözümleyerek uygun yanıtı belirler.
                /listMeals: Vejetaryen ve vegan kriterlerine göre yemekleri listeler.
                /getMeal: Bir yemeği ID'sine göre getirir.

    Sunucu Çalıştırma
        run fonksiyonu, HTTP sunucusunu 8000 portunda kurar ve başlatır.
        Betik, food.json verilerini kullanarak bir Restaurant nesnesi başlatır ve sunucuyu başlatır.

Restaurant Sınıfı

Başlatma (__init__ metodu):

    JSON dosyasından yemek verilerini okur.
    Dosya bulunamaması ve JSON çözümleme hatalarını işler.
    Beklenen örnek JSON yapısı:

    json

    [
        {
            "id": 1,
            "name": "Yemek İsmi",
            "ingredients": ["malzeme1", "malzeme2"]
        },
        ...
    ]

Yemekleri Listeleme (list_meals metodu):

    Vejetaryen ve vegan seçeneklerine göre yemekleri filtreler.
    Yemekleri filtrelemek için _is_meal_vegetarian ve _is_meal_vegan metodlarını kullanır.
    id, name ve ingredients bilgileriyle yemek listesini döner.

Yemek Getirme (get_meal metodu):

    Bir yemeği ID'sine göre arar.
    Bulunursa yemek detaylarını döner, aksi takdirde None döner.

Vejetaryen ve Vegan Kontrolleri:

    _is_meal_vegetarian ve _is_meal_vegan, bir yemekteki tüm malzemelerin vejetaryen veya vegan olup olmadığını kontrol eder.
    _is_ingredient_vegetarian ve _is_ingredient_vegan yer tutucuları her zaman True döner. Bu metodlar gerçek kontrollerle uygulanmalıdır.

RequestHandler Sınıfı

Başlıkları Ayarlama (_set_headers metodu):

    İçerik türü (JSON) ve CORS için HTTP yanıt başlıklarını ayarlar.

GET İsteklerini İşleme (do_GET metodu):

    URL ve sorgu parametrelerini çözümler.
    Yola bağlı olarak Restaurant sınıfının uygun metodunu çağırarak yanıt verilerini alır.
    Yol /listMeals ise, is_vegetarian ve is_vegan sorgu parametrelerini kontrol eder.
    Yol /getMeal ise, belirli bir yemeği getirmek için id parametresini alır.
    Yol tanınmaz veya yemek bulunmazsa 404 yanıtı gönderir.

Sunucu Çalıştırma

Sunucuyu Başlatma (run fonksiyonu):

    Sunucu adresini ve portunu (8000) ayarlar.
    HTTPServer sınıfını kullanarak HTTP sunucusunu başlatır.
    Gelen istekleri işlemek için sonsuz bir döngüye girer.

Zarif Kapatma:

    Klavye kesintilerini ele almaya çalışarak sunucuyu düzgün şekilde kapatır.(ctrl-c)

Öneriler

    Bileşen Kontrollerini Uygulama:
        _is_ingredient_vegetarian ve _is_ingredient_vegan metodlarını gerçek bileşen kontrolleriyle tamamlayın.

    Hata Yönetimi:
        Daha iyi hata ayıklama ve kullanıcı geri bildirimi için hata yönetimi ve günlük kaydını geliştirin.

    Birim Testleri:
        Restaurant sınıfı metodları için birim testleri yazarak işlevselliği garanti altına alın.

    Yapılandırma:
        Sunucu portu ve veri dosyasını komut satırı argümanları veya ortam değişkenleri aracılığıyla yapılandırılabilir hale getirin.

Bu önerileri takip ederek, betiği daha iyi işlevsellik, güvenilirlik ve bakım kolaylığı için geliştirebilirsiniz.


<h1>Aynı zamanda aynı python programının golang ile yazılması da mümkündür.
Aşağıda golang ile yazılmış aynı programın açılması yer almaktadır;</h1>

bir restoranın menüsünü yönetmek ve istemcilerin bu menüye erişimini sağlamak amacıyla geliştirilmiş olan Go dilinde yazılmış bir web uygulamasını açıklamaktadır. Uygulama, JSON formatında bir dosyadan menü verilerini yükler, çeşitli filtreleme seçenekleriyle yemekleri listeler ve belirli bir yemek hakkında ayrıntılı bilgi sağlar.
Genel Yapı

Uygulama iki ana veri yapısı üzerinde çalışır:

    Meal (Yemek): Bir yemeği temsil eder ve ID, Name, Ingredients (Malzemeler) gibi alanları içerir.
    Restaurant (Restoran): Bir restoranı temsil eder ve menüsündeki yemekleri Menu alanında tutar.

Fonksiyonlar ve İşlevleri

    LoadMenu: Bir JSON dosyasından menü verilerini yükler. Dosya bulunamazsa veya geçersizse hata döner.
    ListMeals: Belirtilen filtreleme seçeneklerine göre (vejetaryen ve vegan) menüdeki yemekleri listeler.
    GetMeal: Belirtilen ID'ye sahip yemeği döner.
    isMealVegetarian: Bir yemeğin vejetaryen olup olmadığını kontrol eder.
    isMealVegan: Bir yemeğin vegan olup olmadığını kontrol eder.
    isIngredientVegetarian: Bir malzemenin vejetaryen olup olmadığını kontrol eder (bu işlevin uygulanması gerekir).
    isIngredientVegan: Bir malzemenin vegan olup olmadığını kontrol eder (bu işlevin uygulanması gerekir).

HTTP Handler Fonksiyonları

    listMealsHandler: HTTP GET isteği ile gelen is_vegetarian ve is_vegan parametrelerine göre yemekleri listeler ve JSON formatında döner.
    getMealHandler: HTTP GET isteği ile gelen id parametresine göre belirtilen yemeği döner. Yemeğin bulunamaması durumunda 404 hatası döner.

Ana İşlev

main fonksiyonu şu işlemleri gerçekleştirir:

    dataset.json dosyasından menüyü yükler.
    listMeals ve getMeal HTTP handler fonksiyonlarını belirler.
    HTTP sunucusunu localhost:5500 adresinde başlatır.

Sonuç

Bu uygulama, bir restoranın menü yönetimini ve kullanıcıların menüye erişimini kolaylaştıran temel bir web sunucusu sağlar. JSON formatındaki bir dosyadan menü verilerini yükleyerek, çeşitli filtreleme seçenekleriyle yemekleri listeler ve belirli bir yemek hakkında bilgi verir. Uygulamanın genişletilebilmesi ve malzemelerin vejetaryen/vegan kontrolü için ek işlevler eklenmesi mümkündür.


![Ekran görüntüsü 2024-05-24 150618](https://github.com/arazumut/server-to-listen-website-backend/assets/150933483/873d1907-82e5-4574-9952-5cc7744eaa6d)
![Ekran görüntüsü 2024-05-24 150642](https://github.com/arazumut/server-to-listen-website-backend/assets/150933483/f73d3af2-f941-48f7-9b29-f4ccd33354d1)
![Ekran görüntüsü 2024-05-24 150653](https://github.com/arazumut/server-to-listen-website-backend/assets/150933483/a8d4b9e9-a948-4c10-b33e-bba9507533d9)
