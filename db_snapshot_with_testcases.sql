-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:8889
-- Generation Time: Dec 19, 2021 at 03:01 AM
-- Server version: 5.7.34
-- PHP Version: 7.4.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `project`
--

-- --------------------------------------------------------

--
-- Table structure for table `airline`
--

CREATE TABLE `airline` (
  `airline_name` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`airline_name`) VALUES
('Emirates');

-- --------------------------------------------------------

--
-- Table structure for table `airline_staff`
--

CREATE TABLE `airline_staff` (
  `username` varchar(20) NOT NULL,
  `airline_name` varchar(20) DEFAULT NULL,
  `staff_password` varchar(50) DEFAULT NULL,
  `first_name` varchar(20) DEFAULT NULL,
  `last_name` varchar(20) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airline_staff`
--

INSERT INTO `airline_staff` (`username`, `airline_name`, `staff_password`, `first_name`, `last_name`, `date_of_birth`) VALUES
('admin', 'Emirates', 'abcd', 'Roe', 'Jones', '1978-05-25'),
('student', 'Emirates', 'abcd1234', 'Hello', 'World', '2000-01-01');

-- --------------------------------------------------------

--
-- Table structure for table `airplane`
--

CREATE TABLE `airplane` (
  `airline_name` varchar(20) NOT NULL,
  `airplane_ID` varchar(20) NOT NULL,
  `num_seats` decimal(4,0) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`airline_name`, `airplane_ID`, `num_seats`) VALUES
('Emirates', '1', '4'),
('Emirates', '2', '4'),
('Emirates', '3', '50'),
('Emirates', '500', '2000');

-- --------------------------------------------------------

--
-- Table structure for table `airport`
--

CREATE TABLE `airport` (
  `code` decimal(5,0) NOT NULL,
  `airport_name` varchar(20) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`code`, `airport_name`, `city`) VALUES
('1', 'JFK', 'NYC'),
('2', 'BOS', 'Boston'),
('3', 'PVG', 'Shanghai'),
('4', 'BEI', 'Beijing'),
('5', 'SHEN', 'Shenzhen'),
('6', 'SFO', 'San Francisco'),
('7', 'LAX', 'Los Angeles'),
('8', 'HKA', 'Hong Kong'),
('9', 'ORD', 'Orlando');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `email` varchar(320) NOT NULL,
  `customer_name` varchar(20) DEFAULT NULL,
  `customer_password` varchar(50) DEFAULT NULL,
  `building_number` varchar(20) DEFAULT NULL,
  `street` varchar(20) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `state_province` varchar(20) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `passport_number` varchar(20) DEFAULT NULL,
  `passport_expiration` date DEFAULT NULL,
  `passport_country` varchar(20) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email`, `customer_name`, `customer_password`, `building_number`, `street`, `city`, `state_province`, `phone_number`, `passport_number`, `passport_expiration`, `passport_country`, `date_of_birth`) VALUES
('testcustomer@nyu.edu', 'Test Customer 1', '1234', '1555', 'Jay St', 'Brooklyn', 'New York', '123-4321-4321', '54321', '2025-12-24', 'USA', '1999-12-19'),
('user1@nyu.edu', 'User 1', '1234', '5405', 'Jay St', 'Brooklyn', 'New York', '123-4322-4322', '54322', '2025-12-25', 'USA', '1999-11-19'),
('user2@nyu.edu', 'User 2', '1234', '1702', 'Jay St', 'Brooklyn', 'New York', '123-4323-4323', '54323', '2025-10-24', 'USA', '1999-10-19'),
('user3@nyu.edu', 'User 3', '1234', '1890', 'Jay St', 'Brooklyn', 'New York', '123-4324-4324', '54324', '2025-09-24', 'USA', '1999-09-19');

-- --------------------------------------------------------

--
-- Table structure for table `flight`
--

