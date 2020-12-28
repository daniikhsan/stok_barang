import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import mysql.connector
import os

# Database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stok_barang"
)

def edit_barang(id_barang):
    print(f'Berhasil diupdate!{id_barang}')

def hapus_barang(id_barang):
    print(f'Berhasil dihapus!{id_barang}')

app = QApplication([])
window = QMainWindow()

qtRectangle = window.geometry()
center = QDesktopWidget().availableGeometry().center()
qtRectangle.moveCenter(center)
window.move(qtRectangle.topLeft())
window.resize(778,500)
window.setWindowTitle("Stok Barang")


# Header
header = QLabel("Gudangg Barang")
header.setFont(QFont('Arial',15))
header.setAlignment(Qt.AlignCenter)
header.setFixedHeight(30)

# Tombol Tambah Barang
btn_tambah = QPushButton('Tambah Barang')
btn_tambah.clicked.connect(tambah_barang)
btn_tambah.setFixedHeight(40)

# Table Barang
cursor = db.cursor()
sql = "SELECT * FROM barang ORDER BY last_update DESC"
cursor.execute(sql)
results = cursor.fetchall()
print(len(results))
tbl_barang = QTableWidget()
tbl_barang.setRowCount(len(results))
tbl_barang.setRowHeight(0,50)
tbl_barang.setRowHeight(1,50)
tbl_barang.setRowHeight(2,50)
tbl_barang.setRowHeight(3,50)
tbl_barang.setRowHeight(4,50)
tbl_barang.setColumnCount(5)
header_table = tbl_barang.horizontalHeader()
header_table.setSectionResizeMode(0,QHeaderView.Stretch)
header_table.setSectionResizeMode(1,QHeaderView.Stretch)
header_table.setSectionResizeMode(2,QHeaderView.Stretch)
header_table.setSectionResizeMode(3,QHeaderView.Stretch)
header_table.setSectionResizeMode(4,QHeaderView.Stretch)
tbl_barang.setHorizontalHeaderLabels(['Nama Barang','Stok Barang','Keterangan Barang','Terakhir Diperbarui','Aksi'])
tbl_barang.setEditTriggers(QAbstractItemView.NoEditTriggers)

# Looping data
if cursor.rowcount == 0:
    print("Tidak ada data")
else:
    for index,data in enumerate(results):
        btn_edit = QPushButton('Edit')
        btn_edit.setFixedHeight(25)
        btn_edit.clicked.connect(lambda: edit_barang(data[0]))
        btn_hapus = QPushButton('Hapus')
        btn_hapus.clicked.connect(lambda: hapus_barang(data[0]))
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_edit)
        btn_layout.addWidget(btn_hapus)
        btn_widget = QWidget()
        btn_widget.setLayout(btn_layout)
        tbl_barang.setItem(index,0,QTableWidgetItem(str(data[1])))
        tbl_barang.setItem(index,1,QTableWidgetItem(str(data[2])))
        tbl_barang.setItem(index,2,QTableWidgetItem(str(data[3])))
        tbl_barang.setItem(index,3,QTableWidgetItem(str(data[4])))
        tbl_barang.setCellWidget(index,4,btn_widget)

# Horizontal Layout
# Baris 1
hor_layout1 = QHBoxLayout()
hor_layout1.addWidget(header)
# Baris 2
hor_layout2 = QHBoxLayout()
hor_layout2.addWidget(btn_tambah)

ver_layout = QVBoxLayout()
ver_layout.addLayout(hor_layout1)
ver_layout.addLayout(hor_layout2)
ver_layout.addWidget(tbl_barang)


widget = QWidget()
widget.setLayout(ver_layout)
window.setCentralWidget(widget)

window.show()
sys.exit(app.exec_())

