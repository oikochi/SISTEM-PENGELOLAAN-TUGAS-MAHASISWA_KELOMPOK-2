"""
views/tugas_view.py
Tampilan SITAMA — gaya rounded card, label di atas input, tabel header biru muda lembut,
badge status kotak rata kiri, tombol aksi admin selalu terlihat (fixed bottom bar, rata kiri).
"""

import os
import webbrowser
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from datetime import date, datetime
from tkcalendar import DateEntry
from controllers.tugas_controller import TugasController, STATUS_TUGAS
from controllers.pengguna_controller import PenggunaController
from views import tema as t

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.png")

PERTANYAAN_KEAMANAN = [
    "Nama hewan peliharaan pertama Anda?",
    "Nama kota kelahiran Anda?",
    "Nama idola Anda?",
]

NOMOR_WA_ADMIN = "+6285179777840"  # nomor oiko sementara


def _hubungi_admin():
    pesan = "Halo Admin SITAMA, saya butuh bantuan terkait akun saya."
    url = f"https://wa.me/{NOMOR_WA_ADMIN}?text={pesan.replace(' ', '%20')}"
    webbrowser.open(url)


def _muat_logo(ukuran=(90, 100)):
    if os.path.exists(LOGO_PATH):
        return ctk.CTkImage(Image.open(LOGO_PATH), size=ukuran)
    return None


def _sapaan_waktu():
    jam = datetime.now().hour
    if 4 <= jam < 11:
        return "Selamat pagi"
    elif 11 <= jam < 15:
        return "Selamat siang"
    elif 15 <= jam < 18:
        return "Selamat sore"
    return "Selamat malam"


def _warna_badge_status(status, terlambat=False):
    """Warna solid untuk badge status (dipakai di tabel)."""
    if terlambat and status != "Selesai":
        return t.WARNA_BAHAYA
    return t.warna_status(status)


def _warna_baris_tugas(d, indeks):
    if d.get("terlambat") and d["status"] != "Selesai":
        return "#FDECEC"
    if d["status"] == "Selesai":
        return "#EDFAF4"
    return t.WARNA_KARTU


def _hitung_progress_tenggat(tenggat_str, status, terlambat=False):
    if status == "Selesai":
        return 1.0
    try:
        d_tenggat = datetime.strptime(str(tenggat_str), "%d/%m/%Y").date()
    except Exception:
        return 0.5
    sisa_hari = (d_tenggat - date.today()).days
    if sisa_hari < 0 or terlambat:
        return 1.0
    rentang_wajar = 14
    return max(0.05, min(0.95, (rentang_wajar - sisa_hari) / rentang_wajar))


def _kartu_tugas_progress(parent, data):
    kartu = ctk.CTkFrame(parent, fg_color=t.WARNA_KARTU, corner_radius=t.RADIUS,
                          width=300, height=150, border_width=1, border_color="#ECEEF5")
    kartu.pack_propagate(False)

    warna_badge_kat = t.warna_kategori(data["mata_kuliah"])
    terlambat_aktif = bool(data.get("terlambat")) and data["status"] != "Selesai"
    warna_stat = t.WARNA_BAHAYA if terlambat_aktif else t.warna_status(data["status"])
    progress = _hitung_progress_tenggat(data["tenggat"], data["status"], data.get("terlambat"))

    badge = ctk.CTkFrame(kartu, fg_color=warna_badge_kat, width=34, height=34, corner_radius=10)
    badge.place(x=16, y=16)
    ctk.CTkLabel(badge, text=(data["mata_kuliah"][:1] or "?").upper(), font=("Segoe UI", 14, "bold"),
                 text_color="white").place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(kartu, text=data["nama_tugas"], font=t.FONT_LABEL_TEBAL,
                 text_color=t.WARNA_TEKS, anchor="w", wraplength=210,
                 justify="left").place(x=60, y=14)
    ctk.CTkLabel(kartu, text=data["mata_kuliah"], font=t.FONT_KECIL,
                 text_color=t.WARNA_TEKS_SEKUNDER, anchor="w").place(x=60, y=40)

    isi = ctk.CTkFrame(kartu, fg_color="transparent")
    isi.pack(fill="x", padx=16, pady=(62, 12))

    baris = ctk.CTkFrame(isi, fg_color="transparent")
    baris.pack(fill="x")
    ctk.CTkLabel(baris, text="Status", font=t.FONT_KECIL,
                 text_color=t.WARNA_TEKS_SEKUNDER).pack(side="left")
    ctk.CTkLabel(baris, text=data["status"], font=("Segoe UI", 10, "bold"),
                 text_color=warna_stat).pack(side="right")

    bar = ctk.CTkProgressBar(isi, progress_color=warna_stat, fg_color=t.WARNA_ABU, height=8)
    bar.set(progress)
    bar.pack(fill="x", pady=(6, 6))

    ctk.CTkLabel(isi, text=f'Tenggat: {data["tenggat"]}', font=t.FONT_KECIL,
                 text_color=t.WARNA_TEKS_SEKUNDER, anchor="w").pack(fill="x")
    return kartu


def _tombol_sekunder(parent, text, command, width=160, height=38):
    return ctk.CTkButton(parent, text=text, command=command, width=width, height=height,
                          corner_radius=8, fg_color=t.WARNA_KARTU, hover_color=t.WARNA_ABU_HOVER,
                          text_color=t.WARNA_UTAMA, border_width=1.5, border_color=t.WARNA_UTAMA,
                          font=t.FONT_LABEL_TEBAL)


def _field_berlabel(parent, label, placeholder="", sembunyikan=False, lebar=None):
    wrapper = ctk.CTkFrame(parent, fg_color="transparent")
    ctk.CTkLabel(wrapper, text=label, font=t.FONT_LABEL,
                 text_color=t.WARNA_TEKS_SEKUNDER).pack(anchor="w", pady=(0, 4))
    entry = ctk.CTkEntry(wrapper, placeholder_text=placeholder, height=40, corner_radius=8,
                          width=lebar or t.LEBAR_INPUT, fg_color=t.WARNA_LATAR,
                          border_color=t.WARNA_ABU_HOVER, show="*" if sembunyikan else "")
    entry.pack(fill="x" if lebar is None else "none")
    return wrapper, entry


