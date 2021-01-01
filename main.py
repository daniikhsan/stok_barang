import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import mysql.connector
import datetime

# Database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stok_barang"
)

# Nama Aplikasi
nama_aplikasi = "eStock"

# Tab Informasi Barang Masuk
class InfoBarangMasuk(QWidget):
    def __init__(self,id_barang):
        super().__init__()
        self.cursor = db.cursor()
        self.sql = "SELECT * FROM barang_masuk WHERE id_barang=%s"
        self.val = (id_barang,)
        self.cursor.execute(self.sql,self.val)
        self.results = self.cursor.fetchall()
        # Looping data
        if self.cursor.rowcount == 0:
            self.label = QLabel('Tidak ada')
            self.label.setAlignment(Qt.AlignCenter)
            ver_layout.addWidget(self.label)
        else:
            self.tbl_barang = QTableWidget()
            self.tbl_barang.setColumnCount(3)
            self.header_table = self.tbl_barang.horizontalHeader()
            self.header_table.setSectionResizeMode(0,QHeaderView.Stretch)
            self.header_table.setSectionResizeMode(1,QHeaderView.Stretch)
            self.header_table.setSectionResizeMode(2,QHeaderView.Stretch)
            self.tbl_barang.setHorizontalHeaderLabels(['Tanggal Masuk','Jumlah Masuk','Keterangan'])
            self.tbl_barang.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tbl_barang.setRowCount(len(self.results))
            for index,data in enumerate(self.results):
                self.tbl_barang.setRowHeight(index,50)
                # Menampilkan Baris
                self.tbl_barang.setItem(index,0,QTableWidgetItem(data[2].strftime("%A,%d %B %Y %X")))
                self.tbl_barang.setItem(index,1,QTableWidgetItem(str(data[3])))
                self.tbl_barang.setItem(index,2,QTableWidgetItem(str(data[4])))

        ver_layout = QVBoxLayout()
        ver_layout.addWidget(self.tbl_barang)

        self.setLayout(ver_layout)

# Tab Informasi Barang Keluar
class InfoBarangKeluar(QWidget):
    def __init__(self,id_barang):
        ver_layout = QVBoxLayout()
        super().__init__()
        self.cursor = db.cursor()
        self.sql = "SELECT * FROM barang_keluar WHERE id_barang=%s"
        self.val = (id_barang,)
        self.cursor.execute(self.sql,self.val)
        self.results = self.cursor.fetchall()
        # Looping data
        if self.cursor.rowcount == 0:
            self.label = QLabel('Tidak ada')
            self.label.setAlignment(Qt.AlignCenter)
            ver_layout.addWidget(self.label)
        else:
            self.tbl_barang = QTableWidget()
            self.tbl_barang.setColumnCount(3)
            self.header_table = self.tbl_barang.horizontalHeader()
            self.header_table.setSectionResizeMode(0,QHeaderView.Stretch)
            self.header_table.setSectionResizeMode(1,QHeaderView.Stretch)
            self.header_table.setSectionResizeMode(2,QHeaderView.Stretch)
            self.tbl_barang.setHorizontalHeaderLabels(['Tanggal Keluar','Jumlah Masuk','Keterangan'])
            self.tbl_barang.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tbl_barang.setRowCount(len(self.results))
            for index,data in enumerate(self.results):
                self.tbl_barang.setRowHeight(index,50)
                # Menampilkan Baris
                self.tbl_barang.setItem(index,0,QTableWidgetItem(data[2].strftime("%A,%d %B %Y %X")))
                self.tbl_barang.setItem(index,1,QTableWidgetItem(str(data[4])))
                self.tbl_barang.setItem(index,2,QTableWidgetItem(str(data[3])))
            
            ver_layout.addWidget(self.tbl_barang)

        self.setLayout(ver_layout)

