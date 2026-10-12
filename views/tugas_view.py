import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import messagebox
from controllers.tugas_controller import TugasController, STATUS_TUGAS

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

# ------------------------------------------------------------------ Akun login
# Laporan (hal. Login) meminta NIM + kata sandi, tetapi belum mendefinisikan tabel pengguna.
# Sementara, akun disimpan di sini. Ganti sesuai kebutuhan kelompok.
NIM_ANGGOTA = [
    "F5212520082", "F5212530092", "F5212530112",
    "F5212530096", "F5212530099", "F5212530095",
]
KATA_SANDI = "kelompok2"
AKUN = {nim: KATA_SANDI for nim in NIM_ANGGOTA}

# ------------------------------------------------------------ Palet (dari mockup laporan)
BG = "#f4f8fd"
BIRU = "#1f6fd0"
BIRU_H = "#1859ab"
NAVY = "#132b5e"
NAVY_SOFT = "#2c4a7c"
MUTED = "#5b6f94"
BORDER = "#c9d8ec"
INPUT_BORDER = "#9db4d8"
HEADER_BG = "#e3f0fd"
HEADER_FG = "#1f4a96"
ROW_ALT = "#f6f9fe"
AMBER = "#b07400"
AMBER_H = "#8f5f00"
MERAH = "#c0392b"
MERAH_H = "#9c2e22"
PLACEHOLDER = "#7d8798"

FONT = "Segoe UI"


def f(ukuran, tebal=False):
    return ctk.CTkFont(FONT, ukuran, "bold" if tebal else "normal")


GAYA_TOMBOL = {
    "biru": dict(fg_color=BIRU, hover_color=BIRU_H, text_color="white", border_width=0),
    "amber": dict(fg_color=AMBER, hover_color=AMBER_H, text_color="white", border_width=0),
    "merah": dict(fg_color=MERAH, hover_color=MERAH_H, text_color="white", border_width=0),
    "garis": dict(fg_color="white", hover_color="#eaf2fc", text_color=NAVY_SOFT,
                  border_width=1, border_color=INPUT_BORDER),
    "garis_biru": dict(fg_color="white", hover_color="#eaf2fc", text_color=BIRU,
                       border_width=2, border_color=BIRU),
}


def tombol(parent, teks, perintah, gaya="biru", **kw):
    opsi = dict(height=46, corner_radius=10, font=f(14, True))
    opsi.update(GAYA_TOMBOL[gaya])
    opsi.update(kw)
    return ctk.CTkButton(parent, text=teks, command=perintah, **opsi)


def label(parent, teks, **kw):
    return ctk.CTkLabel(parent, text=teks, font=f(14, True), text_color=NAVY, anchor="w", **kw)


def kolom_input(parent, placeholder, **kw):
    opsi = dict(height=44, corner_radius=8, border_width=1, border_color=INPUT_BORDER,
                fg_color="white", text_color=NAVY, placeholder_text=placeholder,
                placeholder_text_color=PLACEHOLDER, font=f(14))
    opsi.update(kw)
    return ctk.CTkEntry(parent, **opsi)


def kosongkan(entry):
    """Kosongkan CTkEntry lalu pastikan teks petunjuk (placeholder) tampil kembali.
    CTkEntry.delete() saja tidak memunculkan placeholder karena status fokus awalnya keliru."""
    entry.delete(0, "end")
    try:
        if entry.focus_get() is not entry._entry:
            entry._activate_placeholder()
    except Exception:
        pass


class TextboxPlaceholder(ctk.CTkTextbox):
    """CTkTextbox dengan teks petunjuk (placeholder)."""

    def __init__(self, master, placeholder, **kw):
        super().__init__(master, text_color=NAVY, **kw)
        self._ph = placeholder
        self._aktif = False
        self.bind("<FocusIn>", self._hapus_ph)
        self.bind("<Key>", self._hapus_ph)
        self.bind("<FocusOut>", self._tampil_ph)
        self._tampil_ph()

    def _tampil_ph(self, _=None):
        if not self._aktif and not self.get("0.0", "end").strip():
            self.delete("0.0", "end")
            self.insert("0.0", self._ph)
            self.configure(text_color=PLACEHOLDER)
            self._aktif = True

    def _hapus_ph(self, _=None):
        if self._aktif:
            self.delete("0.0", "end")
            self.configure(text_color=NAVY)
            self._aktif = False

    def ambil(self):
        return "" if self._aktif else self.get("0.0", "end").strip()

    def isi(self, teks):
        self._aktif = False
        self.delete("0.0", "end")
        self.configure(text_color=NAVY)
        if teks:
            self.insert("0.0", teks)
        else:
            self._tampil_ph()


