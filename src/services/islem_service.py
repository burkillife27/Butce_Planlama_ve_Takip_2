# Islem (Gelir/Gider) CRUD islemleri
from src.database.connection import baglanti_al

def islem_ekle(tur, kategori_id, miktar, tarih, aciklama):
    baglanti = baglanti_al()
    imlec = baglanti.cursor()

    imlec.execute("""
    INSERT INTO islemler (tur, kategori_id, miktar, tarih, aciklama)
    VALUES (?, ?, ?, ?, ?)
""",(tur, kategori_id, miktar, tarih, aciklama))

    baglanti.commit()
    baglanti.close()

def islemleri_getir(filtre=None):
    sql = """
    SELECT
        islemler.id,
        islemler.tur,
        islemler.miktar,
        islemler.tarih,
        islemler.aciklama,
        kategoriler.kategori_adi
    FROM islemler
    JOIN kategoriler ON islemler.kategori_id = kategoriler.id
"""
    if filtre == "gelir":
        sql += " WHERE islemler.tur = 1"
    elif filtre == "gider":
        sql += " WHERE islemler.tur = 0"
    elif filtre == "son_1_ay":
        sql += " WHERE islemler.tarih >= date('now','-30 days')"

    sql += " ORDER BY islemler.tarih DESC, islemler.id DESC"

    baglanti = baglanti_al()
    imlec = baglanti.cursor()

    imlec.execute(sql)
    islemler = imlec.fetchall()

    baglanti.close()

    return islemler

def islem_sil(islem_id):
    baglanti = baglanti_al()
    imlec = baglanti.cursor()

    imlec.execute("DELETE FROM islemler WHERE id = ?", (islem_id,))

    baglanti.commit()
    baglanti.close()

def islem_guncelle(islem_id, tur, kategori_id, miktar, tarih, aciklama):
    baglanti = baglanti_al()
    imlec = baglanti.cursor()

    imlec.execute("""
    UPDATE islemler
    SET tur = ?, kategori_id = ?, miktar = ?, tarih = ?, aciklama = ?
    WHERE id = ?
    """, (tur, kategori_id, miktar, tarih, aciklama, islem_id))

    baglanti.commit()
    baglanti.close()