# Window Untuk Detail Barang (Barang Masuk dan Keluar)
class DetailBarangWindow(QDialog):
    def __init__(self,id_barang):
        super().__init__()
        self.id_barang = id_barang
        self.cursor = db.cursor()
        self.sql = "SELECT * FROM barang WHERE id_barang=%s"
        self.val = (id_barang,)
        self.cursor.execute(self.sql,self.val)
        self.data = self.cursor.fetchone()
        self.setWindowTitle(f'Detail Barang - {self.data[1]}  | {nama_aplikasi}')
        self.tampilan()

    def tampilan(self):
        self.resize(800,400)
        
        # Header
        self.header = QLabel("Detail Barang")
        self.header.setFont(QFont('Arial',15))
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFixedHeight(50)

        # Nama Barang
        self.lbl_nama = QLabel("Nama Barang")
        self.lbl_nama.setFixedWidth(130)
        self.lbl_nama.adjustSize()
        self.lbl_nama.setFont(QFont('Arial',13))
        self.input_nama = QLineEdit()
        self.input_nama.setFixedHeight(30)
        self.input_nama.setText(self.data[1])
        self.input_nama.setFont(QFont('Arial',15))
        self.input_nama.setDisabled(True)

        # Stok Barang
        self.lbl_stok = QLabel("Jumlah Sekarang")
        self.lbl_stok.setFixedWidth(130)
        self.lbl_stok.adjustSize()
        self.lbl_stok.setFont(QFont('Arial',13))
        self.input_stok = QLineEdit()
        self.input_stok.setFixedHeight(30)
        self.input_stok.setText(str(self.data[2]))
        self.input_stok.setFont(QFont('Arial',15))
        self.input_stok.setDisabled(True)

        self.form_layout = QFormLayout()
        self.form_layout.addRow(self.lbl_nama,self.input_nama)
        self.form_layout.addRow(self.lbl_stok,self.input_stok)

        self.tabWidget = QTabWidget()
        barang_masuk = InfoBarangMasuk(self.id_barang)
        barang_keluar = InfoBarangKeluar(self.id_barang)

        self.tabWidget.addTab(barang_masuk,"Barang Masuk")
        self.tabWidget.addTab(barang_keluar,"Barang Keluar")

        ver_layout = QVBoxLayout()
        ver_layout.addWidget(self.header)
        ver_layout.addLayout(self.form_layout)
        ver_layout.addWidget(self.tabWidget)
        self.setLayout(ver_layout)

