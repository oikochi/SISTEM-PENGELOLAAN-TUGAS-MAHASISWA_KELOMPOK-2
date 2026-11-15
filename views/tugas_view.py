import os
import webbrowser
import customtkinter as ctk
from tkinter import messagebox, ttk
from PIL import Image
from datetime import date
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

NOMOR_WA_ADMIN = "+6285179777840"  #nomor oiko sementara


def _hubungi_admin():
    pesan = "Halo Admin SITAMA, saya butuh bantuan terkait akun saya."
    url = f"https://wa.me/{NOMOR_WA_ADMIN}?text={pesan.replace(' ', '%20')}"
    webbrowser.open(url)


def _muat_logo(ukuran=(90, 100)):
    if os.path.exists(LOGO_PATH):
        return ctk.CTkImage(Image.open(LOGO_PATH), size=ukuran)
    return None


def _atur_gaya_tabel():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", font=("Segoe UI", 11), rowheight=32,
                     background="white", fieldbackground="white", borderwidth=0)
    style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"),
                     background=t.WARNA_UTAMA, foreground="white", relief="flat", padding=6)
    style.map("Treeview.Heading", background=[("active", t.WARNA_UTAMA_HOVER)])
    style.map("Treeview",
              background=[("selected", "#EEF3FB")],
              foreground=[("selected", t.WARNA_TEKS)])


class TugasView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SITAMA — Sistem Pengelolaan Tugas Mahasiswa")
        self.geometry("920x700")
        self.configure(fg_color=t.WARNA_LATAR)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        _atur_gaya_tabel()

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
        self.logo_besar = _muat_logo((90, 100))

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


class HalamanAuth(ctk.CTkFrame):
    def __init__(self, parent, lebar_kartu=380):
        super().__init__(parent, fg_color=t.WARNA_LATAR)
        self.kartu = ctk.CTkFrame(self, fg_color=t.WARNA_KARTU, corner_radius=t.RADIUS,
                                   width=lebar_kartu)
        self.kartu.place(relx=0.5, rely=0.5, anchor="center")


class LoginPage(HalamanAuth):
    def __init__(self, parent, controller, view):
        super().__init__(parent)
        self.view = view
        isi = ctk.CTkFrame(self.kartu, fg_color="transparent")
        isi.pack(padx=40, pady=36)

        if view.logo_besar:
            ctk.CTkLabel(isi, image=view.logo_besar, text="").pack(pady=(0, 12))

        ctk.CTkLabel(isi, text="SITAMA", font=t.FONT_JUDUL, text_color=t.WARNA_UTAMA).pack()
        ctk.CTkLabel(isi, text="Sistem Pengelolaan Tugas Mahasiswa",
                     font=t.FONT_SUBJUDUL, text_color=t.WARNA_TEKS_SEKUNDER).pack(pady=(0, 20))

        self.input_nim = ctk.CTkEntry(isi, placeholder_text="NIM", width=t.LEBAR_INPUT, height=40)
        self.input_nim.pack(pady=6)
        self.input_sandi = ctk.CTkEntry(isi, placeholder_text="Kata sandi", show="*",
                                         width=t.LEBAR_INPUT, height=40)
        self.input_sandi.pack(pady=6)

        self.tampil_sandi = ctk.CTkCheckBox(isi, text="Tampilkan kata sandi",
                                             font=t.FONT_LABEL, command=self._toggle_sandi)
        self.tampil_sandi.pack(pady=(4, 16), anchor="w")

        ctk.CTkButton(isi, text="Masuk", width=t.LEBAR_TOMBOL, height=42,
                      fg_color=t.WARNA_UTAMA, hover_color=t.WARNA_UTAMA_HOVER,
                      font=t.FONT_LABEL_TEBAL, command=self._masuk).pack(pady=(0, 10))

        baris_bawah = ctk.CTkFrame(isi, fg_color="transparent")
        baris_bawah.pack(pady=(4, 0))
        ctk.CTkButton(baris_bawah, text="Lupa kata sandi?", fg_color="transparent",
                      hover_color=t.WARNA_LATAR, text_color=t.WARNA_UTAMA, font=t.FONT_LABEL,
                      command=lambda: self.view.tampil("ForgotPasswordPage")).pack(side="left", padx=4)
        ctk.CTkButton(baris_bawah, text="Daftar akun baru", fg_color="transparent",
                      hover_color=t.WARNA_LATAR, text_color=t.WARNA_AKSEN, font=t.FONT_LABEL,
                      command=self._ke_daftar).pack(side="left", padx=4)

        ctk.CTkButton(isi, text="💬 Butuh bantuan? Hubungi Admin", fg_color="transparent",
                      hover_color=t.WARNA_LATAR, text_color=t.WARNA_AKSEN, font=t.FONT_LABEL,
                      command=_hubungi_admin).pack(pady=(10, 0))

    def muat_data(self):
        self.input_nim.delete(0, "end")
        self.input_sandi.delete(0, "end")

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