def buat_header(parent, eyebrow, judul, app):
    bar = ctk.CTkFrame(parent, fg_color="transparent")
    bar.pack(fill="x", padx=70, pady=(34, 18))
    kiri = ctk.CTkFrame(bar, fg_color="transparent")
    kiri.pack(side="left")
    lbl = ctk.CTkLabel(kiri, text=eyebrow, font=f(13), text_color=MUTED, anchor="w")
    lbl.pack(anchor="w")
    ctk.CTkLabel(kiri, text=judul, font=f(32, True), text_color=NAVY, anchor="w").pack(anchor="w")
    tombol(bar, "Kembali ke utama", lambda: app.tampil("dashboard"), "garis",
           width=170, height=42, font=f(14)).pack(side="right", anchor="n")
    return lbl


class Halaman(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color=BG, corner_radius=0)
        self.app = app
        self.ctrl = app.controller

    def on_show(self, **kwargs):
        pass


# =========================================================== Halaman Login
class LoginPage(Halaman):
    def __init__(self, master, app):
        super().__init__(master, app)
        self.grid_columnconfigure((0, 1), weight=1, uniform="kol")
        self.grid_rowconfigure(0, weight=1)

        kiri = ctk.CTkFrame(self, fg_color=BIRU, corner_radius=0)
        kiri.grid(row=0, column=0, sticky="nsew")
        isi = ctk.CTkFrame(kiri, fg_color="transparent")
        isi.place(relx=0.5, rely=0.5, anchor="center")
        ctk.CTkLabel(isi, text="SELAMAT DATANG", font=f(13), text_color="#cfe2fb",
                     anchor="w").pack(anchor="w", pady=(0, 10))
        ctk.CTkLabel(isi, text="Sistem Pengelolaan\nTugas Mahasiswa", font=f(38, True),
                     text_color="white", justify="left", anchor="w").pack(anchor="w")
        ctk.CTkLabel(isi, text="Masuk untuk mencatat, memantau, dan merapikan\nseluruh tugas kuliah.",
                     font=f(16), text_color="#e6f0fc", justify="left",
                     anchor="w").pack(anchor="w", pady=(18, 0))

        kanan = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        kanan.grid(row=0, column=1, sticky="nsew")
        kartu = ctk.CTkFrame(kanan, fg_color="white", corner_radius=18, border_width=1,
                             border_color=BORDER)
        kartu.place(relx=0.5, rely=0.5, anchor="center")
        dalam = ctk.CTkFrame(kartu, fg_color="transparent")
        dalam.pack(padx=42, pady=38)

        ctk.CTkLabel(dalam, text="Login", font=f(28, True), text_color=NAVY,
                     anchor="w").pack(anchor="w", pady=(0, 16))
        label(dalam, "NIM").pack(anchor="w", pady=(0, 6))
        self.e_nim = kolom_input(dalam, "Masukkan NIM", width=380, height=48)
        self.e_nim.pack(pady=(0, 16))
        label(dalam, "Kata sandi").pack(anchor="w", pady=(0, 6))
        self.e_sandi = kolom_input(dalam, "Masukkan kata sandi", width=380, height=48, show="•")
        self.e_sandi.pack(pady=(0, 14))

        self.cek = ctk.CTkCheckBox(dalam, text="Tampilkan kata sandi", command=self._toggle,
                                   font=f(14), text_color=NAVY_SOFT, fg_color=BIRU,
                                   hover_color=BIRU_H, border_color=INPUT_BORDER,
                                   checkbox_width=22, checkbox_height=22, corner_radius=5)
        self.cek.pack(anchor="w", pady=(0, 14))

        self.lbl_error = ctk.CTkLabel(dalam, text="", font=f(13), text_color=MERAH, anchor="w")
        self.lbl_error.pack(anchor="w")
        tombol(dalam, "Masuk", self.masuk, "biru", width=380, height=50,
               font=f(16, True)).pack(pady=(4, 0))

        for e in (self.e_nim, self.e_sandi):
            e.bind("<Return>", lambda ev: self.masuk())

    def _toggle(self):
        self.e_sandi.configure(show="" if self.cek.get() else "•")

    def masuk(self):
        nim = self.e_nim.get().strip()
        sandi = self.e_sandi.get()
        if AKUN.get(nim) == sandi and nim:
            self.on_show()
            self.app.tampil("dashboard")
        else:
            self.lbl_error.configure(text="NIM atau kata sandi salah.")

    def on_show(self, **kwargs):
        kosongkan(self.e_nim)
        kosongkan(self.e_sandi)
        self.cek.deselect()
        self.e_sandi.configure(show="•")
        self.lbl_error.configure(text="")


