# Veritabani baglanti yonetimi

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR/"data"/"butce.db"

def baglanti_al():
    baglanti = sqlite3.connect(DB_PATH)
    baglanti.execute("PRAGMA foreign_keys = ON")
    baglanti.row_factory = sqlite3.Row
    return baglanti