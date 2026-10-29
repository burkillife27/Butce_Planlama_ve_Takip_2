"""
Bütçe Planlama ve Takip Uygulaması
Giriş Noktası (Entry Point)
"""

import sys
from pathlib import Path

# Proje ana dizinini Python yoluna ekle
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.database.schema import tablolari_olustur
from src.cli.menuler import ana_menu
from src.gui.app import baslat as gui_baslat

def main():
    # 1. Veritabanını ve tabloları otomatik hazırla
    tablolari_olustur()
    
    # 2. Kullanıcıya hangi arayüzü istediğini sor veya doğrudan GUI aç
    print("=" * 45)
    print("     BÜTÇE PLANLAMA VE TAKİP")
    print("=" * 45)
    print("1. Görsel Arayüz (Flet GUI - Masaüstü)")
    print("2. Terminal Arayüzü (Konsol)")
    print("=" * 45)
    
    secim = input("Lütfen seçim yapınız (1/2) [Varsayılan: 1]: ").strip()
    
    if secim == "2":
        ana_menu()
    else:
        print("\nGörsel arayüz başlatılıyor...\n")
        gui_baslat()

if __name__ == "__main__":
    main()
