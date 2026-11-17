"""
app.py
Entry point aplikasi SITAMA — Sistem Pengelolaan Tugas Mahasiswa.
Menampilkan splash screen sebelum masuk ke halaman Login.
"""

import os
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageOps

from views.tugas_view import TugasView, LOGO_PATH


def _buat_logo_bundar(path, ukuran=120):
    if not os.path.exists(path):
        return None
    img = Image.open(path).convert("RGBA")
    besar = ukuran * 4
    img = ImageOps.fit(img, (besar, besar), method=Image.LANCZOS)
    mask = Image.new("L", (besar, besar), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, besar, besar), fill=255)
    img.putalpha(mask)
    return img.resize((ukuran, ukuran), Image.LANCZOS)


def tampilkan_splash(app, path_logo, on_selesai, durasi_ms=2200):
    app.withdraw()

    splash = ctk.CTkToplevel(app)
    splash.overrideredirect(True)
    splash.configure(fg_color="#FFFFFF")       # cegah latar hitam bawaan sistem
    lebar, tinggi = 340, 400
    sx = (splash.winfo_screenwidth() - lebar) // 2
    sy = (splash.winfo_screenheight() - tinggi) // 2
    splash.geometry(f"{lebar}x{tinggi}+{sx}+{sy}")
    splash.attributes("-topmost", True)

    # Bingkai menutup SELURUH jendela, tanpa celah -> tidak ada warna hitam yang tembus
    bingkai = ctk.CTkFrame(splash, fg_color="#FFFFFF", corner_radius=0)
    bingkai.pack(fill="both", expand=True)

    logo_img = _buat_logo_bundar(path_logo, 120)
    lbl_logo = ctk.CTkLabel(bingkai, text="", width=120, height=120)
    if logo_img:
        lbl_logo.configure(image=ctk.CTkImage(logo_img, size=(120, 120)))
    lbl_logo.pack(pady=(70, 18))

    ctk.CTkLabel(bingkai, text="SITAMA", font=("Segoe UI", 20, "bold"),
                 text_color="#1B2340").pack()
    ctk.CTkLabel(bingkai, text="Sistem Pengelolaan Tugas Mahasiswa",
                 font=("Segoe UI", 11), text_color="#8E93A6").pack(pady=(2, 28))

    bar = ctk.CTkProgressBar(bingkai, width=220, height=6,
                              progress_color="#3D6CF6", fg_color="#EEF0F6")
    bar.set(0)
    bar.pack(pady=(0, 10))

    lbl_status = ctk.CTkLabel(bingkai, text="Memuat...", font=("Segoe UI", 10),
                               text_color="#8E93A6")
    lbl_status.pack()

    splash.update_idletasks()
    splash.deiconify()
    splash.lift()
    splash.focus_force()

    langkah = {"n": 0}
    total_langkah = 40
    pesan_tahap = ["Memuat...", "Menyiapkan data...", "Hampir selesai..."]

    def animasi():
        langkah["n"] += 1
        progres = min(langkah["n"] / total_langkah, 1.0)
        try:
            bar.set(progres)
            if progres < 0.4:
                lbl_status.configure(text=pesan_tahap[0])
            elif progres < 0.8:
                lbl_status.configure(text=pesan_tahap[1])
            else:
                lbl_status.configure(text=pesan_tahap[2])
        except Exception:
            pass
        if langkah["n"] < total_langkah:
            splash.after(max(1, durasi_ms // total_langkah), animasi)
        else:
            tutup()

    def tutup():
        try:
            if splash.winfo_exists():
                splash.destroy()
        except Exception:
            pass
        app.deiconify()
        app.lift()
        app.focus_force()
        app.attributes("-topmost", True)
        app.after(200, lambda: app.attributes("-topmost", False))
        on_selesai()

    splash.after(durasi_ms + 800, tutup)   # timer pengaman: paksa tutup walau animasi gagal
    splash.after(30, animasi)


if __name__ == "__main__":
    app = TugasView()
    tampilkan_splash(app, LOGO_PATH, lambda: app.tampil("LoginPage"))
    app.mainloop()