class TabelData(ctk.CTkFrame):
    """Tabel data custom — card putih rounded, header biru muda lembut dengan teks navy tebal,
    baris lega dipisah garis tipis, highlight biru saat baris diklik.
    Mendukung satu kolom opsional dirender sebagai badge kotak berwarna rata kiri (status)."""

    def __init__(self, parent, kolom, tinggi=None, on_pilih=None, kolom_badge=None):
        super().__init__(parent, fg_color=t.WARNA_KARTU, corner_radius=t.RADIUS,
                          border_width=1, border_color="#E7E9F0")
        self.kolom = kolom
        self.on_pilih = on_pilih
        self.kolom_badge = kolom_badge  # indeks kolom yang dirender sebagai badge
        self._baris = []
        self._idx_terpilih = None
        self._pesan_kosong = None  # referensi label "Belum ada data", agar ikut dibersihkan

        header = ctk.CTkFrame(self, fg_color="#E8F0FE", corner_radius=0, height=48)
        header.pack(fill="x")
        header.pack_propagate(False)
        for i, (judul, lebar, anchor) in enumerate(kolom):
            ctk.CTkLabel(header, text=judul, font=t.FONT_LABEL_TEBAL, text_color=t.WARNA_UTAMA,
                         width=lebar, anchor=anchor).pack(side="left", padx=(20, 6) if i == 0 else (6, 6))

        kwargs_body = {"fg_color": t.WARNA_KARTU, "corner_radius": 0,
                       "scrollbar_button_color": t.WARNA_ABU}
        if tinggi:
            kwargs_body["height"] = tinggi
        self.body = ctk.CTkScrollableFrame(self, **kwargs_body)
        self.body.pack(fill="both", expand=True)

    def kosongkan(self):
        for b in self._baris:
            b["frame"].destroy()
        self._baris.clear()
        self._idx_terpilih = None
        if self._pesan_kosong is not None:
            self._pesan_kosong.destroy()
            self._pesan_kosong = None

    def kosong_pesan(self, teks):
        self._pesan_kosong = ctk.CTkLabel(self.body, text=teks, font=t.FONT_LABEL,
                                           text_color=t.WARNA_TEKS_SEKUNDER)
        self._pesan_kosong.pack(pady=24)

    def tambah_baris(self, nilai, data=None, bg=None, warna_teks=None, warna_badge=None):
        """warna_badge: warna solid untuk kolom badge (dipakai hanya jika kolom_badge diset)."""
        idx = len(self._baris)
        latar = bg or t.WARNA_KARTU
        baris = ctk.CTkFrame(self.body, fg_color=latar, corner_radius=0, height=54)
        baris.pack(fill="x")
        baris.pack_propagate(False)

        garis = ctk.CTkFrame(self.body, fg_color="#EEF0F6", height=1)
        garis.pack(fill="x")

        widget_list = [baris]
        for i, ((judul, lebar, anchor), teks) in enumerate(zip(self.kolom, nilai)):
            if self.kolom_badge is not None and i == self.kolom_badge:
                # Sel badge: frame penampung lebar tetap, badge kotak rounded RATA KIRI
                sel = ctk.CTkFrame(baris, fg_color="transparent", width=lebar, height=54)
                sel.pack(side="left", padx=(6, 6))
                sel.pack_propagate(False)
                badge = ctk.CTkFrame(sel, fg_color=warna_badge or t.WARNA_TEKS_SEKUNDER,
                                      corner_radius=8, height=28)
                badge.place(relx=0, rely=0.5, anchor="w")
                lbl_badge = ctk.CTkLabel(badge, text=str(teks), font=("Segoe UI", 11, "bold"),
                                         text_color="white")
                lbl_badge.pack(padx=14, pady=4)
                widget_list.extend([sel, badge, lbl_badge])
            else:
                lbl = ctk.CTkLabel(baris, text=str(teks), font=t.FONT_LABEL,
                                   text_color=warna_teks or t.WARNA_TEKS,
                                   width=lebar, anchor=anchor)
                lbl.pack(side="left", padx=(20, 6) if i == 0 else (6, 6))
                widget_list.append(lbl)

        def _klik(event=None, i=idx):
            self._pilih(i)

        for w in widget_list:
            w.bind("<Button-1>", _klik)

        self._baris.append({"frame": baris, "data": data, "bg": latar})
        return idx

    def _pilih(self, idx):
        for i, b in enumerate(self._baris):
            b["frame"].configure(fg_color="#E3ECFF" if i == idx else b["bg"])
        self._idx_terpilih = idx
        if self.on_pilih:
            self.on_pilih(self._baris[idx]["data"])

    def data_terpilih(self):
        if self._idx_terpilih is None or self._idx_terpilih >= len(self._baris):
            return None
        return self._baris[self._idx_terpilih]["data"]


class TugasView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SITAMA — Sistem Pengelolaan Tugas Mahasiswa")
        self.geometry("1100x720")
        self.minsize(1000, 640)
        self.configure(fg_color=t.WARNA_LATAR)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        if os.path.exists(LOGO_PATH):
            try:
                from PIL import ImageTk
                self._icon_img = ImageTk.PhotoImage(Image.open(LOGO_PATH))
                self.iconphoto(False, self._icon_img)
            except Exception:
                pass

        self.controller = TugasController()
        self.controller_pengguna = PenggunaController()
        self.id_terpilih = None
        self.pengguna_aktif = None
        self.logo_kecil = _muat_logo((44, 50))
        self.logo_besar = _muat_logo((130, 140))

        self.halaman = {}
        for Halaman in (LoginPage, RegisterPage, ForgotPasswordPage, DashboardPage,
                         AdminDashboardPage, PantauTugasPage, KeamananPage, FormPage, DaftarPage):
            frame = Halaman(parent=self, controller=self.controller, view=self)
            self.halaman[Halaman.__name__] = frame
            frame.place(relwidth=1, relheight=1)

        self.tampil("LoginPage")

    def tampil(self, nama_halaman):
        frame = self.halaman[nama_halaman]
        if hasattr(frame, "muat_data"):
            frame.muat_data()
        frame.tkraise()


# ======================================================================
# HALAMAN AUTENTIKASI
# ======================================================================

class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller, view):
        super().__init__(parent, fg_color=t.WARNA_KARTU)
        self.view = view

        panel_kiri = ctk.CTkFrame(self, fg_color=t.WARNA_UTAMA, width=380, corner_radius=0)
        panel_kiri.pack(side="left", fill="both")
        panel_kiri.pack_propagate(False)

        # Logo + teks jadi satu blok, di-center vertikal bersama, jarak dirapatkan
        isi_kiri = ctk.CTkFrame(panel_kiri, fg_color="transparent")
        isi_kiri.place(relx=0.08, rely=0.5, anchor="w")

        if view.logo_besar:
            ctk.CTkLabel(isi_kiri, image=view.logo_besar, text="").pack(anchor="w", pady=(0, 18))

        ctk.CTkLabel(isi_kiri, text="SELAMAT DATANG", font=("Segoe UI", 11, "bold"),
                     text_color="#AAB4F5").pack(anchor="w", pady=(0, 8))
        ctk.CTkLabel(isi_kiri, text="Sistem Pengelolaan\nTugas Mahasiswa",
                     font=("Segoe UI", 26, "bold"), text_color="white",
                     justify="left").pack(anchor="w")
        ctk.CTkLabel(isi_kiri, text="Masuk untuk mencatat, memantau, dan\nmerapikan seluruh tugas kuliah.",
                     font=t.FONT_SUBJUDUL, text_color="#C4CBE8",
                     justify="left").pack(anchor="w", pady=(14, 0))

        panel_kanan = ctk.CTkFrame(self, fg_color=t.WARNA_LATAR, corner_radius=0)
        panel_kanan.pack(side="left", fill="both", expand=True)

        kartu = ctk.CTkFrame(panel_kanan, fg_color=t.WARNA_KARTU, corner_radius=t.RADIUS,
                              border_width=1, border_color="#E7E9F0", width=360)
        kartu.place(relx=0.5, rely=0.5, anchor="center")
        isi = ctk.CTkFrame(kartu, fg_color="transparent")
        isi.pack(padx=40, pady=36)

        ctk.CTkLabel(isi, text="Login", font=("Segoe UI", 22, "bold"),
                     text_color=t.WARNA_UTAMA).pack(anchor="w", pady=(0, 20))

        wrap_nim, self.input_nim = _field_berlabel(isi, "NIM", "Masukkan NIM")
        wrap_nim.pack(pady=(0, 14))

        wrap_sandi, self.input_sandi = _field_berlabel(isi, "Kata sandi", "Masukkan kata sandi",
                                                         sembunyikan=True)
        wrap_sandi.pack(pady=(0, 10))

        self.tampil_sandi = ctk.CTkCheckBox(isi, text="Tampilkan kata sandi",
                                             font=t.FONT_LABEL, text_color=t.WARNA_TEKS_SEKUNDER,
                                             checkbox_width=18, checkbox_height=18,
                                             command=self._toggle_sandi)
        self.tampil_sandi.pack(pady=(0, 20), anchor="w")

        ctk.CTkButton(isi, text="Masuk", width=t.LEBAR_INPUT, height=44, corner_radius=8,
                      fg_color=t.WARNA_AKSEN, hover_color=t.WARNA_AKSEN_HOVER,
                      font=t.FONT_LABEL_TEBAL, command=self._masuk).pack(pady=(0, 14))

        baris_bawah = ctk.CTkFrame(isi, fg_color="transparent")
        baris_bawah.pack()
        ctk.CTkButton(baris_bawah, text="Lupa kata sandi?", fg_color="transparent",
                      hover_color=t.WARNA_LATAR, text_color=t.WARNA_TEKS_SEKUNDER, font=t.FONT_LABEL,
                      command=lambda: self.view.tampil("ForgotPasswordPage")).pack(side="left", padx=4)
        ctk.CTkButton(baris_bawah, text="Daftar akun baru", fg_color="transparent",
                      hover_color=t.WARNA_LATAR, text_color=t.WARNA_AKSEN, font=t.FONT_LABEL,
                      command=self._ke_daftar).pack(side="left", padx=4)

        ctk.CTkButton(isi, text="💬 Butuh bantuan? Hubungi Admin", fg_color="transparent",
                      hover_color=t.WARNA_LATAR, text_color=t.WARNA_AKSEN, font=t.FONT_LABEL,
                      command=_hubungi_admin).pack(pady=(16, 0))

    def muat_data(self):
        self.input_nim.delete(0, "end")
        self.input_sandi.delete(0, "end")
        self.tampil_sandi.deselect()
        self.input_sandi.configure(show="*")

    def _toggle_sandi(self):
        self.input_sandi.configure(show="" if self.tampil_sandi.get() else "*")

    def _ke_daftar(self):
        self.view.tampil("RegisterPage")

    def _masuk(self):
        nim = self.input_nim.get().strip()
        sandi = self.input_sandi.get().strip()
        if not nim or not sandi:
            messagebox.showwarning("Peringatan", "NIM dan kata sandi wajib diisi.")
            return
        try:
            berhasil, pengguna = self.view.controller_pengguna.masuk(nim, sandi)
        except Exception as e:
            messagebox.showerror("Kesalahan", f"Gagal terhubung ke database:\n{e}")
            return
        if berhasil:
            self.view.pengguna_aktif = pengguna
            if pengguna.get("peran") == "admin":
                self.view.tampil("AdminDashboardPage")
            else:
                self.view.tampil("DashboardPage")
        else:
            messagebox.showerror("Gagal", "NIM atau kata sandi salah.")


