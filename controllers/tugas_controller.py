import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from models.tugas_model import TugasModel

STATUS_TUGAS = ("Belum Dikerjakan", "Sedang Dikerjakan", "Selesai")  # BR-04


class TugasController:
    """Memvalidasi input (BR-01..BR-04) dan mengatur operasi ke Model.
    Setiap operasi mengembalikan (berhasil: bool, pesan: str)."""

    def __init__(self):
        self.model = TugasModel()

    # ---------------------------------------------------------- Helper
    @staticmethod
    def tampil_tanggal(iso):
        """YYYY-MM-DD (database) -> hh/bb/tttt (tampilan)."""
        try:
            return datetime.strptime(iso, "%Y-%m-%d").strftime("%d/%m/%Y")
        except (ValueError, TypeError):
            return iso or ""

    @staticmethod
    def _parse_tanggal(teks):
        """Terima hh/bb/tttt atau YYYY-MM-DD, kembalikan YYYY-MM-DD atau None."""
        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(teks, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return None

    def _validasi(self, nama, mata_kuliah, tenggat, status):
        """Return (pesan_error, tenggat_iso). Pesan sesuai laporan bab 5.4."""
        if not nama:
            return "Nama tugas wajib diisi.", None
        if not mata_kuliah:
            return "Mata kuliah wajib diisi.", None
        tenggat_iso = self._parse_tanggal(tenggat)
        if tenggat_iso is None:
            return "Format tanggal tidak valid.", None
        if status not in STATUS_TUGAS:
            return "Status tugas tidak valid.", None
        return None, tenggat_iso

    # ------------------------------------------------------- Operasi
    def tambah(self, nama, mata_kuliah, deskripsi, tenggat, status):
        nama, mata_kuliah, deskripsi, tenggat = (s.strip() for s in (nama, mata_kuliah, deskripsi, tenggat))
        error, iso = self._validasi(nama, mata_kuliah, tenggat, status)
        if error:
            return False, error
        try:
            self.model.tambah_tugas(nama, mata_kuliah, deskripsi, iso, status)
        except Exception as e:
            return False, f"Data gagal disimpan: {e}"
        return True, "Tugas berhasil ditambahkan."

    def edit(self, id_tugas, nama, mata_kuliah, deskripsi, tenggat, status):
        nama, mata_kuliah, deskripsi, tenggat = (s.strip() for s in (nama, mata_kuliah, deskripsi, tenggat))
        error, iso = self._validasi(nama, mata_kuliah, tenggat, status)
        if error:
            return False, error
        try:
            ok = self.model.edit_tugas(id_tugas, nama, mata_kuliah, deskripsi, iso, status)
        except Exception as e:
            return False, f"Data gagal diperbarui: {e}"
        return (True, "Perubahan tugas berhasil disimpan.") if ok else (False, "Tugas tidak ditemukan.")

    def ubah_status(self, id_tugas, status):
        if status not in STATUS_TUGAS:
            return False, "Status tugas tidak valid."
        ok = self.model.ubah_status(id_tugas, status)
        return (True, "Status tugas berhasil diperbarui.") if ok else (False, "Tugas tidak ditemukan.")

    def hapus(self, id_tugas):
        ok = self.model.hapus_tugas(id_tugas)
        return (True, "Tugas berhasil dihapus.") if ok else (False, "Tugas tidak ditemukan.")

    def tampilkan(self):
        """Semua tugas, diurutkan; 'no' = nomor urut tampilan (selalu 1..n tanpa bolong)."""
        data = self.model.tampilkan_tugas()
        for i, t in enumerate(data, start=1):
            t["no"] = i
        return data

    def cari(self, kata):
        """Cari berdasarkan nama tugas atau mata kuliah (FR-08)."""
        data = self.tampilkan()
        kata = (kata or "").strip().lower()
        if not kata:
            return data
        return [t for t in data
                if kata in t["nama_tugas"].lower() or kata in t["mata_kuliah"].lower()]

    def ringkasan(self):
        data = self.model.tampilkan_tugas()
        selesai = sum(1 for t in data if t["status"] == "Selesai")
        return {"total": len(data), "selesai": selesai, "belum": len(data) - selesai}