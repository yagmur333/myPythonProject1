import sqlite3

# Veritabanı bağlantısı
db = sqlite3.connect("notlar.sqlite")
cursor = db.cursor()

# Tabloyu oluştur (varsa atla)
cursor.execute("""
CREATE TABLE IF NOT EXISTS notlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    baslik TEXT NOT NULL,
    icerik TEXT NOT NULL
)
""")

db.commit()
db.close()
