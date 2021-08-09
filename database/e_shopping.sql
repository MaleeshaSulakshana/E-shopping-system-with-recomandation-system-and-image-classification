-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 12, 2021 at 12:23 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `e_shopping`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` varchar(30) NOT NULL,
  `first_name` varchar(25) NOT NULL,
  `last_name` varchar(25) NOT NULL,
  `email` varchar(70) NOT NULL,
  `psw` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `first_name`, `last_name`, `email`, `psw`) VALUES
('12345', 'Maleesha', 'Sulakshana', 'mpmsulakshana@gmail.com', 'mano1998');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_code` varchar(30) NOT NULL,
  `product_title` varchar(100) NOT NULL,
  `product_category` varchar(100) NOT NULL,
  `product_sub_category` varchar(100) NOT NULL,
  `price` varchar(20) NOT NULL,
  `discount` varchar(25) NOT NULL,
  `description` varchar(500) NOT NULL,
  `added_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_code`, `product_title`, `product_category`, `product_sub_category`, `price`, `discount`, `description`, `added_date`) VALUES
('1504826', 'Gent Jacket', 'Gents', 'Jackets', '4500.00', '', 'Imported original lather gent jacket. Import from kenya.', '2021-05-06'),
('1504830', 'Ladies Shoe', 'Ladies', 'Shoe', '2500.00', '', 'Imported ladies shoe. Import from America. 100% quality. 3 months warranty.', '2021-05-06'),
('1504832', 'Ladies T-Shirt', 'Ladies', 'T-Shirt', '1500.00', '', 'Imported ladies t-shirt. Import from India.', '2021-05-08');

-- --------------------------------------------------------

--
-- Table structure for table `product_details`
--

CREATE TABLE `product_details` (
  `product_code` varchar(30) NOT NULL,
  `product_colour` varchar(20) NOT NULL,
  `image_1` varchar(50) NOT NULL,
  `image_2` varchar(50) NOT NULL,
  `image_3` varchar(50) NOT NULL,
  `image_4` varchar(50) NOT NULL,
  `image_5` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `product_details`
--

INSERT INTO `product_details` (`product_code`, `product_colour`, `image_1`, `image_2`, `image_3`, `image_4`, `image_5`) VALUES
('1504826', 'Brown', '1504826_Brown_1.jpg', '1504826_Brown_2.jpg', 'None', 'None', 'None'),
('1504826', 'Blue', '1504826_Blue_1.jpg', 'None', 'None', 'None', 'None'),
('1504832', 'White', '1504832_White_1.jpg', '1504832_White_2.jpg', 'None', 'None', 'None'),
('1504832', 'Black', '1504832_Black_1.jpg', 'None', 'None', 'None', 'None');

-- --------------------------------------------------------

--
-- Table structure for table `product_sizes`
--

CREATE TABLE `product_sizes` (
  `product_code` varchar(50) NOT NULL,
  `product_colour` varchar(20) NOT NULL,
  `product_size` varchar(20) NOT NULL,
  `product_qty` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `product_sizes`
--

INSERT INTO `product_sizes` (`product_code`, `product_colour`, `product_size`, `product_qty`) VALUES
('1504826', 'Brown', 'S', 9),
('1504826', 'Brown', 'M', 17),
('1504832', 'White', 'S', 19),
('1504832', 'Black', 'M', 21);

-- --------------------------------------------------------

--
-- Table structure for table `purches`
--

CREATE TABLE `purches` (
  `purchase_id` varchar(50) NOT NULL,
  `user_id` varchar(30) NOT NULL,
  `product_code` varchar(50) NOT NULL,
  `product_colour` varchar(20) NOT NULL,
  `product_size` varchar(12) NOT NULL,
  `qty` int(12) NOT NULL,
  `price` varchar(30) NOT NULL,
  `purchase_date` date DEFAULT NULL,
  `delivered` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `purches`
--

INSERT INTO `purches` (`purchase_id`, `user_id`, `product_code`, `product_colour`, `product_size`, `qty`, `price`, `purchase_date`, `delivered`) VALUES
('20210510003015797906', 'Maleesha951245', '1504826', 'Brown', 'S', 1, '4500.0', '2021-05-10', 'no'),
('20210510003438163708', 'Maleesha951245', '1504826', 'Brown', 'M', 1, '4500.0', '2021-05-10', 'no'),
('20210510003438163708', 'Maleesha951245', '1504832', 'Black', 'M', 1, '1500.0', '2021-05-10', 'no');

-- --------------------------------------------------------

--
-- Table structure for table `searched`
--

CREATE TABLE `searched` (
  `user_id` varchar(30) NOT NULL,
  `product_code` varchar(30) NOT NULL,
  `searched_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `searched`
--

INSERT INTO `searched` (`user_id`, `product_code`, `searched_date`) VALUES
('Maleesha951245', '1504826', '2021-05-10'),
('Maleesha951245', '1504832', '2021-05-10'),
('Maleesha951245', '1504832', '2021-05-09'),
('Maleesha951255', '1504832', '2021-05-09'),
('Maleesha951255', '1504832', '2021-05-07'),
('Maleesha951225', '1504832', '2021-05-07'),
('Maleesha951225', '1504832', '2021-05-11'),
('Maleesha951265', '1504832', '2021-05-11'),
('Maleesha951275', '1504832', '2021-05-12'),
('Maleesha951775', '1504832', '2021-05-12'),
('Maleesha951245', '1504832', '2021-05-12'),
('Maleesha951245', '1504826', '2021-05-12');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` varchar(30) NOT NULL,
  `first_name` varchar(20) NOT NULL,
  `last_name` varchar(20) NOT NULL,
  `email` varchar(60) NOT NULL,
  `nic` varchar(12) NOT NULL,
  `mobile_number` int(10) NOT NULL,
  `psw` varchar(25) NOT NULL,
  `profile_pic` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `first_name`, `last_name`, `email`, `nic`, `mobile_number`, `psw`, `profile_pic`) VALUES
('Maleesha951245', 'Maleesha', 'Sulakshana', 'mpmsulakshana@gmail.com', '982760747V', 767950600, 'mano1998', 'Maleesha951245.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `wishlist`
--

CREATE TABLE `wishlist` (
  `user_id` varchar(30) NOT NULL,
  `product_code` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `wishlist`
--

INSERT INTO `wishlist` (`user_id`, `product_code`) VALUES
('Maleesha951245', '1504832');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