class RegisterPage(HalamanAuth):
    def __init__(self, parent, controller, view):
        super().__init__(parent, lebar_kartu=400)
        self.view = view
        isi = ctk.CTkFrame(self.kartu, fg_color="transparent")
        isi.pack(padx=40, pady=30)

        if view.logo_kecil:
            ctk.CTkLabel(isi, image=view.logo_kecil, text="").pack(pady=(0, 8))

        ctk.CTkLabel(isi, text="Buat Akun Baru", font=t.FONT_JUDUL, text_color=t.WARNA_UTAMA).pack(pady=(0, 16))

        self.input_nama = self._field(isi, "Nama lengkap")
        self.input_nim = self._field(isi, "NIM")
        self.input_sandi = self._field(isi, "Kata sandi", sembunyikan=True)
        self.input_konfirmasi = self._field(isi, "Konfirmasi kata sandi", sembunyikan=True)

        ctk.CTkLabel(isi, text="Pertanyaan keamanan (untuk lupa sandi)",
                     font=t.FONT_LABEL, text_color=t.WARNA_TEKS_SEKUNDER).pack(pady=(10, 4), anchor="w")
        self.pilihan_pertanyaan = ctk.CTkOptionMenu(isi, values=PERTANYAAN_KEAMANAN,
                                                     width=t.LEBAR_INPUT, fg_color=t.WARNA_UTAMA,
                                                     button_color=t.WARNA_UTAMA_HOVER)
        self.pilihan_pertanyaan.pack(pady=(0, 6))
        self.input_jawaban = self._field(isi, "Jawaban keamanan")

        ctk.CTkButton(isi, text="Daftar", width=t.LEBAR_TOMBOL, height=42,
                      fg_color=t.WARNA_AKSEN, hover_color=t.WARNA_AKSEN_HOVER,
                      font=t.FONT_LABEL_TEBAL, command=self._daftar).pack(pady=(16, 8))
        ctk.CTkButton(isi, text="Sudah punya akun? Masuk", fg_color="transparent",
                      hover_color=t.WARNA_LATAR, text_color=t.WARNA_UTAMA, font=t.FONT_LABEL,
                      command=lambda: self.view.tampil("LoginPage")).pack()

    def _field(self, parent, label, sembunyikan=False):
        entry = ctk.CTkEntry(parent, placeholder_text=label, width=t.LEBAR_INPUT, height=38,
                              show="*" if sembunyikan else "")
        entry.pack(pady=5)
        return entry

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
        super().__init__(parent, lebar_kartu=380)
        self.view = view
        self.nim_aktif = None

        self.isi = ctk.CTkFrame(self.kartu, fg_color="transparent")
        self.isi.pack(padx=40, pady=30)

        if view.logo_kecil:
            ctk.CTkLabel(self.isi, image=view.logo_kecil, text="").pack(pady=(0, 8))

        ctk.CTkLabel(self.isi, text="Lupa Kata Sandi", font=t.FONT_JUDUL,
                     text_color=t.WARNA_UTAMA).pack(pady=(0, 16))

        self.input_nim = ctk.CTkEntry(self.isi, placeholder_text="NIM", width=t.LEBAR_INPUT, height=38)
        self.input_nim.pack(pady=6)
        ctk.CTkButton(self.isi, text="Cari Akun", width=t.LEBAR_TOMBOL, height=40,
                      fg_color=t.WARNA_UTAMA, hover_color=t.WARNA_UTAMA_HOVER,
                      font=t.FONT_LABEL_TEBAL, command=self._cari_akun).pack(pady=10)

        self.lbl_pertanyaan = ctk.CTkLabel(self.isi, text="", wraplength=280,
                                            font=t.FONT_LABEL, text_color=t.WARNA_TEKS_SEKUNDER)
        self.lbl_pertanyaan.pack(pady=(4, 4))

        self.input_jawaban = ctk.CTkEntry(self.isi, placeholder_text="Jawaban keamanan",
                                           width=t.LEBAR_INPUT, height=38)
        self.input_sandi_baru = ctk.CTkEntry(self.isi, placeholder_text="Kata sandi baru", show="*",
                                              width=t.LEBAR_INPUT, height=38)
        self.input_konfirmasi_baru = ctk.CTkEntry(self.isi, placeholder_text="Konfirmasi kata sandi baru",
                                                    show="*", width=t.LEBAR_INPUT, height=38)
        self.tombol_reset = ctk.CTkButton(self.isi, text="Reset Kata Sandi", width=t.LEBAR_TOMBOL, height=40,
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
        for widget in (self.input_jawaban, self.input_sandi_baru,
                       self.input_konfirmasi_baru, self.tombol_reset):
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
        self.input_jawaban.pack(pady=5)
        self.input_sandi_baru.pack(pady=5)
        self.input_konfirmasi_baru.pack(pady=5)
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


class KeamananPage(HalamanAuth):
    def __init__(self, parent, controller, view):
        super().__init__(parent, lebar_kartu=380)
        self.view = view
        isi = ctk.CTkFrame(self.kartu, fg_color="transparent")
        isi.pack(padx=40, pady=30)

        ctk.CTkLabel(isi, text="Atur Pertanyaan Keamanan", font=t.FONT_JUDUL,
                     text_color=t.WARNA_UTAMA).pack(pady=(0, 4))
        ctk.CTkLabel(isi, text="Dipakai untuk fitur Lupa Kata Sandi.",
                     font=t.FONT_LABEL, text_color=t.WARNA_TEKS_SEKUNDER).pack(pady=(0, 16))

        self.pilihan_pertanyaan = ctk.CTkOptionMenu(isi, values=PERTANYAAN_KEAMANAN,
                                                     width=t.LEBAR_INPUT, fg_color=t.WARNA_UTAMA,
                                                     button_color=t.WARNA_UTAMA_HOVER)
        self.pilihan_pertanyaan.pack(pady=6)
        self.input_jawaban = ctk.CTkEntry(isi, placeholder_text="Jawaban keamanan",
                                           width=t.LEBAR_INPUT, height=38)
        self.input_jawaban.pack(pady=6)

        ctk.CTkButton(isi, text="Simpan", width=t.LEBAR_TOMBOL, height=40,
                      fg_color=t.WARNA_AKSEN, hover_color=t.WARNA_AKSEN_HOVER,
                      font=t.FONT_LABEL_TEBAL, command=self._simpan).pack(pady=(16, 8))
        ctk.CTkButton(isi, text="Kembali", fg_color=t.WARNA_ABU, hover_color=t.WARNA_ABU_HOVER,
                      width=t.LEBAR_TOMBOL, height=38, command=self._kembali).pack()

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
                  width=90, height=34, command=dengan_keluar_fn).pack(side="right", padx=20)
    return bilah, lbl_judul


