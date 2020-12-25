-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 20 Des 2020 pada 00.18
-- Versi server: 10.4.17-MariaDB
-- Versi PHP: 8.0.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `stok_barang`
--

DELIMITER $$
--
-- Prosedur
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `barang_baru` (IN `nama_barang_masuk` VARCHAR(100), IN `jumlah_barang_masuk` INT, IN `keterangan_barang_masuk` VARCHAR(255))  BEGIN
	INSERT INTO barang (nama_barang,stok_barang,keterangan) 	 VALUES(nama_barang_masuk,jumlah_barang_masuk,keterangan_barang_masuk);
   INSERT INTO barang_masuk(id_barang,tanggal_masuk,jumlah_masuk,keterangan_masuk) 
   VALUES (LAST_INSERT_ID(),NOW(),jumlah_barang_masuk,keterangan_barang_masuk);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `barang_keluar` (IN `id_barang_keluar` INT, IN `jumlah_barang_keluar` INT, IN `keterangan_barang_keluar` VARCHAR(255))  NO SQL
BEGIN
INSERT INTO barang_keluar (id_barang,jumlah_keluar,keterangan_keluar)
VALUES
(id_barang_keluar,jumlah_barang_keluar,keterangan_barang_keluar);
UPDATE barang
SET stok_barang = stok_barang - jumlah_barang_keluar,
last_update = NOW()
WHERE id_barang = id_barang_keluar;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `barang_masuk` (IN `id_barang_masuk` INT, IN `jumlah_barang_masuk` INT, IN `keterangan_barang_masuk` VARCHAR(255))  NO SQL
BEGIN
INSERT INTO barang_masuk (id_barang,jumlah_masuk,keterangan_masuk)
VALUES(id_barang_masuk,jumlah_barang_masuk,keterangan_barang_masuk);
UPDATE barang
SET stok_barang = stok_barang + jumlah_barang_masuk,
last_update = NOW()
WHERE id_barang = id_barang_masuk;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Struktur dari tabel `barang`
--

CREATE TABLE `barang` (
  `id_barang` int(11) NOT NULL,
  `nama_barang` varchar(100) NOT NULL,
  `stok_barang` int(11) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  `last_update` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `barang`
--

INSERT INTO `barang` (`id_barang`, `nama_barang`, `stok_barang`, `keterangan`, `last_update`) VALUES
(2, 'Keyboard', 25, '', '2020-12-19 23:59:59'),
(3, 'Mouse', 45, '', '2020-12-20 00:02:07');

-- --------------------------------------------------------

--
-- Struktur dari tabel `barang_keluar`
--

CREATE TABLE `barang_keluar` (
  `id_keluar` int(11) NOT NULL,
  `id_barang` int(11) NOT NULL,
  `tanggal_keluar` datetime NOT NULL DEFAULT current_timestamp(),
  `keterangan_keluar` varchar(255) DEFAULT NULL,
  `jumlah_keluar` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `barang_keluar`
--

INSERT INTO `barang_keluar` (`id_keluar`, `id_barang`, `tanggal_keluar`, `keterangan_keluar`, `jumlah_keluar`) VALUES
(2, 3, '2020-12-20 00:00:21', '', 5);

-- --------------------------------------------------------

--
-- Struktur dari tabel `barang_masuk`
--

CREATE TABLE `barang_masuk` (
  `id_masuk` int(11) NOT NULL,
  `id_barang` int(11) NOT NULL,
  `tanggal_masuk` datetime NOT NULL DEFAULT current_timestamp(),
  `jumlah_masuk` int(11) NOT NULL,
  `keterangan_masuk` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `barang_masuk`
--

INSERT INTO `barang_masuk` (`id_masuk`, `id_barang`, `tanggal_masuk`, `jumlah_masuk`, `keterangan_masuk`) VALUES
(3, 2, '2020-12-19 23:59:15', 20, ''),
(4, 3, '2020-12-19 23:59:34', 50, 'In the house'),
(5, 2, '2020-12-19 23:59:59', 5, '');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `barang`
--
ALTER TABLE `barang`
  ADD PRIMARY KEY (`id_barang`);

--
-- Indeks untuk tabel `barang_keluar`
--
ALTER TABLE `barang_keluar`
  ADD PRIMARY KEY (`id_keluar`),
  ADD KEY `id_barang_keluar` (`id_barang`);

--
-- Indeks untuk tabel `barang_masuk`
--
ALTER TABLE `barang_masuk`
  ADD PRIMARY KEY (`id_masuk`),
  ADD KEY `id_barang_masuk` (`id_barang`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `barang`
--
ALTER TABLE `barang`
  MODIFY `id_barang` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `barang_keluar`
--
ALTER TABLE `barang_keluar`
  MODIFY `id_keluar` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT untuk tabel `barang_masuk`
--
ALTER TABLE `barang_masuk`
  MODIFY `id_masuk` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `barang_keluar`
--
ALTER TABLE `barang_keluar`
  ADD CONSTRAINT `id_barang_keluar` FOREIGN KEY (`id_barang`) REFERENCES `barang` (`id_barang`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `barang_masuk`
--
ALTER TABLE `barang_masuk`
  ADD CONSTRAINT `id_barang_masuk` FOREIGN KEY (`id_barang`) REFERENCES `barang` (`id_barang`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
