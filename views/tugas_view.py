import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime, date

import customtkinter as ctk
from tkinter import ttk, messagebox
from controllers.tugas_controller import TugasController

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

FORMAT_TANGGAL = "%Y-%m-%d"
FONT = "Segoe UI"

# Palet sederhana: satu warna aksen, sisanya netral (terang, gelap)
AKSEN = ("#2f5d8a", "#4a7fb0")
AKSEN_HOVER = ("#244a70", "#3b6a96")
BAHAYA = ("#b04a45", "#c0605a")
BAHAYA_HOVER = ("#8f3a36", "#a24e49")
LATAR = ("#f3f4f6", "#1e1f22")
KARTU = ("#ffffff", "#2a2b2f")
GARIS = ("#d5d8dd", "#3c3e43")
TEKS_REDUP = ("#6b7280", "#9aa0a8")


class TugasView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.controller = TugasController()
        self.selected_id = None   # ID asli dari database (dipakai untuk ubah/hapus)
        self.data_cache = {}      # {id_tugas: row dict}
        self.nomor = {}           # {id_tugas: nomor urut tampilan}

        self.title("Sistem Pengelolaan Tugas Mahasiswa")
        self.geometry("1100x600")
        self.minsize(950, 520)
        self.configure(fg_color=LATAR)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._buat_form()
        self._buat_tabel()
        self._atur_gaya_tabel()

        self.load_data()
        self._set_mode_edit(False)

    # ------------------------------------------------------------------ UI
    def _buat_form(self):
        self.frame_form = ctk.CTkFrame(self, width=330, corner_radius=8, fg_color=KARTU,
                                       border_width=1, border_color=GARIS)
        self.frame_form.grid(row=0, column=0, padx=(14, 7), pady=14, sticky="nsew")
        self.frame_form.grid_propagate(False)

        ctk.CTkLabel(self.frame_form, text="Data Tugas", anchor="w",
                     font=ctk.CTkFont(FONT, 18, "bold")).pack(fill="x", padx=20, pady=(20, 0))
        self.label_mode = ctk.CTkLabel(self.frame_form, text="", anchor="w",
                                       font=ctk.CTkFont(FONT, 12), text_color=TEKS_REDUP)
        self.label_mode.pack(fill="x", padx=20, pady=(0, 14))

        self._label("Judul")
        self.entry_judul = ctk.CTkEntry(self.frame_form, height=34, corner_radius=6,
                                        font=ctk.CTkFont(FONT, 13), border_color=GARIS,
                                        placeholder_text="Contoh: Praktikum Modul 3")
        self.entry_judul.pack(padx=20, pady=(2, 12), fill="x")

        self._label("Deskripsi")
        self.entry_deskripsi = ctk.CTkTextbox(self.frame_form, height=120, corner_radius=6,
                                              font=ctk.CTkFont(FONT, 13), border_width=2,
                                              border_color=GARIS)
        self.entry_deskripsi.pack(padx=20, pady=(2, 12), fill="x")

        self._label("Deadline")
        self.entry_deadline = ctk.CTkEntry(self.frame_form, height=34, corner_radius=6,
                                           font=ctk.CTkFont(FONT, 13), border_color=GARIS,
                                           placeholder_text="YYYY-MM-DD")
        self.entry_deadline.pack(padx=20, pady=(2, 20), fill="x")

        # Semua tombol dibuat di sini, ditampilkan sesuai mode
        self.frame_tombol = ctk.CTkFrame(self.frame_form, fg_color="transparent")
        self.frame_tombol.pack(fill="x", padx=20)

        kw = dict(height=36, corner_radius=6, font=ctk.CTkFont(FONT, 13))
        self.btn_tambah = ctk.CTkButton(self.frame_tombol, text="Tambah", command=self.clear_form,
                                        fg_color="transparent", border_width=1, border_color=AKSEN,
                                        text_color=AKSEN, hover_color=("#e6edf5", "#2f3a47"), **kw)
        self.btn_simpan = ctk.CTkButton(self.frame_tombol, text="Simpan", command=self.simpan_data,
                                        fg_color=AKSEN, hover_color=AKSEN_HOVER, **kw)
        self.btn_ubah = ctk.CTkButton(self.frame_tombol, text="Ubah", command=self.ubah_data,
                                      fg_color=AKSEN, hover_color=AKSEN_HOVER, **kw)
        self.btn_hapus = ctk.CTkButton(self.frame_tombol, text="Hapus", command=self.hapus_data,
                                       fg_color=BAHAYA, hover_color=BAHAYA_HOVER, **kw)

    def _label(self, teks):
        ctk.CTkLabel(self.frame_form, text=teks, anchor="w", font=ctk.CTkFont(FONT, 12),
                     text_color=TEKS_REDUP).pack(fill="x", padx=22)

    def _buat_tabel(self):
        self.frame_tabel = ctk.CTkFrame(self, corner_radius=8, fg_color=KARTU,
                                        border_width=1, border_color=GARIS)
        self.frame_tabel.grid(row=0, column=1, padx=(7, 14), pady=14, sticky="nsew")
        self.frame_tabel.grid_columnconfigure(0, weight=1)
        self.frame_tabel.grid_rowconfigure(1, weight=1)

        bar = ctk.CTkFrame(self.frame_tabel, fg_color="transparent")
        bar.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))
        bar.grid_columnconfigure(0, weight=1)

        self.entry_cari = ctk.CTkEntry(bar, height=34, corner_radius=6, border_color=GARIS,
                                       font=ctk.CTkFont(FONT, 13),
                                       placeholder_text="Cari judul atau deskripsi")
        self.entry_cari.grid(row=0, column=0, sticky="ew")
        # bind KeyRelease (bukan textvariable) supaya placeholder tetap tampil
        self.entry_cari.bind("<KeyRelease>", lambda e: self.tampilkan_data())

        self.label_jumlah = ctk.CTkLabel(bar, text="0 tugas", font=ctk.CTkFont(FONT, 12),
                                         text_color=TEKS_REDUP)
        self.label_jumlah.grid(row=0, column=1, padx=(14, 0))

        wadah = ctk.CTkFrame(self.frame_tabel, fg_color="transparent")
        wadah.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 8))
        wadah.grid_columnconfigure(0, weight=1)
        wadah.grid_rowconfigure(0, weight=1)

        kolom = ("No", "Judul", "Deskripsi", "Deadline", "Status")
        self.tree = ttk.Treeview(wadah, columns=kolom, show="headings", selectmode="browse")
        for nama, lebar, rata, stretch in [
            ("No", 55, "center", False),
            ("Judul", 190, "w", False),
            ("Deskripsi", 290, "w", True),
            ("Deadline", 105, "center", False),
            ("Status", 110, "center", False),
        ]:
            self.tree.heading(nama, text=nama, anchor=rata)
            self.tree.column(nama, width=lebar, anchor=rata, stretch=stretch)

        scroll = ctk.CTkScrollbar(wadah, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns", padx=(4, 0))

        self.tree.bind("<<TreeviewSelect>>", self.pilih_baris)
        self.tree.bind("<Button-1>", self.klik_tabel, add="+")

        ctk.CTkLabel(self.frame_tabel, anchor="w", font=ctk.CTkFont(FONT, 11),
                     text_color=TEKS_REDUP,
                     text="Klik tugas untuk mengubah atau menghapus. Klik area kosong untuk kembali menambah."
                     ).grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 12))

    def _atur_gaya_tabel(self):
        gelap = ctk.get_appearance_mode() == "Dark"
        bg = "#2a2b2f" if gelap else "#ffffff"
        fg = "#e6e6e6" if gelap else "#1f2937"
        head_bg = "#35373c" if gelap else "#eef0f3"
        head_fg = "#e6e6e6" if gelap else "#374151"
        seleksi = "#3b5b80" if gelap else "#dbe6f2"
        genap = "#2f3034" if gelap else "#f8f9fa"

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=bg, fieldbackground=bg, foreground=fg,
                        rowheight=32, borderwidth=0, font=(FONT, 10))
        style.configure("Treeview.Heading", background=head_bg, foreground=head_fg,
                        font=(FONT, 10, "bold"), relief="flat", padding=(6, 8), borderwidth=0)
        style.map("Treeview", background=[("selected", seleksi)],
                  foreground=[("selected", fg)])
        style.map("Treeview.Heading", background=[("active", head_bg)])

        self.tree.tag_configure("ganjil", background=bg)
        self.tree.tag_configure("genap", background=genap)
        self.tree.tag_configure("lewat", foreground="#c0392b" if not gelap else "#e07a72")
        self.tree.tag_configure("segera", foreground="#b9770e" if not gelap else "#e0a24a")

    # --------------------------------------------------------------- Data
    def load_data(self):
        """Ambil data dari controller, urutkan berdasarkan ID, lalu tampilkan."""
        try:
            data = self.controller.get_daftar_tugas() or []
        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal memuat data:\n{e}")
            data = []

        data = sorted(data, key=lambda r: int(r["id_tugas"]))
        self.data_cache = {int(r["id_tugas"]): r for r in data}
        # Nomor tampilan selalu 1..n tanpa bolong, ID asli tidak diubah
        self.nomor = {id_: i for i, id_ in enumerate(self.data_cache, start=1)}
        self.tampilkan_data()

    def tampilkan_data(self):
        kata = self.entry_cari.get().strip().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)

        tampil = 0
        for id_tugas, row in self.data_cache.items():
            judul = str(row["judul_tugas"] or "")
            deskripsi = str(row["deskripsi"] or "")
            if kata and kata not in judul.lower() and kata not in deskripsi.lower():
                continue

            deadline = str(row["deadline"] or "")[:10]
            status, tag_status = self._hitung_status(deadline)
            tag_baris = "genap" if tampil % 2 else "ganjil"
            tags = (tag_baris, tag_status) if tag_status else (tag_baris,)

            # iid = ID asli, kolom pertama = nomor urut tampilan
            self.tree.insert("", "end", iid=str(id_tugas), tags=tags,
                             values=(self.nomor[id_tugas], judul,
                                     deskripsi.replace("\n", " "), deadline, status))
            tampil += 1

        self.label_jumlah.configure(text=f"{tampil} tugas")

        if self.selected_id is not None and self.tree.exists(str(self.selected_id)):
            self.tree.selection_set(str(self.selected_id))

    @staticmethod
    def _hitung_status(deadline_str):
        try:
            tgl = datetime.strptime(deadline_str, FORMAT_TANGGAL).date()
        except ValueError:
            return "-", None
        selisih = (tgl - date.today()).days
        if selisih < 0:
            return "Terlambat", "lewat"
        if selisih == 0:
            return "Hari ini", "segera"
        if selisih <= 3:
            return f"{selisih} hari lagi", "segera"
        return f"{selisih} hari lagi", None

    # --------------------------------------------------------- Helper form
    def _ambil_input(self):
        judul = self.entry_judul.get().strip()
        deskripsi = self.entry_deskripsi.get("0.0", "end").strip()
        deadline = self.entry_deadline.get().strip()

        if not judul:
            messagebox.showwarning("Validasi", "Judul tugas tidak boleh kosong.")
            self.entry_judul.focus()
            return None
        if not deadline:
            messagebox.showwarning("Validasi", "Deadline tidak boleh kosong.")
            self.entry_deadline.focus()
            return None
        try:
            datetime.strptime(deadline, FORMAT_TANGGAL)
        except ValueError:
            messagebox.showwarning(
                "Validasi", "Format deadline harus YYYY-MM-DD dan tanggalnya valid.\nContoh: 2026-10-31")
            self.entry_deadline.focus()
            return None
        return judul, deskripsi, deadline

    def _isi_form(self, judul="", deskripsi="", deadline=""):
        # Entry hanya di-insert bila ada isinya, supaya placeholder muncul kembali saat kosong
        self.entry_judul.delete(0, "end")
        if judul:
            self.entry_judul.insert(0, judul)
        self.entry_deskripsi.delete("0.0", "end")
        if deskripsi:
            self.entry_deskripsi.insert("0.0", deskripsi)
        self.entry_deadline.delete(0, "end")
        if deadline:
            self.entry_deadline.insert(0, deadline)

    def _set_mode_edit(self, edit: bool):
        """Mode tambah: Tambah + Simpan. Mode edit: Tambah + Ubah + Hapus."""
        for btn in (self.btn_tambah, self.btn_simpan, self.btn_ubah, self.btn_hapus):
            btn.pack_forget()

        self.btn_tambah.pack(pady=4, fill="x")
        if edit:
            self.btn_ubah.pack(pady=4, fill="x")
            self.btn_hapus.pack(pady=4, fill="x")
            self.label_mode.configure(text=f"Mengubah tugas No. {self.nomor.get(self.selected_id, '-')}")
        else:
            self.btn_simpan.pack(pady=4, fill="x")
            self.label_mode.configure(text="Tambah tugas baru")

    # ------------------------------------------------------------- Aksi
    def simpan_data(self):
        hasil = self._ambil_input()
        if hasil is None:
            return
        if self.controller.tambah_tugas(*hasil):
            messagebox.showinfo("Sukses", "Data tugas berhasil disimpan!")
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Gagal", "Data gagal disimpan. Periksa koneksi database.")

    def ubah_data(self):
        if self.selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih tugas pada tabel terlebih dahulu!")
            return
        hasil = self._ambil_input()
        if hasil is None:
            return
        if self.controller.perbarui_tugas(self.selected_id, *hasil):
            messagebox.showinfo("Sukses", "Data tugas berhasil diperbarui!")
            self.clear_form()
            self.load_data()
        else:
            messagebox.showerror("Gagal", "Gagal memperbarui data.")

    def hapus_data(self):
        if self.selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih tugas pada tabel terlebih dahulu!")
            return
        judul = self.entry_judul.get().strip() or f"No. {self.nomor.get(self.selected_id)}"
        if not messagebox.askyesno("Konfirmasi Hapus", f"Yakin ingin menghapus tugas:\n\"{judul}\" ?"):
            return
        if self.controller.hapus_tugas(self.selected_id):
            messagebox.showinfo("Sukses", "Data tugas berhasil dihapus!")
            self.clear_form()
            self.load_data()   # nomor otomatis dihitung ulang, jadi tetap urut
        else:
            messagebox.showerror("Gagal", "Gagal menghapus data.")

    def pilih_baris(self, event=None):
        pilihan = self.tree.selection()
        if not pilihan:
            return
        id_tugas = int(pilihan[0])
        row = self.data_cache.get(id_tugas)
        if row is None:
            return
        self.selected_id = id_tugas
        self._isi_form(str(row["judul_tugas"] or ""),
                       str(row["deskripsi"] or ""),
                       str(row["deadline"] or "")[:10])
        self._set_mode_edit(True)

    def klik_tabel(self, event):
        """Klik area kosong pada tabel -> kembali ke mode tambah."""
        if not self.tree.identify_row(event.y) and self.selected_id is not None:
            self.clear_form()

    def clear_form(self):
        self.selected_id = None
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())
        self._isi_form()
        self._set_mode_edit(False)
        self.focus()   # lepas fokus dari entry agar placeholder tampil


if __name__ == "__main__":
    app = TugasView()
    app.mainloop()