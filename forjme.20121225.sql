-- MySQL dump 10.13  Distrib 5.5.28, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: forjme
-- ------------------------------------------------------
-- Server version	5.5.28-0ubuntu0.12.04.3

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_bda51c3c` (`group_id`),
  KEY `auth_group_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `group_id_refs_id_3cea63fe` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_a7792de1` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_e4470c6e` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_728de91f` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add log entry',7,'add_logentry'),(20,'Can change log entry',7,'change_logentry'),(21,'Can delete log entry',7,'delete_logentry'),(22,'Can add project',8,'add_project'),(23,'Can change project',8,'change_project'),(24,'Can delete project',8,'delete_project'),(25,'Can add use case',9,'add_usecase'),(26,'Can change use case',9,'change_usecase'),(27,'Can delete use case',9,'delete_usecase'),(28,'Can add task',10,'add_task'),(29,'Can change task',10,'change_task'),(30,'Can delete task',10,'delete_task'),(31,'Can add milestone',11,'add_milestone'),(32,'Can change milestone',11,'change_milestone'),(33,'Can delete milestone',11,'delete_milestone');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'gbtux','','','gu.bordes@gmail.com','pbkdf2_sha256$10000$8P4r6Qwn2SOS$YqaF4y6N6J+OrGTLAv8cKPuC6ZgivBNRz4mV40YK/l0=',1,1,1,'2012-12-23 17:58:41','2012-12-23 17:58:13');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_fbfc09f1` (`user_id`),
  KEY `auth_user_groups_bda51c3c` (`group_id`),
  CONSTRAINT `user_id_refs_id_831107f1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `group_id_refs_id_f0ee9890` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_fbfc09f1` (`user_id`),
  KEY `auth_user_user_permissions_1e014c8f` (`permission_id`),
  CONSTRAINT `user_id_refs_id_f2045483` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `permission_id_refs_id_67e79cb` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_milestone`
--

DROP TABLE IF EXISTS `dashboard_milestone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dashboard_milestone` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `version` varchar(25) NOT NULL,
  `project_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `dashboard_milestone_b6620684` (`project_id`),
  CONSTRAINT `project_id_refs_id_ea0469e6` FOREIGN KEY (`project_id`) REFERENCES `dashboard_project` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_milestone`
--

LOCK TABLES `dashboard_milestone` WRITE;
/*!40000 ALTER TABLE `dashboard_milestone` DISABLE KEYS */;
/*!40000 ALTER TABLE `dashboard_milestone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_milestone_use_cases`
--

DROP TABLE IF EXISTS `dashboard_milestone_use_cases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dashboard_milestone_use_cases` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `milestone_id` int(11) NOT NULL,
  `usecase_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `milestone_id` (`milestone_id`,`usecase_id`),
  KEY `dashboard_milestone_use_cases_9cfa291f` (`milestone_id`),
  KEY `dashboard_milestone_use_cases_17bb1722` (`usecase_id`),
  CONSTRAINT `milestone_id_refs_id_f9ef58b7` FOREIGN KEY (`milestone_id`) REFERENCES `dashboard_milestone` (`id`),
  CONSTRAINT `usecase_id_refs_id_75797388` FOREIGN KEY (`usecase_id`) REFERENCES `dashboard_usecase` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_milestone_use_cases`
--

LOCK TABLES `dashboard_milestone_use_cases` WRITE;
/*!40000 ALTER TABLE `dashboard_milestone_use_cases` DISABLE KEYS */;
/*!40000 ALTER TABLE `dashboard_milestone_use_cases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_project`
--

DROP TABLE IF EXISTS `dashboard_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dashboard_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `is_archived` tinyint(1) NOT NULL,
  `creation_date` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_project`
--

LOCK TABLES `dashboard_project` WRITE;
/*!40000 ALTER TABLE `dashboard_project` DISABLE KEYS */;
INSERT INTO `dashboard_project` VALUES (2,'Test','Ceci est un projet de test. Lorem Ipsum bla bla bla qSDQSDQSDQSDQSDQSDQSDQSDQSDQs\r\nqsdqsd\r\nqsdqsdqsdqsdqsfsdgsfgdgnbfgnhfh,ng,hfg',0,'2012-12-23'),(3,'test2','ceci ets un test',0,'2012-12-24'),(4,'test3','test3 de test de test',0,'2012-12-24'),(5,'test4','ceci est un test4',0,'2012-12-24'),(6,'test5','ceci est un projet de test qui dechire',0,'2012-12-24'),(7,'test6','ceci est un projet 6',0,'2012-12-24'),(8,'projet7','qsfqsfqsf',0,'2012-12-24'),(9,'projet8','qfqsfqsfqsf',0,'2012-12-24'),(10,'test9','qsfqsfq',0,'2012-12-24'),(11,'test10','ceci est le test 10',0,'2012-12-25'),(12,'test11','ceic ets le test 111',0,'2012-12-25'),(13,'project12','nouveau projet',0,'2012-12-25'),(14,'project123','nouveau projet de moi que j\'ai',0,'2012-12-25');
/*!40000 ALTER TABLE `dashboard_project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_project_admins`
--

DROP TABLE IF EXISTS `dashboard_project_admins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dashboard_project_admins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_id` (`project_id`,`user_id`),
  KEY `dashboard_project_admins_b6620684` (`project_id`),
  KEY `dashboard_project_admins_fbfc09f1` (`user_id`),
  CONSTRAINT `project_id_refs_id_59df85ad` FOREIGN KEY (`project_id`) REFERENCES `dashboard_project` (`id`),
  CONSTRAINT `user_id_refs_id_ccd71ad1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_project_admins`
--

LOCK TABLES `dashboard_project_admins` WRITE;
/*!40000 ALTER TABLE `dashboard_project_admins` DISABLE KEYS */;
INSERT INTO `dashboard_project_admins` VALUES (1,2,1);
/*!40000 ALTER TABLE `dashboard_project_admins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_project_contributors`
--

DROP TABLE IF EXISTS `dashboard_project_contributors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dashboard_project_contributors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_id` (`project_id`,`user_id`),
  KEY `dashboard_project_contributors_b6620684` (`project_id`),
  KEY `dashboard_project_contributors_fbfc09f1` (`user_id`),
  CONSTRAINT `project_id_refs_id_272be931` FOREIGN KEY (`project_id`) REFERENCES `dashboard_project` (`id`),
  CONSTRAINT `user_id_refs_id_c9d36e7b` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_project_contributors`