# ========================================================= Halaman Dashboard
class DashboardPage(Halaman):
    def __init__(self, master, app):
        super().__init__(master, app)
        ctk.CTkLabel(self, text="HALAMAN UTAMA", font=f(13), text_color=MUTED,
                     anchor="w").pack(fill="x", padx=70, pady=(58, 0))
        ctk.CTkLabel(self, text="Sistem Pengelolaan Tugas Mahasiswa", font=f(36, True),
                     text_color=NAVY, anchor="w").pack(fill="x", padx=70)
        ctk.CTkLabel(self, text="Catat, pantau, dan rapikan seluruh tugas kuliah dalam satu aplikasi.",
                     font=f(16), text_color=MUTED, anchor="w").pack(fill="x", padx=70, pady=(4, 28))

        label(self, "Ringkasan tugas").pack(fill="x", padx=70, pady=(0, 10))
        baris = ctk.CTkFrame(self, fg_color="transparent")
        baris.pack(fill="x", padx=70)
        baris.grid_columnconfigure((0, 1, 2), weight=1, uniform="kartu")
        self.angka = {}
        for i, (kunci, judul) in enumerate([("total", "Jumlah seluruh tugas"),
                                            ("belum", "Belum selesai"),
                                            ("selesai", "Sudah selesai")]):
            k = ctk.CTkFrame(baris, fg_color="white", corner_radius=14, border_width=1,
                             border_color=BORDER)
            k.grid(row=0, column=i, sticky="ew", padx=(0 if i == 0 else 12, 0 if i == 2 else 12))
            ctk.CTkLabel(k, text=judul, font=f(15), text_color=MUTED,
                         anchor="w").pack(fill="x", padx=32, pady=(24, 0))
            lbl = ctk.CTkLabel(k, text="00", font=f(46, True), text_color=BIRU, anchor="w")
            lbl.pack(fill="x", padx=32, pady=(0, 20))
            self.angka[kunci] = lbl

        label(self, "Navigasi").pack(fill="x", padx=70, pady=(34, 10))
        nav = ctk.CTkFrame(self, fg_color="transparent")
        nav.pack(fill="x", padx=70)
        nav.grid_columnconfigure((0, 1), weight=1, uniform="nav")
        tombol(nav, "Formulir Tugas", lambda: app.tampil("form"), "biru", height=60,
               corner_radius=14, font=f(17, True)).grid(row=0, column=0, sticky="ew", padx=(0, 14))
        tombol(nav, "Daftar Tugas", lambda: app.tampil("daftar"), "garis_biru", height=60,
               corner_radius=14, font=f(17, True)).grid(row=0, column=1, sticky="ew", padx=(14, 0))

    def on_show(self, **kwargs):
        r = self.ctrl.ringkasan()
        for kunci, lbl in self.angka.items():
            lbl.configure(text=f"{r[kunci]:02d}")


