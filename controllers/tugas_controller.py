from models.tugas_model import TugasModel

class TugasController:
    def __init__(self):
        self.model = TugasModel()

    def get_daftar_tugas(self):
        return self.model.get_all_tugas()

    def tambah_tugas(self, judul, deskripsi, deadline):
        if judul and deadline:
            return self.model.create_tugas(judul, deskripsi, deadline)
        return False

    def perbarui_tugas(self, id_tugas, judul, deskripsi, deadline):
        if id_tugas and judul:
            return self.model.update_tugas(id_tugas, judul, deskripsi, deadline)
        return False

    def hapus_tugas(self, id_tugas):
        if id_tugas:
            return self.model.delete_tugas(id_tugas)
        return False