def _kartu_statistik(parent, judul, warna_angka=None):
    frame = ctk.CTkFrame(parent, width=160, height=104, fg_color=t.WARNA_KARTU,
                          corner_radius=t.RADIUS, border_width=1, border_color="#E5E7EB")
    frame.pack(side="left", padx=8)
    frame.pack_propagate(False)
    ctk.CTkLabel(frame, text=judul, font=t.FONT_LABEL, text_color=t.WARNA_TEKS_SEKUNDER).pack(pady=(16, 0))
    lbl_angka = ctk.CTkLabel(frame, text="0", font=t.FONT_ANGKA,
                              text_color=warna_angka or t.WARNA_UTAMA)
    lbl_angka.pack(pady=(2, 10))
    return lbl_angka


def _perbarui_penanda(tabel):
    terpilih = set(tabel.selection())
    for iid in tabel.get_children():
        tabel.set(iid, "penanda", "▎" if iid in terpilih else "")


def _buat_treeview(parent, kolom_spec, height):
    semua_kolom = [("penanda", "", 16, "center")] + list(kolom_spec)
    tabel = ttk.Treeview(parent, columns=[k[0] for k in semua_kolom], show="headings", height=height)
    for nama, judul, lebar, anchor in semua_kolom:
        tabel.heading(nama, text=judul)
        tabel.column(nama, width=lebar, anchor=anchor, stretch=(nama != "penanda"))
    tabel.tag_configure("terlambat", background="#FDEAEA", foreground=t.WARNA_BAHAYA)
    tabel.tag_configure("selesai", background="#E8F8F0", foreground=t.WARNA_AKSEN)
    tabel.bind("<<TreeviewSelect>>", lambda e, tb=tabel: _perbarui_penanda(tb))
    return tabel


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller, view):
        super().__init__(parent, fg_color=t.WARNA_LATAR)
        self.controller = controller
        self.view = view

        _, self.lbl_sapaan = _bilah_atas(self, view, "Dashboard", self._keluar)

        isi = ctk.CTkFrame(self, fg_color="transparent")
        isi.pack(pady=30)

        kartu = ctk.CTkFrame(isi, fg_color="transparent")
        kartu.pack(pady=10)
        self.lbl_total = _kartu_statistik(kartu, "Total Tugas")
        self.lbl_belum = _kartu_statistik(kartu, "Belum Selesai", warna_angka=t.WARNA_BAHAYA)
        self.lbl_selesai = _kartu_statistik(kartu, "Selesai", warna_angka=t.WARNA_AKSEN)

        tombol = ctk.CTkFrame(isi, fg_color="transparent")
        tombol.pack(pady=30)
        ctk.CTkButton(tombol, text="Formulir Tugas", width=190, height=40,
                      fg_color=t.WARNA_UTAMA, hover_color=t.WARNA_UTAMA_HOVER, font=t.FONT_LABEL_TEBAL,
                      command=lambda: self.view.tampil("FormPage")).grid(row=0, column=0, padx=8)
        ctk.CTkButton(tombol, text="Daftar Tugas", width=190, height=40,
                      fg_color=t.WARNA_UTAMA, hover_color=t.WARNA_UTAMA_HOVER, font=t.FONT_LABEL_TEBAL,
                      command=lambda: self.view.tampil("DaftarPage")).grid(row=0, column=1, padx=8)
        ctk.CTkButton(tombol, text="Pengaturan Akun", width=190, height=40,
                      fg_color=t.WARNA_ABU, hover_color=t.WARNA_ABU_HOVER, font=t.FONT_LABEL_TEBAL,
                      command=lambda: self.view.tampil("KeamananPage")).grid(row=0, column=2, padx=8)

    def muat_data(self):
        if self.view.pengguna_aktif:
            self.lbl_sapaan.configure(text=f"Halo, {self.view.pengguna_aktif['nama']}")
        ringkasan = self.controller.ringkasan()
        self.lbl_total.configure(text=str(ringkasan["total"]))
        self.lbl_belum.configure(text=str(ringkasan["belum_selesai"]))
        self.lbl_selesai.configure(text=str(ringkasan["selesai"]))

    def _keluar(self):
        if messagebox.askyesno("Konfirmasi", "Keluar dari akun?"):
            self.view.pengguna_aktif = None
            self.view.tampil("LoginPage")


