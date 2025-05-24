# test_db_helper.py
from dbHelper import DBHelper

def print_all_tasks(db):
    tasks = db.lihat_semua_tugas()
    for t in tasks:
        print(t)

if __name__ == "__main__":
    # Make sure your DBHelper uses __init__ not _init_
    db = DBHelper("testuser@example.com")

    print("Tambah tugas...")
    db.tambah_tugas("Tugas 1", "Deskripsi tugas 1", "2025-06-01 10:00")
    db.tambah_tugas("Tugas 2", "Deskripsi tugas 2", "2025-06-02 12:00")
    print_all_tasks(db)

    print("\nEdit tugas id 1...")
    db.edit_tugas(1, "Deskripsi tugas 1 diubah", "2025-06-03 15:00")
    print_all_tasks(db)

    print("\nHapus tugas id 2...")
    db.hapus_tugas(2)
    print_all_tasks(db)