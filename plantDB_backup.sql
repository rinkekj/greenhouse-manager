-- MariaDB dump 10.19  Distrib 10.5.9-MariaDB, for osx10.15 (x86_64)
--
-- Host: localhost    Database: plantDB
-- ------------------------------------------------------
-- Server version	10.5.9-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `plantDB`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `plantDB` /*!40100 DEFAULT CHARACTER SET utf8mb4 */;

USE `plantDB`;

--
-- Table structure for table `contacts`
--

DROP TABLE IF EXISTS `contacts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `contacts` (
  `id` varchar(5) NOT NULL,
  `first_name` varchar(64) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `email` varchar(64) DEFAULT NULL,
  `phone` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `ix_contacts_email` (`email`),
  KEY `ix_contacts_first_name` (`first_name`),
  KEY `ix_contacts_last_name` (`last_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contacts`
--

LOCK TABLES `contacts` WRITE;
/*!40000 ALTER TABLE `contacts` DISABLE KEYS */;
/*!40000 ALTER TABLE `contacts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `employees` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(64) DEFAULT NULL,
  `last_name` varchar(64) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_employees_email` (`email`),
  KEY `role_id` (`role_id`),
  KEY `ix_employees_first_name` (`first_name`),
  KEY `ix_employees_last_name` (`last_name`),
  CONSTRAINT `employees_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES (1,'Admin','Account','admin@greenhouse.com','pbkdf2:sha256:150000$SQrzmW0B$d5a0c5a1ae2b26d01a901f1f3e1d36c636eba3bfaa4677bf97e0e53847c6831b',2),(2,'Kevin','Rinke','kevin.rinke@gmail.com','pbkdf2:sha256:150000$k0QTc9zo$3781c47fa15d8bc079549207327c8ff6dd253cd2f8e49771020971040c314fe2',1);
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `families`
--

DROP TABLE IF EXISTS `families`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `families` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(25) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=617 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `families`
--

