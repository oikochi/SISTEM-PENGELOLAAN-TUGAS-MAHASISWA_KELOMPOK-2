from config.database import koneksi, init_db


class TugasModel:
    def __init__(self):
        init_db()

    def tambah_tugas(self, nama, mata_kuliah, deskripsi, tenggat, status):
        with koneksi() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tugas (nama_tugas, mata_kuliah, deskripsi, tenggat, status) "
                "VALUES (%s, %s, %s, %s, %s)",
                (nama, mata_kuliah, deskripsi or None, tenggat, status),
            )
            cursor.close()

    def tampilkan_tugas(self):
        with koneksi() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM tugas ORDER BY id")
            hasil = cursor.fetchall()
            cursor.close()
            return hasil

    def edit_tugas(self, id_tugas, nama, mata_kuliah, deskripsi, tenggat, status):
        with koneksi() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tugas SET nama_tugas=%s, mata_kuliah=%s, deskripsi=%s, "
                "tenggat=%s, status=%s WHERE id=%s",
                (nama, mata_kuliah, deskripsi or None, tenggat, status, id_tugas),
            )
            terpengaruh = cursor.rowcount
            cursor.close()
            return terpengaruh > 0

    def ubah_status(self, id_tugas, status_baru):
        with koneksi() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE tugas SET status=%s WHERE id=%s", (status_baru, id_tugas))
            terpengaruh = cursor.rowcount
            cursor.close()
            return terpengaruh > 0

    def hapus_tugas(self, id_tugas):
        with koneksi() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tugas WHERE id=%s", (id_tugas,))
            terpengaruh = cursor.rowcount
            cursor.close()
            return terpengaruh > 0

    def cari_tugas(self, kata_kunci):
        with koneksi() as conn:
            cursor = conn.cursor(dictionary=True)
            pola = f"%{kata_kunci}%"
            cursor.execute(
                "SELECT * FROM tugas WHERE nama_tugas LIKE %s OR mata_kuliah LIKE %s ORDER BY id",
                (pola, pola),
            )
            hasil = cursor.fetchall()
            cursor.close()
            return hasil