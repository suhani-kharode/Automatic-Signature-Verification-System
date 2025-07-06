-- MySQL Administrator dump 1.4
--
-- ------------------------------------------------------
-- Server version	5.5.62


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


--
-- Create schema signature_verification_system_db
--

CREATE DATABASE IF NOT EXISTS signature_verification_system_db;
USE signature_verification_system_db;

--
-- Definition of table `user_registration_details`
--

DROP TABLE IF EXISTS `user_registration_details`;
CREATE TABLE `user_registration_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `contact` varchar(15) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `password` (`password`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_registration_details`
--

/*!40000 ALTER TABLE `user_registration_details` DISABLE KEYS */;
INSERT INTO `user_registration_details` (`id`,`name`,`contact`,`email`,`password`) VALUES 
 (1,'aishwarya','1234512345','aish@gmail.com','aish'),
 (2,'ria','5678956789','ria@gmail.com','ria');
/*!40000 ALTER TABLE `user_registration_details` ENABLE KEYS */;


--
-- Definition of table `user_signature_details`
--

DROP TABLE IF EXISTS `user_signature_details`;
CREATE TABLE `user_signature_details` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `signature_path` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_signature_details`
--

/*!40000 ALTER TABLE `user_signature_details` DISABLE KEYS */;
INSERT INTO `user_signature_details` (`id`,`name`,`signature_path`) VALUES 
 (1,'saili','/media/original_1_1_NCs4k5G.png'),
 (2,'mia','/media/original_2_1_XL2wX4d.png'),
 (3,'mansi','/media/original_2_12.png'),
 (4,'radha','/media/sign.jpg'),
 (5,'vaishnavi','/media/original_4_1_7bsl4uB.png'),
 (6,'vaishnavi','/media/original_4_1_gQrzhfp.png'),
 (8,'sakshi','/media/original_5_1_HFnwmhL.png'),
 (9,'manushi','/media/original_7_1.png'),
 (10,'divya','/media/original_8_1.png');
/*!40000 ALTER TABLE `user_signature_details` ENABLE KEYS */;




/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
