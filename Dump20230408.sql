CREATE DATABASE  IF NOT EXISTS `spms` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `spms`;
-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: spms
-- ------------------------------------------------------
-- Server version	8.0.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `area_of_expertise`
--

DROP TABLE IF EXISTS `area_of_expertise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `area_of_expertise` (
  `aoe_id` int NOT NULL,
  `aoe_name` varchar(30) DEFAULT NULL,
  `staff` int DEFAULT NULL,
  PRIMARY KEY (`aoe_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `area_of_expertise`
--

LOCK TABLES `area_of_expertise` WRITE;
/*!40000 ALTER TABLE `area_of_expertise` DISABLE KEYS */;
INSERT INTO `area_of_expertise` VALUES (101,'Astronaut',20),(102,'Aviation Scientist',20),(103,'Communication',20),(104,'Meteorology',20),(105,'Navigation',40);
/*!40000 ALTER TABLE `area_of_expertise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `emp_tasks`
--

DROP TABLE IF EXISTS `emp_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `emp_tasks` (
  `mission_id` int NOT NULL,
  `emp_id` int NOT NULL,
  `task_id` int NOT NULL,
  PRIMARY KEY (`mission_id`,`emp_id`,`task_id`),
  KEY `fk_emp_id_et_emp` (`emp_id`),
  KEY `fk_task_id_et_tas` (`task_id`),
  CONSTRAINT `fk_emp_id_et_emp` FOREIGN KEY (`emp_id`) REFERENCES `employee` (`emp_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_mission_id_et_mis` FOREIGN KEY (`mission_id`) REFERENCES `mission` (`mission_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_task_id_et_tas` FOREIGN KEY (`task_id`) REFERENCES `task` (`task_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `emp_tasks`
--

LOCK TABLES `emp_tasks` WRITE;
/*!40000 ALTER TABLE `emp_tasks` DISABLE KEYS */;
INSERT INTO `emp_tasks` VALUES (3001,1002,202),(3001,1002,203),(3001,1002,204),(3001,1003,202),(3001,1003,205),(3001,1003,206),(3001,1004,203),(3001,1004,204),(3001,1004,205),(3002,1102,202),(3002,1102,203),(3002,1102,204),(3002,1103,202),(3002,1103,205),(3002,1103,206),(3002,1104,203),(3002,1104,204),(3002,1104,205),(3003,1202,202),(3003,1202,203),(3003,1202,204),(3003,1203,202),(3003,1203,205),(3003,1203,206),(3003,1204,203),(3003,1204,204),(3003,1204,205),(3004,1302,202),(3004,1302,203),(3004,1302,204),(3004,1302,208),(3004,1302,211),(3004,1303,202),(3004,1303,205),(3004,1303,206),(3004,1303,212),(3004,1304,203),(3004,1304,204),(3004,1304,206),(3005,1402,202),(3005,1402,203),(3005,1402,204),(3005,1403,202),(3005,1403,205),(3005,1403,206),(3005,1404,203),(3005,1404,204),(3005,1404,205);
/*!40000 ALTER TABLE `emp_tasks` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_delete_emp_tasks` AFTER DELETE ON `emp_tasks` FOR EACH ROW begin
        if (select count(mission_id) from emp_tasks where emp_id=old.emp_id)=0
        then
            delete from ongoing_missions where ongoing_missions.emp_id=old.emp_id and ongoing_missions.mission_id=old.mission_id;
        end if;
    end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `emp_id` int NOT NULL,
  `emp_name` varchar(30) DEFAULT NULL,
  `phno` varchar(10) DEFAULT NULL,
  `gender` char(1) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `aoe_id` int DEFAULT NULL,
  `designation` varchar(1) DEFAULT NULL,
  `status` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`emp_id`),
  KEY `fk_aoe_id_emp_det` (`aoe_id`),
  CONSTRAINT `fk_aoe_id_emp_det` FOREIGN KEY (`aoe_id`) REFERENCES `area_of_expertise` (`aoe_id`) ON DELETE CASCADE,
  CONSTRAINT `check_designation` CHECK ((`designation` in (_utf8mb4'C',_utf8mb4'M',_utf8mb4'E'))),
  CONSTRAINT `check_emp_status` CHECK ((`status` in (_utf8mb4'Y',_utf8mb4'N')))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1000,'SR','9874563210','M','1985-10-10',NULL,'C',NULL),(1001,'Rahul','9874563210','M','1990-01-01',101,'M','N'),(1002,'Raj Aryan','1231231234','M','2002-12-12',101,'E','N'),(1003,'Suraj','9874563210','M','1994-10-10',101,'E','N'),(1004,'Rohan','9874563210','M','1995-10-08',101,'E','N'),(1005,'Riley','9874563210','F','1995-10-05',101,'E','Y'),(1101,'Sam','9874563210','M','1992-02-02',102,'M','N'),(1102,'Scott','9874563210','M','1990-01-01',102,'E','N'),(1103,'James','9874563210','M','1994-10-10',102,'E','N'),(1104,'Ravi','9874563210','M','1992-10-08',102,'E','N'),(1105,'Paula','9874563210','F','1992-10-05',102,'E','Y'),(1201,'John','9874563210','M','1994-04-10',103,'M','N'),(1202,'Ram','9874563210','M','1994-04-10',103,'E','N'),(1203,'Piyush','9874563210','M','1990-01-01',103,'E','N'),(1204,'Sid','9874563210','M','1995-10-08',103,'E','N'),(1205,'Reet','9874563210','F','1995-11-10',103,'E','Y'),(1234,'siddharth','6263539069','M','2002-12-12',103,'M','N'),(1298,'saldkfj','1231231234','M','2023-01-31',102,'M','Y'),(1301,'Anmol Sudhir','123712321','M','2009-09-09',104,'M','N'),(1302,'Abhishek','9874563210','M','1994-04-10',104,'E','N'),(1303,'Shubham','9874563210','M','1990-12-12',104,'E','N'),(1304,'Vikas','9874563210','M','1992-10-08',104,'E','N'),(1305,'Ahana','9874563210','F','1992-11-12',104,'E','Y'),(1401,'Aman','9874563210','M','1994-04-10',105,'M','N'),(1402,'Akul','9874563210','M','1992-02-02',105,'E','N'),(1403,'Pal','9874563210','M','1991-10-10',105,'E','N'),(1404,'Sally','9874563210','F','1994-10-10',105,'E','N'),(1405,'Nisha','9874563210','F','1994-10-01',105,'E','Y'),(2134,'Siddharth','6263539059','M','2002-12-12',103,'M','N'),(2143,'siddharth','6263539069','M','2001-10-10',103,'M','N'),(123456,'siddharth','6263539069','M','2001-10-10',103,'M','N');
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_insert_employee` AFTER INSERT ON `employee` FOR EACH ROW insert into login_details values(concat(if(new.designation='M','manager','employee'),NEW.emp_id),concat(if(new.designation='M','manager','employee'),NEW.emp_id),NEW.emp_id) */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `login_details`
--

