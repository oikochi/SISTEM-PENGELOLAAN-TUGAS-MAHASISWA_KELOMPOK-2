import os
import sqlite3
from contextlib import contextmanager

# tugas.db disimpan di folder utama proyek
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tugas.db")


@contextmanager
def koneksi():
    """Buka koneksi SQLite, commit bila sukses, rollback bila gagal, lalu selalu ditutup."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Buat tabel tugas sesuai Kamus Data (laporan bab 5.3)."""
    with koneksi() as conn:
        kolom = [r["name"] for r in conn.execute("PRAGMA table_info(tugas)")]
        # Bila ada tabel lama dengan struktur berbeda, simpan sebagai cadangan agar data tidak hilang
        if kolom and "nama_tugas" not in kolom:
            conn.execute("ALTER TABLE tugas RENAME TO tugas_lama")
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tugas (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_tugas  TEXT NOT NULL,
                mata_kuliah TEXT NOT NULL,
                deskripsi   TEXT DEFAULT NULL,
                tenggat     TEXT NOT NULL,
                status      TEXT NOT NULL
            )
            """
        )