# Window Untuk Keluar Barang
class KeluarBarangWindow(QMainWindow):
    def __init__(self,id_barang):
        super().__init__()
        self.id_barang = id_barang
        self.cursor = db.cursor()
        self.sql = "SELECT * FROM barang WHERE id_barang=%s"
        self.val = (id_barang,)
        self.cursor.execute(self.sql,self.val)
        self.data = self.cursor.fetchone()
        self.setWindowTitle(f'Keluar Barang - {self.data[1]} | {nama_aplikasi}')
        self.form()
    
    def submit_form(self):
        self.input_jumlah_keluar_barang = str(self.input_jumlah_keluar.text())
        self.input_keterangan_keluar = str(self.input_keterangan.text())
        if(not self.input_jumlah_keluar_barang):
            self.error = QMessageBox()
            self.error.setWindowTitle(f'Gagal! | {nama_aplikasi}')
            self.error.setText('Pastikan nama barang sudah terisi!')
            self.error.setIcon(QMessageBox.Warning)
            self.error.show()
        elif(int(self.input_jumlah_keluar_barang) <= 0 or int(self.input_jumlah_keluar_barang) > self.data[2]):
            self.error = QMessageBox()
            self.error.setWindowTitle(f'Gagal! | {nama_aplikasi}')
            self.error.setText('Pastikan jumlah barang yang keluar lebih dari nol dan tidak lebih dari jumlah barang sekarang!')
            self.error.setIcon(QMessageBox.Warning)
            self.error.show()
        else:
            self.val = (self.id_barang,int(self.input_jumlah_keluar_barang),self.input_keterangan_keluar)
            self.cursor = db.cursor()
            self.sql = "CALL barang_keluar (%s,%s,%s)"
            self.cursor.execute(self.sql,self.val)
            db.commit()
            self.sukses = QMessageBox()
            self.sukses.setWindowTitle(f'Berhasil! | {nama_aplikasi}')
            self.sukses.setText('Data keluar barang berhasil ditambahkan!')
            self.sukses.setIcon(QMessageBox.Information)
            self.sukses.show()
            window.show_semua_barang()
            self.close()

    def form(self):
        self.resize(800,300)
        self.form_layout = QFormLayout()
        # Header
        self.header = QLabel("Keluar Barang")
        self.header.setFont(QFont('Arial',15))
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFixedHeight(50)

        # input nama
        self.lbl_nama = QLabel("Nama Barang")
        self.lbl_nama.setFixedWidth(130)
        self.lbl_nama.adjustSize()
        self.lbl_nama.setFont(QFont('Arial',13))

        self.input_nama = QLineEdit()
        self.input_nama.setFixedHeight(30)
        self.input_nama.setText(self.data[1])
        self.input_nama.setDisabled(True)
        self.input_nama.setFont(QFont('Arial',15))

        # input stok
        self.lbl_stok = QLabel("Jumlah Sekarang")
        self.lbl_stok.setFixedWidth(130)
        self.lbl_stok.adjustSize()
        self.lbl_stok.setFont(QFont('Arial',13))

        self.input_stok = QLineEdit()
        self.input_stok.setFixedHeight(40)
        self.input_stok.setText(str(self.data[2]))
        self.input_stok.setDisabled(True)
        self.input_stok.setFont(QFont('Arial',15))

        # input jumlah keluar
        self.lbl_jumlah_keluar = QLabel("Jumlah keluar")
        self.lbl_jumlah_keluar.setFixedWidth(130)
        self.lbl_jumlah_keluar.adjustSize()
        self.lbl_jumlah_keluar.setFont(QFont('Arial',13))

        self.input_jumlah_keluar = QLineEdit()
        self.input_jumlah_keluar.setFixedHeight(40)
        self.input_jumlah_keluar.setValidator(QIntValidator())
        self.input_jumlah_keluar.setFont(QFont('Arial',15))

        # input keterangan
        self.lbl_keterangan = QLabel("Keterangan")
        self.lbl_keterangan.setFixedWidth(130)
        self.lbl_keterangan.adjustSize()
        self.lbl_keterangan.setFont(QFont('Arial',13))

        self.input_keterangan = QLineEdit()
        self.input_keterangan.setFixedHeight(40)
        self.input_keterangan.setFont(QFont('Arial',15))

        # submit
        self.submit = QPushButton('Simpan')
        self.submit.setFixedHeight(40)
        self.submit.clicked.connect(self.submit_form)

        self.form_layout.addRow(self.lbl_nama,self.input_nama)
        self.form_layout.addRow(self.lbl_stok,self.input_stok)
        self.form_layout.addRow(self.lbl_jumlah_keluar,self.input_jumlah_keluar)
        self.form_layout.addRow(self.lbl_keterangan,self.input_keterangan)
        self.form_layout.addRow(self.submit)

        self.ver_layout = QVBoxLayout()
        self.ver_layout.addWidget(self.header)
        self.ver_layout.addLayout(self.form_layout)
        self.ver_layout.setSpacing(10)

        self.widget = QWidget()
        self.widget.setLayout(self.ver_layout)
        self.setCentralWidget(self.widget)