class HalamanAuth(ctk.CTkFrame):
    def __init__(self, parent, lebar_panel_kiri=320):
        super().__init__(parent, fg_color=t.WARNA_KARTU)

        panel_kiri = ctk.CTkFrame(self, fg_color=t.WARNA_UTAMA, width=lebar_panel_kiri, corner_radius=0)
        panel_kiri.pack(side="left", fill="y")
        panel_kiri.pack_propagate(False)

        self.isi_kiri = ctk.CTkFrame(panel_kiri, fg_color="transparent")
        self.isi_kiri.place(relx=0.5, rely=0.5, anchor="center")

        panel_kanan = ctk.CTkFrame(self, fg_color=t.WARNA_LATAR, corner_radius=0)
        panel_kanan.pack(side="left", fill="both", expand=True)

        self.kartu = ctk.CTkFrame(panel_kanan, fg_color=t.WARNA_KARTU, corner_radius=t.RADIUS,
                                   border_width=1, border_color="#E7E9F0")
        self.kartu.place(relx=0.5, rely=0.5, anchor="center")

    def isi_branding(self, view, tagline):
        if view.logo_besar:
            ctk.CTkLabel(self.isi_kiri, image=view.logo_besar, text="").pack(pady=(0, 16))
        ctk.CTkLabel(self.isi_kiri, text="SITAMA", font=("Segoe UI", 26, "bold"),
                     text_color="white").pack()
        ctk.CTkLabel(self.isi_kiri, text=tagline, font=t.FONT_SUBJUDUL, text_color="#C4CBE8",
                     wraplength=220, justify="center").pack(pady=(8, 0))


class RegisterPage(HalamanAuth):
    def __init__(self, parent, controller, view):
        super().__init__(parent)
        self.view = view
        self.isi_branding(view, "Satu akun untuk mencatat semua tugas dan tenggat kuliahmu.")

        isi = ctk.CTkFrame(self.kartu, fg_color="transparent")
        isi.pack(padx=40, pady=32)

        ctk.CTkLabel(isi, text="Buat Akun Baru", font=t.FONT_JUDUL,
                     text_color=t.WARNA_UTAMA).pack(anchor="w", pady=(0, 18))

        wrap, self.input_nama = _field_berlabel(isi, "Nama lengkap", "Nama lengkap")
        wrap.pack(pady=(0, 10))
        wrap, self.input_nim = _field_berlabel(isi, "NIM", "NIM")
        wrap.pack(pady=(0, 10))
        wrap, self.input_sandi = _field_berlabel(isi, "Kata sandi", "Kata sandi", sembunyikan=True)
        wrap.pack(pady=(0, 10))
        wrap, self.input_konfirmasi = _field_berlabel(isi, "Konfirmasi kata sandi",
                                                        "Konfirmasi kata sandi", sembunyikan=True)
        wrap.pack(pady=(0, 10))

        ctk.CTkLabel(isi, text="Pertanyaan keamanan (untuk lupa sandi)",
                     font=t.FONT_LABEL, text_color=t.WARNA_TEKS_SEKUNDER).pack(pady=(6, 4), anchor="w")
        self.pilihan_pertanyaan = ctk.CTkOptionMenu(isi, values=PERTANYAAN_KEAMANAN,
                                                     width=t.LEBAR_INPUT, height=40, corner_radius=8,
                                                     fg_color=t.WARNA_UTAMA, button_color=t.WARNA_UTAMA_HOVER)
        self.pilihan_pertanyaan.pack(pady=(0, 10))
        wrap, self.input_jawaban = _field_berlabel(isi, "Jawaban keamanan", "Jawaban keamanan")
        wrap.pack(pady=(0, 10))

        ctk.CTkButton(isi, text="Daftar", width=t.LEBAR_INPUT, height=44, corner_radius=8,
                      fg_color=t.WARNA_AKSEN, hover_color=t.WARNA_AKSEN_HOVER,
                      font=t.FONT_LABEL_TEBAL, command=self._daftar).pack(pady=(16, 8))
        ctk.CTkButton(isi, text="Sudah punya akun? Masuk", fg_color="transparent",
                      hover_color=t.WARNA_LATAR, text_color=t.WARNA_UTAMA, font=t.FONT_LABEL,
                      command=lambda: self.view.tampil("LoginPage")).pack()

    def muat_data(self):
        for entry in (self.input_nama, self.input_nim, self.input_sandi,
                      self.input_konfirmasi, self.input_jawaban):
            entry.delete(0, "end")
        self.pilihan_pertanyaan.set(PERTANYAAN_KEAMANAN[0])

    def _daftar(self):
        nama = self.input_nama.get().strip()
        nim = self.input_nim.get().strip()
        sandi = self.input_sandi.get().strip()
        konfirmasi = self.input_konfirmasi.get().strip()
        pertanyaan = self.pilihan_pertanyaan.get()
        jawaban = self.input_jawaban.get().strip()
        try:
            berhasil, pesan = self.view.controller_pengguna.daftar(
                nim, nama, sandi, konfirmasi, pertanyaan, jawaban
            )
        except Exception as e:
            messagebox.showerror("Kesalahan", f"Gagal terhubung ke database:\n{e}")
            return
        if berhasil:
            messagebox.showinfo("Info", pesan)
            self.view.tampil("LoginPage")
        else:
            messagebox.showwarning("Peringatan", pesan)


