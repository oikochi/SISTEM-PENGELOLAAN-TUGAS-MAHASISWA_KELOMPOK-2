import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from controllers.tugas_controller import TugasController


def test_tambah_dan_tampilkan_tugas():
    controller = TugasController()
    berhasil, pesan = controller.tambah(
        "Tugas CI Test", "Mata Kuliah Uji", "Deskripsi otomatis dari pipeline",
        "31/12/2026", "Belum Dikerjakan"
    )
    assert berhasil is True

    data = controller.tampilkan()
    assert any(t["nama_tugas"] == "Tugas CI Test" for t in data)


def test_validasi_tanggal_salah():
    controller = TugasController()
    berhasil, pesan = controller.tambah(
        "Tugas Invalid", "Mata Kuliah", "", "tanggal-ngasal", "Belum Dikerjakan"
    )
    assert berhasil is False


def test_validasi_nama_kosong():
    controller = TugasController()
    berhasil, pesan = controller.tambah(
        "", "Mata Kuliah", "", "31/12/2026", "Belum Dikerjakan"
    )
    assert berhasil is False