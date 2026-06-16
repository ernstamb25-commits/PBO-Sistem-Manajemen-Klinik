import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from models import Pasien, Antrian, Resep, Alamat, JadwalPraktek, DokterFactory
from database import DatabaseKlinik

# =====================================================
# GUI — APLIKASI TKINTER
# =====================================================
class KlinikApp(tk.Tk):
    # Warna tema
    BG        = "#F8F9FA"
    SIDEBAR   = "#1E2A3A"
    SIDEBAR_H = "#2C3E50"
    ACCENT    = "#3498DB"
    WHITE     = "#FFFFFF"
    TEXT_D    = "#2C3E50"
    TEXT_L    = "#ECEFF1"
    TEXT_M    = "#7F8C8D"
    SUCCESS   = "#27AE60"
    WARNING   = "#F39C12"
    DANGER    = "#E74C3C"
    ROW_A     = "#F2F7FB"
    ROW_B     = "#FFFFFF"

    def __init__(self, db: DatabaseKlinik):
        super().__init__()
        self.db = db
        self.title("Sistem Manajemen Klinik")
        self.geometry("1100x680")
        self.configure(bg=self.BG)
        self.resizable(True, True)

        # Style ttk
        self._setup_style()
        self._build_ui()
        self.show_dashboard()

    # --------------------------------------------------
    def _setup_style(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure("Treeview",
                    background=self.WHITE, foreground=self.TEXT_D,
                    rowheight=26, fieldbackground=self.WHITE, font=("Segoe UI", 10))
        s.configure("Treeview.Heading",
                    background=self.SIDEBAR, foreground=self.TEXT_L,
                    font=("Segoe UI", 10, "bold"), relief="flat")
        s.map("Treeview", background=[("selected", self.ACCENT)])
        s.configure("TCombobox", font=("Segoe UI", 10))
        s.configure("TNotebook", background=self.BG)
        s.configure("TNotebook.Tab", font=("Segoe UI", 10), padding=[10, 4])

    # --------------------------------------------------
    def _build_ui(self):
        # --- Sidebar ---
        self.sidebar = tk.Frame(self, bg=self.SIDEBAR, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        # Logo
        tk.Label(self.sidebar, text="🏥 KlinikApp",
                 bg=self.SIDEBAR, fg=self.TEXT_L,
                 font=("Segoe UI", 14, "bold"), pady=20).pack(fill=tk.X)
        tk.Label(self.sidebar, text="Sistem Manajemen Klinik",
                 bg=self.SIDEBAR, fg=self.TEXT_M,
                 font=("Segoe UI", 8)).pack()
        tk.Frame(self.sidebar, bg="#34495E", height=1).pack(fill=tk.X, pady=10)

        # Nav buttons
        nav_items = [
            ("📊  Dashboard",  self.show_dashboard),
            ("👥  Pasien",      self.show_pasien),
            ("🩺  Dokter",      self.show_dokter),
            ("📋  Antrian",     self.show_antrian),
            ("💊  Obat",        self.show_obat),
            ("🧾  Resep",       self.show_resep),
        ]
        self._nav_btns = []
        for label, cmd in nav_items:
            btn = tk.Button(self.sidebar, text=label, command=cmd,
                            bg=self.SIDEBAR, fg=self.TEXT_L,
                            font=("Segoe UI", 10), bd=0, pady=10, padx=14,
                            anchor="w", activebackground=self.SIDEBAR_H,
                            activeforeground=self.TEXT_L, cursor="hand2")
            btn.pack(fill=tk.X)
            self._nav_btns.append((btn, cmd))

        # DB info di bawah sidebar
        tk.Frame(self.sidebar, bg="#34495E", height=1).pack(fill=tk.X, side=tk.BOTTOM, pady=0)
        tk.Label(self.sidebar, text=f"Singleton DB\nID: {self.db.id[:12]}",
                 bg=self.SIDEBAR, fg=self.TEXT_M,
                 font=("Courier", 8), pady=8).pack(side=tk.BOTTOM, fill=tk.X)

        # --- Main area ---
        self.main = tk.Frame(self, bg=self.BG)
        self.main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Topbar
        self.topbar = tk.Frame(self.main, bg=self.WHITE, height=50)
        self.topbar.pack(fill=tk.X)
        self.topbar.pack_propagate(False)
        self.lbl_title = tk.Label(self.topbar, text="Dashboard",
                                  bg=self.WHITE, fg=self.TEXT_D,
                                  font=("Segoe UI", 14, "bold"), padx=20)
        self.lbl_title.pack(side=tk.LEFT, pady=12)
        tk.Label(self.topbar, text="● Online", bg=self.WHITE,
                 fg=self.SUCCESS, font=("Segoe UI", 10), padx=14).pack(side=tk.RIGHT, pady=12)

        # Content
        self.content = tk.Frame(self.main, bg=self.BG)
        self.content.pack(fill=tk.BOTH, expand=True, padx=16, pady=14)

    # --------------------------------------------------
    def _clear(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _set_title(self, t):
        self.lbl_title.config(text=t)

    def _card(self, parent, title="", pady=8):
        """Kartu dengan judul opsional."""
        f = tk.Frame(parent, bg=self.WHITE, bd=1, relief="solid")
        if title:
            tk.Label(f, text=title, bg=self.WHITE, fg=self.TEXT_M,
                     font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=12, pady=(8,2))
            tk.Frame(f, bg="#E0E0E0", height=1).pack(fill=tk.X)
        return f

    def _metric(self, parent, label, value, color=None):
        f = tk.Frame(parent, bg=color or self.WHITE, bd=1, relief="solid")
        tk.Label(f, text=value, bg=color or self.WHITE, fg=self.TEXT_D,
                 font=("Segoe UI", 20, "bold")).pack(pady=(10,2))
        tk.Label(f, text=label, bg=color or self.WHITE, fg=self.TEXT_M,
                 font=("Segoe UI", 9)).pack(pady=(0,10))
        return f

    def _treeview(self, parent, columns, widths):
        tv = ttk.Treeview(parent, columns=columns, show="headings",
                          selectmode="browse")
        for col, w in zip(columns, widths):
            tv.heading(col, text=col)
            tv.column(col, width=w, anchor="w")
        tv.tag_configure("odd",  background=self.ROW_A)
        tv.tag_configure("even", background=self.ROW_B)
        sb = ttk.Scrollbar(parent, orient="vertical", command=tv.yview)
        tv.configure(yscrollcommand=sb.set)
        tv.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        return tv

    def _entry_row(self, parent, label, var, width=22):
        row = tk.Frame(parent, bg=self.WHITE)
        row.pack(fill=tk.X, padx=12, pady=3)
        tk.Label(row, text=label, bg=self.WHITE, fg=self.TEXT_D,
                 font=("Segoe UI", 10), width=16, anchor="w").pack(side=tk.LEFT)
        e = tk.Entry(row, textvariable=var, width=width,
                     font=("Segoe UI", 10), relief="solid", bd=1)
        e.pack(side=tk.LEFT, ipady=3)
        return e

    def _combo_row(self, parent, label, var, values, width=22):
        row = tk.Frame(parent, bg=self.WHITE)
        row.pack(fill=tk.X, padx=12, pady=3)
        tk.Label(row, text=label, bg=self.WHITE, fg=self.TEXT_D,
                 font=("Segoe UI", 10), width=16, anchor="w").pack(side=tk.LEFT)
        cb = ttk.Combobox(row, textvariable=var, values=values,
                          width=width, state="readonly", font=("Segoe UI", 10))
        cb.pack(side=tk.LEFT)
        if values:
            cb.current(0)
        return cb

    def _btn(self, parent, text, cmd, color=None):
        c = color or self.ACCENT
        btn = tk.Button(parent, text=text, command=cmd,
                        bg=c, fg=self.WHITE, font=("Segoe UI", 10, "bold"),
                        bd=0, padx=14, pady=6, cursor="hand2",
                        activebackground=self.SIDEBAR, activeforeground=self.WHITE)
        return btn

    # --------------------------------------------------
    # PAGES
    # --------------------------------------------------
    def show_dashboard(self):
        self._clear(); self._set_title("Dashboard")
        c = self.content

        # Metric row
        mf = tk.Frame(c, bg=self.BG)
        mf.pack(fill=tk.X, pady=(0,12))
        total_pend = sum(r.total_biaya for r in self.db.get_resep())
        menunggu   = sum(1 for a in self.db.get_antrian() if a.status == "menunggu")
        metrics = [
            ("Total Pasien",          str(len(self.db.get_pasien())),  "#EBF5FB"),
            ("Dokter Aktif",          str(len(self.db.get_dokter())),  "#EAFAF1"),
            ("Antrian Menunggu",      str(menunggu),                   "#FEF9E7"),
            ("Pendapatan Hari Ini",   f"Rp {total_pend:,}",           "#FDEDEC"),
        ]
        for lbl, val, col in metrics:
            m = self._metric(mf, lbl, val, col)
            m.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=4)

        # Bawah: antrian + polimorfisme
        bot = tk.Frame(c, bg=self.BG)
        bot.pack(fill=tk.BOTH, expand=True)

        # Antrian
        aq_card = self._card(bot, "Antrian Aktif")
        aq_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,8))
        cols = ("No", "Pasien", "Dokter", "Waktu", "Status")
        widths = (40, 130, 160, 60, 110)
        tv = self._treeview(aq_card, cols, widths)
        for i, a in enumerate(self.db.get_antrian()):
            tag = "odd" if i % 2 else "even"
            tv.insert("", "end", values=(a.nomor, a.pasien.nama,
                                         a.dokter.nama, a.waktu, a.status), tags=(tag,))

        # Polimorfisme
        poly_card = self._card(bot, "Biaya Konsultasi")
        poly_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cols2 = ("Dokter", "Tipe Class", "Tarif Konsul")
        widths2 = (170, 130, 110)
        tv2 = self._treeview(poly_card, cols2, widths2)
        for i, d in enumerate(self.db.get_dokter()):
            tag = "odd" if i % 2 else "even"
            tv2.insert("", "end", values=(d.nama, d.__class__.__name__,
                                           f"Rp {d.hitung_biaya():,}"), tags=(tag,))

    # --------------------------------------------------
    def show_pasien(self):
        self._clear(); self._set_title("Data Pasien")
        c = self.content

        top = tk.Frame(c, bg=self.BG)
        top.pack(fill=tk.BOTH, expand=True)

        # Form tambah pasien
        form_card = self._card(top, "Tambah Pasien Baru")
        form_card.pack(side=tk.LEFT, fill=tk.Y, padx=(0,8))
        tk.Frame(form_card, bg=self.WHITE, height=6).pack()

        v_nama  = tk.StringVar()
        v_tgl   = tk.StringVar(value="2000-01-01")
        v_telp  = tk.StringVar()
        v_jalan = tk.StringVar()
        v_kota  = tk.StringVar(value="Yogyakarta")
        v_kpos  = tk.StringVar(value="55000")
        v_id_edit = tk.StringVar()

        self._entry_row(form_card, "Nama lengkap", v_nama)
        self._entry_row(form_card, "Tanggal lahir", v_tgl)
        self._entry_row(form_card, "No. Telepon", v_telp)
        self._entry_row(form_card, "Jalan", v_jalan)
        self._entry_row(form_card, "Kota", v_kota)
        self._entry_row(form_card, "Kode Pos", v_kpos)

        def do_tambah():
            nama = v_nama.get().strip()
            tgl  = v_tgl.get().strip()
            if not nama or not tgl:
                messagebox.showwarning("Input", "Nama dan tanggal lahir wajib diisi!")
                return
            id_p = f"P{len(self.db.get_pasien())+1:03d}"
            p = Pasien(id_p, nama, tgl,
                       Alamat(v_jalan.get() or "-", v_kota.get() or "Yogyakarta", v_kpos.get() or "55000"),
                       v_telp.get() or "-")
            self.db.tambah_pasien(p)
            messagebox.showinfo("Berhasil", f"Pasien {nama} didaftarkan!\nID: {id_p}")
            self.show_pasien()

        # === FUNGSI UPDATE BARU ===
        def do_update():
            id_p = v_id_edit.get()
            if not id_p:
                messagebox.showwarning("Pilih Data", "Pilih pasien dari tabel terlebih dahulu!")
                return
            nama = v_nama.get().strip()
            tgl  = v_tgl.get().strip()

            self.db.update_pasien(id_p, nama, tgl, v_jalan.get() or "-", v_kota.get() or "Yogyakarta", v_kpos.get() or "55000", v_telp.get() or "-")
            messagebox.showinfo("Berhasil", f"Data pasien {nama} berhasil diperbarui!")
            self.show_pasien() # Refresh halaman

        # === FUNGSI HAPUS DATA ===
        def do_hapus():
            id_p = v_id_edit.get()
            if not id_p:
                messagebox.showwarning("Pilih Data", "Pilih pasien dari tabel terlebih dahulu yang ingin dihapus!")
                return
            
            # Memunculkan popup konfirmasi (Yes/No)
            konfirmasi = messagebox.askyesno("Konfirmasi Hapus", f"Apakah Anda yakin ingin menghapus data pasien {v_nama.get()}?")
            
            if konfirmasi:
                if self.db.hapus_pasien(id_p):
                    messagebox.showinfo("Berhasil", "Data pasien berhasil dihapus!")
                    self.show_pasien() # Refresh halaman dan bersihkan form
                else:
                    messagebox.showerror("Error", "Gagal menghapus data. Pasien tidak ditemukan.")

        def do_hapus_semua():
            if messagebox.askyesno("Hapus Semua", "Yakin hapus SEMUA data pasien?\nTindakan ini tidak bisa dibatalkan!"):
                self.db.hapus_semua_pasien()
                messagebox.showinfo("Berhasil", "Semua data pasien berhasil dihapus!")
                self.show_pasien()

        tk.Frame(form_card, bg=self.WHITE, height=4).pack()
        
        #SUSUNAN TOMBOL
        btn_frame = tk.Frame(form_card, bg=self.WHITE)
        btn_frame.pack(padx=12, pady=8, anchor="w")
        
        self._btn(btn_frame, "  + Daftarkan", do_tambah).pack(side=tk.LEFT)
        self._btn(btn_frame, "Simpan Edit", do_update, color=self.WARNING).pack(side=tk.LEFT, padx=(5, 0))
        self._btn(btn_frame, "Hapus", do_hapus, color=self.DANGER).pack(side=tk.LEFT, padx=(5, 0))
        self._btn(btn_frame, "Hapus Semua", do_hapus_semua, color=self.DANGER).pack(side=tk.LEFT, padx=(5, 0))

        # Tabel pasien
        tbl_card = self._card(top, "Daftar Pasien")
        tbl_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cols = ("ID", "Nama", "Umur", "No. Telp", "Kota")
        widths = (60, 150, 50, 120, 110)
        tv = self._treeview(tbl_card, cols, widths)
        
        # === TAMBAHKAN KODE INI AGAR DATA NAIK KE FORM SAAT DIKLIK ===
        def on_tabel_click(event):
            selected = tv.selection()
            if not selected: return
            
            # Ambil ID dari baris yang diklik
            id_p = tv.item(selected[0], 'values')[0]
            p = self.db.cari_pasien(id_p)
            
            if p:
                # Masukkan data ke kotak input (Entry)
                v_id_edit.set(p.id_pasien)
                v_nama.set(p.nama)
                v_tgl.set(p.tgl_lahir)
                v_telp.set(p.no_telp)
                v_jalan.set(p.alamat.jalan)
                v_kota.set(p.alamat.kota)
                v_kpos.set(p.alamat.kode_pos)

        tv.bind('<ButtonRelease-1>', on_tabel_click)
        
        for i, p in enumerate(self.db.get_pasien()):
            tag = "odd" if i % 2 else "even"
            tv.insert("", "end",
                      values=(p.id_pasien, p.nama, f"{p.umur} th", p.no_telp, p.alamat.kota),
                      tags=(tag,))

    # --------------------------------------------------
    def show_dokter(self):
        self._clear(); self._set_title("Data Dokter")
        c = self.content

        top = tk.Frame(c, bg=self.BG)
        top.pack(fill=tk.BOTH, expand=True)

        # Form tambah dokter
        form_card = self._card(top, "Tambah Dokter")
        form_card.pack(side=tk.LEFT, fill=tk.Y, padx=(0,8))
        tk.Frame(form_card, bg=self.WHITE, height=6).pack()

        v_nama  = tk.StringVar()
        v_tipe  = tk.StringVar(value="umum")
        v_spes  = tk.StringVar(value="Umum")
        v_k     = tk.StringVar(value="2.5")
        v_hari  = tk.StringVar(value="Senin-Jumat")
        v_j1    = tk.StringVar(value="08:00")
        v_j2    = tk.StringVar(value="14:00")
        v_id_edit = tk.StringVar()

        self._entry_row(form_card, "Nama dokter", v_nama)
        self._combo_row(form_card, "Tipe", v_tipe, ["umum", "spesialis"])
        self._entry_row(form_card, "Spesialisasi", v_spes)
        self._entry_row(form_card, "Kelipatan tarif", v_k, width=8)
        self._entry_row(form_card, "Hari praktek", v_hari)
        self._entry_row(form_card, "Jam mulai", v_j1, width=8)
        self._entry_row(form_card, "Jam selesai", v_j2, width=8)

        def do_tambah():
            nama = v_nama.get().strip()
            if not nama:
                messagebox.showwarning("Input", "Nama dokter wajib diisi!"); return
            id_d = f"D{len(self.db.get_dokter())+1:03d}"
            jadwal = JadwalPraktek(v_hari.get(), v_j1.get(), v_j2.get())
            alamat = Alamat("Jl. Klinik", "Yogyakarta", "55000")
            try:
                k = float(v_k.get())
            except ValueError:
                k = 2.5
            d = DokterFactory.buat(v_tipe.get(), id_d, nama, alamat,
                                   v_spes.get(), jadwal, k)
            self.db.tambah_dokter(d)
            messagebox.showinfo("Berhasil",
                                f"Dokter {nama} ditambahkan via Factory!\n"
                                f"Class: {d.__class__.__name__}\n"
                                f"Tarif: Rp {d.hitung_biaya():,}")
            self.show_dokter()

        def do_update_dokter():
            id_d = v_id_edit.get()
            if not id_d:
                messagebox.showwarning("Pilih Data", "Pilih dokter dari tabel terlebih dahulu!")
                return
            try: k = float(v_k.get())
            except ValueError: k = 2.5
            
            if self.db.update_dokter(id_d, v_nama.get(), v_spes.get(), v_hari.get(), v_j1.get(), v_j2.get(), k):
                messagebox.showinfo("Berhasil", "Data dokter diperbarui!")
                self.show_dokter()

        def do_hapus_dokter():
            id_d = v_id_edit.get()
            if not id_d:
                messagebox.showwarning("Pilih Data", "Pilih dokter dari tabel terlebih dahulu!")
                return
            if messagebox.askyesno("Hapus", f"Yakin hapus dokter {v_nama.get()}?"):
                self.db.hapus_dokter(id_d)
                messagebox.showinfo("Berhasil", "Dokter dihapus!")
                self.show_dokter()

        def do_hapus_semua_dokter():
            if messagebox.askyesno("Hapus Semua", "Yakin hapus SEMUA data dokter?"):
                self.db.hapus_semua_dokter()
                messagebox.showinfo("Berhasil", "Semua data dokter dihapus!")
                self.show_dokter()

        tk.Frame(form_card, bg=self.WHITE, height=4).pack()
        
        btn_frame = tk.Frame(form_card, bg=self.WHITE)
        btn_frame.pack(padx=12, pady=8, anchor="w")
        self._btn(btn_frame, "+ Buat via Factory", do_tambah).pack(side=tk.LEFT)
        self._btn(btn_frame, "Update", do_update_dokter, color=self.WARNING).pack(side=tk.LEFT, padx=(5, 0))
        self._btn(btn_frame, "Hapus", do_hapus_dokter, color=self.DANGER).pack(side=tk.LEFT, padx=(5, 0))
        self._btn(btn_frame, "Hapus Semua", do_hapus_semua_dokter, color=self.DANGER).pack(side=tk.LEFT, padx=(5, 0))

        # Tabel dokter
        tbl_card = self._card(top, "Daftar Dokter")
        tbl_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cols = ("ID", "Nama", "Class", "Spesialisasi", "Jadwal", "Tarif Konsul")
        widths = (50, 170, 130, 100, 140, 110)
        tv = self._treeview(tbl_card, cols, widths)

        def on_tabel_dokter_click(event):
            selected = tv.selection()
            if not selected: return
            id_d = tv.item(selected[0], 'values')[0]
            d = self.db.cari_dokter(id_d)
            if d:
                v_id_edit.set(d.id_pegawai)
                v_nama.set(d.nama)
                v_tipe.set("spesialis" if "Spesialis" in d.__class__.__name__ else "umum")
                v_spes.set(d.spesialisasi)
                v_hari.set(d.jadwal.hari)
                v_j1.set(d.jadwal.jam_mulai)
                v_j2.set(d.jadwal.jam_selesai)
                if hasattr(d, 'kelipatan'):
                    v_k.set(str(d.kelipatan))
                else:
                    v_k.set("2.5")

        tv.bind('<ButtonRelease-1>', on_tabel_dokter_click)

        for i, d in enumerate(self.db.get_dokter()):
            tag = "odd" if i % 2 else "even"
            tv.insert("", "end",
                      values=(d.id_pegawai, d.nama, d.__class__.__name__,
                              d.spesialisasi, str(d.jadwal),
                              f"Rp {d.hitung_biaya():,}"),
                      tags=(tag,))

    # --------------------------------------------------
    def show_antrian(self):
        self._clear(); self._set_title("Antrian Pasien")
        c = self.content

        top = tk.Frame(c, bg=self.BG)
        top.pack(fill=tk.BOTH, expand=True)

        # Form tambah antrian
        form_card = self._card(top, "Tambah Antrian")
        form_card.pack(side=tk.LEFT, fill=tk.Y, padx=(0,8))
        tk.Frame(form_card, bg=self.WHITE, height=6).pack()

        pasien_list = [f"{p.id_pasien} — {p.nama}" for p in self.db.get_pasien()]
        dokter_list = [f"{d.id_pegawai} — {d.nama}" for d in self.db.get_dokter()]

        v_pasien = tk.StringVar()
        v_dokter = tk.StringVar()
        v_waktu  = tk.StringVar(value="09:00")
        v_st     = tk.StringVar(value="menunggu") # Tambahan input status

        self._combo_row(form_card, "Pasien", v_pasien, pasien_list, width=26)
        self._combo_row(form_card, "Dokter", v_dokter, dokter_list, width=26)
        self._entry_row(form_card, "Waktu (HH:MM)", v_waktu, width=8)
        self._combo_row(form_card, "Status", v_st, ["menunggu", "dalam perawatan", "selesai"], width=16)

        def do_tambah():
            if not v_pasien.get() or not v_dokter.get():
                messagebox.showwarning("Input", "Pilih pasien dan dokter!"); return
            pid = v_pasien.get().split(" — ")[0]
            did = v_dokter.get().split(" — ")[0]
            p = self.db.cari_pasien(pid)
            d = self.db.cari_dokter(did)
            if not p or not d:
                messagebox.showerror("Error", "Pasien atau dokter tidak ditemukan!"); return
            a = Antrian(self.db.next_nomor(), p, d, v_waktu.get())
            self.db.tambah_antrian(a)
            messagebox.showinfo("Berhasil", f"Antrian no.{a.nomor} ditambahkan!")
            self.show_antrian()

        tk.Frame(form_card, bg=self.WHITE, height=4).pack()
        
        # Baris pertama untuk tombol Tambah
        btn_frame1 = tk.Frame(form_card, bg=self.WHITE)
        btn_frame1.pack(padx=12, pady=(8, 4), anchor="w")
        self._btn(btn_frame1, "+ Tambah", do_tambah, color=self.ACCENT).pack(side=tk.LEFT)

        # Baris kedua untuk tombol Update & Hapus
        btn_frame2 = tk.Frame(form_card, bg=self.WHITE)
        btn_frame2.pack(padx=12, pady=(0, 8), anchor="w")
        self._btn(btn_frame2, "Update", lambda: ubah_status(), color=self.WARNING).pack(side=tk.LEFT)
        self._btn(btn_frame2, "Hapus", lambda: do_hapus_antrian(), color=self.DANGER).pack(side=tk.LEFT, padx=(5, 0))
        self._btn(btn_frame2, "Hapus Semua", lambda: do_hapus_semua_antrian(), color=self.DANGER).pack(side=tk.LEFT, padx=(5, 0))

        # Tabel antrian
        tbl_card = self._card(top, "Antrian Hari Ini")
        tbl_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cols = ("No", "Pasien", "Dokter", "Waktu", "Status")
        widths = (40, 150, 170, 60, 110)
        tv = self._treeview(tbl_card, cols, widths)

        status_opts = ["menunggu", "dalam perawatan", "selesai"]
        tag_color = {"menunggu": "#FEF9E7", "dalam perawatan": "#EAFAF1", "selesai": "#F4F4F4"}

        for i, a in enumerate(self.db.get_antrian()):
            tv.insert("", "end", iid=str(i),
                      values=(a.nomor, a.pasien.nama, a.dokter.nama, a.waktu, a.status))

        # Event listener agar saat klik tabel, statusnya langsung mengisi combobox form otomatis
        def on_tabel_click(event):
            sel = tv.selection()
            if not sel: return
            v_st.set(tv.item(sel[0], 'values')[4])

        tv.bind('<ButtonRelease-1>', on_tabel_click)

        def ubah_status():
            sel = tv.selection()
            if not sel:
                messagebox.showwarning("Pilih", "Pilih antrian terlebih dahulu!"); return
            idx = int(sel[0])
            self.db.get_antrian()[idx].status = v_st.get()
            self.db.save_data()  # <-- Menyimpan perubahan status antrian
            self.show_antrian()

        # === TAMBAHKAN FUNGSI HAPUS DI SINI ===
        def do_hapus_antrian():
            sel = tv.selection()
            if not sel:
                messagebox.showwarning("Pilih", "Pilih antrian dari tabel terlebih dahulu yang ingin dihapus!")
                return
            
            nomor_antrian = int(tv.item(sel[0], 'values')[0])
            nama_pasien = tv.item(sel[0], 'values')[1]
            
            konfirmasi = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus Antrian No. {nomor_antrian} atas nama {nama_pasien}?")
            if konfirmasi:
                if self.db.hapus_antrian(nomor_antrian):
                    messagebox.showinfo("Berhasil", "Data antrian berhasil dihapus!")
                    self.show_antrian()
                else:
                    messagebox.showerror("Error", "Gagal menghapus antrian.")
        

        def do_hapus_semua_antrian():
            if messagebox.askyesno("Hapus Semua", "Yakin hapus SEMUA antrian hari ini?"):
                self.db.hapus_semua_antrian()
                messagebox.showinfo("Berhasil", "Semua antrian dihapus dan nomor antrian di-reset!")
                self.show_antrian()


    def show_obat(self):
        self._clear(); self._set_title("Data Obat")
        c = self.content

        top = tk.Frame(c, bg=self.BG)
        top.pack(fill=tk.BOTH, expand=True)

        form_card = self._card(top, "Kelola Data Obat")
        form_card.pack(side=tk.LEFT, fill=tk.Y, padx=(0,8))
        tk.Frame(form_card, bg=self.WHITE, height=6).pack()

        v_nama   = tk.StringVar()
        v_satuan = tk.StringVar(value="Strip")
        v_harga  = tk.StringVar()
        v_stok   = tk.StringVar()
        v_id_edit = tk.StringVar()

        self._entry_row(form_card, "Nama Obat", v_nama)
        self._combo_row(form_card, "Satuan", v_satuan, ["Strip", "Botol", "Tablet", "Kapsul", "Ampul"])
        self._entry_row(form_card, "Harga (Rp)", v_harga)
        self._entry_row(form_card, "Stok", v_stok)

        def do_tambah():
            nama = v_nama.get().strip()
            if not nama:
                messagebox.showwarning("Input", "Nama obat wajib diisi!")
                return
            try:
                harga, stok = int(v_harga.get()), int(v_stok.get())
            except ValueError:
                messagebox.showwarning("Input", "Harga dan Stok harus angka!")
                return
            id_o = f"OB{len(self.db.get_obat())+1:03d}"
            from models import Obat
            o = Obat(id_o, nama, v_satuan.get(), harga, stok)
            self.db.tambah_obat(o)
            messagebox.showinfo("Berhasil", f"Obat {nama} ditambahkan!")
            self.show_obat()

        def do_update():
            id_o = v_id_edit.get()
            if not id_o:
                messagebox.showwarning("Pilih Data", "Pilih obat di tabel!")
                return
            try:
                harga, stok = int(v_harga.get()), int(v_stok.get())
            except ValueError:
                messagebox.showwarning("Input", "Harga dan Stok harus angka!")
                return
            if self.db.update_obat(id_o, v_nama.get(), v_satuan.get(), harga, stok):
                messagebox.showinfo("Berhasil", "Data diperbarui!")
                self.show_obat()

        def do_hapus():
            id_o = v_id_edit.get()
            if not id_o: return
            if messagebox.askyesno("Hapus", f"Yakin hapus {v_nama.get()}?"):
                self.db.hapus_obat(id_o)
                messagebox.showinfo("Berhasil", "Obat dihapus!")
                self.show_obat()

        def do_hapus_semua_obat():
            if messagebox.askyesno("Hapus Semua", "Yakin hapus SEMUA data obat?"):
                self.db.hapus_semua_obat()
                messagebox.showinfo("Berhasil", "Semua data obat dihapus!")
                self.show_obat()

        tk.Frame(form_card, bg=self.WHITE, height=4).pack()
        btn_frame = tk.Frame(form_card, bg=self.WHITE)
        btn_frame.pack(padx=12, pady=8, anchor="w")
        
        self._btn(btn_frame, "  + Tambah", do_tambah).pack(side=tk.LEFT)
        self._btn(btn_frame, "Update", do_update, color=self.WARNING).pack(side=tk.LEFT, padx=(5, 0))
        self._btn(btn_frame, "Hapus", do_hapus, color=self.DANGER).pack(side=tk.LEFT, padx=(5, 0))
        self._btn(btn_frame, "Hapus Semua", do_hapus_semua_obat, color=self.DANGER).pack(side=tk.LEFT, padx=(5, 0))

        tbl_card = self._card(top, "Daftar Obat")
        tbl_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cols = ("ID Obat", "Nama", "Satuan", "Harga", "Stok")
        widths = (70, 150, 80, 100, 70)
        tv = self._treeview(tbl_card, cols, widths)

        def on_tabel_click(event):
            sel = tv.selection()
            if not sel: return
            o = self.db.cari_obat(tv.item(sel[0], 'values')[0])
            if o:
                v_id_edit.set(o.id_obat)
                v_nama.set(o.nama)
                v_satuan.set(o.satuan)
                v_harga.set(str(o.harga))
                v_stok.set(str(o.stok))

        tv.bind('<ButtonRelease-1>', on_tabel_click)

        for i, o in enumerate(self.db.get_obat()):
            tag = "odd" if i % 2 else "even"
            tv.insert("", "end", values=(o.id_obat, o.nama, o.satuan, f"Rp {o.harga:,}", o.stok), tags=(tag,))

    def show_resep(self):
        self._clear(); self._set_title("Manajemen Resep")
        c = self.content

        top = tk.Frame(c, bg=self.BG)
        top.pack(fill=tk.BOTH, expand=True)

        # Form resep
        form_card = self._card(top, "Buat Resep")
        form_card.pack(side=tk.LEFT, fill=tk.Y, padx=(0,8))
        tk.Frame(form_card, bg=self.WHITE, height=6).pack()

        pasien_list = [f"{p.id_pasien} — {p.nama}" for p in self.db.get_pasien()]
        dokter_list = [f"{d.id_pegawai} — {d.nama}" for d in self.db.get_dokter()]
        obat_list   = [f"{o.id_obat} — {o.nama}" for o in self.db.get_obat()]

        v_p  = tk.StringVar()
        v_d  = tk.StringVar()
        v_o  = tk.StringVar()
        v_jm = tk.StringVar(value="10")
        v_at = tk.StringVar(value="3x1 sesudah makan")
        v_id_resep_edit = tk.StringVar()

        # 1. Combobox khusus Antrian Aktif
        antrian_aktif = [f"Antrian {a.nomor} - {a.pasien.nama}" for a in self.db.get_antrian() if a.status != "selesai"]
        v_antrian = tk.StringVar()
        cb_antrian = self._combo_row(form_card, "Pilih Antrian", v_antrian, antrian_aktif, 26)

        # 2. Tangkap object combobox Pasien & Dokter lalu matikan (disabled)
        cb_pasien = self._combo_row(form_card, "Pasien", v_p, pasien_list, 26)
        cb_dokter = self._combo_row(form_card, "Dokter", v_d, dokter_list, 26)
        cb_pasien.config(state="disabled")
        cb_dokter.config(state="disabled")

        # 3. Fungsi Auto-fill
        def on_antrian_selected(event):
            if not v_antrian.get(): return
            no_antrian = int(v_antrian.get().split(" ")[1])
            a = next((x for x in self.db.get_antrian() if x.nomor == no_antrian), None)
            if a:
                v_p.set(f"{a.pasien.id_pasien}   {a.pasien.nama}")
                v_d.set(f"{a.dokter.id_pegawai}   {a.dokter.nama}")

        cb_antrian.bind("<<ComboboxSelected>>", on_antrian_selected)
        tk.Frame(form_card, bg="#E0E0E0", height=1).pack(fill=tk.X, pady=10)
        tk.Label(form_card, text="Detail Obat", bg=self.WHITE, fg=self.TEXT_M, font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=12)

        self._combo_row(form_card, "Obat", v_o, obat_list, 26)
        self._entry_row(form_card, "Jumlah", v_jm, 6)
        self._entry_row(form_card, "Aturan pakai", v_at, 22)

        keranjang = [] 
        lbl_keranjang = tk.Label(form_card, text="Keranjang Kosong", bg=self.WHITE, fg=self.TEXT_M, justify="left")
        lbl_keranjang.pack(padx=12, pady=5, anchor="w")

        def update_ui_keranjang():
            if not keranjang:
                lbl_keranjang.config(text="Keranjang Kosong", fg=self.TEXT_M)
            else:
                teks = "Isi Keranjang:\n"
                for i, item in enumerate(keranjang):
                    teks += f"{i+1}. {item['obat'].nama} ({item['jumlah']}x) - {item['aturan']}\n"
                lbl_keranjang.config(text=teks, fg=self.TEXT_D)

        def do_tambah_keranjang():
            if not v_o.get():
                messagebox.showwarning("Input", "Pilih obat terlebih dahulu!"); return
            
            oid = v_o.get().split(" — ")[0]
            o = self.db.cari_obat(oid)
            try: jml = int(v_jm.get())
            except ValueError: jml = 1
                
            keranjang.append({"obat": o, "jumlah": jml, "aturan": v_at.get()})
            update_ui_keranjang()
            messagebox.showinfo("Berhasil", f"{o.nama} dimasukkan ke keranjang!")

        def do_simpan_resep():
            if not v_p.get() or not v_d.get():
                messagebox.showwarning("Input", "Pilih pasien dan dokter!"); return
            if len(keranjang) == 0:
                messagebox.showwarning("Input", "Keranjang obat masih kosong!"); return

            pid = v_p.get().split(" — ")[0]
            did = v_d.get().split(" — ")[0]
            p = self.db.cari_pasien(pid)
            d = self.db.cari_dokter(did)

            id_r = f"RX{len(self.db.get_resep())+1:03d}"
            r = Resep(id_r, p, d, str(date.today()))

            for item in keranjang:
                r.tambah_obat(item["obat"], item["jumlah"], item["aturan"])

            self.db.tambah_resep(r)
            messagebox.showinfo("Berhasil",
                                f"Resep {id_r} berhasil dibuat!\n"
                                f"Tarif dokter : Rp {d.hitung_biaya():,}\n"
                                f"Total obat   : Rp {r.total_obat:,}\n"
                                f"Grand total  : Rp {r.total_biaya:,}")
            self.show_resep()

        def do_update_resep():
            id_r = v_id_resep_edit.get()
            if not id_r:
                messagebox.showwarning("Pilih Data", "Pilih resep dari tabel terlebih dahulu!")
                return
            pid = v_p.get().split(" — ")[0]
            did = v_d.get().split(" — ")[0]
            if self.db.update_resep(id_r, self.db.cari_pasien(pid), self.db.cari_dokter(did)):
                messagebox.showinfo("Berhasil", "Resep berhasil diperbarui!")
                self.show_resep()

        def do_hapus_resep():
            id_r = v_id_resep_edit.get()
            if not id_r:
                messagebox.showwarning("Pilih Data", "Pilih resep dari tabel terlebih dahulu!")
                return
            if messagebox.askyesno("Hapus", f"Yakin hapus resep {id_r}?"):
                self.db.hapus_resep(id_r)
                messagebox.showinfo("Berhasil", "Resep dihapus!")
                self.show_resep()

        tk.Frame(form_card, bg=self.WHITE, height=4).pack()
        
        btn_keranjang = tk.Frame(form_card, bg=self.WHITE)
        btn_keranjang.pack(padx=12, pady=4, anchor="w")
        self._btn(btn_keranjang, "+ Tambah ke Keranjang", do_tambah_keranjang, color=self.ACCENT).pack(side=tk.LEFT)

        def do_hapus_semua_resep():
            if messagebox.askyesno("Hapus Semua", "Yakin hapus SEMUA riwayat resep?"):
                self.db.hapus_semua_resep()
                messagebox.showinfo("Berhasil", "Semua riwayat resep dihapus!")
                self.show_resep()

        tk.Frame(form_card, bg="#E0E0E0", height=1).pack(fill=tk.X, pady=8)

        btn_frame = tk.Frame(form_card, bg=self.WHITE)
        btn_frame.pack(padx=12, pady=8, anchor="w")
        self._btn(btn_frame, "Simpan Resep", do_simpan_resep, color=self.SUCCESS).pack(side=tk.LEFT)
        self._btn(btn_frame, "Update", do_update_resep, color=self.WARNING).pack(side=tk.LEFT, padx=(5, 0))
        self._btn(btn_frame, "Hapus", do_hapus_resep, color=self.DANGER).pack(side=tk.LEFT, padx=(5, 0))
        self._btn(btn_frame, "Hapus Semua", do_hapus_semua_resep, color=self.DANGER).pack(side=tk.LEFT, padx=(5, 0))

        # Tabel resep
        tbl_card = self._card(top, "Riwayat Resep")
        tbl_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cols = ("ID Resep", "Pasien", "Dokter", "Tarif Dokter", "Total Obat", "Grand Total", "Tgl")
        widths = (70, 120, 160, 100, 100, 110, 90)
        tv = self._treeview(tbl_card, cols, widths)

        def on_tabel_resep_click(event):
            selected = tv.selection()
            if selected:
                v_id_resep_edit.set(tv.item(selected[0], 'values')[0])

        tv.bind('<ButtonRelease-1>', on_tabel_resep_click)

        for i, r in enumerate(self.db.get_resep()):
            tag = "odd" if i % 2 else "even"
            tv.insert("", "end",
                      values=(r.id_resep, r.pasien.nama, r.dokter.nama,
                              f"Rp {r.dokter.hitung_biaya():,}",
                              f"Rp {r.total_obat:,}",
                              f"Rp {r.total_biaya:,}", r.tanggal),
                      tags=(tag,))