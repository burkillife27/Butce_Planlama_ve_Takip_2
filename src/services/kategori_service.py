# Kategori CRUD islemleri
from src.database.connection import baglanti_al

def kategorileri_getir():
    baglanti = baglanti_al()
    imlec = baglanti.cursor()

    imlec.execute("SELECT*FROM kategoriler")

    kategoriler = imlec.fetchall()

    baglanti.close()

    return kategoriler

def kategori_ekle(kategori_adi):
    baglanti = baglanti_al()
    imlec = baglanti.cursor()

    imlec.execute("INSERT OR IGNORE INTO kategoriler (kategori_adi) VALUES (?)", (kategori_adi,))

    baglanti.commit()
    baglanti.close()