class ForgotPasswordPage(HalamanAuth):
    def __init__(self, parent, controller, view):
        super().__init__(parent)
        self.view = view
        self.nim_aktif = None
        self.isi_branding(view, "Lupa sandi bisa terjadi. Jawab pertanyaan keamananmu untuk reset.")

        self.isi = ctk.CTkFrame(self.kartu, fg_color="transparent")
        self.isi.pack(padx=40, pady=32)

        ctk.CTkLabel(self.isi, text="Lupa Kata Sandi", font=t.FONT_JUDUL,
                     text_color=t.WARNA_UTAMA).pack(anchor="w", pady=(0, 18))

        wrap, self.input_nim = _field_berlabel(self.isi, "NIM", "NIM")
        wrap.pack(pady=(0, 10))

        ctk.CTkButton(self.isi, text="Cari Akun", width=t.LEBAR_TOMBOL, height=40, corner_radius=8,
                      fg_color=t.WARNA_UTAMA, hover_color=t.WARNA_UTAMA_HOVER,
                      font=t.FONT_LABEL_TEBAL, command=self._cari_akun).pack(pady=10)

        self.lbl_pertanyaan = ctk.CTkLabel(self.isi, text="", wraplength=280,
                                            font=t.FONT_LABEL, text_color=t.WARNA_TEKS_SEKUNDER)
        self.lbl_pertanyaan.pack(pady=(4, 4))

        self._wrap_jawaban, self.input_jawaban = _field_berlabel(self.isi, "Jawaban keamanan", "Jawaban keamanan")
        self._wrap_sandi, self.input_sandi_baru = _field_berlabel(self.isi, "Kata sandi baru",
                                                                     "Kata sandi baru", sembunyikan=True)
        self._wrap_konf, self.input_konfirmasi_baru = _field_berlabel(self.isi, "Konfirmasi kata sandi baru",
                                                                         "Konfirmasi kata sandi baru",
                                                                         sembunyikan=True)

        self.tombol_reset = ctk.CTkButton(self.isi, text="Reset Kata Sandi", width=t.LEBAR_TOMBOL,
                                           height=40, corner_radius=8,
                                           fg_color=t.WARNA_AKSEN, hover_color=t.WARNA_AKSEN_HOVER,
                                           font=t.FONT_LABEL_TEBAL, command=self._reset)

        ctk.CTkButton(self.isi, text="Kembali ke Login", fg_color="transparent",
                      hover_color=t.WARNA_LATAR, text_color=t.WARNA_UTAMA, font=t.FONT_LABEL,
                      command=lambda: self.view.tampil("LoginPage")).pack(pady=(14, 0))

        ctk.CTkButton(self.isi, text="💬 Butuh bantuan? Hubungi Admin", fg_color="transparent",
                      hover_color=t.WARNA_LATAR, text_color=t.WARNA_AKSEN, font=t.FONT_LABEL,
                      command=_hubungi_admin).pack(pady=(6, 0))

    def muat_data(self):
        self.nim_aktif = None
        self.input_nim.delete(0, "end")
        self.lbl_pertanyaan.configure(text="")
        self.input_jawaban.delete(0, "end")
        self.input_sandi_baru.delete(0, "end")
        self.input_konfirmasi_baru.delete(0, "end")
        for widget in (self._wrap_jawaban, self._wrap_sandi, self._wrap_konf, self.tombol_reset):
            widget.pack_forget()

    def _cari_akun(self):
        nim = self.input_nim.get().strip()
        if not nim:
            messagebox.showwarning("Peringatan", "NIM wajib diisi.")
            return
        try:
            berhasil, hasil = self.view.controller_pengguna.ambil_pertanyaan_keamanan(nim)
        except Exception as e:
            messagebox.showerror("Kesalahan", f"Gagal terhubung ke database:\n{e}")
            return
        if not berhasil:
            messagebox.showerror("Gagal", hasil)
            return
        self.nim_aktif = nim
        self.lbl_pertanyaan.configure(text=f"Pertanyaan: {hasil}")
        self._wrap_jawaban.pack(pady=5)
        self._wrap_sandi.pack(pady=5)
        self._wrap_konf.pack(pady=5)
        self.tombol_reset.pack(pady=12)

    def _reset(self):
        jawaban = self.input_jawaban.get().strip()
        sandi_baru = self.input_sandi_baru.get().strip()
        konfirmasi = self.input_konfirmasi_baru.get().strip()
        try:
            berhasil, pesan = self.view.controller_pengguna.reset_sandi_mandiri(
                self.nim_aktif, jawaban, sandi_baru, konfirmasi
            )
        except Exception as e:
            messagebox.showerror("Kesalahan", f"Gagal terhubung ke database:\n{e}")
            return
        if berhasil:
            messagebox.showinfo("Info", pesan)
            self.view.tampil("LoginPage")
        else:
            messagebox.showwarning("Peringatan", pesan)


class KeamananPage(ctk.CTkFrame):
    def __init__(self, parent, controller, view):
        super().__init__(parent, fg_color=t.WARNA_LATAR)
        self.view = view
        kartu = ctk.CTkFrame(self, fg_color=t.WARNA_KARTU, corner_radius=t.RADIUS,
                              border_width=1, border_color="#ECEEF5")
        kartu.place(relx=0.5, rely=0.5, anchor="center")
        isi = ctk.CTkFrame(kartu, fg_color="transparent")
        isi.pack(padx=40, pady=30)

        ctk.CTkLabel(isi, text="Atur Pertanyaan Keamanan", font=t.FONT_JUDUL,
                     text_color=t.WARNA_UTAMA).pack(anchor="w", pady=(0, 4))
        ctk.CTkLabel(isi, text="Dipakai untuk fitur Lupa Kata Sandi.",
                     font=t.FONT_LABEL, text_color=t.WARNA_TEKS_SEKUNDER).pack(anchor="w", pady=(0, 20))

        ctk.CTkLabel(isi, text="Pertanyaan", font=t.FONT_LABEL,
                     text_color=t.WARNA_TEKS_SEKUNDER).pack(anchor="w", pady=(0, 4))
        self.pilihan_pertanyaan = ctk.CTkOptionMenu(isi, values=PERTANYAAN_KEAMANAN,
                                                     width=t.LEBAR_INPUT, height=40, corner_radius=8,
                                                     fg_color=t.WARNA_UTAMA, button_color=t.WARNA_UTAMA_HOVER)
        self.pilihan_pertanyaan.pack(pady=(0, 10))

        wrap, self.input_jawaban = _field_berlabel(isi, "Jawaban keamanan", "Jawaban keamanan")
        wrap.pack(pady=(0, 10))

        ctk.CTkButton(isi, text="Simpan", width=t.LEBAR_TOMBOL, height=40, corner_radius=8,
                      fg_color=t.WARNA_AKSEN, hover_color=t.WARNA_AKSEN_HOVER,
                      font=t.FONT_LABEL_TEBAL, command=self._simpan).pack(pady=(16, 8))
        _tombol_sekunder(isi, "Kembali", self._kembali, width=t.LEBAR_TOMBOL, height=38).pack()

        ctk.CTkButton(isi, text="💬 Butuh bantuan? Hubungi Admin", fg_color="transparent",
                      hover_color=t.WARNA_LATAR, text_color=t.WARNA_AKSEN, font=t.FONT_LABEL,
                      command=_hubungi_admin).pack(pady=(14, 0))

    def muat_data(self):
        self.pilihan_pertanyaan.set(PERTANYAAN_KEAMANAN[0])
        self.input_jawaban.delete(0, "end")

    def _kembali(self):
        if self.view.pengguna_aktif and self.view.pengguna_aktif.get("peran") == "admin":
            self.view.tampil("AdminDashboardPage")
        else:
            self.view.tampil("DashboardPage")

    def _simpan(self):
        jawaban = self.input_jawaban.get().strip()
        pertanyaan = self.pilihan_pertanyaan.get()
        nim = self.view.pengguna_aktif["nim"]
        try:
            berhasil, pesan = self.view.controller_pengguna.atur_keamanan(nim, pertanyaan, jawaban)
        except Exception as e:
            messagebox.showerror("Kesalahan", f"Gagal terhubung ke database:\n{e}")
            return
        messagebox.showinfo("Info", pesan) if berhasil else messagebox.showwarning("Peringatan", pesan)
        if berhasil:
            self._kembali()


