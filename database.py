import uuid
import pickle
import os
from models import Pasien, Dokter, Obat, Resep, Antrian

# =====================================================
# SINGLETON: DatabaseKlinik
# =====================================================
class DatabaseKlinik:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        self.id = "DB-" + str(uuid.uuid4())[:8].upper()
        self._pasien: list[Pasien] = []
        self._dokter: list[Dokter] = []
        self._antrian: list[Antrian] = []
        self._obat: list[Obat] = []
        self._resep: list[Resep] = []
        self._nomor_antrian = 1

    # === FUNGSI PENYIMPANAN KE FILE ===
    def save_data(self):
        data = {
            'pasien': self._pasien,
            'dokter': self._dokter,
            'antrian': self._antrian,
            'obat': self._obat,
            'resep': self._resep,
            'nomor_antrian': self._nomor_antrian
        }
        with open('data_klinik.pkl', 'wb') as f:
            pickle.dump(data, f)

    def load_data(self) -> bool:
        if os.path.exists('data_klinik.pkl'):
            with open('data_klinik.pkl', 'rb') as f:
                data = pickle.load(f)
                self._pasien = data['pasien']
                self._dokter = data['dokter']
                self._antrian = data['antrian']
                self._obat = data['obat']
                self._resep = data['resep']
                self._nomor_antrian = data['nomor_antrian']
                return True
        return False

    # --- Pasien ---
    def tambah_pasien(self, p: Pasien): 
        self._pasien.append(p)
        self.save_data()
        
    def get_pasien(self) -> list: return self._pasien
    
    def cari_pasien(self, id_p: str) -> Pasien:
        return next((p for p in self._pasien if p.id_pasien == id_p), None)

    def update_pasien(self, id_p: str, nama: str, tgl_lahir: str, jalan: str, kota: str, kpos: str, no_telp: str):
        pasien = self.cari_pasien(id_p)
        if pasien:
            from models import Alamat 
            pasien.nama = nama
            pasien.tgl_lahir = tgl_lahir
            pasien.alamat = Alamat(jalan, kota, kpos)
            pasien.no_telp = no_telp
            self.save_data()
            return True
        return False

    def hapus_pasien(self, id_p: str) -> bool:
        pasien = self.cari_pasien(id_p)
        if pasien:
            self._pasien.remove(pasien) 
            self.save_data()
            return True
        return False

    # --- Dokter ---
    def tambah_dokter(self, d: Dokter): 
        self._dokter.append(d)
        self.save_data()
        
    def get_dokter(self) -> list: return self._dokter
    
    def cari_dokter(self, id_d: str) -> Dokter:
        return next((d for d in self._dokter if d.id_pegawai == id_d), None)

    def update_dokter(self, id_d: str, nama: str, spesialisasi: str, hari: str, j1: str, j2: str, kelipatan: float) -> bool:
        d = self.cari_dokter(id_d)
        if d:
            from models import JadwalPraktek
            d.nama = nama
            d.spesialisasi = spesialisasi
            d.jadwal = JadwalPraktek(hari, j1, j2)
            if hasattr(d, 'kelipatan'):
                d.kelipatan = kelipatan
            self.save_data()
            return True
        return False

    def hapus_dokter(self, id_d: str) -> bool:
        d = self.cari_dokter(id_d)
        if d:
            self._dokter.remove(d)
            self.save_data()
            return True
        return False

    # --- Obat ---
    def tambah_obat(self, o: Obat): 
        self._obat.append(o)
        self.save_data()
        
    def get_obat(self) -> list: return self._obat
    
    def cari_obat(self, id_o: str) -> Obat:
        return next((o for o in self._obat if o.id_obat == id_o), None)
    def update_obat(self, id_o: str, nama: str, satuan: str, harga: int, stok: int) -> bool:
        o = self.cari_obat(id_o)
        if o:
            o.nama = nama
            o.satuan = satuan
            o.harga = harga
            o.stok = stok
            self.save_data()
            return True
        return False

    def hapus_obat(self, id_o: str) -> bool:
        o = self.cari_obat(id_o)
        if o:
            self._obat.remove(o)
            self.save_data()
            return True
        return False

    # --- Antrian ---
    def tambah_antrian(self, a: Antrian): 
        self._antrian.append(a)
        self.save_data()
        
    def get_antrian(self) -> list: return self._antrian
    
    def next_nomor(self) -> int:
        # Cek jika daftar antrian kosong, reset counter kembali ke 1
        if len(self._antrian) == 0:
            self._nomor_antrian = 1
            
        n = self._nomor_antrian
        self._nomor_antrian += 1
        self.save_data()
        return n

    def hapus_antrian(self, nomor: int) -> bool:
        antrian = next((a for a in self._antrian if a.nomor == nomor), None)
        if antrian:
            self._antrian.remove(antrian)
            self.save_data()
            return True
        return False

    # --- Resep ---
    def tambah_resep(self, r: Resep): 
        self._resep.append(r)
        self.save_data()
        
    def get_resep(self) -> list: return self._resep

    def cari_resep(self, id_r: str):
        return next((r for r in self._resep if r.id_resep == id_r), None)

    def update_resep(self, id_r: str, pasien_baru, dokter_baru) -> bool:
        resep = self.cari_resep(id_r)
        if resep:
            resep.pasien = pasien_baru
            resep.dokter = dokter_baru
            self.save_data()
            return True
        return False

    def hapus_resep(self, id_r: str) -> bool:
        resep = self.cari_resep(id_r)
        if resep:
            self._resep.remove(resep)
            self.save_data()
            return True
        return False