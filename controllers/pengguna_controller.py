import hashlib
from models.pengguna_model import PenggunaModel
from models.admin_model import AdminModel


class PenggunaController:
    def __init__(self):
        self.model = PenggunaModel()
        self.model_admin = AdminModel()

    def _hash(self, teks):
        return hashlib.sha256(teks.encode()).hexdigest()

    def _cari_model(self, nim):
        if self.model.cari_dengan_nim(nim):
            return self.model
        if self.model_admin.cari_dengan_nim(nim):
            return self.model_admin
        return None

    def daftar(self, nim, nama, sandi, konfirmasi, pertanyaan, jawaban):
        if not nim or not nama or not sandi:
            return False, "NIM, nama, dan kata sandi wajib diisi."
        if sandi != konfirmasi:
            return False, "Konfirmasi kata sandi tidak cocok."
        if self.model.cari_dengan_nim(nim) or self.model_admin.cari_dengan_nim(nim):
            return False, "NIM sudah terdaftar."
        if not pertanyaan or not jawaban:
            return False, "Pertanyaan dan jawaban keamanan wajib diisi."
        self.model.tambah(nim, nama, self._hash(sandi), pertanyaan, self._hash(jawaban))
        return True, "Pendaftaran berhasil, silakan masuk."

    def masuk(self, nim, sandi):
        hash_sandi = self._hash(sandi)

        pengguna = self.model.cari_dengan_nim(nim)
        if pengguna and pengguna["kata_sandi"] == hash_sandi:
            pengguna["peran"] = "mahasiswa"
            return True, pengguna

        admin = self.model_admin.cari_dengan_nim(nim)
        if admin and admin["kata_sandi"] == hash_sandi:
            admin["peran"] = "admin"
            return True, admin

        return False, None

    def ambil_pertanyaan_keamanan(self, nim):
        model = self._cari_model(nim)
        if model is None:
            return False, "NIM tidak ditemukan."
        data = model.cari_dengan_nim(nim)
        if not data.get("pertanyaan_keamanan"):
            return False, "Akun ini belum memiliki pertanyaan keamanan. Silakan atur lewat menu Pengaturan Akun setelah login dengan sandi lama."
        return True, data["pertanyaan_keamanan"]

    def reset_sandi_mandiri(self, nim, jawaban, sandi_baru, konfirmasi):
        model = self._cari_model(nim)
        if model is None:
            return False, "NIM tidak ditemukan."
        data = model.cari_dengan_nim(nim)
        if not data.get("jawaban_keamanan") or data["jawaban_keamanan"] != self._hash(jawaban):
            return False, "Jawaban keamanan salah."
        if not sandi_baru or sandi_baru != konfirmasi:
            return False, "Konfirmasi kata sandi baru tidak cocok."
        model.set_sandi(nim, self._hash(sandi_baru))
        return True, "Kata sandi berhasil diperbarui, silakan masuk."

    def atur_keamanan(self, nim, pertanyaan, jawaban):
        if not jawaban:
            return False, "Jawaban keamanan wajib diisi."
        model = self._cari_model(nim)
        if model is None:
            return False, "NIM tidak ditemukan."
        model.set_keamanan(nim, pertanyaan, self._hash(jawaban))
        return True, "Pertanyaan keamanan berhasil disimpan."

    def daftar_mahasiswa(self):
        return self.model.tampilkan_semua()

    def daftar_admin(self):
        return self.model_admin.tampilkan_semua()

    def reset_sandi(self, nim, sandi_baru):
        model = self._cari_model(nim)
        if model is None:
            return False, "NIM tidak ditemukan."
        model.set_sandi(nim, self._hash(sandi_baru))
        return True, f"Sandi berhasil direset ke '{sandi_baru}'."

    def hapus_pengguna(self, nim):
        model = self._cari_model(nim)
        if model is None:
            return False, "NIM tidak ditemukan."
        berhasil = model.hapus(nim)
        return (True, "Akun berhasil dihapus.") if berhasil else (False, "Gagal menghapus akun.")