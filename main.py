from database import DatabaseKlinik
from gui import KlinikApp

# Jika Anda tidak ingin menggunakan init_data sama sekali, 
# Anda bisa menghapus import init_data di bawah ini
# from database import init_data 

def main():
    db = DatabaseKlinik()       
    db2 = DatabaseKlinik()      
    assert db is db2, "Singleton gagal!"

    # Coba muat data dari file .pkl
    if not db.load_data():
        print("Data tidak ditemukan, memuat data awal...")
        # Jika Anda masih ingin ada data default saat pertama kali install:
        # init_data(db) 
        # db.save_data()
    else:
        print("Data berhasil dimuat dari data_klinik.pkl")

    app = KlinikApp(db)
    app.mainloop()
    
    # Simpan data terakhir saat aplikasi ditutup
    db.save_data()

if __name__ == "__main__":
    main()