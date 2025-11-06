from sqlalchemy import text
from config.database import engine  # pastikan import engine sudah benar

# Nama tabel yang ingin dihapus
menu_orders = "menu_orders"

# Query untuk menghapus tabel
drop_query = text(f"DROP TABLE IF EXISTS {menu_orders};")

# Eksekusi query
with engine.connect() as connection:
    try:
        connection.execute(drop_query)
        connection.commit()
        print(f"✅ Tabel '{menu_orders}' berhasil dihapus dari database.")
    except Exception as e:
        print("❌ Terjadi error saat menghapus tabel:", e)