CREATE TABLE `flight` (
  `airline_name` varchar(20) NOT NULL,
  `flight_number` varchar(20) NOT NULL,
  `departure_date` date NOT NULL,
  `departure_time` time NOT NULL,
  `airplane_ID` varchar(20) DEFAULT NULL,
  `departure_airport` decimal(5,0) DEFAULT NULL,
  `arrival_airport` decimal(5,0) DEFAULT NULL,
  `arrival_date` date DEFAULT NULL,
  `arrival_time` time DEFAULT NULL,
  `base_price` decimal(8,2) DEFAULT NULL,
  `flight_status` varchar(7) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`airline_name`, `flight_number`, `departure_date`, `departure_time`, `airplane_ID`, `departure_airport`, `arrival_airport`, `arrival_date`, `arrival_time`, `base_price`, `flight_status`) VALUES
('Emirates', '102', '2021-11-12', '13:25:25', '3', '6', '7', '2021-11-12', '16:50:25', '300.00', 'on-time'),
('Emirates', '104', '2021-12-09', '13:25:25', '3', '3', '4', '2021-12-09', '16:50:25', '300.00', 'on-time'),
('Emirates', '106', '2021-10-12', '13:25:25', '3', '6', '7', '2021-10-12', '16:50:25', '350.00', 'delayed'),
('Emirates', '134', '2021-08-12', '13:25:25', '3', '1', '2', '2021-08-12', '16:50:25', '300.00', 'delayed'),
('Emirates', '206', '2022-01-09', '13:25:25', '2', '6', '7', '2022-01-09', '16:50:25', '400.00', 'on-time'),
('Emirates', '207', '2022-02-12', '13:25:25', '2', '7', '6', '2022-02-12', '16:50:25', '300.00', 'on-time'),
('Emirates', '296', '2022-01-01', '13:25:25', '1', '3', '6', '2022-01-01', '16:50:25', '3000.00', 'delayed'),
('Emirates', '715', '2021-11-28', '10:25:25', '1', '3', '4', '2021-11-28', '13:50:25', '500.00', 'delayed'),
('Emirates', '839', '2021-02-12', '13:25:25', '3', '5', '6', '2021-02-12', '16:50:25', '800.00', 'on-time'),
('Emirates', '96', '2022-12-18', '10:30:00', '500', '6', '9', '2022-12-18', '16:00:00', '300.00', 'on-time');

-- --------------------------------------------------------

--
-- Stand-in structure for view `phone_count_list`
-- (See below for the actual view)
--
CREATE TABLE `phone_count_list` (
`username` varchar(20)
,`phone_count` bigint(21)
);

-- --------------------------------------------------------

--
-- Table structure for table `rating`
--