# ======================================================================
# BAGIAN BERSAMA (header bar, kartu statistik, bilah pencarian)
# ======================================================================

def _bilah_atas(parent, view, judul, dengan_keluar_fn):
    bilah = ctk.CTkFrame(parent, fg_color=t.WARNA_UTAMA, corner_radius=0, height=64)
    bilah.pack(fill="x", side="top")
    bilah.pack_propagate(False)

    kiri = ctk.CTkFrame(bilah, fg_color="transparent")
    kiri.pack(side="left", padx=20, pady=10)
    if view.logo_kecil:
        ctk.CTkLabel(kiri, image=view.logo_kecil, text="").pack(side="left", padx=(0, 10))
    lbl_judul = ctk.CTkLabel(kiri, text=judul, font=t.FONT_LABEL_TEBAL, text_color="white")
    lbl_judul.pack(side="left")

    ctk.CTkButton(bilah, text="Keluar", fg_color=t.WARNA_BAHAYA, hover_color=t.WARNA_BAHAYA_HOVER,
                  width=90, height=34, corner_radius=8, command=dengan_keluar_fn).pack(side="right", padx=20)
    return bilah, lbl_judul


def _kartu_statistik(parent, judul, warna_angka=None):
    frame = ctk.CTkFrame(parent, width=160, height=104, fg_color=t.WARNA_KARTU,
                          corner_radius=t.RADIUS, border_width=1, border_color="#ECEEF5")
    frame.pack(side="left", padx=8)
    frame.pack_propagate(False)
    ctk.CTkLabel(frame, text=judul, font=t.FONT_LABEL, text_color=t.WARNA_TEKS_SEKUNDER).pack(pady=(16, 0))
    lbl_angka = ctk.CTkLabel(frame, text="0", font=t.FONT_ANGKA,
                              text_color=warna_angka or t.WARNA_UTAMA)
    lbl_angka.pack(pady=(2, 10))
    return lbl_angka


def _bilah_cari(parent, placeholder, on_cari, on_reset):
    input_cari = ctk.CTkEntry(parent, placeholder_text=placeholder, width=220, height=36,
                               corner_radius=8, fg_color=t.WARNA_KARTU, border_color=t.WARNA_ABU_HOVER)
    input_cari.pack(side="right", padx=5)
    ctk.CTkButton(parent, text="Cari", width=70, height=36, corner_radius=8,
                  fg_color=t.WARNA_UTAMA, hover_color=t.WARNA_UTAMA_HOVER,
                  command=on_cari).pack(side="right")
    tombol_reset = _tombol_sekunder(parent, "↺ Tampilkan Semua", on_reset, width=150, height=32)
    return input_cari, tombol_reset


