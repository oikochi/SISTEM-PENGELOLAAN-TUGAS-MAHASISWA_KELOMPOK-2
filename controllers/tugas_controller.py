from datetime import datetime, date
from models.tugas_model import TugasModel

STATUS_TUGAS = ["Belum Dikerjakan", "Sedang Dikerjakan", "Selesai"]


class TugasController:
    def __init__(self):
        self.model = TugasModel()

    def _parse_tanggal(self, teks):
        for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(teks, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
        return None

    def _validasi(self, nama, mata_kuliah, tenggat, status):
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

    def tambah(self, nama, mata_kuliah, deskripsi, tenggat, status):
        pesan_error, tenggat_iso = self._validasi(nama, mata_kuliah, tenggat, status)
        if pesan_error:
            return False, pesan_error
        self.model.tambah_tugas(nama, mata_kuliah, deskripsi, tenggat_iso, status)
        return True, "Tugas berhasil ditambahkan."

    def edit(self, id_tugas, nama, mata_kuliah, deskripsi, tenggat, status):
        pesan_error, tenggat_iso = self._validasi(nama, mata_kuliah, tenggat, status)
        if pesan_error:
            return False, pesan_error
        berhasil = self.model.edit_tugas(id_tugas, nama, mata_kuliah, deskripsi, tenggat_iso, status)
        if not berhasil:
            return False, "Tugas tidak ditemukan."
        return True, "Perubahan tugas berhasil disimpan."

    def ubah_status(self, id_tugas, status_baru):
        if status_baru not in STATUS_TUGAS:
            return False, "Status tugas tidak valid."
        berhasil = self.model.ubah_status(id_tugas, status_baru)
        if not berhasil:
            return False, "Tugas tidak ditemukan."
        return True, "Status tugas berhasil diperbarui."

    def hapus(self, id_tugas):
        berhasil = self.model.hapus_tugas(id_tugas)
        if not berhasil:
            return False, "Tugas tidak ditemukan."
        return True, "Tugas berhasil dihapus."

    def _tandai(self, data):
        hari_ini = date.today()
        for nomor, baris in enumerate(data, start=1):
            baris["nomor"] = nomor
            tenggat = baris["tenggat"]
            if isinstance(tenggat, str):
                try:
                    tenggat = datetime.strptime(tenggat, "%Y-%m-%d").date()
                except ValueError:
                    tenggat = None
            baris["terlambat"] = bool(
                tenggat and tenggat < hari_ini and baris["status"] != "Selesai"
            )
        return data

    def tampilkan(self):
        data = self.model.tampilkan_tugas()
        return self._tandai(data)

    def cari(self, kata_kunci):
        if not kata_kunci:
            return self.tampilkan()
        data = self.model.cari_tugas(kata_kunci)
        return self._tandai(data)

    def ringkasan(self):
        data = self.model.tampilkan_tugas()
        total = len(data)
        selesai = sum(1 for d in data if d["status"] == "Selesai")
        return {"total": total, "selesai": selesai, "belum_selesai": total - selesai}