# Window Untuk Masuk Barang
class MasukBarangWindow(QMainWindow):
    def __init__(self,id_barang):
        super().__init__()
        self.id_barang = id_barang
        self.cursor = db.cursor()
        self.sql = "SELECT * FROM barang WHERE id_barang=%s"
        self.val = (id_barang,)
        self.cursor.execute(self.sql,self.val)
        self.data = self.cursor.fetchone()
        self.setWindowTitle(f'Masuk Barang - {self.data[1]} | {nama_aplikasi}')
        self.form()
    
    def submit_form(self):
        self.input_jumlah_masuk_barang = str(self.input_jumlah_masuk.text())
        self.input_keterangan_masuk = str(self.input_keterangan.text())
        if(not self.input_jumlah_masuk_barang):
            self.error = QMessageBox()
            self.error.setWindowTitle(f'Gagal! | {nama_aplikasi}')
            self.error.setText('Pastikan nama barang sudah terisi!')
            self.error.setIcon(QMessageBox.Warning)
            self.error.show()
        elif(int(self.input_jumlah_masuk_barang) <= 0):
            self.error = QMessageBox()
            self.error.setWindowTitle(f'Gagal! | {nama_aplikasi}')
            self.error.setText('Pastikan jumlah barang yang masuk lebih dari nol!')
            self.error.setIcon(QMessageBox.Warning)
            self.error.show()
        else:
            self.val = (self.id_barang,int(self.input_jumlah_masuk_barang),self.input_keterangan_masuk)
            self.cursor = db.cursor()
            self.sql = "CALL barang_masuk (%s,%s,%s)"
            self.cursor.execute(self.sql,self.val)
            db.commit()
            self.sukses = QMessageBox()
            self.sukses.setWindowTitle(f'Berhasil! | {nama_aplikasi}')
            self.sukses.setText('Data masuk barang berhasil ditambahkan!')
            self.sukses.setIcon(QMessageBox.Information)
            self.sukses.show()
            window.show_semua_barang()
            self.close()

    def form(self):
        self.resize(800,300)
        self.form_layout = QFormLayout()
        # Header
        self.header = QLabel("Masuk Barang")
        self.header.setFont(QFont('Arial',15))
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFixedHeight(50)

        # input nama
        self.lbl_nama = QLabel("Nama Barang")
        self.lbl_nama.setFixedWidth(130)
        self.lbl_nama.adjustSize()
        self.lbl_nama.setFont(QFont('Arial',13))

        self.input_nama = QLineEdit()
        self.input_nama.setFixedHeight(30)
        self.input_nama.setText(self.data[1])
        self.input_nama.setDisabled(True)
        self.input_nama.setFont(QFont('Arial',15))

        # input stok
        self.lbl_stok = QLabel("Jumlah Sekarang")
        self.lbl_stok.setFixedWidth(130)
        self.lbl_stok.adjustSize()
        self.lbl_stok.setFont(QFont('Arial',13))

        self.input_stok = QLineEdit()
        self.input_stok.setFixedHeight(40)
        self.input_stok.setText(str(self.data[2]))
        self.input_stok.setDisabled(True)
        self.input_stok.setFont(QFont('Arial',15))

        # input jumlah masuk
        self.lbl_jumlah_masuk = QLabel("Jumlah Masuk")
        self.lbl_jumlah_masuk.setFixedWidth(130)
        self.lbl_jumlah_masuk.adjustSize()
        self.lbl_jumlah_masuk.setFont(QFont('Arial',13))

        self.input_jumlah_masuk = QLineEdit()
        self.input_jumlah_masuk.setFixedHeight(40)
        self.input_jumlah_masuk.setValidator(QIntValidator(self))
        self.input_jumlah_masuk.setFont(QFont('Arial',15))

        # input keterangan
        self.lbl_keterangan = QLabel("Keterangan")
        self.lbl_keterangan.setFixedWidth(130)
        self.lbl_keterangan.adjustSize()
        self.lbl_keterangan.setFont(QFont('Arial',13))

        self.input_keterangan = QLineEdit()
        self.input_keterangan.setFixedHeight(40)
        self.input_keterangan.setFont(QFont('Arial',15))

        # submit
        self.submit = QPushButton('Simpan')
        self.submit.setFixedHeight(40)
        self.submit.clicked.connect(self.submit_form)

        self.form_layout.addRow(self.lbl_nama,self.input_nama)
        self.form_layout.addRow(self.lbl_stok,self.input_stok)
        self.form_layout.addRow(self.lbl_jumlah_masuk,self.input_jumlah_masuk)
        self.form_layout.addRow(self.lbl_keterangan,self.input_keterangan)
        self.form_layout.addRow(self.submit)

        self.ver_layout = QVBoxLayout()
        self.ver_layout.addWidget(self.header)
        self.ver_layout.addLayout(self.form_layout)
        self.ver_layout.setSpacing(10)

        self.widget = QWidget()
        self.widget.setLayout(self.ver_layout)
        self.setCentralWidget(self.widget)