# ======================================================================
# DASHBOARD MAHASISWA
# ======================================================================

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller, view):
        super().__init__(parent, fg_color=t.WARNA_LATAR)
        self.controller = controller
        self.view = view

        _, self.lbl_sapaan = _bilah_atas(self, view, "Dashboard", self._keluar)

        self.lbl_subsapaan = ctk.CTkLabel(self, text=_sapaan_waktu(), font=t.FONT_LABEL,
                                           text_color=t.WARNA_TEKS_SEKUNDER)
        self.lbl_subsapaan.pack(pady=(10, 0))

        isi = ctk.CTkFrame(self, fg_color="transparent")
        isi.pack(pady=(6, 0))

        kartu = ctk.CTkFrame(isi, fg_color="transparent")
        kartu.pack(pady=10)
        self.lbl_total = _kartu_statistik(kartu, "Total Tugas")
        self.lbl_belum = _kartu_statistik(kartu, "Belum Selesai", warna_angka=t.WARNA_BAHAYA)
        self.lbl_selesai = _kartu_statistik(kartu, "Selesai", warna_angka=t.WARNA_SUKSES)

        tombol = ctk.CTkFrame(isi, fg_color="transparent")
        tombol.pack(pady=18)
        ctk.CTkButton(tombol, text="Formulir Tugas", width=190, height=40, corner_radius=8,
                      fg_color=t.WARNA_AKSEN, hover_color=t.WARNA_AKSEN_HOVER, font=t.FONT_LABEL_TEBAL,
                      command=lambda: self.view.tampil("FormPage")).grid(row=0, column=0, padx=8)
        ctk.CTkButton(tombol, text="Daftar Tugas", width=190, height=40, corner_radius=8,
                      fg_color=t.WARNA_UTAMA, hover_color=t.WARNA_UTAMA_HOVER, font=t.FONT_LABEL_TEBAL,
                      command=lambda: self.view.tampil("DaftarPage")).grid(row=0, column=1, padx=8)
        _tombol_sekunder(tombol, "Pengaturan Akun",
                         lambda: self.view.tampil("KeamananPage"), width=190).grid(row=0, column=2, padx=8)

        baris_judul = ctk.CTkFrame(self, fg_color="transparent")
        baris_judul.pack(fill="x", padx=40, pady=(4, 4))
        ctk.CTkLabel(baris_judul, text="Tugas Berjalan", font=t.FONT_LABEL_TEBAL,
                     text_color=t.WARNA_TEKS).pack(side="left")
        ctk.CTkButton(baris_judul, text="Lihat semua →", fg_color="transparent",
                      hover_color=t.WARNA_LATAR, text_color=t.WARNA_AKSEN, font=t.FONT_LABEL,
                      command=lambda: self.view.tampil("DaftarPage")).pack(side="right")

        self.frame_tugas_berjalan = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_tugas_berjalan.pack(fill="both", expand=True, padx=32, pady=(0, 16))
        self.frame_tugas_berjalan.grid_columnconfigure((0, 1), weight=1, uniform="kolom")

    def muat_data(self):
        if self.view.pengguna_aktif:
            self.lbl_sapaan.configure(text=f"Halo, {self.view.pengguna_aktif['nama']}")
        self.lbl_subsapaan.configure(text=_sapaan_waktu())

        ringkasan = self.controller.ringkasan()
        self.lbl_total.configure(text=str(ringkasan["total"]))
        self.lbl_belum.configure(text=str(ringkasan["belum_selesai"]))
        self.lbl_selesai.configure(text=str(ringkasan["selesai"]))

        for widget in self.frame_tugas_berjalan.winfo_children():
            widget.destroy()

        data = self.controller.tampilkan()
        belum_selesai = [d for d in data if d["status"] != "Selesai"]
        selesai = [d for d in data if d["status"] == "Selesai"]
        ditampilkan = (belum_selesai + selesai)[:4]

        if not ditampilkan:
            ctk.CTkLabel(self.frame_tugas_berjalan,
                         text="Belum ada tugas. Tambahkan lewat Formulir Tugas.",
                         font=t.FONT_LABEL, text_color=t.WARNA_TEKS_SEKUNDER).grid(
                row=0, column=0, columnspan=2, pady=20)
            return

        for i, tugas in enumerate(ditampilkan):
            kartu_tugas = _kartu_tugas_progress(self.frame_tugas_berjalan, tugas)
            kartu_tugas.grid(row=i // 2, column=i % 2, sticky="nsew", padx=8, pady=8)

    def _keluar(self):
        if messagebox.askyesno("Konfirmasi", "Keluar dari akun?"):
            self.view.pengguna_aktif = None
            self.view.tampil("LoginPage")


# ======================================================================
# DASHBOARD ADMIN — header tetap, tombol aksi tetap di bawah (rata kiri), tengah discroll
# ======================================================================

class AdminDashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller, view):
        super().__init__(parent, fg_color=t.WARNA_LATAR)
        self.controller = controller
        self.view = view

        _, self.lbl_sapaan = _bilah_atas(self, view, "Dashboard Admin / Tim IT", self._keluar)

        # --- Bilah tombol aksi admin: pack(side="bottom") DULU, sebelum area
        #     scroll di-pack, supaya dia pin di bawah window. Tombol rata kiri. ---
        bawah = ctk.CTkFrame(self, fg_color=t.WARNA_KARTU, height=74,
                              border_width=1, border_color="#ECEEF5")
        bawah.pack(side="bottom", fill="x")
        bawah.pack_propagate(False)

        isi_bawah = ctk.CTkFrame(bawah, fg_color="transparent")
        isi_bawah.pack(side="left", padx=20, pady=16, anchor="w")

        ctk.CTkButton(isi_bawah, text="Reset Sandi ke Default", fg_color=t.WARNA_UTAMA, corner_radius=8,
                      height=40, width=180, hover_color=t.WARNA_UTAMA_HOVER,
                      command=self._reset_sandi).pack(side="left", padx=6)
        ctk.CTkButton(isi_bawah, text="Hapus Akun", fg_color=t.WARNA_BAHAYA, corner_radius=8,
                      height=40, width=140, hover_color=t.WARNA_BAHAYA_HOVER,
                      command=self._hapus_akun).pack(side="left", padx=6)
        _tombol_sekunder(isi_bawah, "Pantau Tugas", lambda: self.view.tampil("PantauTugasPage"),
                         width=150, height=40).pack(side="left", padx=6)
        _tombol_sekunder(isi_bawah, "Pengaturan Akun", lambda: self.view.tampil("KeamananPage"),
                         width=160, height=40).pack(side="left", padx=6)

        # --- Area tengah discroll (statistik + tabel) ---
        self.area = ctk.CTkScrollableFrame(self, fg_color="transparent",
                                            scrollbar_button_color=t.WARNA_ABU)
        self.area.pack(fill="both", expand=True)

        kartu = ctk.CTkFrame(self.area, fg_color="transparent")
        kartu.pack(pady=14)
        self.lbl_total = _kartu_statistik(kartu, "Total Tugas")
        self.lbl_belum = _kartu_statistik(kartu, "Belum Selesai", warna_angka=t.WARNA_BAHAYA)
        self.lbl_selesai = _kartu_statistik(kartu, "Selesai", warna_angka=t.WARNA_SUKSES)
        self.lbl_pengguna = _kartu_statistik(kartu, "Total Pengguna")

        isi = ctk.CTkFrame(self.area, fg_color="transparent")
        isi.pack(fill="x", padx=20)

        ctk.CTkLabel(isi, text="Daftar Mahasiswa", font=t.FONT_LABEL_TEBAL,
                     text_color=t.WARNA_TEKS).pack(pady=(6, 6), anchor="w")
        self.tabel_mahasiswa = TabelData(isi, [
            ("NIM", 200, "w"), ("Nama", 400, "w"), ("Terdaftar Sejak", 260, "w"),
        ], tinggi=220)
        self.tabel_mahasiswa.pack(fill="x", pady=(0, 16))

        ctk.CTkLabel(isi, text="Daftar Admin / Tim IT Lainnya", font=t.FONT_LABEL_TEBAL,
                     text_color=t.WARNA_TEKS).pack(pady=(0, 6), anchor="w")
        self.tabel_admin = TabelData(isi, [
            ("NIM", 200, "w"), ("Nama", 400, "w"), ("Terdaftar Sejak", 260, "w"),
        ], tinggi=140)
        self.tabel_admin.pack(fill="x", pady=(0, 16))

    def muat_data(self):
        if self.view.pengguna_aktif:
            self.lbl_sapaan.configure(text=f"Dashboard Admin — {self.view.pengguna_aktif['nama']}")
        ringkasan = self.controller.ringkasan()
        self.lbl_total.configure(text=str(ringkasan["total"]))
        self.lbl_belum.configure(text=str(ringkasan["belum_selesai"]))
        self.lbl_selesai.configure(text=str(ringkasan["selesai"]))

        nim_sendiri = self.view.pengguna_aktif["nim"] if self.view.pengguna_aktif else None
        daftar_mhs = self.view.controller_pengguna.daftar_mahasiswa()
        daftar_admin = [p for p in self.view.controller_pengguna.daftar_admin() if p["nim"] != nim_sendiri]
        self.lbl_pengguna.configure(text=str(len(daftar_mhs) + len(daftar_admin) + 1))

        self.tabel_mahasiswa.kosongkan()
        if not daftar_mhs:
            self.tabel_mahasiswa.kosong_pesan("Belum ada mahasiswa terdaftar.")
        else:
            for p in daftar_mhs:
                self.tabel_mahasiswa.tambah_baris([p["nim"], p["nama"], str(p["dibuat_pada"])], data=p)

        self.tabel_admin.kosongkan()
        if not daftar_admin:
            self.tabel_admin.kosong_pesan("Tidak ada admin lain.")
        else:
            for p in daftar_admin:
                self.tabel_admin.tambah_baris([p["nim"], p["nama"], str(p["dibuat_pada"])], data=p)

    def _nim_terpilih(self):
        d = self.tabel_mahasiswa.data_terpilih() or self.tabel_admin.data_terpilih()
        if not d:
            messagebox.showwarning("Peringatan", "Pilih pengguna pada salah satu tabel terlebih dahulu.")
            return None
        return d["nim"]

    def _reset_sandi(self):
        nim = self._nim_terpilih()
        if nim is None:
            return
        if messagebox.askyesno("Konfirmasi", f"Reset sandi {nim} ke default ('ubahsandi123')?"):
            berhasil, pesan = self.view.controller_pengguna.reset_sandi(nim, "ubahsandi123")
            messagebox.showinfo("Info", pesan) if berhasil else messagebox.showwarning("Peringatan", pesan)

    def _hapus_akun(self):
        nim = self._nim_terpilih()
        if nim is None:
            return
        if self.view.pengguna_aktif and nim == self.view.pengguna_aktif["nim"]:
            messagebox.showwarning("Peringatan", "Tidak bisa menghapus akun yang sedang digunakan.")
            return
        if messagebox.askyesno("Konfirmasi", f"Hapus akun {nim}?"):
            berhasil, pesan = self.view.controller_pengguna.hapus_pengguna(nim)
            messagebox.showinfo("Info", pesan) if berhasil else messagebox.showwarning("Peringatan", pesan)
            self.muat_data()

    def _keluar(self):
        if messagebox.askyesno("Konfirmasi", "Keluar dari akun?"):
            self.view.pengguna_aktif = None
            self.view.tampil("LoginPage")


# ======================================================================
# PANTAU TUGAS (ADMIN)
# ======================================================================

