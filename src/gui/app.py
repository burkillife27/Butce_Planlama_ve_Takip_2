"""
Bütçe Planlama ve Takip - Flet GUI Arayüzü
"""

import sys
from pathlib import Path

# Proje ana dizinini Python yoluna ekle (her yerden hatasız çalışması için)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import flet as ft
from datetime import date

from src.database.schema import tablolari_olustur
from src.services.kategori_service import kategorileri_getir, kategori_ekle
from src.services.islem_service import islemleri_getir, islem_ekle, islem_sil
from src.services.rapor_service import aylik_ozet_getir


def main(page: ft.Page):
    tablolari_olustur()

    page.title = "Bütçe Planlama ve Takip"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # ==========================================
    # 1. BİLDİRİM / MESAJ YARDIMCISI
    # ==========================================
    durum_cubugu = ft.Container(
        content=ft.Text("", size=14, weight=ft.FontWeight.W_500),
        padding=12,
        border_radius=8,
        visible=False,
    )

    def mesaj_goster(metin: str, basarili: bool = True):
        durum_cubugu.content.value = metin
        durum_cubugu.bgcolor = ft.Colors.GREEN_700 if basarili else ft.Colors.RED_700
        durum_cubugu.visible = True
        page.update()

    # ==========================================
    # 2. SEKME 1: ÖZET / DASHBOARD
    # ==========================================
    kart_gelir = ft.Text("0.00 TL", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400)
    kart_gider = ft.Text("0.00 TL", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_400)
    kart_net = ft.Text("0.00 TL", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_400)
    kart_tasarruf = ft.Text("%0.0", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_400)
    durum_mesaji = ft.Text("", size=14, italic=True)

    def ozet_guncelle():
        ozet = aylik_ozet_getir()
        kart_gelir.value = f"{ozet['toplam_gelir']:.2f} TL"
        kart_gider.value = f"{ozet['toplam_gider']:.2f} TL"
        kart_net.value = f"{ozet['net_durum']:.2f} TL"
        kart_tasarruf.value = f"%{ozet['tasarruf_orani']}"

        if ozet["tasarruf_orani"] >= 20:
            durum_mesaji.value = "🎉 Harika! Bütçenizi çok sağlıklı yönetiyorsunuz."
            durum_mesaji.color = ft.Colors.GREEN_400
        elif ozet["tasarruf_orani"] > 0:
            durum_mesaji.value = "💡 Tasarruf yapıyorsunuz, giderleri biraz daha optimize edebilirsiniz."
            durum_mesaji.color = ft.Colors.AMBER_400
        else:
            durum_mesaji.value = "⚠️ Dikkat: Harcamalarınız gelirlerinize denk veya geçmiş!"
            durum_mesaji.color = ft.Colors.RED_400

    def kart_olustur(baslik: str, deger_bileseni: ft.Control, ikon):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ikon, size=24, color=ft.Colors.WHITE_70),
                            ft.Text(baslik, size=15, color=ft.Colors.WHITE_70),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    deger_bileseni,
                ],
                spacing=8,
            ),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            border_radius=12,
            padding=18,
            expand=True,
        )

    ozet_sekmesi = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text("Aylık Finansal Özet (Son 30 Gün)", size=20, weight=ft.FontWeight.BOLD),
                    ft.IconButton(
                        icon=ft.Icons.REFRESH,
                        tooltip="Yenile",
                        on_click=lambda e: (ozet_guncelle(), page.update()),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(),
            ft.Row(
                controls=[
                    kart_olustur("Toplam Gelir", kart_gelir, ft.Icons.ARROW_UPWARD),
                    kart_olustur("Toplam Gider", kart_gider, ft.Icons.ARROW_DOWNWARD),
                    kart_olustur("Net Durum", kart_net, ft.Icons.ACCOUNT_BALANCE_WALLET),
                    kart_olustur("Tasarruf Oranı", kart_tasarruf, ft.Icons.SAVINGS),
                ],
                spacing=12,
            ),
            ft.Container(content=durum_mesaji, padding=ft.Padding.only(top=10)),
        ],
        spacing=15,
    )

    # ==========================================
    # 3. SEKME 2: İŞLEMLER (GELİR / GİDER)
    # ==========================================
    dd_tur = ft.Dropdown(
        label="İşlem Türü",
        width=160,
        options=[
            ft.DropdownOption(key="0", text="Gider"),
            ft.DropdownOption(key="1", text="Gelir"),
        ],
        value="0",
    )

    dd_kategori = ft.Dropdown(label="Kategori", width=220)

    def kategorileri_yukle():
        kategoriler = kategorileri_getir()
        dd_kategori.options = [
            ft.DropdownOption(key=str(k["id"]), text=k["kategori_adi"]) for k in kategoriler
        ]
        if dd_kategori.options:
            dd_kategori.value = dd_kategori.options[0].key

    txt_miktar = ft.TextField(label="Miktar (TL)", width=150, keyboard_type=ft.KeyboardType.NUMBER)
    txt_tarih = ft.TextField(label="Tarih", value=date.today().isoformat(), width=150)
    txt_aciklama = ft.TextField(label="Açıklama (Örn: Market)", expand=True)

    tablo_islemler = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Tarih")),
            ft.DataColumn(ft.Text("Tür")),
            ft.DataColumn(ft.Text("Kategori")),
            ft.DataColumn(ft.Text("Miktar")),
            ft.DataColumn(ft.Text("Açıklama")),
            ft.DataColumn(ft.Text("İşlem")),
        ],
        rows=[],
    )

    dd_filtre = ft.Dropdown(
        label="Filtrele",
        width=200,
        options=[
            ft.DropdownOption(key="hepsi", text="Tüm İşlemler"),
            ft.DropdownOption(key="son_1_ay", text="Son 1 Ay"),
            ft.DropdownOption(key="gelir", text="Sadece Gelirler"),
            ft.DropdownOption(key="gider", text="Sadece Giderler"),
        ],
        value="hepsi",
    )

    def islemleri_tabloya_doldur():
        secilen_filtre = None if dd_filtre.value == "hepsi" else dd_filtre.value
        islemler = islemleri_getir(secilen_filtre)
        tablo_islemler.rows.clear()

        for islem in islemler:
            islem_id = islem["id"]
            tur_str = "Gelir" if islem["tur"] == 1 else "Gider"
            tur_renk = ft.Colors.GREEN_400 if islem["tur"] == 1 else ft.Colors.RED_400

            def silme_tiklandi(e, silinecek_id=islem_id):
                islem_sil(silinecek_id)
                mesaj_goster(f"{silinecek_id} numaralı işlem silindi.")
                islemleri_tabloya_doldur()
                ozet_guncelle()
                page.update()

            tablo_islemler.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(islem["id"]))),
                        ft.DataCell(ft.Text(islem["tarih"])),
                        ft.DataCell(ft.Text(tur_str, color=tur_renk, weight=ft.FontWeight.BOLD)),
                        ft.DataCell(ft.Text(islem["kategori_adi"])),
                        ft.DataCell(ft.Text(f"{islem['miktar']:.2f} TL")),
                        ft.DataCell(ft.Text(islem["aciklama"] or "-")),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_color=ft.Colors.RED_400,
                                tooltip="Sil",
                                on_click=silme_tiklandi,
                            )
                        ),
                    ]
                )
            )

    dd_filtre.on_select = lambda e: (islemleri_tabloya_doldur(), page.update())

    def yeni_islem_kaydet(e):
        try:
            miktar = float(txt_miktar.value.strip())
            if miktar <= 0:
                mesaj_goster("Miktar 0'dan büyük olmalıdır!", basarili=False)
                return
        except (ValueError, AttributeError):
            mesaj_goster("Lütfen geçerli bir sayısal miktar giriniz!", basarili=False)
            return

        if not dd_kategori.value:
            mesaj_goster("Lütfen bir kategori seçiniz!", basarili=False)
            return

        tur = int(dd_tur.value)
        kategori_id = int(dd_kategori.value)
        tarih = txt_tarih.value.strip() or date.today().isoformat()
        aciklama = txt_aciklama.value.strip()

        islem_ekle(tur, kategori_id, miktar, tarih, aciklama)
        mesaj_goster("İşlem başarıyla kaydedildi!")

        txt_miktar.value = ""
        txt_aciklama.value = ""
        islemleri_tabloya_doldur()
        ozet_guncelle()
        page.update()

    islemler_sekmesi = ft.Column(
        controls=[
            ft.Text("Yeni İşlem Ekle", size=18, weight=ft.FontWeight.BOLD),
            ft.Row(
                controls=[
                    dd_tur,
                    dd_kategori,
                    txt_miktar,
                    txt_tarih,
                ],
                wrap=True,
            ),
            ft.Row(
                controls=[
                    txt_aciklama,
                    ft.FilledButton(
                        content="Kaydet",
                        icon=ft.Icons.ADD,
                        on_click=yeni_islem_kaydet,
                        height=48,
                    ),
                ],
            ),
            ft.Divider(),
            ft.Row(
                controls=[
                    ft.Text("İşlem Geçmişi", size=18, weight=ft.FontWeight.BOLD),
                    dd_filtre,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Container(
                content=tablo_islemler,
                border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                border_radius=8,
                padding=10,
            ),
        ],
        spacing=15,
    )

    # ==========================================
    # 4. SEKME 3: KATEGORİLER
    # ==========================================
    txt_yeni_kategori = ft.TextField(label="Yeni Kategori Adı", expand=True)
    liste_kategoriler = ft.ListView(expand=True, spacing=8, height=350)

    def kategorileri_listeye_doldur():
        liste_kategoriler.controls.clear()
        kategoriler = kategorileri_getir()
        for kat in kategoriler:
            liste_kategoriler.controls.append(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.LABEL_OUTLINE, size=20, color=ft.Colors.PRIMARY),
                            ft.Text(f"[{kat['id']}] {kat['kategori_adi']}", size=15),
                        ],
                    ),
                    bgcolor=ft.Colors.SURFACE_CONTAINER,
                    padding=12,
                    border_radius=8,
                )
            )

    def yeni_kategori_kaydet(e):
        ad = txt_yeni_kategori.value.strip()
        if not ad:
            mesaj_goster("Kategori adı boş bırakılamaz!", basarili=False)
            return

        kategori_ekle(ad)
        mesaj_goster(f"'{ad}' kategorisi eklendi!")
        txt_yeni_kategori.value = ""
        kategorileri_yukle()
        kategorileri_listeye_doldur()
        page.update()

    kategoriler_sekmesi = ft.Column(
        controls=[
            ft.Text("Kategori Yönetimi", size=18, weight=ft.FontWeight.BOLD),
            ft.Row(
                controls=[
                    txt_yeni_kategori,
                    ft.FilledButton(
                        content="Kategori Ekle",
                        icon=ft.Icons.ADD,
                        on_click=yeni_kategori_kaydet,
                        height=48,
                    ),
                ],
            ),
            ft.Divider(),
            ft.Text("Mevcut Kategoriler", size=16, weight=ft.FontWeight.W_500),
            liste_kategoriler,
        ],
        spacing=15,
    )

    # ==========================================
    # 5. ÜST MENÜ VE İÇERİK ALANI
    # ==========================================
    icerik_alani = ft.Container(content=ozet_sekmesi, padding=15)

    def sekme_degistir(secim: str):
        durum_cubugu.visible = False
        if secim == "ozet":
            ozet_guncelle()
            icerik_alani.content = ozet_sekmesi
        elif secim == "islemler":
            islemleri_tabloya_doldur()
            icerik_alani.content = islemler_sekmesi
        elif secim == "kategoriler":
            kategorileri_listeye_doldur()
            icerik_alani.content = kategoriler_sekmesi
        page.update()

    ust_menu = ft.Row(
        controls=[
            ft.FilledButton(
                content="Özet Paneli",
                icon=ft.Icons.DASHBOARD,
                on_click=lambda e: sekme_degistir("ozet"),
            ),
            ft.FilledButton(
                content="İşlemler",
                icon=ft.Icons.RECEIPT_LONG,
                on_click=lambda e: sekme_degistir("islemler"),
            ),
            ft.FilledButton(
                content="Kategoriler",
                icon=ft.Icons.CATEGORY,
                on_click=lambda e: sekme_degistir("kategoriler"),
            ),
        ],
        spacing=10,
    )

    # Başlangıç verilerini yükle
    kategorileri_yukle()
    kategorileri_listeye_doldur()
    islemleri_tabloya_doldur()
    ozet_guncelle()

    page.add(
        ft.Text("Bütçe Planlama ve Takip", size=24, weight=ft.FontWeight.BOLD),
        ust_menu,
        durum_cubugu,
        ft.Divider(),
        icerik_alani,
    )


def baslat():
    ft.run(main)


if __name__ == "__main__":
    baslat()
