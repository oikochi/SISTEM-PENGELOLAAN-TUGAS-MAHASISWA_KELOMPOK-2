import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.database import koneksi, init_db


class TugasModel:
    """Mengelola data tugas. Semua query memakai parameter (NFR-02)."""

    def __init__(self):
        init_db()

    def tambah_tugas(self, nama, mata_kuliah, deskripsi, tenggat, status):
        with koneksi() as conn:
            conn.execute(
                "INSERT INTO tugas (nama_tugas, mata_kuliah, deskripsi, tenggat, status) "
                "VALUES (?, ?, ?, ?, ?)",
                (nama, mata_kuliah, deskripsi or None, tenggat, status),
            )
        return True

    def tampilkan_tugas(self):
        with koneksi() as conn:
            baris = conn.execute("SELECT * FROM tugas ORDER BY id ASC").fetchall()
        return [dict(b) for b in baris]

    def edit_tugas(self, id_tugas, nama, mata_kuliah, deskripsi, tenggat, status):
        with koneksi() as conn:
            cur = conn.execute(
                "UPDATE tugas SET nama_tugas=?, mata_kuliah=?, deskripsi=?, tenggat=?, status=? "
                "WHERE id=?",
                (nama, mata_kuliah, deskripsi or None, tenggat, status, id_tugas),
            )
            return cur.rowcount > 0

    def ubah_status(self, id_tugas, status):
        with koneksi() as conn:
            cur = conn.execute("UPDATE tugas SET status=? WHERE id=?", (status, id_tugas))
            return cur.rowcount > 0

    def hapus_tugas(self, id_tugas):
        with koneksi() as conn:
            cur = conn.execute("DELETE FROM tugas WHERE id=?", (id_tugas,))
            return cur.rowcount > 0