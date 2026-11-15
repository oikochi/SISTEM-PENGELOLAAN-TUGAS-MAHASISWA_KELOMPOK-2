import mysql.connector
from contextlib import contextmanager

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "use_pure": True,
}

NAMA_DATABASE = "sitama"


def _pastikan_database():
    """Membuat database jika belum ada, agar aplikasi tetap bisa jalan
    walau skrip SQL belum dijalankan manual di phpMyAdmin."""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS {NAMA_DATABASE} "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )
    cursor.close()
    conn.close()


@contextmanager
def koneksi():
    _pastikan_database()
    conn = mysql.connector.connect(database=NAMA_DATABASE, **DB_CONFIG)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def init_db():
    with koneksi() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tugas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama_tugas VARCHAR(255) NOT NULL,
                mata_kuliah VARCHAR(255) NOT NULL,
                deskripsi TEXT NULL DEFAULT NULL,
                tenggat DATE NOT NULL,
                status ENUM('Belum Dikerjakan', 'Sedang Dikerjakan', 'Selesai')
                    NOT NULL DEFAULT 'Belum Dikerjakan'
            ) ENGINE=InnoDB
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pengguna (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nim VARCHAR(30) NOT NULL UNIQUE,
                nama VARCHAR(255) NOT NULL,
                kata_sandi VARCHAR(255) NOT NULL,
                pertanyaan_keamanan VARCHAR(255) NULL,
                jawaban_keamanan VARCHAR(255) NULL,
                dibuat_pada TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admin (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nim VARCHAR(30) NOT NULL UNIQUE,
                nama VARCHAR(255) NOT NULL,
                kata_sandi VARCHAR(255) NOT NULL,
                pertanyaan_keamanan VARCHAR(255) NULL,
                jawaban_keamanan VARCHAR(255) NULL,
                dibuat_pada TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB
        """)
        cursor.close()