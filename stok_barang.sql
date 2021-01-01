-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 01 Jan 2021 pada 14.44
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
	INSERT INTO barang (nama_barang,stok_barang) 	 VALUES(nama_barang_masuk,jumlah_barang_masuk);
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
  `last_update` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `barang`
--

INSERT INTO `barang` (`id_barang`, `nama_barang`, `stok_barang`, `last_update`) VALUES
(68, 'Spidol Papan Tulis Snowman (Permanen)', 198, '2021-01-01 21:36:26'),
(69, 'Spidol Papan Tulis Snowman (Non Permanen)', 0, '2021-01-01 21:37:25'),
(70, 'Penghapus Papan Tulis', 123, '2021-01-01 21:39:26');

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
(15, 68, '2021-01-01 21:36:26', 'Segel rusak', 2),
(16, 69, '2021-01-01 21:37:25', 'Hilang', 500);

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
(83, 68, '2021-01-01 21:36:01', 200, '10 barang segelnya sudah rusak'),
(84, 69, '2021-01-01 21:36:56', 500, ''),
(85, 70, '2021-01-01 21:39:26', 123, '');

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
  MODIFY `id_barang` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=72;

--
-- AUTO_INCREMENT untuk tabel `barang_keluar`
--
ALTER TABLE `barang_keluar`
  MODIFY `id_keluar` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT untuk tabel `barang_masuk`
--
ALTER TABLE `barang_masuk`
  MODIFY `id_masuk` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=88;

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
