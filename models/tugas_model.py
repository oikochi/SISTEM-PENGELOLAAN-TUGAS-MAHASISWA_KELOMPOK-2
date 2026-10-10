from config.database import Database

class TugasModel:
    def __init__(self):
        db = Database()
        self.conn = db.get_connection()
        self.table_name = "tugas"

    def get_all_tugas(self):
        cursor = self.conn.cursor(dictionary=True)
        query = f"SELECT * FROM {self.table_name}"
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def create_tugas(self, judul, deskripsi, deadline):
        cursor = self.conn.cursor()
        query = f"INSERT INTO {self.table_name} (judul_tugas, deskripsi, deadline) VALUES (%s, %s, %s)"
        cursor.execute(query, (judul, deskripsi, deadline))
        self.conn.commit()
        cursor.close()
        return True

    def update_tugas(self, id_tugas, judul, deskripsi, deadline):
        cursor = self.conn.cursor()
        query = f"UPDATE {self.table_name} SET judul_tugas = %s, deskripsi = %s, deadline = %s WHERE id_tugas = %s"
        cursor.execute(query, (judul, deskripsi, deadline, id_tugas))
        self.conn.commit()
        cursor.close()
        return True

    def delete_tugas(self, id_tugas):
        cursor = self.conn.cursor()
        query = f"DELETE FROM {self.table_name} WHERE id_tugas = %s"
        cursor.execute(query, (id_tugas,))
        self.conn.commit()
        cursor.close()
        return True