LOCK TABLES `families` WRITE;
/*!40000 ALTER TABLE `families` DISABLE KEYS */;
INSERT INTO `families` VALUES (45,'Apocynacea'),(65,'Araceae'),(616,'Asphodelaceae'),(54,'Crassulaceae'),(218,'Marantaceae'),(149,'Moraceae'),(32,'Orchidaceae'),(69,'Rubiaceae'),(495,'Strelitziaceae');
/*!40000 ALTER TABLE `families` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genera`
--

DROP TABLE IF EXISTS `genera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `genera` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(25) DEFAULT NULL,
  `family` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `family` (`family`),
  CONSTRAINT `genera_ibfk_1` FOREIGN KEY (`family`) REFERENCES `families` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43616 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genera`
--

LOCK TABLES `genera` WRITE;
/*!40000 ALTER TABLE `genera` DISABLE KEYS */;
INSERT INTO `genera` VALUES (279,'Aloe',616),(1926,'Coffea',69),(2083,'Crassula',54),(2794,'Epipremnum',65),(2795,'Philodendron',65),(3630,'Hoya',45),(4700,'Monstera',65),(6381,'Strelitzia',495),(6850,'Vanilla',32),(8147,'Raphidophora',65),(13632,'Goeppertia',218),(13633,'Stromanthe',218),(43615,'Ficus',149);
/*!40000 ALTER TABLE `genera` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `items` (
  `sku` varchar(5) NOT NULL,
  `quantity` int(11) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `location` varchar(1) DEFAULT NULL,
  `living` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`sku`),
  UNIQUE KEY `sku` (`sku`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`living` in (0,1))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `plant` varchar(5) NOT NULL,
  `water` tinyint(1) NOT NULL,
  `feed` tinyint(1) NOT NULL,
  `date` date NOT NULL,
  `notes` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `plant` (`plant`),
  CONSTRAINT `logs_ibfk_1` FOREIGN KEY (`plant`) REFERENCES `plants` (`sku`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`water` in (0,1)),
  CONSTRAINT `CONSTRAINT_2` CHECK (`feed` in (0,1))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orders` (
  `id` varchar(5) NOT NULL,
  `item` varchar(5) NOT NULL,
  `qty` int(11) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `date_received` date DEFAULT NULL,
  `supplier` varchar(5) NOT NULL,
  PRIMARY KEY (`id`,`item`),
  KEY `supplier` (`supplier`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`supplier`) REFERENCES `suppliers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plants`
--

DROP TABLE IF EXISTS `plants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `plants` (
  `sku` varchar(5) NOT NULL,
  `species` int(11) DEFAULT NULL,
  `variety` varchar(5) DEFAULT NULL,
  `size` int(11) DEFAULT NULL,
  `user` int(11) DEFAULT NULL,
  `date_received` date DEFAULT NULL,
  PRIMARY KEY (`sku`),
  UNIQUE KEY `sku` (`sku`),
  KEY `species` (`species`),
  KEY `variety` (`variety`),
  KEY `user` (`user`),
  CONSTRAINT `plants_ibfk_1` FOREIGN KEY (`sku`) REFERENCES `items` (`sku`),
  CONSTRAINT `plants_ibfk_2` FOREIGN KEY (`species`) REFERENCES `species` (`id`),
  CONSTRAINT `plants_ibfk_3` FOREIGN KEY (`variety`) REFERENCES `varieties` (`id`),
  CONSTRAINT `plants_ibfk_4` FOREIGN KEY (`user`) REFERENCES `employees` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plants`
--

LOCK TABLES `plants` WRITE;
/*!40000 ALTER TABLE `plants` DISABLE KEYS */;
/*!40000 ALTER TABLE `plants` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products` (
  `sku` varchar(5) NOT NULL,
  `name` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`sku`),
  UNIQUE KEY `sku` (`sku`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`sku`) REFERENCES `items` (`sku`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `index` varchar(64) DEFAULT NULL,
  `default` tinyint(1) DEFAULT NULL,
  `permissions` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_roles_default` (`default`),
  CONSTRAINT `CONSTRAINT_1` CHECK (`default` in (0,1))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Employee','main',1,1),(2,'Administrator','admin',0,255);
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sales`
--

DROP TABLE IF EXISTS `sales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sales` (
  `id` varchar(5) NOT NULL,
  `date` date DEFAULT NULL,
  `customer` varchar(5) NOT NULL,
  `item` varchar(5) NOT NULL,
  `qty` int(11) DEFAULT NULL,
  `salePrice` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`,`item`),
  KEY `customer` (`customer`),
  CONSTRAINT `sales_ibfk_1` FOREIGN KEY (`customer`) REFERENCES `contacts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sales`
--

LOCK TABLES `sales` WRITE;
/*!40000 ALTER TABLE `sales` DISABLE KEYS */;
/*!40000 ALTER TABLE `sales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `species`
--

DROP TABLE IF EXISTS `species`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `species` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(25) NOT NULL,
  `genus` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `genus` (`genus`),
  CONSTRAINT `species_ibfk_1` FOREIGN KEY (`genus`) REFERENCES `genera` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=99999940 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `species`
--

LOCK TABLES `species` WRITE;
/*!40000 ALTER TABLE `species` DISABLE KEYS */;
INSERT INTO `species` VALUES (122300,'arabica',1926),(123796,'ovata',2083),(132808,'pinnatum',2794),(132809,'aureum',2794),(143475,'carnosa',3630),(157552,'adansonii',4700),(157554,'deliciosa',4700),(165585,'hederaceum',2795),(184915,'reginae',6381),(191077,'planifolia',6850),(222369,'erubescens',2795),(222644,'burle-marxii',2795),(699609,'thalia',13633),(780168,'ornata',13632),(780214,'kegeljanii',13632),(780423,'elliptica',13632),(780486,'majestica',13632),(780646,'concinna',13632),(780719,'makoyana',13632),(780835,'orbifolia',13632),(1234157,'elastica',43615),(99999905,'lyrata',43615),(99999937,'natalensis',43615),(99999939,'tetrasperma',8147);
/*!40000 ALTER TABLE `species` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `suppliers` (
  `id` varchar(5) NOT NULL,
  `name` varchar(50) NOT NULL,
  `address` varchar(50) DEFAULT NULL,
  `city` varchar(20) DEFAULT NULL,
  `state` varchar(2) DEFAULT NULL,
  `zip` int(11) DEFAULT NULL,
  `contact` varchar(5) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `contact` (`contact`),
  CONSTRAINT `suppliers_ibfk_1` FOREIGN KEY (`contact`) REFERENCES `contacts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suppliers`
--

LOCK TABLES `suppliers` WRITE;
/*!40000 ALTER TABLE `suppliers` DISABLE KEYS */;
/*!40000 ALTER TABLE `suppliers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `varieties`
--

DROP TABLE IF EXISTS `varieties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `varieties` (
  `id` varchar(5) NOT NULL,
  `name` varchar(50) NOT NULL,
  `species` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `species` (`species`),
  CONSTRAINT `varieties_ibfk_1` FOREIGN KEY (`species`) REFERENCES `species` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `varieties`
--

LOCK TABLES `varieties` WRITE;
/*!40000 ALTER TABLE `varieties` DISABLE KEYS */;
INSERT INTO `varieties` VALUES ('4pWgM','\"Manjula\"',132809),('B2VWb','\"Golden\"',132809),('Ba8qS','\"Peacock\"',780719),('E6gXD','\"Triostar\"',699609),('EVGtK','\"Network\"',780214),('JZo99','\"Chelsea\"',143475),('RoGG4','\"Thai Constellation\"',157554),('SzVbb','\"Marble Queen\"',132809),('UxVn2','\"Triangularis\"',99999937),('V9XKH','\"Cebu Blue\"',132808),('Y473K','\"Jade\"',123796);
/*!40000 ALTER TABLE `varieties` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-04-28 20:36:33