# ============================================================ Halaman Formulir
class FormPage(Halaman):
    TEKS_STATUS = "Pilih status"

    def __init__(self, master, app):
        super().__init__(master, app)
        self.id_edit = None
        self.lbl_eyebrow = buat_header(self, "HALAMAN FORMULIR", "Formulir Tugas", app)

        kartu = ctk.CTkFrame(self, fg_color="white", corner_radius=14, border_width=1,
                             border_color=BORDER)
        kartu.pack(fill="x", padx=70)
        kartu.grid_columnconfigure((0, 1), weight=1, uniform="isi")

        kiri, kanan = (36, 18), (18, 36)
        label(kartu, "Nama tugas").grid(row=0, column=0, sticky="w", padx=kiri, pady=(28, 6))
        label(kartu, "Mata kuliah").grid(row=0, column=1, sticky="w", padx=kanan, pady=(28, 6))
        self.e_nama = kolom_input(kartu, "Tulis nama tugas")
        self.e_nama.grid(row=1, column=0, sticky="ew", padx=kiri)
        self.e_mk = kolom_input(kartu, "Tulis mata kuliah")
        self.e_mk.grid(row=1, column=1, sticky="ew", padx=kanan)

        label(kartu, "Tanggal tenggat").grid(row=2, column=0, sticky="w", padx=kiri, pady=(18, 6))
        label(kartu, "Status").grid(row=2, column=1, sticky="w", padx=kanan, pady=(18, 6))
        self.e_tenggat = kolom_input(kartu, "hh/bb/tttt")
        self.e_tenggat.grid(row=3, column=0, sticky="ew", padx=kiri)
        self.cb_status = ctk.CTkComboBox(
            kartu, values=list(STATUS_TUGAS), state="readonly", height=44, corner_radius=8,
            border_width=1, border_color=INPUT_BORDER, fg_color="white", text_color=NAVY,
            button_color=HEADER_BG, button_hover_color="#cfe2fb", font=f(14),
            dropdown_fg_color="white", dropdown_text_color=NAVY,
            dropdown_hover_color=HEADER_BG, dropdown_font=f(14))
        self.cb_status.grid(row=3, column=1, sticky="ew", padx=kanan)

        label(kartu, "Deskripsi").grid(row=4, column=0, columnspan=2, sticky="w", padx=36, pady=(18, 6))
        self.t_deskripsi = TextboxPlaceholder(kartu, "Tulis deskripsi tugas", height=100,
                                              corner_radius=8, border_width=1,
                                              border_color=INPUT_BORDER, fg_color="white",
                                              font=f(14))
        self.t_deskripsi.grid(row=5, column=0, columnspan=2, sticky="ew", padx=36, pady=(0, 32))

        self.baris_tombol = ctk.CTkFrame(self, fg_color="transparent")
        self.baris_tombol.pack(anchor="w", padx=70, pady=22)
        kw = dict(width=118, height=42, corner_radius=8)
        self.btn_tambah = tombol(self.baris_tombol, "Tambah", self.tambah, "biru", **kw)
        self.btn_edit = tombol(self.baris_tombol, "Edit", self.edit, "amber", **kw)
        self.btn_bersih = tombol(self.baris_tombol, "Bersihkan", self.bersihkan, "garis", **kw)
        self._atur_mode(False)

    # -------------------------------------------------------------- helper
    def _atur_mode(self, edit):
        for b in (self.btn_tambah, self.btn_edit, self.btn_bersih):
            b.pack_forget()
        (self.btn_edit if edit else self.btn_tambah).pack(side="left", padx=(0, 14))
        self.btn_bersih.pack(side="left")

    @staticmethod
    def _isi_entry(entry, teks):
        kosongkan(entry)
        if teks:
            entry.insert(0, teks)

    def _ambil(self):
        return (self.e_nama.get(), self.e_mk.get(), self.t_deskripsi.ambil(),
                self.e_tenggat.get(), self.cb_status.get())

    def on_show(self, tugas=None):
        if tugas:
            self.id_edit = tugas["id"]
            self._isi_entry(self.e_nama, tugas["nama_tugas"])
            self._isi_entry(self.e_mk, tugas["mata_kuliah"])
            self._isi_entry(self.e_tenggat, self.ctrl.tampil_tanggal(tugas["tenggat"]))
            self.cb_status.set(tugas["status"])
            self.t_deskripsi.isi(tugas["deskripsi"] or "")
            self.lbl_eyebrow.configure(text=f"MENGUBAH TUGAS NO. {tugas['no']:03d}")
            self._atur_mode(True)
        else:
            self.bersihkan()

    # -------------------------------------------------------------- aksi
    def tambah(self):
        ok, pesan = self.ctrl.tambah(*self._ambil())
        if ok:
            messagebox.showinfo("Sukses", pesan)
            self.bersihkan()
        else:
            messagebox.showwarning("Validasi", pesan)

    def edit(self):
        if self.id_edit is None:
            messagebox.showwarning("Peringatan", "Pilih tugas dari Daftar Tugas terlebih dahulu.")
            return
        ok, pesan = self.ctrl.edit(self.id_edit, *self._ambil())
        if ok:
            messagebox.showinfo("Sukses", pesan)
            self.bersihkan()
            self.app.tampil("daftar")
        else:
            messagebox.showwarning("Validasi", pesan)

    def bersihkan(self):
        self.id_edit = None
        for e in (self.e_nama, self.e_mk, self.e_tenggat):
            self._isi_entry(e, "")
        self.cb_status.set(self.TEKS_STATUS)
        self.t_deskripsi.isi("")
        self.lbl_eyebrow.configure(text="HALAMAN FORMULIR")
        self._atur_mode(False)
        self.focus()


