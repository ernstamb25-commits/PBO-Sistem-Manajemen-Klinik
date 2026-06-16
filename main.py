from datetime import date
from models import Alamat, JadwalPraktek, DokterFactory, Pasien, Obat, Resep, Antrian
from database import DatabaseKlinik
from gui import KlinikApp

# =====================================================
# INISIALISASI DATA CONTOH
# =====================================================
def init_data(db: DatabaseKlinik):
    # Jadwal
    j1 = JadwalPraktek("Senin-Jumat", "08:00", "14:00")
    j2 = JadwalPraktek("Selasa-Sabtu", "14:00", "20:00")
    j3 = JadwalPraktek("Senin-Kamis", "09:00", "15:00")

    # Alamat
    a_klinik = Alamat("Jl. Sudirman No.15", "Yogyakarta", "55224")

    # Dokter via Factory
    d1 = DokterFactory.buat("umum", "D001", "dr. Budi Santoso",
                             Alamat("Jl. Melati 3", "Yogyakarta", "55225"), "Umum", j1)
    d2 = DokterFactory.buat("spesialis", "D002", "dr. Sari Dewi, Sp.JP",
                             Alamat("Jl. Mawar 7", "Yogyakarta", "55226"), "Jantung", j2, 3.0)
    d3 = DokterFactory.buat("spesialis", "D003", "dr. Ahmad Fauzi, Sp.A",
                             Alamat("Jl. Anggrek 12", "Yogyakarta", "55227"), "Anak", j3, 2.5)
    d4 = DokterFactory.buat("spesialis", "D004", "dr. Rina Kusuma, Sp.OG",
                             Alamat("Jl. Kamboja 5", "Yogyakarta", "55228"), "Kandungan", j1, 2.8)
    for d in [d1, d2, d3, d4]:
        db.tambah_dokter(d)

    # Pasien
    p1 = Pasien("P001", "Agus Prasetyo", "1990-05-12",
                Alamat("Jl. Wates 22", "Yogyakarta", "55231"), "0812-3456-7890")
    p2 = Pasien("P002", "Dewi Rahayu", "2005-08-30",
                Alamat("Jl. Kaliurang 88", "Yogyakarta", "55232"), "0813-9876-5432")
    p3 = Pasien("P003", "Hendra Wijaya", "1978-11-03",
                Alamat("Jl. Solo 45", "Yogyakarta", "55233"), "0815-1122-3344")
    p4 = Pasien("P004", "Siti Nurhaliza", "1995-02-18",
                Alamat("Jl. Parangtritis 10", "Yogyakarta", "55234"), "0819-8877-6655")
    for p in [p1, p2, p3, p4]:
        db.tambah_pasien(p)

    # Obat
    o1 = Obat("OBT001", "Amoksisilin 500mg", "kapsul", 5_000, 200)
    o2 = Obat("OBT002", "Paracetamol 500mg", "tablet", 2_000, 500)
    o3 = Obat("OBT003", "Omeprazol 20mg",    "kapsul", 8_000, 150)
    o4 = Obat("OBT004", "Captopril 25mg",    "tablet", 6_000, 300)
    for o in [o1, o2, o3, o4]:
        db.tambah_obat(o)

    # Resep contoh
    r1 = Resep("RX001", p1, d1, str(date.today()))
    r1.tambah_obat(o2, 10, "3x1 sesudah makan")
    r1.tambah_obat(o1, 14, "2x1 selama 7 hari")
    db.tambah_resep(r1)

    # Antrian
    db.tambah_antrian(Antrian(db.next_nomor(), p1, d1, "09:00", "dalam perawatan"))
    db.tambah_antrian(Antrian(db.next_nomor(), p2, d3, "09:30", "menunggu"))
    db.tambah_antrian(Antrian(db.next_nomor(), p3, d2, "10:00", "menunggu"))
    db.tambah_antrian(Antrian(db.next_nomor(), p4, d1, "10:30", "menunggu"))


# =====================================================
# MAIN
# =====================================================
def main():
    db = DatabaseKlinik()       # Singleton — instance pertama dibuat
    db2 = DatabaseKlinik()      # Singleton — mengembalikan instance yang sama
    assert db is db2, "Singleton gagal!"

    # Coba muat data yang tersimpan. Jika tidak ada, pakai data awal (init_data) lalu simpan.
    if not db.load_data():
        init_data(db)
        db.save_data()

    app = KlinikApp(db)
    app.mainloop()
    
    # Pastikan data tersimpan saat aplikasi ditutup
    db.save_data()


if __name__ == "__main__":
    main()