--

LOCK TABLES `dashboard_project_contributors` WRITE;
/*!40000 ALTER TABLE `dashboard_project_contributors` DISABLE KEYS */;
/*!40000 ALTER TABLE `dashboard_project_contributors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_project_readers`
--

DROP TABLE IF EXISTS `dashboard_project_readers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dashboard_project_readers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_id` (`project_id`,`user_id`),
  KEY `dashboard_project_readers_b6620684` (`project_id`),
  KEY `dashboard_project_readers_fbfc09f1` (`user_id`),
  CONSTRAINT `project_id_refs_id_37379c70` FOREIGN KEY (`project_id`) REFERENCES `dashboard_project` (`id`),
  CONSTRAINT `user_id_refs_id_7003c6ce` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_project_readers`
--

LOCK TABLES `dashboard_project_readers` WRITE;
/*!40000 ALTER TABLE `dashboard_project_readers` DISABLE KEYS */;
/*!40000 ALTER TABLE `dashboard_project_readers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_task`
--

DROP TABLE IF EXISTS `dashboard_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dashboard_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `creation_date` date NOT NULL,
  `description` longtext NOT NULL,
  `estimationInDays` int(11) NOT NULL,
  `date_start` datetime NOT NULL,
  `date_end` datetime NOT NULL,
  `assigned_to_id` int(11) NOT NULL,
  `use_case_id` int(11) NOT NULL,
  `thefile` varchar(100) DEFAULT NULL,
  `created_by_id` int(11) NOT NULL,
  `status` varchar(11) NOT NULL,
  `typeTask` varchar(12) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `dashboard_task_54f3bd39` (`assigned_to_id`),
  KEY `dashboard_task_accb9414` (`use_case_id`),
  KEY `dashboard_task_b5de30be` (`created_by_id`),
  CONSTRAINT `created_by_id_refs_id_237837e6` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `assigned_to_id_refs_id_237837e6` FOREIGN KEY (`assigned_to_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `use_case_id_refs_id_1abc5fd2` FOREIGN KEY (`use_case_id`) REFERENCES `dashboard_usecase` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_task`
--

LOCK TABLES `dashboard_task` WRITE;
/*!40000 ALTER TABLE `dashboard_task` DISABLE KEYS */;
/*!40000 ALTER TABLE `dashboard_task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dashboard_usecase`
--

DROP TABLE IF EXISTS `dashboard_usecase`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dashboard_usecase` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `creation_date` date NOT NULL,
  `description` longtext NOT NULL,
  `estimationInDays` int(11) NOT NULL,
  `difficulty` varchar(2) NOT NULL,
  `typeCase` varchar(7) NOT NULL,
  `status` varchar(11) NOT NULL,
  `created_by_id` int(11) NOT NULL,
  `thefile` varchar(100) DEFAULT NULL,
  `project_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `dashboard_usecase_b5de30be` (`created_by_id`),
  KEY `dashboard_usecase_b6620684` (`project_id`),
  CONSTRAINT `project_id_refs_id_4fca8da5` FOREIGN KEY (`project_id`) REFERENCES `dashboard_project` (`id`),
  CONSTRAINT `created_by_id_refs_id_9341c1f9` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dashboard_usecase`
--

LOCK TABLES `dashboard_usecase` WRITE;
/*!40000 ALTER TABLE `dashboard_usecase` DISABLE KEYS */;
/*!40000 ALTER TABLE `dashboard_usecase` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_fbfc09f1` (`user_id`),
  KEY `django_admin_log_e4470c6e` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_288599e6` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `user_id_refs_id_c8665aa` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2012-12-23 18:00:45',1,8,'2','Project 2 : Test',1,'');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'log entry','admin','logentry'),(8,'project','dashboard','project'),(9,'use case','dashboard','usecase'),(10,'task','dashboard','task'),(11,'milestone','dashboard','milestone');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_c25c2c28` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('27b16d25bf08cdf14e832bab6be05fe3','YTJkOTNlYjc0YTFkOWY2MDBiMDE5MDcxZDI2YWQ2MWI3ZjAyZjhmYTqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQSKAQF1Lg==\n','2013-01-06 17:58:41');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-12-25 20:02:26
