import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import mysql.connector
import os


def edit(id_barang):
    print(f'Berhasil diupdate!{id_barang}')

def hapus(id_barang):
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
btn_tambah.setFixedHeight(40)

# Table Barang
tbl_barang = QTableWidget()
tbl_barang.setRowCount(3)
tbl_barang.setRowHeight(0,50)
tbl_barang.setRowHeight(1,50)
tbl_barang.setRowHeight(2,50)
tbl_barang.setRowHeight(3,50)
tbl_barang.setColumnCount(4)
tbl_barang.setColumnWidth(0,180)
tbl_barang.setColumnWidth(1,180)
tbl_barang.setColumnWidth(2,180)
tbl_barang.setColumnWidth(3,180)
tbl_barang.setHorizontalHeaderLabels(['Nama Barang','Stok Barang','Keterangan Barang','Aksi'])
tbl_barang.setEditTriggers(QAbstractItemView.NoEditTriggers)

# Looping data
btn_edit = QPushButton('Edit')
btn_edit.setFixedHeight(25)
btn_edit.clicked.connect(lambda: edit(2))
btn_hapus = QPushButton('Hapus')
btn_hapus.clicked.connect(lambda: hapus(2))
btn_layout = QHBoxLayout()
btn_layout.addWidget(btn_edit)
btn_layout.addWidget(btn_hapus)
btn_widget = QWidget()
btn_widget.setLayout(btn_layout)
tbl_barang.setItem(0,0,QTableWidgetItem('Buku'))
tbl_barang.setItem(0,1,QTableWidgetItem('10'))
tbl_barang.setItem(0,2,QTableWidgetItem(''))
tbl_barang.setCellWidget(0,3,btn_widget)

hor_layout1 = QHBoxLayout()
hor_layout1.addWidget(header)


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

