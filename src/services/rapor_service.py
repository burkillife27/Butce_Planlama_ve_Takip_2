# Gelir, gider ve tasarruf orani hesaplamalari

from src.database.connection import baglanti_al

def aylik_ozet_getir():
    baglanti = baglanti_al()
    imlec = baglanti.cursor()

    imlec.execute("""
        SELECT SUM(miktar) FROM islemler
        WHERE tur = 1 AND tarih >= date('now', '-30 days')
    """)
    toplam_gelir = imlec.fetchone()[0] or 0.0

    imlec.execute("""
        SELECT SUM(miktar) FROM islemler
        WHERE tur = 0 AND tarih >= date('now', '-30 days')
    """)
    toplam_gider = imlec.fetchone()[0] or 0.0

    baglanti.close()

    net_durum = toplam_gelir - toplam_gider

    tasarruf_orani = 0.0
    if toplam_gelir > 0:
        tasarruf_orani = (net_durum / toplam_gelir)*100

    return {
        "toplam_gelir": toplam_gelir,
        "toplam_gider": toplam_gider,
        "net_durum": net_durum,
        "tasarruf_orani": round(tasarruf_orani, 2)
    }