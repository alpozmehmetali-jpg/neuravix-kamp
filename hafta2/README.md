# Görev Noktası Okuyucu (2. Hafta Projesi)

Bu proje, şartnamedeki görev kombinasyonlarından (`kombinasyon_001.geojson`) alınan `gorevler.geojson` dosyasındaki GPS görev noktalarını okuyarak nesne tabanlı (OOP) bir yapıda tutar ve Haversine formülü kullanarak ardışık noktalar arasındaki mesafeler ile toplam rota uzunluğunu metre cinsinden hesaplar[cite: 6, 11].

## Gereksinimler
- Python 3.12 (Harici kütüphane gerektirmez; standart `json` ve `math` modülleri kullanılır[cite: 6].)

## Çalıştırma
Terminalde `hafta2/` klasörünün içine girerek aşağıdaki komutu çalıştırın:

```bash
python3 main.py