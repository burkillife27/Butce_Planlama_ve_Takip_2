# Terminal menuleri ve kullanici etkilesim akisi

from src.cli.ekran import baslik_yazdir, devam_icin_bekle
from src.services.kategori_service import kategori_ekle, kategorileri_getir
from src.services.islem_service import islemleri_getir, islem_ekle, islem_sil, islem_guncelle
from datetime import date
from src.services.rapor_service import aylik_ozet_getir

def kategori_ekle_menusu():
    baslik_yazdir("YENİ KATEGORİ EKLE")
    print("Geri dönmek için [Enter]'a basın\n")

    kategori_adi = input("Kategori Adı: ").strip()

    if not kategori_adi:
        return

    kategori_ekle(kategori_adi)
    print(f"\n'{kategori_adi}' kategorisi başarıyla eklendi!")
    devam_icin_bekle()

def islemleri_listele_menusu():
    baslik_yazdir("İŞLEMLERİ LİSTELE")
    print("1. Hepsini Listele")
    print("2. Son 1 Ayı Listele")
    print("3. Sadece Gelirleri Listele")
    print("4. Sadece Giderleri Listele")
    print("0. Ana Menüye Dön\n")

    secim = input("Seçiminiz: ").strip()

    if secim == "0":
        return
    elif secim == "1":
        filtre = None
    elif secim == "2":
        filtre = "son_1_ay"
    elif secim == "3":
        filtre = "gelir"
    elif secim == "4":
        filtre = "gider"
    else:
        print("\n Hatalı seçim yaptınız!")
        devam_icin_bekle()
        return

    islemler = islemleri_getir(filtre)

    if not islemler:
        print("\nKayıtlı işlem bulunamadı.")
        devam_icin_bekle()
        return

    print("\n" + "-"*70)
    print(f"{'ID':<4} {'Tarih':<12} {'Tür':<8} {'Kategori':<12} {'Miktar':<12} {'Açıklama'}")
    print("-" * 70)
    
    for islem in islemler:
        tur_metni = "Gelir" if islem["tur"] == 1 else "Gider"
        miktar_metni = f"{islem['miktar']:.2f} TL"
        print(f"{islem['id']:<4} {islem['tarih']:<12} {tur_metni:<8} {islem['kategori_adi']:<12} {miktar_metni:<12} {islem['aciklama'] or ''}")

    print("-" * 70)
    devam_icin_bekle()

def islem_ekle_menusu():
    baslik_yazdir("YENİ İŞLEM EKLE")
    print("Vazgeçmek için miktarı 0 olarak giriniz.")

    try:
        miktar = float(input("Miktar (TL): "))
        if miktar <= 0:
            return
    except ValueError:
        print("\n Lütfen geçerli bir sayı giriniz!")
        devam_icin_bekle()
        return

    tur_giris = input("Tür(1: Gelir, 0: Gider) [varsayılan: 0]: ").strip()
    tur = 1 if tur_giris == "1" else 0

    print("\nKategoriler:")
    kategoriler = kategorileri_getir()
    for kat in kategoriler:
        print(f"[{kat['id']}] {kat['kategori_adi']}")

    try:
        kategori_id = int(input("\nKategori Numarası: ").strip())
    except ValueError:
        print("\nGeçersiz kategori numarası!")
        devam_icin_bekle()
        return

    bugun = date.today().isoformat()
    tarih_giris = (input(f"Tarih (YYYY-AA-GG) [Varsayılan: {bugun}]")).strip()
    tarih = tarih_giris if tarih_giris else bugun

    aciklama = input("Açıklama: ").strip()

    islem_ekle(tur, kategori_id, miktar, tarih, aciklama)
    print("\nİşlem başarıyla kaydedildi!")
    devam_icin_bekle()

def islem_sil_menusu():
    baslik_yazdir("İŞLEM SİL")
    print("Vazgeçmek için işlme numarası kısmına 0 yazınız. \n")

    try:
        islem_id = int(input("Silinecek işlem numarası (ID): ").strip())
        if islem_id <= 0:
            return

    except ValueError:
        print("\n Geçersiz işlem numarası!")
        devam_icin_bekle()
        return

    onay = input(f"\n{islem_id} numaralı işlemi silmek istediğinize emin misiniz?(e/h): ").strip().lower()

    if onay == "e":
        islem_sil(islem_id)
        print("\nİşlem başarıyla silindi!")
    else:
        print("\nSilme işlemi iptal edildi!")

    devam_icin_bekle()

