import datetime

class Generate:
    def __init__(self, df):
        """Konstruktor untuk menerima DataFrame mahasiswa"""
        self.df = df  # DataFrame mahasiswa

    def generateNim(self, kodeProdi):
        """Fungsi ini untuk membuat NIM secara otomatis"""
        now = datetime.datetime.now()
        tahun = str(now.year)
        bulan = "{:02d}".format(now.month)
        hari = "{:02d}".format(now.day)

        # Pastikan kolom 'NIM' ada di DataFrame
        if 'NIM' not in self.df.columns:
            self.df['NIM'] = ""  # Tambahkan kolom 'NIM' jika belum ada
        self.df['NIM'] = self.df['NIM'].astype(str)

        # Filter data berdasarkan kode program studi
        df_prodi = self.df[self.df['NIM'].str[8:10] == kodeProdi]

        # Cari nomor urut terakhir untuk kode program studi
        if not df_prodi.empty:
            try:
                no_urut_terakhir = df_prodi['NIM'].str[10:].astype(int).max()
                no_urut_baru = "{:02d}".format(no_urut_terakhir + 1)
            except ValueError:
                no_urut_baru = "01"
        else:
            no_urut_baru = "01"  # Nomor urut dimulai dari 01 jika belum ada data

        # Format NIM: YYYYMMDDKKUU
        nim = f"{tahun}{bulan}{hari}{kodeProdi}{no_urut_baru}"
        return nim

    def generateKodeKelas(self, kode_prodi, kelas):
        """Fungsi untuk membuat kode kelas berdasarkan kode program studi dan kelas"""
        self.inisial_prodi = ""
        self.inisial_kelas = ""

        # Tentukan inisial program studi (kode_prodi ke initial)
        if kode_prodi == "01":
            self.inisial_prodi = "I"  # Informatika
        elif kode_prodi == "02":
            self.inisial_prodi = "S"  # Sistem Informasi
        elif kode_prodi == "03":
            self.inisial_prodi = "R"  # Rekayasa Perangkat Lunak
        elif kode_prodi == "04":
            self.inisial_prodi = "B"  # Kebidanan
        else:
            return "Jurusan tidak ditemukan."

        # Validasi khusus untuk program studi Kebidanan
        if kode_prodi == "04" and kelas.lower() != "pagi":
            return "Program studi Kebidanan hanya mendukung kelas pagi."

        # Tentukan inisial kelas (input kelas ke initial)
        valid_classes = ["pagi", "malam", "karyawan"]
        if kelas.lower() in valid_classes:
            if kelas.lower() == "pagi":
                self.inisial_kelas = "P"
            elif kelas.lower() == "malam":
                self.inisial_kelas = "M"
            elif kelas.lower() == "karyawan":
                self.inisial_kelas = "K"
        else:
            return f"Kelas '{kelas}' tidak valid. Pilihan kelas: Pagi, Malam, Karyawan."

        # Format kode kelas: [Inisial Prodi][Inisial Kelas][Tahun][Nomor Urut]
        tahun_daftar = str(datetime.datetime.now().year)[2:]  # Tahun pendaftaran 2 digit terakhir

        # Nomor urut untuk kode kelas
        if "Kode_Kelas" not in self.df.columns:
            self.df["Kode_Kelas"] = ""  # Tambahkan kolom jika belum ada
        filter_kelas = self.df[self.df["Kode_Kelas"].str.startswith(f"{self.inisial_prodi}{self.inisial_kelas}")]
        if not filter_kelas.empty:
            try:
                nomor_urut_terakhir = filter_kelas["Kode_Kelas"].str[-1].astype(int).max()
                nomor_urut = str(nomor_urut_terakhir + 1)
            except ValueError:
                nomor_urut = "1"  # Jika data ada tetapi tidak valid
        else:
            nomor_urut = "1"  # Nomor urut dimulai dari 1 jika belum ada data

        # Format Kode Kelas: [Prodi Initial][Kelas Initial][Tahun][Urut]
        kode_kelas = f"{self.inisial_prodi}{self.inisial_kelas}{tahun_daftar}{nomor_urut}"
        return kode_kelas
