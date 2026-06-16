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

    # --- Dokter ---
    def tambah_dokter(self, d: Dokter): self._dokter.append(d)
    def get_dokter(self) -> list: return self._dokter
    def cari_dokter(self, id_d: str) -> Dokter:
        return next((d for d in self._dokter if d.id_pegawai == id_d), None)

    # --- Obat ---
    def tambah_obat(self, o: Obat): self._obat.append(o)
    def get_obat(self) -> list: return self._obat
    def cari_obat(self, id_o: str) -> Obat:
        return next((o for o in self._obat if o.id_obat == id_o), None)

    # --- Antrian ---
    def tambah_antrian(self, a: Antrian): self._antrian.append(a)
    def get_antrian(self) -> list: return self._antrian
    def next_nomor(self) -> int:
        n = self._nomor_antrian
        self._nomor_antrian += 1
        return n

    # --- Resep ---
    def tambah_resep(self, r: Resep): self._resep.append(r)
    def get_resep(self) -> list: return self._resep