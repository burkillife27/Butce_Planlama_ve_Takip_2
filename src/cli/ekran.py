# Terminal ekran temizleme ve yardimci konsol fonksiyonlari
import os

def ekrani_temizle():
    os.system("cls" if os.name == "nt" else "clear")

def baslik_yazdir(baslik):
    ekrani_temizle()
    print("="*45)
    print(f"            {baslik.upper()}")
    print("="*45)
    print()

def devam_icin_bekle():
    input("\nDevam etmek için [Enter] tuşuna basınız...")