-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 04, 2025 at 05:45 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `disease_pred`
--

-- --------------------------------------------------------

--
-- Table structure for table `add_check`
--

CREATE TABLE `add_check` (
  `add_id` int(10) NOT NULL,
  `ngo_name` text NOT NULL,
  `type_check` varchar(255) NOT NULL,
  `date` date NOT NULL,
  `time` varchar(6) NOT NULL,
  `contact` varchar(333) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `add_check`
--

INSERT INTO `add_check` (`add_id`, `ngo_name`, `type_check`, `date`, `time`, `contact`) VALUES
(1, 'nss', 'eye checkup', '2023-04-09', '01:00', '898989989'),
(2, 'nss', 'teeth checkup', '2023-04-16', '0000-0', '898988989'),
(3, 'tanmann', 'free check-ups', '2023-05-20', '13:00', '898989898'),
(4, 'tanmann', 'eye checkup', '2023-05-20', '23:15', '898989898'),
(5, 'tanmann', 'physical check-up', '2023-05-27', '10:00', '989898989'),
(6, 'Demongo', 'blood donation', '2025-03-08', '08:45', '789456123'),
(7, 'demo', 'body check up', '2025-03-26', '10:34', '897524178');

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `appointment_id` int(11) NOT NULL,
  `doctor_id` int(11) NOT NULL,
  `doctor_name` varchar(100) NOT NULL,
  `patient_name` varchar(100) NOT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` time NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`appointment_id`, `doctor_id`, `doctor_name`, `patient_name`, `appointment_date`, `appointment_time`, `created_at`) VALUES
(1, 6, 'Dr. Amit', 'Swen Rodrigues', '2025-04-24', '11:00:00', '2025-04-04 14:49:41');

-- --------------------------------------------------------

--
-- Table structure for table `blood_donation`
--

CREATE TABLE `blood_donation` (
  `id` int(11) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `age` int(11) NOT NULL,
  `blood_group` varchar(5) NOT NULL,
  `past_illness` varchar(255) DEFAULT NULL,
  `mobile` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `b_donation`
--

CREATE TABLE `b_donation` (
  `b_id` int(10) NOT NULL,
  `name` varchar(255) NOT NULL,
  `blood_group` varchar(255) NOT NULL,
  `age` int(200) NOT NULL,
  `mobile` varchar(200) NOT NULL,
  `past_illness` varchar(255) NOT NULL,
  `posted_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `b_donation`
--

INSERT INTO `b_donation` (`b_id`, `name`, `blood_group`, `age`, `mobile`, `past_illness`, `posted_at`) VALUES
(33, 'Neil Lopes', 'O+', 20, '9172282492', 'None', '2025-04-01 15:17:34'),
(34, 'Ross Dmello', 'O+', 20, '7045197220', 'None', '2025-04-01 15:29:27'),
(35, 'Swen Rodrigues', 'O+', 20, '8767813654', 'None', '2025-04-03 05:35:16');

-- --------------------------------------------------------

--
-- Table structure for table `doctors`
--

CREATE TABLE `doctors` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `specialty` varchar(255) NOT NULL,
  `location` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `doc_list`
--

CREATE TABLE `doc_list` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `specialty` varchar(100) NOT NULL,
  `location` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doc_list`
--

INSERT INTO `doc_list` (`id`, `name`, `specialty`, `location`) VALUES
(1, 'Dr. Hemant Bhandari', 'Dermatologist', 'Nagpur'),
(2, 'Dr. Hitesh Kubadia', 'Dermatologist', 'Pune'),
(3, 'Dr. Om Parshuram Patil', 'Dermatologist', 'Aurangabad'),
(4, 'Dr. Prasad Chaudhari', 'Neurologist', 'Aurangabad'),
(5, 'Dr. Safiuddin', 'Cardiologist', 'Aurangabad'),
(6, 'Dr. Sarang Deshpande', 'Pediatrician', 'Pune'),
(7, 'Dr. Girish Bhalerao', 'Dermatologist', 'Nashik'),
(8, 'Dr. Dhrumin Sangoi', 'General Surgeon', 'Nagpur'),
(9, 'Dr. Abhijit Kale', 'Pediatrician', 'Pune'),
(10, 'Dr. Mudit Khanna', 'Dermatologist', 'Nashik'),
(11, 'Dr. Mohit Kukreja', 'ENT Specialist', 'Mumbai'),
(12, 'Dr. Kunal Makhija', 'ENT Specialist', 'Nagpur'),
(13, 'Dr. Biswajeet Naidu', 'Pediatrician', 'Nagpur'),
(14, 'Dr. Ranjan Burnwal', 'Dermatologist', 'Mumbai'),
(15, 'Dr. Kaustubh Ravindra Durve', 'ENT Specialist', 'Pune'),
(16, 'Dr. Ajay Rathod', 'General Surgeon', 'Aurangabad'),
(17, 'Dr. Prajyot Jagtap', 'General Surgeon', 'Aurangabad'),
(18, 'Dr. Satyen Mehta', 'Cardiologist', 'Pune'),
(19, 'Dr. Ashish Agarwal', 'Cardiologist', 'Mumbai'),
(20, 'Dr. Yajuvendra Gawai', 'Pediatrician', 'Nashik'),
(21, 'Dr. Samarjit S. Bansal', 'ENT Specialist', 'Nagpur'),
(22, 'Dr. Umesh Shetty', 'Cardiologist', 'Pune'),
(23, 'Dr. Shreedhar Archik', 'ENT Specialist', 'Pune'),
(24, 'Dr. Uday M Pawar', 'Pediatrician', 'Nashik'),
(25, 'Dr. Bhavin Shial', 'General Surgeon', 'Nagpur'),
(26, 'Dr. Darshan Bafna', 'Cardiologist', 'Mumbai'),
(27, 'Dr. Zahir Abbas Merchant', 'Pediatrician', 'Mumbai'),
(28, 'Dr. Neelkanth Dhamnaskar', 'ENT Specialist', 'Mumbai'),
(29, 'Dr. Shaival Chauhan', 'ENT Specialist', 'Nagpur'),
(30, 'Dr. Utkarsh Pawar', 'General Surgeon', 'Aurangabad'),
(31, 'Dr. Jairam Jagiasi', 'ENT Specialist', 'Mumbai'),
(32, 'Dr. Chirag Patel', 'Cardiologist', 'Nagpur'),
(33, 'Dr. Devesh Dholakia', 'Cardiologist', 'Nashik'),
(34, 'Dr. Kapil Lalwani', 'General Surgeon', 'Aurangabad'),
(35, 'Dr. Akash A Saraogi', 'General Surgeon', 'Mumbai'),
(36, 'Dr. Siddharth M. Shah', 'Cardiologist', 'Nashik'),
(37, 'Dr. Rajesh Gayakwad', 'ENT Specialist', 'Nagpur'),
(38, 'Dr. Lalit Panchal', 'Cardiologist', 'Mumbai'),
(39, 'Dr. Amit Grover', 'Cardiologist', 'Nagpur'),
(40, 'Dr. Rahul Prakash', 'Pediatrician', 'Aurangabad'),
(41, 'Dr. Atul Patil', 'Cardiologist', 'Aurangabad'),
(42, 'Dr. Anmol R Mittal', 'Cardiologist', 'Mumbai'),
(43, 'Dr. Chintan H. Patel', 'Cardiologist', 'Pune'),
(44, 'Dr. Saikat Jena', 'General Surgeon', 'Mumbai'),
(45, 'Dr. Nihit Gadodia', 'Pediatrician', 'Nagpur'),
(46, 'Dr. Pranjal Kodkani', 'Dermatologist', 'Nashik'),
(47, 'Dr. Jeet Savla', 'General Surgeon', 'Nashik'),
(48, 'Dr. Mayur Rabhadiya', 'Cardiologist', 'Mumbai'),
(49, 'Dr. Anoop Dhamangaonkar', 'Dermatologist', 'Aurangabad'),
(50, 'Dr. Siddharth Shah', 'Neurologist', 'Aurangabad'),
(51, 'Dr. Viraj N Gandbhir', 'Dermatologist', 'Mumbai'),
(52, 'Dr. Hardik Bhangde', 'General Surgeon', 'Aurangabad'),
(53, 'Dr. Kumar R Dussa', 'Neurologist', 'Aurangabad'),
(54, 'Dr. M T Khan', 'Cardiologist', 'Aurangabad'),
(55, 'Dr. Nisarg Bhatt', 'Neurologist', 'Nashik'),
(56, 'Dr. Aditya Rao', 'Dermatologist', 'Mumbai'),
(57, 'Dr. Govind Baranwal', 'General Surgeon', 'Mumbai'),
(58, 'Dr. Chirag Dalal', 'General Surgeon', 'Aurangabad'),
(59, 'Dr. Neeraj R Bijlani', 'Neurologist', 'Aurangabad'),
(60, 'Dr. Rakesh Dhake', 'Dermatologist', 'Aurangabad'),
(61, 'Dr. Amyn Rajani', 'ENT Specialist', 'Aurangabad'),
(62, 'Dr. Vikas Jain', 'Cardiologist', 'Mumbai'),
(63, 'Dr. Vaibhav B. Kasodekar', 'Pediatrician', 'Mumbai'),
(64, 'Dr. Ashok Rajgopal', 'ENT Specialist', 'Nagpur'),
(65, 'Dr. Kishore Manek', 'Cardiologist', 'Nashik'),
(66, 'Dr. Shantanu K Kundgir', 'Neurologist', 'Aurangabad'),
(67, 'Dr. Aditya Sai', 'Neurologist', 'Mumbai'),
(68, 'Dr. Chetan Anchan', 'Neurologist', 'Nagpur'),
(69, 'Dr. D. Shrinivas', 'Cardiologist', 'Pune'),
(70, 'Dr. Dnyanesh Lad', 'Pediatrician', 'Nagpur'),
(71, 'Dr. Santosh Shetty', 'ENT Specialist', 'Mumbai'),
(72, 'Dr. Bhushan Sabnis', 'General Surgeon', 'Pune'),
(73, 'Dr. Sachin Vilhekar', 'Cardiologist', 'Nashik'),
(74, 'Dr. Nilen Shah', 'ENT Specialist', 'Nashik'),
(75, 'Dr. Arjun Dhawale', 'General Surgeon', 'Pune');

-- --------------------------------------------------------

--
-- Table structure for table `doc_user`
--

CREATE TABLE `doc_user` (
  `sr_no` int(10) NOT NULL,
  `d_name` varchar(233) NOT NULL,
  `email` varchar(333) NOT NULL,
  `passwrd1` varchar(333) NOT NULL,
  `number` varchar(333) NOT NULL,
  `address` varchar(333) NOT NULL,
  `special` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doc_user`
--

INSERT INTO `doc_user` (`sr_no`, `d_name`, `email`, `passwrd1`, `number`, `address`, `special`) VALUES
(6, 'Dr. Amit', 'amit@gmail.com', '$2b$12$UtrbFFM/JnqBR6R.tNTE3eo4knvRttwyBTuTrcf3zjgRcpBtwVr0G', '1234567801', 'lincon street 41', 'Cardiologist'),
(7, 'Dr. Mehra', 'mehra@gmail.com', '$2b$12$1P1nHGB/cD3slRrtmIAywOTvv9H9DQIGR9H2QRHmcrk2sP3WF2OX.', '789456123', '41 street ', 'Neurologist'),
(8, 'abc', 'abc@123', '$2b$12$9rdgErd90KQf8OH8/TYbe.ROeR4qeZqmFnQRYfeuobBx4m0cnVflG', '123457890', '44 street', 'Cardiologist');

-- --------------------------------------------------------

--
-- Table structure for table `ngo_users`
--

CREATE TABLE `ngo_users` (
  `ngo_name` varchar(255) NOT NULL,
  `pass1` varchar(255) NOT NULL,
  `type1` varchar(255) NOT NULL,
  `number` varchar(244) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `sr_no` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ngo_users`
--

INSERT INTO `ngo_users` (`ngo_name`, `pass1`, `type1`, `number`, `created_at`, `sr_no`) VALUES
('wie', '$2b$12$0QElBBARmfdAuiVBCUtIzO9sLf5AOyr2oSLpHU6mNNQ09U3lWbpDm', 'blood camps', '6768787878', '2023-01-16 16:47:12', 4),
('adani', '$2b$12$/5rG60XacEiQqGnVVo2SZuTdVRLYZVEjXdc3zLurlnq8Lcjd1oS.G', 'social work', '898989898', '2023-02-02 18:55:10', 5),
('sav', '$2b$12$MZ5Zl3QtKDIYX3LtJFjy5OU8oV8Cn52oUzd.bWiVCZGPKJ9kHVbPm', 'check-ups', '8989989889', '2023-02-09 08:15:22', 6),
('nss12', '$2b$12$W8XAWuXLqBKAUhL/B4tBuuaA3BVQhZ0W7oN340LsBYYgOTE1V1Ftu', 'free medications', '8080909090', '2023-03-15 17:04:19', 7),
('nss34', '$2b$12$433CuJOP/uHnu6fW4CpKgeCa9TUwA1QeHSbIhSlyvu3XY3p0lV0nm', 'check-ups', '809090909', '2023-03-15 17:05:41', 8),
('key', '$2b$12$sOv22YeVIi6NQAlSBFoe..UIyBxR9yj5/p75tOL69MEU7f141qKs2', 'blood camps', '8989898898', '2023-04-07 09:42:38', 9),
('tanmann', '$2b$12$nGTAqcrUKCigSbO67.Cxte68unyKhqhFPMcvuBnE.FG11OVbfnwcu', 'check-ups', '8998989898', '2023-05-01 08:09:09', 10),
('Demongo', '$2b$12$NVgOOD77wuwu2K5U3VQYmOHBpXteNtuGZFter4rRnbBCP0rNkUSwG', 'community', '012345678', '2025-02-28 16:10:46', 11),
('demo', '$2b$12$z0u4ukX.GC0ZnCtoU1eqL.2gj4X6fBG/N7wzOwdlqtAqPEShN/m4q', 'blood donation', '789456123', '2025-03-01 05:03:16', 12),
('NGO123', '$2b$12$ZDnD20UjUmBiiTq6EK/vMubTANQDIeVkZBJ0RDAiQ766EQrQZPoXa', 'community', '789456123', '2025-03-29 10:35:58', 13);

-- --------------------------------------------------------

--
-- Table structure for table `patient_users`
--

CREATE TABLE `patient_users` (
  `sr_no` int(10) NOT NULL,
  `p_name` varchar(233) NOT NULL,
  `number` varchar(333) NOT NULL,
  `email` varchar(333) NOT NULL,
  `password1` varchar(333) NOT NULL,
  `address` varchar(333) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patient_users`
--

INSERT INTO `patient_users` (`sr_no`, `p_name`, `number`, `email`, `password1`, `address`, `created_at`) VALUES
(10, 'swen', '1234567890', 'swen@gmail.com', '$2b$12$ioPdzk.0jxeuT3e2JAW5xOSW2NrOxZDnr8D1yq/Hrb8EroyPAT5gy', 'nan', '2024-11-16 07:22:00'),
(11, 'Swen', '123456788', 'dummy@gmail.com', '$2b$12$OdVIX8SxW/2Rq3gyvuRl.eb7creTR9Uum0W8.VRurG3SjvXctU8i.', 'fr.crce', '2025-02-28 16:15:15'),
(12, 'Roman', '789456123', 'rom123@gmail.com', '$2b$12$RTrHjQAwzj0WrpxezueBU.jZNNkLl2I9EZWMmqC1iLK7lDuDJlAPS', 'baker street,42 mary road', '2025-03-29 10:17:47');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `add_check`
--
ALTER TABLE `add_check`
  ADD PRIMARY KEY (`add_id`);

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`appointment_id`),
  ADD KEY `doctor_id` (`doctor_id`);

--
-- Indexes for table `blood_donation`
--
ALTER TABLE `blood_donation`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `b_donation`
--
ALTER TABLE `b_donation`
  ADD PRIMARY KEY (`b_id`);

--
-- Indexes for table `doctors`
--
ALTER TABLE `doctors`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `doc_list`
--
ALTER TABLE `doc_list`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `doc_user`
--
ALTER TABLE `doc_user`
  ADD PRIMARY KEY (`sr_no`);

--
-- Indexes for table `ngo_users`
--
ALTER TABLE `ngo_users`
  ADD PRIMARY KEY (`sr_no`);

--
-- Indexes for table `patient_users`
--
ALTER TABLE `patient_users`
  ADD PRIMARY KEY (`sr_no`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `add_check`
--
ALTER TABLE `add_check`
  MODIFY `add_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `appointment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `blood_donation`
--
ALTER TABLE `blood_donation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `b_donation`
--
ALTER TABLE `b_donation`
  MODIFY `b_id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `doctors`
--
ALTER TABLE `doctors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `doc_list`
--
ALTER TABLE `doc_list`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=76;

--
-- AUTO_INCREMENT for table `doc_user`
--
ALTER TABLE `doc_user`
  MODIFY `sr_no` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `ngo_users`
--
ALTER TABLE `ngo_users`
  MODIFY `sr_no` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `patient_users`
--
ALTER TABLE `patient_users`
  MODIFY `sr_no` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointments`
--
ALTER TABLE `appointments`
  ADD CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `doc_user` (`sr_no`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