class PantauTugasPage(ctk.CTkFrame):
    def __init__(self, parent, controller, view):
        super().__init__(parent, fg_color=t.WARNA_LATAR)
        self.controller = controller
        self.view = view

        atas = ctk.CTkFrame(self, fg_color="transparent")
        atas.pack(fill="x", padx=20, pady=16)

        kiri_atas = ctk.CTkFrame(atas, fg_color="transparent")
        kiri_atas.pack(side="left")
        ctk.CTkButton(kiri_atas, text="←", width=36, height=36, corner_radius=18,
                      fg_color=t.WARNA_UTAMA, hover_color=t.WARNA_UTAMA_HOVER,
                      font=("Segoe UI", 16, "bold"),
                      command=lambda: self.view.tampil("AdminDashboardPage")).pack(side="left", padx=(0, 12))
        ctk.CTkLabel(kiri_atas, text="Pantau Tugas", font=t.FONT_JUDUL,
                     text_color=t.WARNA_UTAMA).pack(side="left")

        self.input_cari, self.tombol_tampilkan_semua = _bilah_cari(
            atas, "Cari nama tugas / mata kuliah", self._cari, self._reset_pencarian)

        self.tabel = TabelData(self, [
            ("No", 60, "center"), ("Nama Tugas", 420, "w"),
            ("Mata Kuliah", 300, "w"), ("Tenggat", 150, "center"), ("Status", 200, "w"),
        ], kolom_badge=4)
        self.tabel.pack(fill="both", expand=True, padx=20, pady=5)

        ctk.CTkLabel(
            self,
            text="Mode pemantauan — penambahan dan pengeditan tugas tetap dilakukan oleh Mahasiswa.",
            font=t.FONT_LABEL, text_color=t.WARNA_TEKS_SEKUNDER,
        ).pack(pady=(0, 10))

    def muat_data(self, kata_kunci=""):
        self.tabel.kosongkan()
        data = self.controller.cari(kata_kunci) if kata_kunci else self.controller.tampilkan()

        if kata_kunci:
            self.tombol_tampilkan_semua.pack(side="right", padx=5)
        else:
            self.tombol_tampilkan_semua.pack_forget()

        if not data:
            self.tabel.kosong_pesan("Belum ada tugas.")
            return
        for i, d in enumerate(data):
            terlambat_aktif = bool(d.get("terlambat")) and d["status"] != "Selesai"
            self.tabel.tambah_baris(
                [d["nomor"], d["nama_tugas"], d["mata_kuliah"], d["tenggat"], d["status"]],
                data=d, bg=_warna_baris_tugas(d, i),
                warna_badge=_warna_badge_status(d["status"], terlambat_aktif),
            )

    def _cari(self):
        self.muat_data(self.input_cari.get().strip())

    def _reset_pencarian(self):
        self.input_cari.delete(0, "end")
        self.muat_data()


# ======================================================================
# FORMULIR TUGAS
# ======================================================================

class FormPage(ctk.CTkFrame):
    def __init__(self, parent, controller, view):
        super().__init__(parent, fg_color=t.WARNA_LATAR)
        self.controller = controller
        self.view = view
        self.status_sekarang = STATUS_TUGAS[0]

        kartu = ctk.CTkFrame(self, fg_color=t.WARNA_KARTU, corner_radius=t.RADIUS,
                              border_width=1, border_color="#ECEEF5", width=640)
        kartu.pack(pady=30)
        isi = ctk.CTkFrame(kartu, fg_color="transparent")
        isi.pack(padx=36, pady=28)

        header = ctk.CTkFrame(isi, fg_color="transparent")
        header.pack(fill="x", pady=(0, 20))
        kiri_header = ctk.CTkFrame(header, fg_color="transparent")
        kiri_header.pack(side="left", anchor="w")
        ctk.CTkLabel(kiri_header, text="HALAMAN FORMULIR", font=t.FONT_KECIL,
                     text_color=t.WARNA_TEKS_SEKUNDER).pack(anchor="w")
        ctk.CTkLabel(kiri_header, text="Formulir Tugas", font=t.FONT_JUDUL,
                     text_color=t.WARNA_UTAMA).pack(anchor="w")
        _tombol_sekunder(header, "Kembali ke utama",
                         lambda: self.view.tampil("DaftarPage"),
                         width=160, height=36).pack(side="right", anchor="e")

        grid = ctk.CTkFrame(isi, fg_color="transparent")
        grid.pack(fill="x")
        grid.grid_columnconfigure((0, 1), weight=1, uniform="kolom")

        wrap_nama, self.input_nama = _field_berlabel(grid, "Nama tugas", "Tulis nama tugas")
        wrap_nama.grid(row=0, column=0, sticky="we", padx=(0, 10))
        wrap_matkul, self.input_matkul = _field_berlabel(grid, "Mata kuliah", "Tulis mata kuliah")
        wrap_matkul.grid(row=0, column=1, sticky="we", padx=(10, 0))

        ctk.CTkLabel(grid, text="Tanggal tenggat", font=t.FONT_LABEL,
                     text_color=t.WARNA_TEKS_SEKUNDER).grid(row=1, column=0, sticky="w", pady=(10, 4), padx=(0, 10))
        ctk.CTkLabel(grid, text="Status", font=t.FONT_LABEL,
                     text_color=t.WARNA_TEKS_SEKUNDER).grid(row=1, column=1, sticky="w", pady=(10, 4), padx=(10, 0))

        self.input_tenggat = DateEntry(grid, width=20, date_pattern="dd/mm/yyyy",
                                        background=t.WARNA_UTAMA, foreground="white",
                                        bordercolor=t.WARNA_ABU_HOVER, headersbackground=t.WARNA_LATAR,
                                        normalbackground="white", font=("Segoe UI", 12))
        self.input_tenggat.grid(row=2, column=0, sticky="we", padx=(0, 10), ipady=5)

        self.pilihan_status = ctk.CTkOptionMenu(grid, values=STATUS_TUGAS, width=240, height=40,
                                                  fg_color=t.WARNA_KARTU, text_color=t.WARNA_TEKS,
                                                  button_color=t.WARNA_AKSEN, button_hover_color=t.WARNA_AKSEN_HOVER,
                                                  dropdown_fg_color=t.WARNA_KARTU,
                                                  corner_radius=8)
        self.pilihan_status.grid(row=2, column=1, sticky="we", padx=(10, 0))

        ctk.CTkLabel(isi, text="Deskripsi", font=t.FONT_LABEL,
                     text_color=t.WARNA_TEKS_SEKUNDER).pack(anchor="w", pady=(16, 4))
        self.input_deskripsi = ctk.CTkTextbox(isi, width=560, height=90, corner_radius=8,
                                               fg_color=t.WARNA_LATAR, border_width=1,
                                               border_color=t.WARNA_ABU_HOVER)
        self.input_deskripsi.pack(fill="x")

        tombol = ctk.CTkFrame(isi, fg_color="transparent")
        tombol.pack(pady=(22, 0), anchor="w")
        ctk.CTkButton(tombol, text="Tambah", width=120, height=40, corner_radius=8,
                      fg_color=t.WARNA_AKSEN, hover_color=t.WARNA_AKSEN_HOVER,
                      font=t.FONT_LABEL_TEBAL, command=self._tambah).grid(row=0, column=0, padx=(0, 8))
        ctk.CTkButton(tombol, text="Edit", width=120, height=40, corner_radius=8,
                      fg_color=t.WARNA_PERINGATAN, hover_color="#E09B1A",
                      font=t.FONT_LABEL_TEBAL, command=self._edit).grid(row=0, column=1, padx=8)
        _tombol_sekunder(tombol, "Bersihkan", self._bersihkan, width=120, height=40).grid(row=0, column=2, padx=8)

    def muat_data(self):
        id_terpilih = self.view.id_terpilih
        if id_terpilih is None:
            self.status_sekarang = STATUS_TUGAS[0]
            self.pilihan_status.set(STATUS_TUGAS[0])
            return
        data = next((d for d in self.controller.tampilkan() if d["id"] == id_terpilih), None)
        if data:
            self.input_nama.delete(0, "end"); self.input_nama.insert(0, data["nama_tugas"])
            self.input_matkul.delete(0, "end"); self.input_matkul.insert(0, data["mata_kuliah"])
            self.input_deskripsi.delete("1.0", "end"); self.input_deskripsi.insert("1.0", data["deskripsi"] or "")
            self.input_tenggat.set_date(data["tenggat"])
            self.status_sekarang = data["status"]
            self.pilihan_status.set(data["status"])

    def _ambil_input(self):
        return (self.input_nama.get().strip(), self.input_matkul.get().strip(),
                self.input_deskripsi.get("1.0", "end").strip(), self.input_tenggat.get())

    def _tambah(self):
        nama, matkul, deskripsi, tenggat = self._ambil_input()
        berhasil, pesan = self.controller.tambah(nama, matkul, deskripsi, tenggat, self.pilihan_status.get())
        messagebox.showinfo("Info", pesan) if berhasil else messagebox.showwarning("Peringatan", pesan)
        if berhasil:
            self._bersihkan()
            self.view.tampil("DaftarPage")

    def _edit(self):
        if self.view.id_terpilih is None:
            messagebox.showwarning("Peringatan", "Pilih tugas dari Daftar Tugas untuk diedit.")
            return
        nama, matkul, deskripsi, tenggat = self._ambil_input()
        berhasil, pesan = self.controller.edit(self.view.id_terpilih, nama, matkul, deskripsi,
                                                tenggat, self.pilihan_status.get())
        messagebox.showinfo("Info", pesan) if berhasil else messagebox.showwarning("Peringatan", pesan)
        if berhasil:
            self.view.id_terpilih = None
            self._bersihkan()
            self.view.tampil("DaftarPage")

    def _bersihkan(self):
        self.input_nama.delete(0, "end")
        self.input_matkul.delete(0, "end")
        self.input_deskripsi.delete("1.0", "end")
        self.input_tenggat.set_date(date.today())
        self.status_sekarang = STATUS_TUGAS[0]
        self.pilihan_status.set(STATUS_TUGAS[0])