# Window Untuk Edit Barang
class EditWindow(QMainWindow):
    def __init__(self,id_barang):
        super().__init__()
        self.id_barang = id_barang
        self.cursor = db.cursor()
        self.sql = "SELECT * FROM barang WHERE id_barang=%s"
        self.val = (id_barang,)
        self.cursor.execute(self.sql,self.val)
        self.data = self.cursor.fetchone()
        self.setWindowTitle(f'Edit Barang - {self.data[1]} | {nama_aplikasi}')
        self.form()
    
    def submit_form(self):
        self.nama_barang = str(self.input_nama.text())
        if(not self.nama_barang):
            self.error = QMessageBox()
            self.error.setWindowTitle(f'Gagal! | {nama_aplikasi}')
            self.error.setText('Pastikan nama barang sudah terisi!')
            self.error.setIcon(QMessageBox.Warning)
            self.error.show()
        else:
            self.sql = "UPDATE barang SET nama_barang=%s, last_update = NOW() WHERE id_barang=%s"
            self.val =(self.nama_barang,self.id_barang)
            self.cursor.execute(self.sql,self.val)
            db.commit()
            self.sukses = QMessageBox()
            self.sukses.setWindowTitle(f'Berhasil! | {nama_aplikasi}')
            self.sukses.setText('Data barang berhasil diperbarui!')
            self.sukses.setIcon(QMessageBox.Information)
            self.sukses.show()
            window.show_semua_barang()
            self.close()

    def form(self):
        self.resize(800,200)
        self.form_layout = QFormLayout()
        # Header
        self.header = QLabel("Edit Barang")
        self.header.setFont(QFont('Arial',15))
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFixedHeight(50)

        # input nama
        self.lbl_nama = QLabel("Nama Barang")
        self.lbl_nama.setFixedWidth(130)
        self.lbl_nama.adjustSize()
        self.lbl_nama.setFont(QFont('Arial',13))

        self.input_nama = QLineEdit()
        self.input_nama.setFixedHeight(30)
        self.input_nama.setText(self.data[1])
        self.input_nama.setFont(QFont('Arial',15))

        # submit
        self.submit = QPushButton('Simpan')
        self.submit.setFixedHeight(40)
        self.submit.clicked.connect(self.submit_form)

        self.form_layout.addRow(self.lbl_nama,self.input_nama)
        self.form_layout.addRow(self.submit)

        self.ver_layout = QVBoxLayout()
        self.ver_layout.addWidget(self.header)
        self.ver_layout.addLayout(self.form_layout)
        self.ver_layout.setSpacing(10)

        self.widget = QWidget()
        self.widget.setLayout(self.ver_layout)
        self.setCentralWidget(self.widget)

# Window Untuk Tambah Data Barang Baru
class TambahWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f'Tambah Barang | {nama_aplikasi}')
        self.form()
    
    def submit_form(self):
        nama_barang = str(self.input_nama.text())
        stok_barang = str(self.input_stok.text())
        keterangan = str(self.input_keterangan.text())

        if(not nama_barang or not stok_barang):
            self.error = QMessageBox()
            self.error.setWindowTitle(f'Gagal! | {nama_aplikasi}')
            self.error.setText('Pastikan nama dan stok barang sudah terisi!')
            self.error.setIcon(QMessageBox.Warning)
            self.error.show()
        elif(int(stok_barang) <= 0):
            self.error = QMessageBox()
            self.error.setWindowTitle(f'Gagal! | {nama_aplikasi}')
            self.error.setText('Pastikan jumlah stok barang lebih dari nol!')
            self.error.setIcon(QMessageBox.Warning)
            self.error.show()
        else:
            val = (nama_barang,stok_barang,keterangan)
            cursor = db.cursor()
            sql = "CALL barang_baru (%s,%s,%s)"
            cursor.execute(sql,val)
            db.commit()
            self.sukses = QMessageBox()
            self.sukses.setWindowTitle(f'Berhasil! | {nama_aplikasi}')
            self.sukses.setText('Data barang berhasil ditambahkan!')
            self.sukses.setIcon(QMessageBox.Information)
            self.sukses.show()
            window.show_semua_barang()
            self.close()

    def form(self):
        self.resize(800,200)
        self.form_layout = QFormLayout()
        # Header
        self.header = QLabel("Tambah Barang")
        self.header.setFont(QFont('Arial',15))
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFixedHeight(50)

        # input nama
        self.lbl_nama = QLabel("Nama Barang")
        self.lbl_nama.setFixedWidth(130)
        self.lbl_nama.adjustSize()
        self.lbl_nama.setFont(QFont('Arial',13))

        self.input_nama = QLineEdit()
        self.input_nama.setFixedHeight(30)
        self.input_nama.setFont(QFont('Arial',15))

        # input stok
        self.lbl_stok = QLabel("Stok Barang")
        self.lbl_stok.setFixedWidth(130)
        self.lbl_stok.adjustSize()
        self.lbl_stok.setFont(QFont('Arial',13))

        self.input_stok = QLineEdit()
        self.input_stok.setFixedHeight(30)
        self.input_stok.setValidator(QIntValidator(self))
        self.input_stok.setFont(QFont('Arial',15))

        # input keterangan
        self.lbl_keterangan = QLabel("""Keterangan (Opt)""")
        self.lbl_keterangan.setFixedWidth(130)
        self.lbl_keterangan.adjustSize()
        self.lbl_keterangan.setFont(QFont('Arial',13))

        self.input_keterangan = QLineEdit()
        self.input_keterangan.setFixedHeight(40)
        self.input_keterangan.setFont(QFont('Arial',15))

        # submit
        self.submit = QPushButton('Simpan')
        self.submit.setFixedHeight(40)
        self.submit.clicked.connect(self.submit_form)

        self.form_layout.addRow(self.lbl_nama,self.input_nama)
        self.form_layout.addRow(self.lbl_stok,self.input_stok)
        self.form_layout.addRow(self.lbl_keterangan,self.input_keterangan)
        self.form_layout.addRow(self.submit)

        self.ver_layout = QVBoxLayout()
        self.ver_layout.addWidget(self.header)
        self.ver_layout.addLayout(self.form_layout)
        self.ver_layout.setSpacing(10)

        self.widget = QWidget()
        self.widget.setLayout(self.ver_layout)
        self.setCentralWidget(self.widget)

