# Tablo semalari ve ilk kurulum
from src.database.connection import baglanti_al
def tablolari_olustur():
    baglanti = baglanti_al()
    imlec = baglanti.cursor()

    imlec.execute("""
            CREATE TABLE IF NOT EXISTS islemler(
            id INTEGER PRIMARY KEY,
            tur INTEGER NOT NULL CHECK (tur IN (0, 1)),
            kategori_id INTEGER NOT NULL,
            tarih TEXT NOT NULL DEFAULT CURRENT_DATE,
            miktar REAL NOT NULL,
            aciklama TEXT,
            FOREIGN KEY (kategori_id) REFERENCES kategoriler (id)
            )
        """)
        # Tür değeri 0 gider 1 gelir
    
        #Kategori tablosu
    imlec.execute("""
        CREATE TABLE IF NOT EXISTS kategoriler(
        id INTEGER PRIMARY KEY,
        kategori_adi TEXT NOT NULL UNIQUE
        )
    """)

    varsayılan_kategoriler = [
        ("Maaş",),
        ("Market",),
        ("Fatura",),
        ("Kira",),
        ("Eğlence",),
        ("Diğer",),
    ]

    imlec.executemany(
        "INSERT OR IGNORE INTO kategoriler (kategori_adi) VALUES (?)",
        varsayılan_kategoriler
    )

    baglanti.commit()
    baglanti.close()