class AdminDashboardPage(ctk.CTkFrame):
    def __init__(self, parent, controller, view):
        super().__init__(parent, fg_color=t.WARNA_LATAR)
        self.controller = controller
        self.view = view

        _, self.lbl_sapaan = _bilah_atas(self, view, "Dashboard Admin / Tim IT", self._keluar)

        kartu = ctk.CTkFrame(self, fg_color="transparent")
        kartu.pack(pady=14)
        self.lbl_total = _kartu_statistik(kartu, "Total Tugas")
        self.lbl_belum = _kartu_statistik(kartu, "Belum Selesai", warna_angka=t.WARNA_BAHAYA)
        self.lbl_selesai = _kartu_statistik(kartu, "Selesai", warna_angka=t.WARNA_AKSEN)
        self.lbl_pengguna = _kartu_statistik(kartu, "Total Pengguna")

        isi = ctk.CTkFrame(self, fg_color="transparent")
        isi.pack(fill="both", expand=True, padx=20)

        ctk.CTkLabel(isi, text="Daftar Mahasiswa", font=t.FONT_LABEL_TEBAL,
                     text_color=t.WARNA_TEKS).pack(pady=(6, 4), anchor="w")
        self.tabel_mahasiswa = _buat_treeview(isi, [
            ("nim", "NIM", 140, "center"), ("nama", "Nama", 260, "w"),
            ("dibuat_pada", "Terdaftar Sejak", 170, "center"),
        ], height=5)
        self.tabel_mahasiswa.pack(fill="x", pady=(0, 10))

        ctk.CTkLabel(isi, text="Daftar Admin / Tim IT Lainnya", font=t.FONT_LABEL_TEBAL,
                     text_color=t.WARNA_TEKS).pack(pady=(4, 4), anchor="w")
        self.tabel_admin = _buat_treeview(isi, [
            ("nim", "NIM", 140, "center"), ("nama", "Nama", 260, "w"),
            ("dibuat_pada", "Terdaftar Sejak", 170, "center"),
        ], height=3)
        self.tabel_admin.pack(fill="x")

        bawah = ctk.CTkFrame(self, fg_color="transparent")
        bawah.pack(pady=14)
        ctk.CTkButton(bawah, text="Reset Sandi ke Default", fg_color=t.WARNA_UTAMA,
                      hover_color=t.WARNA_UTAMA_HOVER, command=self._reset_sandi).grid(row=0, column=0, padx=6)
        ctk.CTkButton(bawah, text="Hapus Akun", fg_color=t.WARNA_BAHAYA,
                      hover_color=t.WARNA_BAHAYA_HOVER, command=self._hapus_akun).grid(row=0, column=1, padx=6)
        ctk.CTkButton(bawah, text="Pantau Tugas", fg_color=t.WARNA_ABU,
                      hover_color=t.WARNA_ABU_HOVER,
                      command=lambda: self.view.tampil("PantauTugasPage")).grid(row=0, column=2, padx=6)
        ctk.CTkButton(bawah, text="Pengaturan Akun", fg_color=t.WARNA_ABU,
                      hover_color=t.WARNA_ABU_HOVER,
                      command=lambda: self.view.tampil("KeamananPage")).grid(row=0, column=3, padx=6)

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

        self.tabel_mahasiswa.delete(*self.tabel_mahasiswa.get_children())
        for p in daftar_mhs:
            self.tabel_mahasiswa.insert("", "end", iid=p["nim"],
                                         values=("", p["nim"], p["nama"], str(p["dibuat_pada"])))

        self.tabel_admin.delete(*self.tabel_admin.get_children())
        if not daftar_admin:
            self.tabel_admin.insert("", "end", values=("", "", "Tidak ada admin lain.", ""))
        for p in daftar_admin:
            self.tabel_admin.insert("", "end", iid=p["nim"],
                                     values=("", p["nim"], p["nama"], str(p["dibuat_pada"])))

    def _nim_terpilih(self):
        pilihan = self.tabel_mahasiswa.selection()
        if pilihan:
            return pilihan[0]
        pilihan = self.tabel_admin.selection()
        if pilihan:
            return pilihan[0]
        messagebox.showwarning("Peringatan", "Pilih pengguna pada salah satu tabel terlebih dahulu.")
        return None

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

        self.input_cari = ctk.CTkEntry(atas, placeholder_text="Cari nama tugas / mata kuliah", width=220)
        self.input_cari.pack(side="right", padx=5)
        ctk.CTkButton(atas, text="Cari", width=70, fg_color=t.WARNA_UTAMA,
                      hover_color=t.WARNA_UTAMA_HOVER, command=self._cari).pack(side="right")

        self.tombol_tampilkan_semua = ctk.CTkButton(
            atas, text="↺ Tampilkan Semua", width=150, fg_color=t.WARNA_ABU,
            hover_color=t.WARNA_ABU_HOVER, command=self._reset_pencarian
        )

        self.tabel = _buat_treeview(self, [
            ("nomor", "No", 50, "center"), ("nama_tugas", "Nama Tugas", 260, "w"),
            ("mata_kuliah", "Mata Kuliah", 180, "w"), ("tenggat", "Tenggat", 120, "center"),
            ("status", "Status", 160, "center"),
        ], height=16)
        self.tabel.pack(fill="both", expand=True, padx=20, pady=5)

        ctk.CTkLabel(
            self,
            text="Mode pemantauan — penambahan dan pengeditan tugas tetap dilakukan oleh Mahasiswa.",
            font=t.FONT_LABEL, text_color=t.WARNA_TEKS_SEKUNDER,
        ).pack(pady=(0, 10))

    def muat_data(self, kata_kunci=""):
        self.tabel.delete(*self.tabel.get_children())
        data = self.controller.cari(kata_kunci) if kata_kunci else self.controller.tampilkan()

        if kata_kunci:
            self.tombol_tampilkan_semua.pack(side="right", padx=5)
        else:
            self.tombol_tampilkan_semua.pack_forget()

        if not data:
            self.tabel.insert("", "end", values=("", "", "Belum ada tugas.", "", "", ""))
            return
        for d in data:
            if d.get("terlambat"):
                tag = "terlambat"
            elif d["status"] == "Selesai":
                tag = "selesai"
            else:
                tag = ""
            self.tabel.insert("", "end", iid=d["id"], tags=(tag,) if tag else (),
                               values=("", d["nomor"], d["nama_tugas"], d["mata_kuliah"], d["tenggat"], d["status"]))

    def _cari(self):
        self.muat_data(self.input_cari.get().strip())

    def _reset_pencarian(self):
        self.input_cari.delete(0, "end")
        self.muat_data()