# ===================================================== Dialog ubah status
class DialogStatus(ctk.CTkToplevel):
    def __init__(self, master, nama, status_sekarang, on_simpan):
        super().__init__(master, fg_color=BG)
        self.on_simpan = on_simpan
        self.title("Ubah Status")
        self.geometry("400x250")
        self.resizable(False, False)
        self.transient(master)

        ctk.CTkLabel(self, text="Ubah status tugas", font=f(18, True), text_color=NAVY,
                     anchor="w").pack(fill="x", padx=28, pady=(24, 0))
        ctk.CTkLabel(self, text=nama, font=f(13), text_color=MUTED, anchor="w",
                     justify="left", wraplength=340).pack(fill="x", padx=28, pady=(2, 14))
        self.var = ctk.StringVar(value=status_sekarang)
        ctk.CTkComboBox(self, values=list(STATUS_TUGAS), variable=self.var, state="readonly",
                        height=42, corner_radius=8, border_width=1, border_color=INPUT_BORDER,
                        fg_color="white", text_color=NAVY, button_color=HEADER_BG,
                        button_hover_color="#cfe2fb", font=f(14), dropdown_fg_color="white",
                        dropdown_text_color=NAVY, dropdown_hover_color=HEADER_BG,
                        dropdown_font=f(14)).pack(fill="x", padx=28)
        baris = ctk.CTkFrame(self, fg_color="transparent")
        baris.pack(anchor="w", padx=28, pady=24)
        tombol(baris, "Simpan", self._simpan, "biru", width=110, height=40, corner_radius=8).pack(side="left", padx=(0, 12))
        tombol(baris, "Batal", self.destroy, "garis", width=110, height=40, corner_radius=8).pack(side="left")
        self.after(150, self._fokus)

    def _fokus(self):
        try:
            self.grab_set()
            self.focus()
        except Exception:
            pass

    def _simpan(self):
        self.on_simpan(self.var.get())
        self.destroy()


# ============================================================== Halaman Daftar
# (weight, lebar minimum) tiap kolom: ID, Nama tugas, Mata kuliah, Tenggat, Status, Aksi
KOLOM = [(0, 80), (3, 170), (3, 170), (2, 120), (2, 165), (0, 310)]


def atur_kolom(frame):
    """Kolom berbobot diberi 'uniform' agar lebarnya identik di header dan semua baris."""
    for i, (bobot, minimal) in enumerate(KOLOM):
        frame.grid_columnconfigure(i, weight=bobot, minsize=minimal,
                                   uniform="data" if bobot else "")


