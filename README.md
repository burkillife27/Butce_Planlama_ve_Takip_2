# 💰 Bütçe Planlama ve Takip Uygulaması

Modern, modüler ve katmanlı mimari (Layered Architecture) prensipleriyle geliştirilmiş kişisel bütçe planlama ve harcama takip uygulaması. 

Uygulama; gelir-gider yönetimi, kategori takibi ve aylık tasarruf oranı analizlerini hem **modern masaüstü görsel arayüzü (Flet GUI)** hem de **interaktif terminal konsolu (CLI)** üzerinden sunar.

---

## 🌟 Temel Özellikler

- **Katmanlı Mimari:** Veritabanı, iş mantığı (servisler) ve kullanıcı arayüzü tamamen birbirinden bağımsız modüller halinde inşa edilmiştir.
- **Çift Arayüz Desteği:**
  - 🖥️ **Flet GUI:** Flutter tabanlı, modern karanlık temalı (Dark Mode) masaüstü arayüzü.
  - ⌨️ **Terminal (CLI):** Hızlı, pratik ve doğrudan konsoldan çalışan menü arayüzü.
- **İlişkisel Veritabanı (SQLite):**
  - Otomatik tablo kurulumu ve başlangıç kategorileri yükleme.
  - `FOREIGN KEY` doğrulamaları ile veri bütünlüğü.
  - Dinamik yol yönetimi (`pathlib`) ile her işletim sisteminde (Windows/Mac/Linux) sorunsuz çalışma.
- **Finansal Analiz & Tasarruf Hesabı:**
  - Son 30 günün toplam gelir ve gider hesabı.
  - Net bakiye ve dinamik **Tasarruf Oranı (%)** hesaplama formülü:
    $$\text{Tasarruf Oranı} = \frac{\text{Gelir} - \text{Gider}}{\text{Gelir}} \times 100$$
- **Esnek Filtreleme:** Tüm işlemler, Son 1 Ay, Sadece Gelirler veya Sadece Giderler bazında anlık filtreleme.

---

## 📁 Proje Klasör Yapısı

```text
butce_takip/
│
├── docs/                               # Tasarım ve algoritma akış şemaları
│   └── algoritma ve tasarım.png
│
├── data/                               # SQLite veritabanı dizini
│   └── .gitkeep
│
├── src/                                # Kaynak kodlar
│   ├── database/                       # Veritabanı Katmanı
│   │   ├── connection.py               # Dinamik SQLite bağlantı yönetimi
│   │   └── schema.py                   # Tablo şemaları ve ilk kurulum
│   │
│   ├── services/                       # İş Mantığı Katmanı (GUI & CLI ortak kullanır)
│   │   ├── islem_service.py            # İşlem (Gelir/Gider) CRUD sorguları
│   │   ├── kategori_service.py         # Kategori CRUD sorguları
│   │   └── rapor_service.py            # Aylık finansal analiz ve tasarruf hesaplama
│   │
│   ├── cli/                            # Terminal Arayüzü (Aşama 1)
│   │   ├── ekran.py                    # Ekran temizleme ve konsol yardımcıları
│   │   └── menuler.py                  # Terminal menü akışı
│   │
│   └── gui/                            # Görsel Arayüz (Aşama 2 - Flet)
│       └── app.py                      # Modern masaüstü uygulaması
│
├── main.py                             # Ana giriş noktası (GUI veya CLI seçimi)
├── requirements.txt                    # Gerekli harici kütüphaneler
├── .gitignore                          # Git dışlama kuralları
└── README.md                           # Proje dokümantasyonu
```

---

## 🚀 Kurulum ve Çalıştırma

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/burkillife27/Butce_Planlama_ve_Takip_2.git
cd Butce_Planlama_ve_Takip_2
```

### 2. Gerekli Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### 3. Uygulamayı Başlatın
```bash
python main.py
```
*(Açılan konsol üzerinden `1` yazarak **Görsel Arayüzü (Flet GUI)** veya `2` yazarak **Terminal Arayüzünü** başlatabilirsiniz).*

---

## 🛠️ Kullanılan Teknolojiler

- **Programlama Dili:** Python 3.10+
- **Görsel Arayüz (GUI):** [Flet](https://flet.dev/) (Flutter for Python)
- **Veritabanı:** SQLite3 (İlişkisel Veritabanı)
- **Mimari:** Katmanlı Mimari (Separation of Concerns / N-Tier Architecture)

---

## 👨‍💻 Geliştirici

- **Geliştirici:** [burkillife27](https://github.com/burkillife27)
- **Lisans:** MIT