class FormPage(ctk.CTkFrame):
    def __init__(self, parent, controller, view):
        super().__init__(parent, fg_color=t.WARNA_LATAR)
        self.controller = controller
        self.view = view
        self.status_sekarang = STATUS_TUGAS[0]

        kartu = ctk.CTkFrame(self, fg_color=t.WARNA_KARTU, corner_radius=t.RADIUS)
        kartu.pack(pady=24)
        isi = ctk.CTkFrame(kartu, fg_color="transparent")
        isi.pack(padx=40, pady=30)

        ctk.CTkLabel(isi, text="Formulir Tugas", font=t.FONT_JUDUL, text_color=t.WARNA_UTAMA).pack(pady=(0, 14))

        self.input_nama = self._field(isi, "Nama tugas")
        self.input_matkul = self._field(isi, "Mata kuliah")
        self.input_deskripsi = self._field(isi, "Deskripsi (opsional)")

        ctk.CTkLabel(isi, text="Tenggat", font=t.FONT_LABEL, text_color=t.WARNA_TEKS_SEKUNDER).pack(pady=(8, 2), anchor="w")
        self.input_tenggat = DateEntry(isi, width=25, date_pattern="dd/mm/yyyy",
                                        background=t.WARNA_UTAMA, foreground="white",
                                        bordercolor=t.WARNA_UTAMA, headersbackground=t.WARNA_LATAR,
                                        normalbackground="white", font=("Segoe UI", 12))
        self.input_tenggat.pack(pady=2, ipady=5)

        ctk.CTkLabel(
            isi, text="Status tugas diubah lewat tombol \"Ubah Status\" di Daftar Tugas.",
            font=("Segoe UI", 11), text_color=t.WARNA_TEKS_SEKUNDER,
        ).pack(pady=(10, 0))

        tombol = ctk.CTkFrame(isi, fg_color="transparent")
        tombol.pack(pady=18)
        ctk.CTkButton(tombol, text="Tambah", fg_color=t.WARNA_AKSEN, hover_color=t.WARNA_AKSEN_HOVER,
                      command=self._tambah).grid(row=0, column=0, padx=5)
        ctk.CTkButton(tombol, text="Edit", fg_color=t.WARNA_UTAMA, hover_color=t.WARNA_UTAMA_HOVER,
                      command=self._edit).grid(row=0, column=1, padx=5)
        ctk.CTkButton(tombol, text="Bersihkan", fg_color=t.WARNA_ABU, hover_color=t.WARNA_ABU_HOVER,
                      command=self._bersihkan).grid(row=0, column=2, padx=5)
        ctk.CTkButton(tombol, text="Kembali", fg_color=t.WARNA_ABU, hover_color=t.WARNA_ABU_HOVER,
                      command=lambda: self.view.tampil("DaftarPage")).grid(row=0, column=3, padx=5)

    def _field(self, parent, label):
        ctk.CTkLabel(parent, text=label, font=t.FONT_LABEL, text_color=t.WARNA_TEKS_SEKUNDER).pack(pady=(8, 2), anchor="w")
        entry = ctk.CTkEntry(parent, width=t.LEBAR_INPUT, height=38)
        entry.pack(pady=2)
        return entry

    def muat_data(self):
        id_terpilih = self.view.id_terpilih
        if id_terpilih is None:
            self.status_sekarang = STATUS_TUGAS[0]
            return
        data = next((d for d in self.controller.tampilkan() if d["id"] == id_terpilih), None)
        if data:
            self.input_nama.delete(0, "end"); self.input_nama.insert(0, data["nama_tugas"])
            self.input_matkul.delete(0, "end"); self.input_matkul.insert(0, data["mata_kuliah"])
            self.input_deskripsi.delete(0, "end"); self.input_deskripsi.insert(0, data["deskripsi"] or "")
            self.input_tenggat.set_date(data["tenggat"])
            self.status_sekarang = data["status"]

    def _ambil_input(self):
        return (self.input_nama.get().strip(), self.input_matkul.get().strip(),
                self.input_deskripsi.get().strip(), self.input_tenggat.get())

    def _tambah(self):
        nama, matkul, deskripsi, tenggat = self._ambil_input()
        berhasil, pesan = self.controller.tambah(nama, matkul, deskripsi, tenggat, STATUS_TUGAS[0])
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
                                                tenggat, self.status_sekarang)
        messagebox.showinfo("Info", pesan) if berhasil else messagebox.showwarning("Peringatan", pesan)
        if berhasil:
            self.view.id_terpilih = None
            self._bersihkan()
            self.view.tampil("DaftarPage")

    def _bersihkan(self):
        for entry in (self.input_nama, self.input_matkul, self.input_deskripsi):
            entry.delete(0, "end")
        self.input_tenggat.set_date(date.today())
        self.status_sekarang = STATUS_TUGAS[0]


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
        self.pilihan = ctk.CTkOptionMenu(self, values=STATUS_TUGAS, width=240,
                                          fg_color=t.WARNA_UTAMA, button_color=t.WARNA_UTAMA_HOVER)
        self.pilihan.set(status_sekarang)
        self.pilihan.pack(pady=5)

        tombol = ctk.CTkFrame(self, fg_color="transparent")
        tombol.pack(pady=24)
        ctk.CTkButton(tombol, text="Simpan", fg_color=t.WARNA_AKSEN, hover_color=t.WARNA_AKSEN_HOVER,
                      command=self._simpan).grid(row=0, column=0, padx=6)
        ctk.CTkButton(tombol, text="Batal", fg_color=t.WARNA_ABU, hover_color=t.WARNA_ABU_HOVER,
                      command=self.destroy).grid(row=0, column=1, padx=6)

    def _simpan(self):
        self.hasil = self.pilihan.get()
        self.destroy()

    def get_input(self):
        self.master.wait_window(self)
        return self.hasil