DROP TABLE IF EXISTS `login_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login_details` (
  `uname` varchar(30) NOT NULL,
  `passwd` varchar(30) DEFAULT NULL,
  `emp_id` int DEFAULT NULL,
  PRIMARY KEY (`uname`),
  KEY `fk_emp_id_ld_emp` (`emp_id`),
  CONSTRAINT `fk_emp_id_ld_emp` FOREIGN KEY (`emp_id`) REFERENCES `employee` (`emp_id`) ON DELETE CASCADE,
  CONSTRAINT `check_upass_length` CHECK (((length(`uname`) > 7) and (length(`passwd`) > 7)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login_details`
--

LOCK TABLES `login_details` WRITE;
/*!40000 ALTER TABLE `login_details` DISABLE KEYS */;
INSERT INTO `login_details` VALUES ('admin123','admin123',1000),('anmol1301','askd1234',1301),('eabhi1302','eabhi1302',1302),('employee1000','employee1000',1000),('employee1002','employee1002',1002),('employee1003','employee1003',1003),('employee1004','employee1004',1004),('employee1005','employee1005',1005),('employee1102','employee1102',1102),('employee1103','employee1103',1103),('employee1104','employee1104',1104),('employee1105','employee1105',1105),('employee1202','employee1202',1202),('employee1203','employee1203',1203),('employee1204','employee1204',1204),('employee1205','employee1205',1205),('employee1302','employee1302',1302),('employee1303','employee1303',1303),('employee1304','employee1304',1304),('employee1305','employee1305',1305),('employee1402','employee1402',1402),('employee1403','employee1403',1403),('employee1404','employee1404',1404),('employee1405','employee1405',1405),('eraj1002','eraj1002',1002),('manager1001','manager1001',1001),('manager1101','manager1101',1101),('manager1201','manager1201',1201),('manager1234','manager1234',1234),('manager123456','manager123456',123456),('manager1298','manager1298',1298),('manager1301','askd1234',1301),('manager1401','manager1401',1401),('manager2134','manager2134',2134),('manager2143','manager2143',2143),('rahul1001','rahul1001',1001);
/*!40000 ALTER TABLE `login_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mission`
--

DROP TABLE IF EXISTS `mission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mission` (
  `mission_id` int NOT NULL,
  `mission_name` varchar(30) DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `dir_id` int DEFAULT NULL,
  PRIMARY KEY (`mission_id`),
  KEY `fk_dir_id_mis_emp` (`dir_id`),
  CONSTRAINT `fk_dir_id_mis_emp` FOREIGN KEY (`dir_id`) REFERENCES `employee` (`emp_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mission`
--

LOCK TABLES `mission` WRITE;
/*!40000 ALTER TABLE `mission` DISABLE KEYS */;
INSERT INTO `mission` VALUES (234,'chnad','2002-12-12','2003-12-12',123456),(1999,'Mission Jupyter','2002-11-11','2003-12-12',2143),(2231,'Mission Jupyter','2002-12-12','2003-12-12',2134),(3001,'MOM','2020-10-10','2024-08-15',1001),(3002,'aditya l-1','2021-10-10','2024-08-15',1101),(3003,'apollo-21','2020-10-10','2025-08-15',1201),(3004,'helio spec','2021-10-10','2023-08-15',1301),(3005,'moon obs','2020-10-10','2023-08-15',1401),(3124,'MangalYaan','2002-12-22','2003-12-23',1234);
/*!40000 ALTER TABLE `mission` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_mission_creation` AFTER INSERT ON `mission` FOR EACH ROW update  employee set status='N' where emp_id=new.dir_id */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `ongoing_missions`
--

DROP TABLE IF EXISTS `ongoing_missions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ongoing_missions` (
  `mission_id` int NOT NULL,
  `emp_id` int NOT NULL,
  PRIMARY KEY (`mission_id`,`emp_id`),
  KEY `fk_emp_id_cw_emp` (`emp_id`),
  CONSTRAINT `fk_emp_id_cw_emp` FOREIGN KEY (`emp_id`) REFERENCES `employee` (`emp_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_mission_id_cw_mis` FOREIGN KEY (`mission_id`) REFERENCES `mission` (`mission_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ongoing_missions`
--

LOCK TABLES `ongoing_missions` WRITE;
/*!40000 ALTER TABLE `ongoing_missions` DISABLE KEYS */;
INSERT INTO `ongoing_missions` VALUES (234,1001),(1999,1001),(2231,1001),(3001,1001),(3124,1001),(2231,1002),(3001,1003),(3001,1004),(234,1101),(1999,1101),(2231,1101),(3002,1101),(3124,1101),(3002,1102),(3002,1103),(3002,1104),(234,1201),(1999,1201),(2231,1201),(3003,1201),(3124,1201),(234,1202),(1999,1202),(2231,1202),(3003,1202),(3124,1202),(234,1203),(1999,1203),(2231,1203),(3003,1203),(3124,1203),(1999,1204),(2231,1204),(3003,1204),(234,1301),(1999,1301),(2231,1301),(3004,1301),(3124,1301),(3004,1302),(3004,1303),(3004,1304),(234,1401),(1999,1401),(2231,1401),(3005,1401),(3124,1401),(3005,1402),(3005,1403),(3005,1404);
/*!40000 ALTER TABLE `ongoing_missions` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `on_mission_assignment` AFTER INSERT ON `ongoing_missions` FOR EACH ROW update employee set status='N' where emp_id in (NEW.emp_id) */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_delete_on_ongoing_missions` AFTER DELETE ON `ongoing_missions` FOR EACH ROW begin
    update employee set status='Y' where emp_id in (OLD.emp_id);
    insert into past_missions values(old.mission_id,old.emp_id);
    if (select count(mission_id)from ongoing_missions)=0
        then
        update employee set status='Y' where emp_id=(select dir_id from mission where mission.mission_id=old.mission_id);
        insert into past_missions values(old.mission_id,(select dir_id from mission where mission.mission_id=OLD.mission_id));
    end if;
end */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `past_missions`
--

DROP TABLE IF EXISTS `past_missions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `past_missions` (
  `mission_id` int NOT NULL,
  `emp_id` int NOT NULL,
  PRIMARY KEY (`mission_id`,`emp_id`),
  KEY `fk_emp_id_his_emp` (`emp_id`),
  CONSTRAINT `fk_emp_id_his_emp` FOREIGN KEY (`emp_id`) REFERENCES `employee` (`emp_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_mission_id_his_mis` FOREIGN KEY (`mission_id`) REFERENCES `mission` (`mission_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `past_missions`
--

LOCK TABLES `past_missions` WRITE;
/*!40000 ALTER TABLE `past_missions` DISABLE KEYS */;
INSERT INTO `past_missions` VALUES (3001,1002);
/*!40000 ALTER TABLE `past_missions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task`
--

DROP TABLE IF EXISTS `task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task` (
  `task_id` int NOT NULL,
  `task_desc` varchar(30) DEFAULT NULL,
  `aoe_id` int DEFAULT NULL,
  PRIMARY KEY (`task_id`),
  KEY `fk_aoe_id_task_aoe` (`aoe_id`),
  CONSTRAINT `fk_aoe_id_task_aoe` FOREIGN KEY (`aoe_id`) REFERENCES `area_of_expertise` (`aoe_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task`
--

LOCK TABLES `task` WRITE;
/*!40000 ALTER TABLE `task` DISABLE KEYS */;
INSERT INTO `task` VALUES (201,'health monitoring',101),(202,'equipment checkup',101),(203,'informantion stock',101),(204,'Spacecraft design',102),(205,'Fuel',102),(206,'spacecraft maintainence',102),(207,'Radar system',103),(208,'infrared imaging',103),(209,'radio frequncy',103),(210,'weather updates',104),(211,'radio blackouts',104),(212,'geomagnetic storms',104),(213,'satellite positioning',105),(214,'mapping',105),(215,'geological updates',105);
/*!40000 ALTER TABLE `task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'spms'
--

--
-- Dumping routines for database 'spms'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-08 22:47:01