def islem_duzenle_menusu():
    baslik_yazdir("İŞLEM DÜZENLE")
    print("İpucu: Vazgeçmek için İşlem Numarası kısmına 0 yazın.\n")

    try:
        islem_id = int(input("Düzenlenecek İşlem Numarası (ID): ").strip())
        if islem_id <= 0:
            return
    except ValueError:
        print("\n Geçersiz işlem numarası!")
        devam_icin_bekle()
        return

    print(f"\n--- {islem_id} Numaralı İşlem İçin Yeni Bilgileri Giriniz ---")

    try:
        miktar = float(input("Yeni Miktar (TL): ").strip())
        if miktar <= 0:
            print("\n Miktar 0'dan büyük olmalıdır!")
            devam_icin_bekle()
            return
    except ValueError:
        print("\n Geçersiz miktar!")
        devam_icin_bekle()
        return

    tur_giris = input("Yeni Tür (1: Gelir, 0: Gider) [Varsayılan: 0]: ").strip()
    tur = 1 if tur_giris == "1" else 0

    print("\nKategoriler:")
    kategoriler = kategorileri_getir()
    for kat in kategoriler:
        print(f"[{kat['id']}] {kat['kategori_adi']}")

    try:
        kategori_id = int(input("\nYeni Kategori Numarası: ").strip())
    except ValueError:
        print("\n Geçersiz kategori numarası!")
        devam_icin_bekle()
        return

    bugun = date.today().isoformat()
    tarih_giris = input(f"Yeni Tarih (YYYY-AA-GG) [Varsayılan: {bugun}]: ").strip()
    tarih = tarih_giris if tarih_giris else bugun

    aciklama = input("Yeni Açıklama: ").strip()

    islem_guncelle(islem_id, tur, kategori_id, miktar, tarih, aciklama)
    print(f"\n {islem_id} numaralı işlem başarıyla güncellendi!")
    devam_icin_bekle()

def rapor_menusu():
    baslik_yazdir("AYLIK BÜTÇE VE TASARRUF RAPORU")
    print("Son 30 günün finansal analizi hazırlanıyor...\n")

    ozet = aylik_ozet_getir()

    print("=" * 45)
    print(f"Toplam Gelir   : {ozet['toplam_gelir']:.2f} TL")
    print(f"Toplam Gider   : {ozet['toplam_gider']:.2f} TL")
    print("-" * 45)
    print(f"Net Durum      : {ozet['net_durum']:.2f} TL")
    print(f"Tasarruf Oranı : %{ozet['tasarruf_orani']}")
    print("=" * 45)

    if ozet['tasarruf_orani'] >= 20:
        print("\n Tebrikler! Bütçenizi çok sağlıklı yönetiyorsunuz.")
    elif ozet['tasarruf_orani'] > 0:
        print("\nİyi gidiyorsunuz ama giderleri biraz daha kısabilirsiniz.")
    else:
        print("\n Dikkat: Harcamalarınız gelirlerinizi geçmiş veya başa baş!")

    devam_icin_bekle()

def ana_menu():
    while True:
        baslik_yazdir("BÜTÇE PLANLAMA VE TAKİP")
        print("1. İşlem Ekle")
        print("2. İşlemleri Listele")
        print("3. İşlem Düzenle")
        print("4. İşlem Sil")
        print("5. Gelir, Gider, Tasarruf Hesapla")
        print("6. Kategori Ekle")
        print("7. Çıkış\n")

        secim = input("Lütfen yapmak istediğiniz işlem numarasını giriniz: ").strip()

        if secim == "1":
            islem_ekle_menusu()
        elif secim == "2":
            islemleri_listele_menusu()
        elif secim == "3":
            islem_duzenle_menusu()
        elif secim == "4":
            islem_sil_menusu()
        elif secim == "5":
            rapor_menusu()
        elif secim == "6":
            kategori_ekle_menusu()
        elif secim == "7":
            print("\nUygulamadan çıkılıyor. İyi günler dileriz!\n")
            break
        else:
            print("\n Hatalı seçim yaptınız! Lütfen 1-7 arasında bir numara giriniz.")
            devam_icin_bekle()