class DaftarPage(ctk.CTkFrame):
    def __init__(self, parent, controller, view):
        super().__init__(parent, fg_color=t.WARNA_LATAR)
        self.controller = controller
        self.view = view
        self._data_tampil = []

        atas = ctk.CTkFrame(self, fg_color="transparent")
        atas.pack(fill="x", padx=20, pady=16)

        ctk.CTkLabel(atas, text="Daftar Tugas", font=t.FONT_JUDUL, text_color=t.WARNA_UTAMA).pack(side="left")

        self.input_cari = ctk.CTkEntry(atas, placeholder_text="Cari nama tugas / mata kuliah", width=220)
        self.input_cari.pack(side="right", padx=5)
        ctk.CTkButton(atas, text="Cari", width=70, fg_color=t.WARNA_UTAMA,
                      hover_color=t.WARNA_UTAMA_HOVER, command=self._cari).pack(side="right")

        self.tombol_tampilkan_semua = ctk.CTkButton(
            atas, text="↺ Tampilkan Semua", width=150, fg_color=t.WARNA_ABU,
            hover_color=t.WARNA_ABU_HOVER, command=self._reset_pencarian
        )

        self.tabel = _buat_treeview(self, [
            ("nomor", "No", 50, "center"), ("nama_tugas", "Nama Tugas", 260, "w"),
            ("mata_kuliah", "Mata Kuliah", 180, "w"), ("tenggat", "Tenggat", 120, "center"),
            ("status", "Status", 160, "center"),
        ], height=14)
        self.tabel.pack(fill="both", expand=True, padx=20, pady=5)

        bawah = ctk.CTkFrame(self, fg_color="transparent")
        bawah.pack(pady=14)
        ctk.CTkButton(bawah, text="Tambah Tugas", fg_color=t.WARNA_AKSEN, hover_color=t.WARNA_AKSEN_HOVER,
                      command=lambda: self._buka_form(None)).grid(row=0, column=0, padx=5)
        ctk.CTkButton(bawah, text="Edit", fg_color=t.WARNA_UTAMA, hover_color=t.WARNA_UTAMA_HOVER,
                      command=self._edit_terpilih).grid(row=0, column=1, padx=5)
        ctk.CTkButton(bawah, text="Ubah Status", fg_color=t.WARNA_UTAMA, hover_color=t.WARNA_UTAMA_HOVER,
                      command=self._ubah_status).grid(row=0, column=2, padx=5)
        ctk.CTkButton(bawah, text="Hapus", fg_color=t.WARNA_BAHAYA, hover_color=t.WARNA_BAHAYA_HOVER,
                      command=self._hapus).grid(row=0, column=3, padx=5)
        ctk.CTkButton(bawah, text="Dashboard", fg_color=t.WARNA_ABU, hover_color=t.WARNA_ABU_HOVER,
                      command=self._ke_dashboard).grid(row=0, column=4, padx=5)

    def muat_data(self, kata_kunci=""):
        self.tabel.delete(*self.tabel.get_children())
        data = self.controller.cari(kata_kunci) if kata_kunci else self.controller.tampilkan()
        self._data_tampil = data

        if kata_kunci:
            self.tombol_tampilkan_semua.pack(side="right", padx=5)
        else:
            self.tombol_tampilkan_semua.pack_forget()

        if not data:
            self.tabel.insert("", "end", values=("", "", "Belum ada tugas. Tambahkan melalui Formulir Tugas.", "", "", ""))
            return
        for d in data:
            if d.get("terlambat"):
                tag = "terlambat"
            elif d["status"] == "Selesai":
                tag = "selesai"
            else:
                tag = ""
            self.tabel.insert("", "end", iid=d["id"], tags=(tag,) if tag else (),
                               values=("", d["nomor"], d["nama_tugas"], d["mata_kuliah"], d["tenggat"], d["status"]))

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

    def _id_terpilih(self):
        pilihan = self.tabel.selection()
        if not pilihan:
            messagebox.showwarning("Peringatan", "Pilih tugas pada tabel terlebih dahulu.")
            return None
        return int(pilihan[0])

    def _buka_form(self, id_tugas):
        self.view.id_terpilih = id_tugas
        self.view.tampil("FormPage")

    def _edit_terpilih(self):
        id_tugas = self._id_terpilih()
        if id_tugas is not None:
            self._buka_form(id_tugas)

    def _ubah_status(self):
        id_tugas = self._id_terpilih()
        if id_tugas is None:
            return
        data_sekarang = next((d for d in self._data_tampil if d["id"] == id_tugas), None)
        status_sekarang = data_sekarang["status"] if data_sekarang else STATUS_TUGAS[0]
        dialog = DialogStatus(self, status_sekarang)
        status_baru = dialog.get_input()
        if status_baru:
            berhasil, pesan = self.controller.ubah_status(id_tugas, status_baru)
            messagebox.showinfo("Info", pesan) if berhasil else messagebox.showwarning("Peringatan", pesan)
            self.muat_data()

    def _hapus(self):
        id_tugas = self._id_terpilih()
        if id_tugas is None:
            return
        if messagebox.askyesno("Konfirmasi", "Hapus tugas ini?"):
            berhasil, pesan = self.controller.hapus(id_tugas)
            messagebox.showinfo("Info", pesan) if berhasil else messagebox.showwarning("Peringatan", pesan)
            self.muat_data()