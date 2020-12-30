import mysql.connector
import os

# Database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="stok_barang"
)

if db.is_connected():
    print("Database Berhasil Terhubung!")
else:
    print("Database Gagal Terhubung")

# Fungsi

# Menampilkan semua data barang
def show_semua_barang(db):
    cursor = db.cursor()
    sql = "SELECT * FROM barang"
    cursor.execute(sql)
    results = cursor.fetchall()

    if cursor.rowcount == 0:
        print("Tidak ada data")
    else:
        for data in results:
            print("--------------------------------")
            print("ID Barang :",data[0])
            print("Nama Barang :",data[1])
            print("Stok Barang :",data[2])
            print("Keterangan :",data[3])
            print("Terakhir diperbarui :",data[4])

# Tambah Barang Baru
def barang_baru(db):
    nama_barang = input("Nama Barang : ")
    stok_barang = int(input("Jumlah Barang : "))
    keterangan = input("Keterangan : ")
    val = (nama_barang,stok_barang,keterangan)
    cursor = db.cursor()
    sql = "CALL barang_baru (%s,%s,%s)"
    cursor.execute(sql,val)
    db.commit()
    print("Data berhasil ditambahkan")

# Barang Masuk
def barang_masuk(db):
    show_semua_barang(db)
    id_barang = int(input("Pilih ID Barang : "))
    jumlah_masuk = int(input("Jumlah Barang Masuk : "))
    keterangan_masuk = input("Keterangan (Optional) = ") 
    val = (id_barang,jumlah_masuk,keterangan_masuk)
    cursor = db.cursor()
    sql = "CALL barang_masuk (%s,%s,%s)"
    cursor.execute(sql,val)
    db.commit()
    print("Data berhasil ditambahkan!")

# Barang Keluar
def barang_keluar(db):
    show_semua_barang(db)
    id_barang = int(input("Pilih ID Barang : "))
    jumlah_keluar = int(input("Jumlah Barang Keluar : "))
    keterangan_keluar = input("Keterangan (Optional) = ") 
    val = (id_barang,jumlah_keluar,keterangan_keluar)
    cursor = db.cursor()
    sql = "CALL barang_keluar (%s,%s,%s)"
    cursor.execute(sql,val)
    db.commit()
    print("Data berhasil ditambahkan!")

# Update Informasi Barang
def informasi_barang(db):
    show_semua_barang(db)
    id_barang = int(input("Pilih ID Barang : "))
    print("-----------------------------")
    cursor = db.cursor()
    sql = "SELECT * FROM barang WHERE id_barang=%s"
    val = (id_barang,)
    cursor.execute(sql,val)
    data = cursor.fetchone()
    print("ID Barang :",data[0])
    print("Nama Barang :",data[1])
    print("Stok Barang :",data[2])
    print("Keterangan :",data[3])
    print("Terakhir diperbarui :",data[4])
    print("-----------------------------")
    print("Silahkan Update dengan data terbaru")
    nama_barang = input("Nama Barang : ")
    keterangan_barang = input("Keterangan : ")

    sql = "UPDATE barang SET nama_barang=%s,keterangan=%s, last_update = NOW() WHERE id_barang=%s"
    val =(nama_barang,keterangan_barang,id_barang)
    cursor.execute(sql,val)
    db.commit()
    print("Data berhasil diperbarui!")

# Informasi Barang Masuk
def informasi_barang_masuk(db):
    show_semua_barang(db)
    print("--------------------------------")
    id_barang = int(input("Pilih ID Barang : "))
    cursor = db.cursor()
    sql = "SELECT * FROM barang_masuk WHERE id_barang=%s"
    val = (id_barang,)
    cursor.execute(sql,val)
    results = cursor.fetchall()

    if cursor.rowcount == 0:
        print("Tidak ada data")
    else:
        count = 0
        for data in results:
            count += 1
            print("--------------------------------")
            print("No :",count)
            print("Tanggal Masuk :",data[1])
            print("Jumlah Barang Masuk :",data[2])
            print("Keterangan :",data[3])

# Informasi Barang Keluar
def informasi_barang_keluar(db):
    show_semua_barang(db)
    print("--------------------------------")
    id_barang = int(input("Pilih ID Barang : "))
    cursor = db.cursor()
    sql = "SELECT * FROM barang_keluar WHERE id_barang=%s"
    val = (id_barang,)
    cursor.execute(sql,val)
    results = cursor.fetchall()

    if cursor.rowcount == 0:
        print("Tidak ada data barang keluar")
    else:
        count = 0
        for data in results:
            count += 1
            print("--------------------------------")
            print("No :",count)
            print("Tanggal Keluar :",data[1])
            print("Jumlah Barang Keluar :",data[2])
            print("Keterangan :",data[3])

# Hapus Barang
def hapus_barang(db):
    show_semua_barang(db)
    id_barang = int(input("Pilih ID Barang : "))
    print("-----------------------------")
    cursor = db.cursor()
    sql = "DELETE FROM barang WHERE id_barang=%s"
    val = (id_barang,)
    cursor.execute(sql,val)
    db.commit()
    print("Data Berhasil Dihapus!")

# Pilih Menu
def show_menu(db):
    print("== STOK BARANG WITH PYTHON ==")
    print("1. Tampilkan Data Barang")
    print("2. Tambahkan Data Barang")
    print("3. Barang Masuk")
    print("4. Barang Keluar")
    print("5. Update Informasi Barang")
    print("6. Informasi Barang Masuk")
    print("7. Informasi Barang Keluar")
    print("8. Hapus Barang")
    print("0. Keluar")
    menu = int(input("Pilih Menu Nomor : "))
    os.system('cls')
    if menu == 1:
        show_semua_barang(db)
    elif menu == 2:
        barang_baru(db)
    elif menu == 3:
        barang_masuk(db)
    elif menu == 4:
        barang_keluar(db)
    elif menu == 5:
        informasi_barang(db)
    elif menu == 6:
        informasi_barang_masuk(db)
    elif menu == 7:
        informasi_barang_keluar(db)
    elif menu == 8:
        hapus_barang(db)
    elif menu == 0:
        exit()
    else:
        print("Pilihan anda salah!")

if __name__ == "__main__":
  while(True):
    show_menu(db)
