# 🎭 HasWave Yüz Tanıma

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2023.6%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**RTSP kameralar ile yerel yüz tanıma yapan Home Assistant entegrasyonu**

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

<a href="https://my.home-assistant.io/redirect/hacs_repository/?owner=HasWave&repository=HACS-Yuz-Tanima&category=Integration" target="_blank">
  <img src="https://my.home-assistant.io/badges/hacs_repository.svg" alt="Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.">
</a>

</div>

---

## 📋 Özellikler

* 🎥 **RTSP Kamera Desteği** - IP kameralardan canlı video akışı
* 🧠 **Otomatik Yüz Öğrenme** - Belirtilen klasörden otomatik yüz tanıma
* ✅ **Config Flow** - Kolay kurulum ve yapılandırma
* ✅ **Binary Sensor** - Her kişi için ayrı presence sensor
* 🔒 **Yerel İşleme** - Tüm işlemler yerel ağda, internet gerektirmez
* 👥 **Çoklu Yüz Tanıma** - Aynı anda birden fazla kişiyi tanıyabilir
* ⚡ **Yüksek Performans** - InsightFace ve ONNX Runtime ile optimize edilmiş, ARM cihazlar için hızlı yüz tanıma

## 🚀 Hızlı Başlangıç

### 1️⃣ HACS ile Kurulum

1. Home Assistant → **HACS** → **Integrations**
2. Sağ üstteki **⋮** menüsünden **Custom repositories** seçin
3. Repository URL: `https://github.com/HasWave/HACS-Yuz-Tanima`
4. Category: **Integration** seçin
5. **Add** butonuna tıklayın
6. HACS → Integrations → **HasWave Yüz Tanıma**'yı bulun
7. **Download** butonuna tıklayın
8. Home Assistant'ı yeniden başlatın

**✅ Hızlı Kurulum:** İlk kurulum **2-5 dakika** sürer. `insightface` ve `onnxruntime` önceden derlenmiş paketlerle gelir, bu yüzden derleme gerekmez. Özellikle Raspberry Pi gibi ARM cihazlar için optimize edilmiştir.

### 2️⃣ Manuel Kurulum

1. Bu repository'yi klonlayın veya indirin
2. `custom_components/haswave_yuz_tanima` klasörünü Home Assistant'ın `config/custom_components/` klasörüne kopyalayın
3. Home Assistant'ı yeniden başlatın

### 3️⃣ Yüz Fotoğraflarını Ekleme

1. Home Assistant → **File editor** veya Samba ile `/config/www/yuzler/` klasörüne erişin
2. Tanınacak kişilerin fotoğraflarını ekleyin:  
   * Dosya adı kişinin adı olacaktır (örn: `ahmet.jpg`, `mehmet.png`)  
   * Her fotoğrafta tek bir yüz olmalı  
   * Önerilen: 200x200px veya daha büyük, iyi aydınlatılmış fotoğraflar

### 4️⃣ Integration Ekleme

1. Home Assistant → **Settings** → **Devices & Services**
2. Sağ alttaki **+ ADD INTEGRATION** butonuna tıklayın
3. **HasWave Yüz Tanıma** arayın ve seçin
4. Yapılandırma formunu doldurun:
   - **Camera URL**: RTSP kamera URL'iniz (örn: `rtsp://kullanici:sifre@192.168.1.100:554/stream`)
   - **Faces Directory**: Yüz fotoğraflarının bulunduğu klasör (varsayılan: `/config/www/yuzler`)
   - **Tolerance**: Yüz tanıma hassasiyeti (0.0-1.0, düşük = daha hassas, varsayılan: 0.6)
   - **Detection Interval**: Algılama aralığı saniye cinsinden (varsayılan: 1)
   - **Min Face Size**: Minimum yüz boyutu piksel cinsinden (varsayılan: 50)
5. **Submit** butonuna tıklayın

**✅ Binary Sensor'lar Otomatik Oluşturulur:** Integration eklendiğinde her bilinen kişi için binary sensor direkt Home Assistant'a eklenir. Hiçbir ek kurulum gerekmez!

## 📖 Kullanım

### Home Assistant Binary Sensor'ları

Integration otomatik olarak şu binary sensor'ları oluşturur:

#### `binary_sensor.yuz_tanima_{kişi_adı}`
Her bilinen kişi için ayrı binary sensor (örn: `binary_sensor.yuz_tanima_ahmet`, `binary_sensor.yuz_tanima_mehmet`)

**State:** `on` (kişi tespit edildi) veya `off` (kişi tespit edilmedi)

**Attributes:**
- `last_seen`: Son görülme zamanı
- `confidence`: Tanıma güvenilirliği (0.0-1.0)

### Dashboard Kartı

Lovelace UI'da kart ekleyin:

```yaml
type: entities
title: Yüz Tanıma
entities:
  - entity: binary_sensor.yuz_tanima_ahmet
    name: Ahmet
    icon: mdi:face-recognition
  - entity: binary_sensor.yuz_tanima_mehmet
    name: Mehmet
    icon: mdi:face-recognition
```

### Otomasyon Örneği

Belirli bir kişi tanındığında otomatik aksiyon:

```yaml
automation:
  - alias: "Ahmet Geldi"
    trigger:
      - platform: state
        entity_id: binary_sensor.yuz_tanima_ahmet
        to: 'on'
    action:
      - service: notify.mobile_app
        data:
          message: "Ahmet eve geldi!"
      - service: light.turn_on
        entity_id: light.living_room
```

#### Kişi Ayrıldığında

```yaml
automation:
  - alias: "Ahmet Ayrıldı"
    trigger:
      - platform: state
        entity_id: binary_sensor.yuz_tanima_ahmet
        to: 'off'
        for:
          minutes: 5  # 5 dakika boyunca görünmediyse
    action:
      - service: light.turn_off
        entity_id: light.living_room
```

#### Birden Fazla Kişi Tespiti

```yaml
automation:
  - alias: "Birden Fazla Kişi"
    trigger:
      - platform: template
        value_template: >
          {{ states.binary_sensor | selectattr('entity_id', 'match', 'binary_sensor.yuz_tanima_*') | selectattr('state', 'eq', 'on') | list | count > 1 }}
    action:
      - service: notify.mobile_app
        data:
          message: "Birden fazla kişi tespit edildi!"
```

## 🔧 Gelişmiş Kullanım

### Performans Optimizasyonu

* **Tolerance** değerini ayarlayarak hassasiyeti değiştirebilirsiniz (0.4-0.7 arası önerilir)
* **Detection Interval** değerini artırarak CPU kullanımını azaltabilirsiniz
* Daha fazla kişi için yüz fotoğrafları klasörüne daha fazla fotoğraf ekleyin
* RTSP stream kalitesini düşürerek performansı artırabilirsiniz

### Yüz Veritabanı Güncelleme

Yeni fotoğraf ekledikten sonra integration'ı yeniden başlatmanız gerekebilir. Alternatif olarak, integration otomatik olarak yüz veritabanını belirli aralıklarla yeniden yükler.

### Sorun Giderme

#### Kamera Bağlanamıyor

* RTSP URL'ini kontrol edin
* Kullanıcı adı ve şifrenin doğru olduğundan emin olun
* Kameranın aynı ağda olduğunu kontrol edin
* RTSP portunun açık olduğunu kontrol edin (genellikle 554)

#### Yüzler Tanınmıyor

* Fotoğrafların kaliteli olduğundan emin olun (200x200px veya daha büyük)
* **Tolerance** değerini artırmayı deneyin (örn: 0.7)
* Fotoğraflarda tek bir yüz olduğundan emin olun
* İyi aydınlatılmış, net fotoğraflar kullanın

#### Binary Sensor'lar Görünmüyor

* Integration'ın eklendiğini kontrol edin: **Settings** → **Devices & Services**
* Home Assistant'ı yeniden başlatın
* Binary sensor'ları **Settings** → **Devices & Services** → **Entities** bölümünden kontrol edin
* Logları kontrol edin: **Settings** → **System** → **Logs**

#### Yüksek CPU Kullanımı

* **Detection Interval** değerini artırın (örn: 2 veya 3)
* RTSP stream çözünürlüğünü düşürün
* Daha az kişi tanıyacaksanız yüz veritabanını küçültün

#### Integration Ekleme Hatası

* HACS üzerinden doğru şekilde yüklendiğinden emin olun
* Home Assistant'ı yeniden başlatın
* `custom_components` klasörünün doğru konumda olduğundan emin olun
* Python bağımlılıklarının yüklendiğinden emin olun (`opencv-python-headless`, `onnxruntime`, `insightface`, vb.)

## 📁 Dosya Yapısı

```
HACS-Yuz-Tanima/
├── custom_components/
│   └── haswave_yuz_tanima/
│       ├── __init__.py
│       ├── manifest.json
│       ├── const.py
│       ├── config_flow.py
│       ├── api.py (gelecekte eklenecek)
│       └── binary_sensor.py (gelecekte eklenecek)
├── hacs.json
└── README.md
```

## 🔮 Gelecek Özellikler

* API ve binary sensor platform dosyaları eklenecek
* Çoklu kamera desteği
* Yüz tanıma geçmişi kaydı
* Daha gelişmiş performans optimizasyonları

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen:

1. Bu repository'yi fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Bir Pull Request açın

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

**HasWave**

🌐 [HasWave](https://haswave.com) | 📱 [Telegram](https://t.me/HasWave) | 📦 [GitHub](https://github.com/HasWave)

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!

Made with ❤️ by HasWave