class DialogStatus(ctk.CTkToplevel):
    def __init__(self, master, status_sekarang):
        super().__init__(master)
        self.title("Ubah Status")
        self.geometry("320x200")
        self.resizable(False, False)
        self.configure(fg_color=t.WARNA_KARTU)
        self.grab_set()
        self.hasil = None

        ctk.CTkLabel(self, text="Pilih status baru", font=t.FONT_LABEL_TEBAL,
                     text_color=t.WARNA_UTAMA).pack(pady=(24, 12))
        self.pilihan = ctk.CTkOptionMenu(self, values=STATUS_TUGAS, width=240, height=40, corner_radius=8,
                                          fg_color=t.WARNA_UTAMA, button_color=t.WARNA_UTAMA_HOVER)
        self.pilihan.set(status_sekarang)
        self.pilihan.pack(pady=5)

        tombol = ctk.CTkFrame(self, fg_color="transparent")
        tombol.pack(pady=24)
        ctk.CTkButton(tombol, text="Simpan", fg_color=t.WARNA_AKSEN, hover_color=t.WARNA_AKSEN_HOVER,
                      corner_radius=8, command=self._simpan).grid(row=0, column=0, padx=6)
        _tombol_sekunder(tombol, "Batal", self.destroy, width=110, height=36).grid(row=0, column=1, padx=6)

    def _simpan(self):
        self.hasil = self.pilihan.get()
        self.destroy()

    def get_input(self):
        self.master.wait_window(self)
        return self.hasil


# ======================================================================
# DAFTAR TUGAS (MAHASISWA)
# ======================================================================

class DaftarPage(ctk.CTkFrame):
    def __init__(self, parent, controller, view):
        super().__init__(parent, fg_color=t.WARNA_LATAR)
        self.controller = controller
        self.view = view

        atas = ctk.CTkFrame(self, fg_color="transparent")
        atas.pack(fill="x", padx=20, pady=16)

        ctk.CTkLabel(atas, text="Daftar Tugas", font=t.FONT_JUDUL, text_color=t.WARNA_UTAMA).pack(side="left")

        self.input_cari, self.tombol_tampilkan_semua = _bilah_cari(
            atas, "Cari nama tugas / mata kuliah", self._cari, self._reset_pencarian)

        self.tabel = TabelData(self, [
            ("No", 60, "center"), ("Nama Tugas", 420, "w"),
            ("Mata Kuliah", 300, "w"), ("Tenggat", 150, "center"), ("Status", 200, "w"),
        ], kolom_badge=4)
        self.tabel.pack(fill="both", expand=True, padx=20, pady=5)

        bawah = ctk.CTkFrame(self, fg_color="transparent")
        bawah.pack(pady=14)
        ctk.CTkButton(bawah, text="Tambah Tugas", fg_color=t.WARNA_AKSEN, hover_color=t.WARNA_AKSEN_HOVER,
                      corner_radius=8, height=40, command=lambda: self._buka_form(None)).grid(row=0, column=0, padx=5)
        ctk.CTkButton(bawah, text="Edit", fg_color=t.WARNA_UTAMA, hover_color=t.WARNA_UTAMA_HOVER,
                      corner_radius=8, height=40, command=self._edit_terpilih).grid(row=0, column=1, padx=5)
        ctk.CTkButton(bawah, text="Ubah Status", fg_color=t.WARNA_PERINGATAN, hover_color="#E09B1A",
                      corner_radius=8, height=40, command=self._ubah_status).grid(row=0, column=2, padx=5)
        ctk.CTkButton(bawah, text="Hapus", fg_color=t.WARNA_BAHAYA, hover_color=t.WARNA_BAHAYA_HOVER,
                      corner_radius=8, height=40, command=self._hapus).grid(row=0, column=3, padx=5)
        _tombol_sekunder(bawah, "Dashboard", self._ke_dashboard, height=40).grid(row=0, column=4, padx=5)

    def muat_data(self, kata_kunci=""):
        self.tabel.kosongkan()
        data = self.controller.cari(kata_kunci) if kata_kunci else self.controller.tampilkan()

        if kata_kunci:
            self.tombol_tampilkan_semua.pack(side="right", padx=5)
        else:
            self.tombol_tampilkan_semua.pack_forget()

        if not data:
            self.tabel.kosong_pesan("Belum ada tugas. Tambahkan melalui Formulir Tugas.")
            return
        for i, d in enumerate(data):
            terlambat_aktif = bool(d.get("terlambat")) and d["status"] != "Selesai"
            self.tabel.tambah_baris(
                [d["nomor"], d["nama_tugas"], d["mata_kuliah"], d["tenggat"], d["status"]],
                data=d, bg=_warna_baris_tugas(d, i),
                warna_badge=_warna_badge_status(d["status"], terlambat_aktif),
            )

    def _ke_dashboard(self):
        if self.view.pengguna_aktif and self.view.pengguna_aktif.get("peran") == "admin":
            self.view.tampil("AdminDashboardPage")
        else:
            self.view.tampil("DashboardPage")

    def _cari(self):
        self.muat_data(self.input_cari.get().strip())

    def _reset_pencarian(self):
        self.input_cari.delete(0, "end")
        self.muat_data()

    def _data_terpilih(self):
        d = self.tabel.data_terpilih()
        if not d:
            messagebox.showwarning("Peringatan", "Pilih tugas pada tabel terlebih dahulu.")
            return None
        return d

    def _buka_form(self, id_tugas):
        self.view.id_terpilih = id_tugas
        self.view.tampil("FormPage")

    def _edit_terpilih(self):
        d = self._data_terpilih()
        if d is not None:
            self._buka_form(d["id"])

    def _ubah_status(self):
        d = self._data_terpilih()
        if d is None:
            return
        dialog = DialogStatus(self, d["status"])
        status_baru = dialog.get_input()
        if status_baru:
            berhasil, pesan = self.controller.ubah_status(d["id"], status_baru)
            messagebox.showinfo("Info", pesan) if berhasil else messagebox.showwarning("Peringatan", pesan)
            self.muat_data()

    def _hapus(self):
        d = self._data_terpilih()
        if d is None:
            return
        if messagebox.askyesno("Konfirmasi", "Hapus tugas ini?"):
            berhasil, pesan = self.controller.hapus(d["id"])
            messagebox.showinfo("Info", pesan) if berhasil else messagebox.showwarning("Peringatan", pesan)
            self.muat_data()