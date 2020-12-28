import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

app = QApplication([])
window = QMainWindow()

qtRectangle = window.geometry()
center = QDesktopWidget().availableGeometry().center()
qtRectangle.moveCenter(center)
window.move(qtRectangle.topLeft())
window.resize(800,250)
window.setWindowTitle("Stok Barang")

form_layout = QFormLayout(window)

# Header
header = QLabel("Tambah Barang")
header.setFont(QFont('Arial',15))
header.setAlignment(Qt.AlignCenter)
header.setFixedHeight(50)

# input nama
lbl_nama = QLabel("Nama Barang")
lbl_nama.setFixedWidth(130)
lbl_nama.adjustSize()
lbl_nama.setFont(QFont('Arial',13))

input_nama = QLineEdit()
input_nama.setFixedHeight(30)

# input stok
lbl_stok = QLabel("Stok Barang")
lbl_stok.setFixedWidth(130)
lbl_stok.adjustSize()
lbl_stok.setFont(QFont('Arial',13))

input_stok = QLineEdit()
input_stok.setFixedHeight(30)

# input keterangan
lbl_keterangan = QLabel("""Keterangan 
Barang (Optional)""")
lbl_keterangan.setFixedWidth(130)
lbl_keterangan.adjustSize()
lbl_keterangan.setFont(QFont('Arial',13))

input_keterangan = QLineEdit()
input_keterangan.setFixedHeight(40)


# submit
submit = QPushButton('Simpan')
submit.setFixedHeight(40)

form_layout.addRow(lbl_nama,input_nama)
form_layout.addRow(lbl_stok,input_stok)
form_layout.addRow(lbl_keterangan,input_keterangan)
form_layout.addRow(submit)

ver_layout = QVBoxLayout()
ver_layout.addWidget(header)
ver_layout.addLayout(form_layout)
ver_layout.setSpacing(10)

widget = QWidget()
widget.setLayout(ver_layout)
window.setCentralWidget(widget)

window.show()
sys.exit(app.exec_())

