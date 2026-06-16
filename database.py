import uuid
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

    # --- Pasien ---
    def tambah_pasien(self, p: Pasien): self._pasien.append(p)
    def get_pasien(self) -> list: return self._pasien
    def cari_pasien(self, id_p: str) -> Pasien:
        return next((p for p in self._pasien if p.id_pasien == id_p), None)

    # === KODE YANG DITAMBAHKAN ===
    def update_pasien(self, id_p: str, nama: str, tgl_lahir: str, jalan: str, kota: str, kpos: str, no_telp: str):
        pasien = self.cari_pasien(id_p)
        if pasien:
            from models import Alamat # Pastikan Alamat bisa diakses
            pasien.nama = nama
            pasien.tgl_lahir = tgl_lahir
            pasien.alamat = Alamat(jalan, kota, kpos)
            pasien.no_telp = no_telp
            return True
        return False

    def hapus_pasien(self, id_p: str) -> bool:
        pasien = self.cari_pasien(id_p)
        if pasien:
            self._pasien.remove(pasien) # Menghapus objek dari list
            return True
        return False

    # --- Dokter ---
    def tambah_dokter(self, d: Dokter): self._dokter.append(d)
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
            return True
        return False

    def hapus_dokter(self, id_d: str) -> bool:
        d = self.cari_dokter(id_d)
        if d:
            self._dokter.remove(d)
            return True
        return False

    # --- Obat ---
    def tambah_obat(self, o: Obat): self._obat.append(o)
    def get_obat(self) -> list: return self._obat
    def cari_obat(self, id_o: str) -> Obat:
        return next((o for o in self._obat if o.id_obat == id_o), None)

    #Antrian
    def tambah_antrian(self, a: Antrian): self._antrian.append(a)
    def get_antrian(self) -> list: return self._antrian
    def next_nomor(self) -> int:
        n = self._nomor_antrian
        self._nomor_antrian += 1
        return n

    #FUNGSI HAPUS ANTRIAN
    def hapus_antrian(self, nomor: int) -> bool:
        antrian = next((a for a in self._antrian if a.nomor == nomor), None)
        if antrian:
            self._antrian.remove(antrian)
            return True
        return False

    #Resep
    def tambah_resep(self, r: Resep): self._resep.append(r)
    def get_resep(self) -> list: return self._resep

    def cari_resep(self, id_r: str):
        return next((r for r in self._resep if r.id_resep == id_r), None)

    def update_resep(self, id_r: str, pasien_baru, dokter_baru) -> bool:
        resep = self.cari_resep(id_r)
        if resep:
            resep.pasien = pasien_baru
            resep.dokter = dokter_baru
            return True
        return False

    def hapus_resep(self, id_r: str) -> bool:
        resep = self.cari_resep(id_r)
        if resep:
            self._resep.remove(resep)
            return True
        return False