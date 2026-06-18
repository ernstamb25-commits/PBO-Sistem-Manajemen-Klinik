import ctypes
from database import DatabaseKlinik
from gui import KlinikApp

# from database import init_data 

def main():
    # Tampilan GUI mengikuti skala DPI monitor
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    db = DatabaseKlinik()       
    db2 = DatabaseKlinik()      
    assert db is db2, "Singleton gagal!"

    # Muat dari file .pkl
    if not db.load_data():
        print("Data tidak ditemukan, memuat data awal...")
    else:
        print("Data berhasil dimuat dari data_klinik.pkl")

    app = KlinikApp(db)
    app.mainloop()
    
    # Simpan data terakhir saat aplikasi ditutup
    db.save_data()

if __name__ == "__main__":
    main()