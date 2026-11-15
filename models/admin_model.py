from config.database import koneksi, init_db


class AdminModel:
    def __init__(self):
        init_db()

    def tambah(self, nim, nama, kata_sandi_hash, pertanyaan=None, jawaban_hash=None):
        with koneksi() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO admin (nim, nama, kata_sandi, pertanyaan_keamanan, jawaban_keamanan) "
                "VALUES (%s, %s, %s, %s, %s)",
                (nim, nama, kata_sandi_hash, pertanyaan, jawaban_hash),
            )
            cursor.close()

    def cari_dengan_nim(self, nim):
        with koneksi() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM admin WHERE nim=%s", (nim,))
            hasil = cursor.fetchone()
            cursor.close()
            return hasil

    def tampilkan_semua(self):
        with koneksi() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT id, nim, nama, dibuat_pada FROM admin ORDER BY id")
            hasil = cursor.fetchall()
            cursor.close()
            return hasil

    def hapus(self, nim):
        with koneksi() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM admin WHERE nim=%s", (nim,))
            berhasil = cursor.rowcount > 0
            cursor.close()
            return berhasil

    def set_sandi(self, nim, kata_sandi_hash):
        with koneksi() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE admin SET kata_sandi=%s WHERE nim=%s", (kata_sandi_hash, nim))
            berhasil = cursor.rowcount > 0
            cursor.close()
            return berhasil

    def set_keamanan(self, nim, pertanyaan, jawaban_hash):
        with koneksi() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE admin SET pertanyaan_keamanan=%s, jawaban_keamanan=%s WHERE nim=%s",
                (pertanyaan, jawaban_hash, nim),
            )
            berhasil = cursor.rowcount > 0
            cursor.close()
            return berhasil