from abc import ABC, abstractmethod
from collections import namedtuple
from datetime import date

# NAMEDTUPLE
Alamat = namedtuple("Alamat", ["jalan", "kota", "kode_pos"])
JadwalPraktek = namedtuple("JadwalPraktek", ["hari", "jam_mulai", "jam_selesai"])


# ABSTRACT BASE CLASS: Pegawai
class Pegawai(ABC):
    def __init__(self, id_pegawai: str, nama: str, alamat: Alamat):
        self.id_pegawai = id_pegawai
        self.nama = nama
        self.alamat = alamat

    @abstractmethod
    def hitung_biaya(self) -> int:
        """Hitung biaya konsultasi/layanan (polimorfisme)."""
        pass

    @property
    @abstractmethod
    def peran(self) -> str:
        """Peran pegawai di klinik."""
        pass

    def __str__(self):
        return f"{self.peran}: {self.nama} ({self.id_pegawai})"


# INHERITANCE: Dokter extends Pegawai
class Dokter(Pegawai):
    TARIF_DASAR = 100_000

    def __init__(self, id_pegawai, nama, alamat, spesialisasi, jadwal: JadwalPraktek):
        super().__init__(id_pegawai, nama, alamat)
        self.spesialisasi = spesialisasi
        self.jadwal = jadwal
        self.tarif_dasar = self.TARIF_DASAR

    def hitung_biaya(self) -> int:
        return self.tarif_dasar

    @property
    def peran(self) -> str:
        return "Dokter"

# POLIMORFISME: DokterUmum & DokterSpesialis
class DokterUmum(Dokter):
    TARIF_DASAR = 75_000

    def __init__(self, id_pegawai, nama, alamat, jadwal):
        super().__init__(id_pegawai, nama, alamat, "Umum", jadwal)
        self.tarif_dasar = self.TARIF_DASAR

    def hitung_biaya(self) -> int:
        return self.tarif_dasar  # flat rate

    @property
    def peran(self) -> str:
        return "Dokter Umum"


class DokterSpesialis(Dokter):
    TARIF_DASAR = 150_000

    def __init__(self, id_pegawai, nama, alamat, spesialisasi, jadwal, kelipatan=2.5):
        super().__init__(id_pegawai, nama, alamat, spesialisasi, jadwal)
        self.tarif_dasar = self.TARIF_DASAR
        self.kelipatan = kelipatan

    def hitung_biaya(self) -> int:
        return int(self.tarif_dasar * self.kelipatan)

    @property
    def peran(self) -> str:
        return f"Spesialis {self.spesialisasi}"

# ABC LAINNYA: Perawat & Admin
class Perawat(Pegawai):
    def hitung_biaya(self) -> int:
        return 0

    @property
    def peran(self) -> str:
        return "Perawat"


class Admin(Pegawai):
    def hitung_biaya(self) -> int:
        return 0

    @property
    def peran(self) -> str:
        return "Admin"


# CLASS: Pasien
class Pasien:
    def __init__(self, id_pasien: str, nama: str, tgl_lahir: str,
                 alamat: Alamat, no_telp: str):
        self.id_pasien = id_pasien
        self.nama = nama
        self.tgl_lahir = tgl_lahir
        self.alamat = alamat
        self.no_telp = no_telp
        self.riwayat: list = []

    @property
    def umur(self) -> int:
        tahun_lahir = int(self.tgl_lahir.split("-")[0])
        return date.today().year - tahun_lahir

    def tambah_riwayat(self, catatan: str):
        self.riwayat.append(catatan)

    def __str__(self):
        return f"{self.nama} ({self.id_pasien})"

# CLASS: Obat
class Obat:
    def __init__(self, id_obat: str, nama: str, satuan: str, harga: int, stok: int):
        self.id_obat = id_obat
        self.nama = nama
        self.satuan = satuan
        self.harga = harga
        self.stok = stok

    def __str__(self):
        return f"{self.nama} ({self.satuan}) — Rp {self.harga:,}"


# CLASS: Resep
class Resep:
    def __init__(self, id_resep: str, pasien: Pasien, dokter: Dokter, tanggal: str):
        self.id_resep = id_resep
        self.pasien = pasien
        self.dokter = dokter
        self.tanggal = tanggal
        self.items: list[dict] = []

    def tambah_obat(self, obat: Obat, jumlah: int, aturan: str):
        self.items.append({"obat": obat, "jumlah": jumlah, "aturan": aturan})

    @property
    def total_obat(self) -> int:
        return sum(item["obat"].harga * item["jumlah"] for item in self.items)

    @property
    def total_biaya(self) -> int:
        return self.dokter.hitung_biaya() + self.total_obat

    def __str__(self):
        return (f"Resep {self.id_resep} | {self.pasien.nama} | "
                f"{self.dokter.nama} | Total: Rp {self.total_biaya:,}")


# CLASS: Antrian
class Antrian:
    def __init__(self, nomor: int, pasien: Pasien, dokter: Dokter,
                 waktu: str, status: str = "menunggu"):
        self.nomor = nomor
        self.pasien = pasien
        self.dokter = dokter
        self.waktu = waktu
        self.status = status


# FACTORY PATTERN: DokterFactory
class DokterFactory:
    @staticmethod
    def buat(tipe: str, id_pegawai: str, nama: str, alamat: Alamat,
             spesialisasi: str, jadwal: JadwalPraktek, kelipatan: float = 2.5) -> Dokter:
        if tipe == "umum":
            return DokterUmum(id_pegawai, nama, alamat, jadwal)
        elif tipe == "spesialis":
            return DokterSpesialis(id_pegawai, nama, alamat, spesialisasi, jadwal, kelipatan)
        else:
            raise ValueError(f"Tipe dokter '{tipe}' tidak dikenal")