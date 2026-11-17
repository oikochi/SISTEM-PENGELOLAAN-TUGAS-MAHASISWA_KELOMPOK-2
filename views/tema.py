"""
tema.py
Palet warna, font, dan ukuran standar untuk seluruh tampilan SITAMA.
Palet warna mengikuti style guide referensi (biru indigo + aksen kuning).
"""

# ---------- WARNA UTAMA ----------
WARNA_UTAMA = "#2B318A"          # navy/indigo gelap - sidebar, header, judul
WARNA_UTAMA_HOVER = "#232869"

WARNA_LATAR = "#F2F5FF"          # latar halaman, sangat lembut
WARNA_KARTU = "#FFFFFF"

WARNA_TEKS = "#1F1F1F"
WARNA_TEKS_SEKUNDER = "#6A6E83"

WARNA_AKSEN = "#5A81FA"          # biru utama - tombol aksi, link
WARNA_AKSEN_HOVER = "#4468E0"

WARNA_ABU = "#F7F8FC"
WARNA_ABU_HOVER = "#EDEFFA"

WARNA_BAHAYA = "#E5484D"
WARNA_BAHAYA_HOVER = "#C53D42"

WARNA_SUKSES = "#1CA672"
WARNA_PERINGATAN = "#FBB03B"     # kuning dari style guide

# Palet warna-warni untuk badge mata kuliah/kategori (konsisten per teks)
PALET_KATEGORI = ["#5A81FA", "#2B318A", "#FBB03B", "#6A6E83", "#9B59B6", "#1ABC9C", "#E67E22"]

# ---------- FONT ----------
FONT_JUDUL = ("Segoe UI", 22, "bold")
FONT_SUBJUDUL = ("Segoe UI", 13)
FONT_LABEL = ("Segoe UI", 12)
FONT_LABEL_TEBAL = ("Segoe UI", 12, "bold")
FONT_ANGKA = ("Segoe UI", 24, "bold")
FONT_KECIL = ("Segoe UI", 10)

# ---------- UKURAN ----------
LEBAR_INPUT = 280
LEBAR_TOMBOL = 180
RADIUS = 16


def warna_kategori(teks):
    """Warna aksen konsisten untuk sebuah mata kuliah/kategori, dipilih dari hash teksnya."""
    if not teks:
        return WARNA_UTAMA
    indeks = sum(ord(c) for c in teks) % len(PALET_KATEGORI)
    return PALET_KATEGORI[indeks]


def warna_status(status):
    """Warna semantik untuk status tugas (dipakai di progress bar & label status)."""
    pemetaan = {
        "Belum Dikerjakan": WARNA_BAHAYA,
        "Sedang Dikerjakan": WARNA_PERINGATAN,
        "Selesai": WARNA_SUKSES,
    }
    return pemetaan.get(status, WARNA_TEKS_SEKUNDER)