class DaftarPage(Halaman):
    def __init__(self, master, app):
        super().__init__(master, app)
        buat_header(self, "HALAMAN DAFTAR", "Daftar Tugas", app)

        cari = ctk.CTkFrame(self, fg_color="transparent")
        cari.pack(fill="x", padx=70, pady=(0, 16))
        label(cari, "Pencarian").pack(side="left", padx=(0, 16))
        self.e_cari = kolom_input(cari, "Cari nama tugas atau mata kuliah", height=46)
        self.e_cari.pack(side="left", fill="x", expand=True)
        self.e_cari.bind("<KeyRelease>", lambda e: self.muat())

        kartu = ctk.CTkFrame(self, fg_color="white", corner_radius=14, border_width=1,
                             border_color=BORDER)
        kartu.pack(fill="both", expand=True, padx=70, pady=(0, 32))

        kepala = ctk.CTkFrame(kartu, fg_color=HEADER_BG, corner_radius=12)
        kepala.pack(fill="x", padx=1, pady=(1, 0))
        dalam = ctk.CTkFrame(kepala, fg_color="transparent")
        dalam.pack(fill="x", padx=(0, 17))   # sisakan ruang untuk scrollbar
        atur_kolom(dalam)
        for i, judul in enumerate(["ID", "Nama tugas", "Mata kuliah", "Tenggat", "Status", "Aksi"]):
            ctk.CTkLabel(dalam, text=judul, font=f(14, True), text_color=HEADER_FG,
                         anchor="w").grid(row=0, column=i, sticky="w",
                                          padx=(24 if i == 0 else 8, 8), pady=16)

        self.body = ctk.CTkScrollableFrame(
            kartu, fg_color="white", corner_radius=0, scrollbar_fg_color="white",
            scrollbar_button_color=BORDER, scrollbar_button_hover_color=INPUT_BORDER)
        self.body.pack(fill="both", expand=True, padx=1, pady=(0, 1))

    def on_show(self, **kwargs):
        kosongkan(self.e_cari)
        self.muat()

    def muat(self):
        kata = self.e_cari.get().strip()
        self._render(self.ctrl.cari(kata), bool(kata))

    def _render(self, data, ada_kata):
        for w in self.body.winfo_children():
            w.destroy()

        if not data:
            pesan = ("Tugas tidak ditemukan." if ada_kata
                     else "Belum ada tugas. Tambahkan melalui Formulir Tugas.")
            ctk.CTkLabel(self.body, text=pesan, font=f(15), text_color=MUTED).pack(pady=50)
            return

        for i, t in enumerate(data):
            baris = ctk.CTkFrame(self.body, fg_color="white" if i % 2 == 0 else ROW_ALT,
                                 corner_radius=0)
            baris.pack(fill="x")
            atur_kolom(baris)

            isi = [f"{t['no']:03d}", t["nama_tugas"], t["mata_kuliah"],
                   self.ctrl.tampil_tanggal(t["tenggat"]), t["status"]]
            for c, teks in enumerate(isi):
                ctk.CTkLabel(baris, text=teks, font=f(14), text_color=NAVY, anchor="w",
                             justify="left", wraplength=160 if c in (1, 2) else 0
                             ).grid(row=0, column=c, sticky="w",
                                    padx=(24 if c == 0 else 8, 8), pady=16)

            aksi = ctk.CTkFrame(baris, fg_color="transparent")
            aksi.grid(row=0, column=5, sticky="w", padx=(14, 8))
            kw = dict(height=38, corner_radius=8, font=f(13, True))
            tombol(aksi, "Edit", lambda t=t: self.edit(t), "amber", width=68, **kw).pack(side="left", padx=(0, 8))
            tombol(aksi, "Ubah Status", lambda t=t: self.ubah_status(t), "biru", width=108, **kw).pack(side="left", padx=(0, 8))
            tombol(aksi, "Hapus", lambda t=t: self.hapus(t), "merah", width=68, **kw).pack(side="left")

            ctk.CTkFrame(self.body, height=1, fg_color=BORDER, corner_radius=0).pack(fill="x")

    # -------------------------------------------------------------- aksi
    def edit(self, tugas):
        self.app.tampil("form", tugas=tugas)

    def ubah_status(self, tugas):
        DialogStatus(self.app, tugas["nama_tugas"], tugas["status"],
                     lambda status: self._simpan_status(tugas["id"], status))

    def _simpan_status(self, id_tugas, status):
        ok, pesan = self.ctrl.ubah_status(id_tugas, status)
        if ok:
            self.muat()
        else:
            messagebox.showerror("Gagal", pesan)

    def hapus(self, tugas):   # BR-05: wajib konfirmasi
        if not messagebox.askyesno("Konfirmasi Hapus",
                                   f"Yakin ingin menghapus tugas:\n\"{tugas['nama_tugas']}\" ?"):
            return
        ok, pesan = self.ctrl.hapus(tugas["id"])
        if ok:
            self.muat()   # nomor urut otomatis dihitung ulang
        else:
            messagebox.showerror("Gagal", pesan)


# ================================================================ Jendela utama
class TugasView(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG)
        self.controller = TugasController()
        self.title("Pengelolaan Tugas Mahasiswa")
        self.geometry("1200x720")
        self.minsize(1100, 680)

        wadah = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        wadah.pack(fill="both", expand=True)

        self.halaman = {
            "login": LoginPage(wadah, self),
            "dashboard": DashboardPage(wadah, self),
            "form": FormPage(wadah, self),
            "daftar": DaftarPage(wadah, self),
        }
        for h in self.halaman.values():
            h.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.tampil("login")

    def tampil(self, nama, **kwargs):
        h = self.halaman[nama]
        h.on_show(**kwargs)
        h.tkraise()


if __name__ == "__main__":
    TugasView().mainloop()