CREATE TABLE `rating` (
  `customer_email` varchar(320) NOT NULL,
  `airline_name` varchar(20) NOT NULL,
  `flight_number` varchar(20) NOT NULL,
  `departure_date` date NOT NULL,
  `departure_time` time NOT NULL,
  `rate` decimal(1,0) DEFAULT NULL,
  `rating_comment` varchar(2000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `rating`
--

INSERT INTO `rating` (`customer_email`, `airline_name`, `flight_number`, `departure_date`, `departure_time`, `rate`, `rating_comment`) VALUES
('testcustomer@nyu.edu', 'Emirates', '102', '2021-11-12', '13:25:25', '4', 'Very Comfortable'),
('testcustomer@nyu.edu', 'Emirates', '104', '2021-12-09', '13:25:25', '1', 'Customer care services are not good'),
('testcustomer@nyu.edu', 'Emirates', '715', '2021-11-28', '10:25:25', '3', 'So-so service, not good at all.'),
('user1@nyu.edu', 'Emirates', '102', '2021-11-12', '13:25:25', '5', 'Relaxing, check-in and onboarding very professional'),
('user1@nyu.edu', 'Emirates', '104', '2021-12-09', '13:25:25', '5', 'Comfortable journey and professional'),
('user2@nyu.edu', 'Emirates', '102', '2021-11-12', '13:25:25', '3', 'Satisfied and will use the same flight again');

-- --------------------------------------------------------

--
-- Table structure for table `staff_phone`
--

CREATE TABLE `staff_phone` (
  `username` varchar(20) DEFAULT NULL,
  `phone` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `staff_phone`
--

INSERT INTO `staff_phone` (`username`, `phone`) VALUES
('admin', '111-222-3333'),
('admin', '444-555-6666');

-- --------------------------------------------------------

--
-- Table structure for table `ticket`
--

CREATE TABLE `ticket` (
  `ID` decimal(10,0) NOT NULL,
  `airline_name` varchar(20) DEFAULT NULL,
  `flight_number` varchar(20) DEFAULT NULL,
  `departure_date` date DEFAULT NULL,
  `departure_time` time DEFAULT NULL,
  `customer_email` varchar(320) DEFAULT NULL,
  `sold_price` decimal(8,2) DEFAULT NULL,
  `card_type` varchar(6) DEFAULT NULL,
  `card_number` varchar(20) DEFAULT NULL,
  `name_on_card` varchar(20) DEFAULT NULL,
  `expiration_date` date DEFAULT NULL,
  `purchase_date` date DEFAULT NULL,
  `purchase_time` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ID`, `airline_name`, `flight_number`, `departure_date`, `departure_time`, `customer_email`, `sold_price`, `card_type`, `card_number`, `name_on_card`, `expiration_date`, `purchase_date`, `purchase_time`) VALUES
('1', 'Emirates', '102', '2021-11-12', '13:25:25', 'testcustomer@nyu.edu', '300.00', 'credit', '1111-2222-3333-4444', 'Test Customer 1', '2023-03-01', '2021-10-14', '11:55:55'),
('2', 'Emirates', '102', '2021-11-12', '13:25:25', 'user1@nyu.edu', '300.00', 'credit', '1111-2222-3333-4444', 'User 1', '2023-03-01', '2021-10-13', '11:55:55'),
('3', 'Emirates', '102', '2021-11-12', '13:25:25', 'user2@nyu.edu', '300.00', 'credit', '1111-2222-3333-4444', 'User 2', '2023-03-01', '2021-11-14', '11:55:55'),
('4', 'Emirates', '104', '2021-12-09', '13:25:25', 'user1@nyu.edu', '300.00', 'credit', '1111-2222-3333-4444', 'User 1', '2023-03-01', '2021-10-21', '11:55:55'),
('5', 'Emirates', '104', '2021-12-09', '13:25:25', 'testcustomer@nyu.edu', '300.00', 'credit', '1111-2222-3333-4444', 'Test Customer 1', '2023-03-01', '2021-11-28', '11:55:55'),
('6', 'Emirates', '106', '2021-10-12', '13:25:25', 'testcustomer@nyu.edu', '350.00', 'credit', '1111-2222-3333-4444', 'Test Customer 1', '2023-03-01', '2021-10-05', '11:55:55'),
('7', 'Emirates', '106', '2021-10-12', '13:25:25', 'user3@nyu.edu', '350.00', 'credit', '1111-2222-3333-4444', 'User 3', '2023-03-01', '2021-09-03', '11:55:55'),
('8', 'Emirates', '839', '2021-02-12', '13:25:25', 'user3@nyu.edu', '300.00', 'credit', '1111-2222-3333-4444', 'User 3', '2023-03-01', '2021-02-13', '11:55:55'),
('9', 'Emirates', '102', '2021-11-12', '13:25:25', 'user3@nyu.edu', '360.00', 'credit', '1111-2222-3333-4444', 'User 3', '2023-03-01', '2021-09-03', '11:55:55'),
('11', 'Emirates', '134', '2021-08-12', '13:25:25', 'user3@nyu.edu', '300.00', 'credit', '1111-2222-3333-4444', 'User 3', '2023-03-01', '2021-02-23', '11:55:55'),
('12', 'Emirates', '715', '2021-11-28', '10:25:25', 'testcustomer@nyu.edu', '500.00', 'credit', '1111-2222-3333-4444', 'Test Customer 1', '2023-03-01', '2021-10-05', '11:55:55'),
('14', 'Emirates', '206', '2022-01-09', '13:25:25', 'user3@nyu.edu', '400.00', 'credit', '1111-2222-3333-4444', 'User 3', '2023-03-01', '2021-12-05', '11:55:55'),
('15', 'Emirates', '206', '2022-01-09', '13:25:25', 'user1@nyu.edu', '400.00', 'credit', '1111-2222-3333-4444', 'User 1', '2023-03-01', '2021-12-06', '11:55:55'),
('16', 'Emirates', '206', '2022-01-09', '13:25:25', 'user2@nyu.edu', '400.00', 'credit', '1111-2222-3333-4444', 'User 2', '2023-03-01', '2021-11-19', '11:55:55'),
('17', 'Emirates', '207', '2022-02-12', '13:25:25', 'user1@nyu.edu', '300.00', 'credit', '1111-2222-3333-4444', 'User 1', '2023-03-01', '2021-10-14', '11:55:55'),
('18', 'Emirates', '207', '2022-02-12', '13:25:25', 'testcustomer@nyu.edu', '300.00', 'credit', '1111-2222-3333-4444', 'Test Customer 1', '2023-03-01', '2021-11-25', '11:55:55'),
('20', 'Emirates', '296', '2022-01-01', '13:25:25', 'testcustomer@nyu.edu', '3000.00', 'credit', '1111-2222-3333-4444', 'Test Customer 1', '2023-03-01', '2021-09-12', '11:55:55');

-- --------------------------------------------------------

--
-- Structure for view `phone_count_list`
--
DROP TABLE IF EXISTS `phone_count_list`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `phone_count_list`  AS   (select `A`.`username` AS `username`,count(`b`.`phone`) AS `phone_count` from (`airline_staff` `A` join `staff_phone` `b`) where (`A`.`username` = `b`.`username`) group by `A`.`username`)  ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `airline`
--
ALTER TABLE `airline`
  ADD PRIMARY KEY (`airline_name`);

--
-- Indexes for table `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD PRIMARY KEY (`username`),
  ADD KEY `airline_name` (`airline_name`);

--
-- Indexes for table `airplane`
--
ALTER TABLE `airplane`
  ADD PRIMARY KEY (`airline_name`,`airplane_ID`);

--
-- Indexes for table `airport`
--
ALTER TABLE `airport`
  ADD PRIMARY KEY (`code`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`airline_name`,`flight_number`,`departure_date`,`departure_time`),
  ADD KEY `airline_name` (`airline_name`,`airplane_ID`),
  ADD KEY `departure_airport` (`departure_airport`),
  ADD KEY `arrival_airport` (`arrival_airport`);

--
-- Indexes for table `rating`
--
ALTER TABLE `rating`
  ADD PRIMARY KEY (`customer_email`,`airline_name`,`flight_number`,`departure_date`,`departure_time`),
  ADD KEY `airline_name` (`airline_name`,`flight_number`,`departure_date`,`departure_time`);

--
-- Indexes for table `staff_phone`
--
ALTER TABLE `staff_phone`
  ADD KEY `username` (`username`);

--
-- Indexes for table `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `airline_name` (`airline_name`,`flight_number`,`departure_date`,`departure_time`),
  ADD KEY `customer_email` (`customer_email`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD CONSTRAINT `airline_staff_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `Airline` (`airline_name`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `Airline` (`airline_name`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `flight`
--
ALTER TABLE `flight`
  ADD CONSTRAINT `arrival_airport` FOREIGN KEY (`arrival_airport`) REFERENCES `airport` (`code`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `departure_airport` FOREIGN KEY (`departure_airport`) REFERENCES `airport` (`code`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `Airline` (`airline_name`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`airline_name`,`airplane_ID`) REFERENCES `Airplane` (`airline_name`, `airplane_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `rating`
--
ALTER TABLE `rating`
  ADD CONSTRAINT `rating_ibfk_1` FOREIGN KEY (`customer_email`) REFERENCES `Customer` (`email`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `rating_ibfk_2` FOREIGN KEY (`airline_name`,`flight_number`,`departure_date`,`departure_time`) REFERENCES `Flight` (`airline_name`, `flight_number`, `departure_date`, `departure_time`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `staff_phone`
--
ALTER TABLE `staff_phone`
  ADD CONSTRAINT `staff_phone_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Airline_Staff` (`username`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`airline_name`,`flight_number`,`departure_date`,`departure_time`) REFERENCES `Flight` (`airline_name`, `flight_number`, `departure_date`, `departure_time`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `ticket_ibfk_2` FOREIGN KEY (`customer_email`) REFERENCES `Customer` (`email`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
