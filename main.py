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

class TambahWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.form()
    
    def submit_form(self):
        self.setWindowTitle('Tambah Barang')
        nama_barang = str(self.input_nama.text())
        stok_barang = int(self.input_stok.text())
        keterangan = str(self.input_keterangan.text())
        val = (nama_barang,stok_barang,keterangan)
        cursor = db.cursor()
        sql = "CALL barang_baru (%s,%s,%s)"
        cursor.execute(sql,val)
        db.commit()
        MainWindow().show_semua_barang()
        self.close()

    def form(self):
        self.resize(800,300)
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
        


class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stok Barang")

        self.menu_utama()

    def menu_utama(self):
        self.resize(800,500)
        # Header
        self.header = QLabel("Gudangg Barang")
        self.header.setFont(QFont('Arial',15))
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFixedHeight(30)

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
        self.tbl_barang.setColumnCount(5)
        self.header_table = self.tbl_barang.horizontalHeader()
        self.header_table.setSectionResizeMode(0,QHeaderView.Stretch)
        self.header_table.setSectionResizeMode(1,QHeaderView.Stretch)
        self.header_table.setSectionResizeMode(2,QHeaderView.Stretch)
        self.header_table.setSectionResizeMode(3,QHeaderView.Stretch)
        self.header_table.setSectionResizeMode(4,QHeaderView.Stretch)
        self.tbl_barang.setHorizontalHeaderLabels(['Nama Barang','Stok Barang','Keterangan Barang','Terakhir Diperbarui','Aksi'])
        self.tbl_barang.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.show_semua_barang()
        # Horizontal Layout
        # Baris 1
        self.hor_layout1 = QHBoxLayout()
        self.hor_layout1.addWidget(self.header)
        # Baris 2
        self.hor_layout2 = QHBoxLayout()
        self.hor_layout2.addWidget(self.btn_tambah)
        self.hor_layout2.addWidget(self.cari_barang)

        # Baris 3
        self.hor_layout3 = QHBoxLayout()
        self.hor_layout3.addWidget(self.tbl_barang)

        # Vertikal Layout
        self.ver_layout = QVBoxLayout()
        self.ver_layout.addLayout(self.hor_layout1)
        self.ver_layout.addLayout(self.hor_layout2)
        self.ver_layout.addLayout(self.hor_layout3)

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
            print('Tidak ada data')
        else:
            for index,data in enumerate(self.results):
                self.tbl_barang.setRowHeight(index,50)
                # Tombol Masuk Barang
                self.btn_masuk = QPushButton(f'Masuk')
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
                self.tbl_barang.setItem(index,2,QTableWidgetItem(str(data[3])))
                self.tbl_barang.setItem(index,3,QTableWidgetItem(data[4].strftime("%A,%d %B %Y %X")))
                self.tbl_barang.setCellWidget(index,4,self.btn_widget)

    # Tampilkan semua data barang
    def show_semua_barang(self):
        self.cursor = db.cursor()
        self.sql = "SELECT * FROM barang ORDER BY last_update DESC"
        self.cursor.execute(self.sql)
        self.results = self.cursor.fetchall()
        self.show_barang(self.cursor,self.results)
    
    # Masuk Barang
    def masuk_barang(self,id_barang):
        print(f'Berhasil Masuk Barang! {id_barang}')

    # Keluar Barang
    def keluar_barang(self,id_barang):
        print(f"Berhasil keluar barang! {id_barang}")

    # Detail Barang
    def detail_barang(self,id_barang):
        print(f"Detail Barang : {id_barang}")

    # Edit Data Barang
    def edit_barang(self,id_barang):
        edit_window = EditWindow(id_barang)
        edit_window.show()

    # Hapus Data Barang
    def hapus_barang(self,id_barang):
        print(f'Data berhasil dihapus! ID Barang = {id_barang}')
    
    # Tambah Data Barang
    def tambah_barang(self):
        self.tambah_window = TambahWindow()
        self.tambah_window.show()
        # MainWindow.close()

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
    sys.exit(app.exec_())