# Window Untuk Halaman Utama Aplikasi
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"Home | {nama_aplikasi}")
        self.menu_utama()

    # Untuk Menampilkan Widget dan Setting Layout
    def menu_utama(self):
        self.resize(1000,500)
        # Header
        self.header = QLabel(nama_aplikasi)
        self.header.setFont(QFont('Arial',30))
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFixedHeight(50)
        self.header.setAlignment(Qt.AlignLeft)

        # Tombol Tambah Barang
        self.btn_tambah = QPushButton('Tambah Barang')
        self.btn_tambah.clicked.connect(self.tambah_barang)
        self.btn_tambah.setFixedHeight(40)

        # Cari Barang
        self.cari_barang = QLineEdit()
        self.cari_barang.setClearButtonEnabled(True)
        self.cari_barang.setFixedHeight(40)
        self.cari_barang.setFixedWidth(250)
        self.cari_barang.setFont(QFont('Arial',15))
        self.cari_barang.setPlaceholderText('Cari barang...')
        self.cari_barang.addAction(QIcon('images/search.ico'),QLineEdit.LeadingPosition)
        self.cari_barang.returnPressed.connect(self.search_barang)

        # Table Barang
        self.tbl_barang = QTableWidget()
        self.tbl_barang.setColumnCount(4)
        self.header_table = self.tbl_barang.horizontalHeader()
        self.header_table.setSectionResizeMode(0,QHeaderView.Stretch)
        self.header_table.setSectionResizeMode(1,500)
        self.header_table.setSectionResizeMode(2,QHeaderView.Stretch)
        self.header_table.setSectionResizeMode(3,QHeaderView.Stretch)
        self.tbl_barang.setHorizontalHeaderLabels(['Nama Barang','Stok Barang','Terakhir Diperbarui','Aksi'])
        self.tbl_barang.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.show_semua_barang()

        # Tombol Tambah dan Cari
        self.ver_right = QVBoxLayout()
        self.ver_right.addWidget(self.btn_tambah)
        self.ver_right.addWidget(self.cari_barang)

        # Horizontal Layout
        # Baris 1
        self.hor_layout1 = QHBoxLayout()
        self.hor_layout1.addWidget(self.header)
        self.hor_layout1.addLayout(self.ver_right)

        # Baris 3
        self.hor_layout3 = QHBoxLayout()
        self.hor_layout3.addWidget(self.tbl_barang)

        # Vertikal Layout
        self.ver_layout = QVBoxLayout()
        self.ver_layout.addLayout(self.hor_layout1)
        # self.ver_layout.addLayout(self.hor_layout2)
        self.ver_layout.addLayout(self.hor_layout3)

        # Membuat Widget
        self.widget = QWidget()
        self.widget.setLayout(self.ver_layout)
        self.setCentralWidget(self.widget)

        self.showMaximized()

    
    # Tampilkan Data Barang ke Table
    def show_barang(self,cursor,results):
        # Looping data
        self.tbl_barang.setRowCount(len(self.results))
        # Looping data
        if self.cursor.rowcount == 0:
            msgBox = QMessageBox(self)
            msgBox.setText('Tidak ada data barang ditemukan!')
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle(nama_aplikasi)
            msgBox.show()
        else:
            for index,data in enumerate(self.results):
                self.tbl_barang.setRowHeight(index,50)
                # Tombol detail Barang
                self.btn_detail = QPushButton('Detail')
                self.btn_detail.clicked.connect(lambda checked, i=data[0] : self.detail_barang(i))
                self.btn_detail.setFixedHeight(30)
                # Tombol Masuk Barang
                self.btn_masuk = QPushButton('Masuk')
                self.btn_masuk.clicked.connect(lambda checked, i=data[0] : self.masuk_barang(i))
                self.btn_masuk.setFixedHeight(30)
                # Tombol Keluar Barang
                self.btn_keluar = QPushButton('Keluar')
                self.btn_keluar.clicked.connect(lambda checked, i=data[0] : self.keluar_barang(i))
                self.btn_keluar.setFixedHeight(30)
                # Tombol Edit
                self.btn_edit = QPushButton('Edit')
                self.btn_edit.setFixedHeight(30)
                self.btn_edit.clicked.connect(lambda checked, i=data[0] : self.edit_barang(i))
                # Tombol Hapus
                self.btn_hapus = QPushButton('Hapus')
                self.btn_hapus.clicked.connect(lambda checked, i=data[0] : self.hapus_barang(i))
                self.btn_hapus.setFixedHeight(30)
                # Layout Tombol
                self.btn_layout = QHBoxLayout()
                self.btn_layout.addWidget(self.btn_detail)
                self.btn_layout.addWidget(self.btn_masuk)
                self.btn_layout.addWidget(self.btn_keluar)
                self.btn_layout.addWidget(self.btn_edit)
                self.btn_layout.addWidget(self.btn_hapus)
                # Layout tombol menjadi widget
                self.btn_widget = QWidget()
                self.btn_widget.setLayout(self.btn_layout)
                # Menampilkan Baris
                self.tbl_barang.setItem(index,0,QTableWidgetItem(str(data[1])))
                self.tbl_barang.setItem(index,1,QTableWidgetItem(str(data[2])))
                self.tbl_barang.setItem(index,2,QTableWidgetItem(data[3].strftime("%A,%d %B %Y %X")))
                self.tbl_barang.setCellWidget(index,3,self.btn_widget)
            

    # Tampilkan semua data barang
    def show_semua_barang(self):
        self.cursor = db.cursor()
        self.sql = "SELECT * FROM barang ORDER BY last_update DESC"
        self.cursor.execute(self.sql)
        self.results = self.cursor.fetchall()
        self.show_barang(self.cursor,self.results)
    
    # Masuk Barang
    def masuk_barang(self,id_barang):
        self.masuk_window = MasukBarangWindow(id_barang)
        self.masuk_window.show()

    # Keluar Barang
    def keluar_barang(self,id_barang):
        self.keluar_window = KeluarBarangWindow(id_barang)
        self.keluar_window.show()

    # Detail Barang
    def detail_barang(self,id_barang):
        self.detail_window = DetailBarangWindow(id_barang)
        self.detail_window.show()
        # print(f"Detail Barang : {id_barang}")

    # Edit Data Barang
    def edit_barang(self,id_barang):
        self.edit_window = EditWindow(id_barang)
        self.edit_window.show()

    # Hapus Data Barang
    def hapus_barang(self,id_barang):
        self.cursor = db.cursor()
        self.sql = "SELECT * FROM barang WHERE id_barang=%s"
        self.val = (id_barang,)
        self.cursor.execute(self.sql,self.val)
        self.data = self.cursor.fetchone()
        self.msgBox = QMessageBox.question(self,'Konfirmasi Penghapusan Barang',f"Apakah anda yakin ingin menghapus semua data barang '{self.data[1]}' ?", QMessageBox.Yes |QMessageBox.No)
        if(self.msgBox == QMessageBox.Yes):
            self.sql = "DELETE FROM barang WHERE id_barang=%s"
            self.val = (id_barang,)
            self.cursor.execute(self.sql,self.val)
            db.commit()
            self.sukses = QMessageBox()
            self.sukses.setWindowTitle('Berhasil!')
            self.sukses.setText('Data berhasil dihapus!')
            self.sukses.setIcon(QMessageBox.Information)
            self.sukses.show()
            self.show_semua_barang()
    
    # Tambah Data Barang
    def tambah_barang(self):
        self.tambah_window = TambahWindow()
        self.tambah_window.show()

    def search_barang(self):
        self.nama_barang = self.cari_barang.text()
        self.cursor = db.cursor()
        self.sql = "SELECT * FROM barang WHERE nama_barang LIKE %s"
        self.val = ("%{}%".format(self.nama_barang),)
        self.cursor.execute(self.sql,self.val)
        self.results = self.cursor.fetchall()
        self.show_barang(self.cursor,self.results)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setFont(QFont('Arial',10))
    sys.exit(app.exec_())
