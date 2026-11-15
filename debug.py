from controllers.pengguna_controller import PenggunaController
from config.database import DB_CONFIG, NAMA_DATABASE

print("Database yang dipakai aplikasi:", NAMA_DATABASE)
print("Host/port:", DB_CONFIG["host"], DB_CONFIG["port"])

pc = PenggunaController()
nim = "F5212530112"
sandi = "rpl2026"

data = pc.model.cari_dengan_nim(nim)
print("Data ditemukan:", data)

if data:
    hash_input = pc._hash(sandi)
    print("Hash dari sandi yang diketik :", hash_input)
    print("Hash yang tersimpan di DB    :", data["kata_sandi"])
    print("Cocok?", hash_input == data["kata_sandi"])
else:
    print("NIM tidak ditemukan sama sekali di database yang sedang dipakai aplikasi.")