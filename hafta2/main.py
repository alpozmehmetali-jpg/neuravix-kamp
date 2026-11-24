import json
import math


class GorevNoktasi:
    def __init__(self, ad, aciklama, enlem, boylam):
        self.ad = ad
        self.aciklama = aciklama
        self.enlem = enlem
        self.boylam = boylam

    def __str__(self):
        return f"{self.ad} ({self.aciklama}) -> Enlem: {self.enlem}, Boylam: {self.boylam}"


def haversine(n1, n2):
    R = 6371000  # Dünya yarıçapı (metre)

    phi1 = math.radians(n1.enlem)
    phi2 = math.radians(n2.enlem)
    delta_phi = math.radians(n2.enlem - n1.enlem)
    delta_lambda = math.radians(n2.boylam - n1.boylam)

    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )
    d = 2 * R * math.asin(math.sqrt(a))
    return d


def gorevleri_yukle(dosya_yolu):
    try:
        with open(dosya_yolu, "r", encoding="utf-8") as dosya:
            veri = json.load(dosya)
    except FileNotFoundError:
        print(f"Hata: '{dosya_yolu}' dosyası bulunamadı. Dosya adını ve konumunu kontrol edin.")
        return []
    except json.JSONDecodeError:
        print(f"Hata: '{dosya_yolu}' geçerli bir JSON/GeoJSON formatında değil.")
        return []

    noktalar = []
    for ozellik in veri.get("features", []):
        ozellikler = ozellik.get("properties", {})
        geometri = ozellik.get("geometry", {})
        koordinatlar = geometri.get("coordinates", [])

        # Şartname dosyalarında 'name'/'description', örneklerde 'ad'/'aciklama' desteklenir
        ad = ozellikler.get("name") or ozellikler.get("ad") or "İsimsiz Nokta"
        aciklama = ozellikler.get("description") or ozellikler.get("aciklama") or "Açıklama yok"

        # Harita referans noktası (datum) rota mesafesine dahil edilmez
        if ad == "datum":
            continue

        if len(koordinatlar) >= 2:
            # GeoJSON formatında koordinat sırası [boylam, enlem] şeklindedir
            boylam = koordinatlar[0]
            enlem = koordinatlar[1]
            noktalar.append(GorevNoktasi(ad, aciklama, enlem, boylam))

    return noktalar


def main():
    dosya_adi = "gorevler.geojson"
    gorev_noktalari = gorevleri_yukle(dosya_adi)

    if not gorev_noktalari:
        return

    print("--- Görev Noktaları ---")
    for nokta in gorev_noktalari:
        print(nokta)

    print("\n--- Ardışık Noktalar Arası Mesafeler ---")
    toplam_mesafe = 0.0

    for i in range(len(gorev_noktalari) - 1):
        n1 = gorev_noktalari[i]
        n2 = gorev_noktalari[i + 1]
        mesafe = haversine(n1, n2)
        toplam_mesafe += mesafe
        print(f"{n1.ad} -> {n2.ad}: {mesafe:.2f} metre")

    print(f"\nToplam Rota Uzunluğu: {toplam_mesafe:.2f} metre")


if __name__ == "__main__":
    main()