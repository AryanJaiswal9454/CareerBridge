-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: careerbridge
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add project',7,'add_project'),(26,'Can change project',7,'change_project'),(27,'Can delete project',7,'delete_project'),(28,'Can view project',7,'view_project'),(29,'Can add certification',8,'add_certification'),(30,'Can change certification',8,'change_certification'),(31,'Can delete certification',8,'delete_certification'),(32,'Can view certification',8,'view_certification'),(33,'Can add education',9,'add_education'),(34,'Can change education',9,'change_education'),(35,'Can delete education',9,'delete_education'),(36,'Can view education',9,'view_education'),(37,'Can add skill',10,'add_skill'),(38,'Can change skill',10,'change_skill'),(39,'Can delete skill',10,'delete_skill'),(40,'Can view skill',10,'view_skill'),(41,'Can add student profile',11,'add_studentprofile'),(42,'Can change student profile',11,'change_studentprofile'),(43,'Can delete student profile',11,'delete_studentprofile'),(44,'Can view student profile',11,'view_studentprofile'),(45,'Can add resume',12,'add_resume'),(46,'Can change resume',12,'change_resume'),(47,'Can delete resume',12,'delete_resume'),(48,'Can view resume',12,'view_resume'),(49,'Can add job description',13,'add_jobdescription'),(50,'Can change job description',13,'change_jobdescription'),(51,'Can delete job description',13,'delete_jobdescription'),(52,'Can view job description',13,'view_jobdescription'),(53,'Can add match result',14,'add_matchresult'),(54,'Can change match result',14,'change_matchresult'),(55,'Can delete match result',14,'delete_matchresult'),(56,'Can view match result',14,'view_matchresult'),(57,'Can add roadmap item',15,'add_roadmapitem'),(58,'Can change roadmap item',15,'change_roadmapitem'),(59,'Can delete roadmap item',15,'delete_roadmapitem'),(60,'Can view roadmap item',15,'view_roadmapitem'),(61,'Can add roadmap',16,'add_roadmap'),(62,'Can change roadmap',16,'change_roadmap'),(63,'Can delete roadmap',16,'delete_roadmap'),(64,'Can view roadmap',16,'view_roadmap'),(65,'Can add interview question',17,'add_interviewquestion'),(66,'Can change interview question',17,'change_interviewquestion'),(67,'Can delete interview question',17,'delete_interviewquestion'),(68,'Can view interview question',17,'view_interviewquestion'),(69,'Can add interview session',18,'add_interviewsession'),(70,'Can change interview session',18,'change_interviewsession'),(71,'Can delete interview session',18,'delete_interviewsession'),(72,'Can view interview session',18,'view_interviewsession'),(73,'Can add community resource',19,'add_communityresource'),(74,'Can change community resource',19,'change_communityresource'),(75,'Can delete community resource',19,'delete_communityresource'),(76,'Can view community resource',19,'view_communityresource');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$600000$Sg9IM7XT1bGXIj166SHk56$FqG2geohUnHTIQVC8/E8wISlWxpf6UYwEHQieFo9mLQ=','2026-09-12 12:54:48.347311',1,'aryan','','','aryanjaiswal90800@gmail.com',1,1,'2026-09-07 17:24:27.006690'),(2,'pbkdf2_sha256$600000$JC17lKFrjQuoZM3joe3m1E$/hbivmrd/8pAT3fOftatu48P3u7MW5tcv+SlUwlc2nU=',NULL,0,'teststudent','','','teststudent@example.com',0,1,'2026-09-07 17:56:02.114021'),(3,'pbkdf2_sha256$600000$iVTMPazYZfTL1EELVHh2Es$uuQb/f+Pq+ObpEWk6CZ/7VGDkJhGTveyasjkBvI/tOQ=',NULL,0,'Amit','','','amit@gmail.com',0,1,'2026-09-10 01:31:17.616667'),(4,'pbkdf2_sha256$600000$VEWnbRUhXBGoAOPwCF6z31$EijuBUlnzsPIk1eT2KI1Wd31hpRJr7l9d6YN8QgspOg=',NULL,0,'Arsh','','','arsh123@gmail.com',0,1,'2026-09-14 16:37:56.861745');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `careers_jobdescription`
--

DROP TABLE IF EXISTS `careers_jobdescription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `careers_jobdescription` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `company_name` varchar(200) NOT NULL,
  `job_title` varchar(200) NOT NULL,
  `source_type` varchar(20) NOT NULL,
  `file` varchar(100) DEFAULT NULL,
  `description` longtext NOT NULL,
  `extracted_text` longtext,
  `created_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  `ai_analysis` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `careers_jobdescription_user_id_62a2c9fc_fk_auth_user_id` (`user_id`),
  CONSTRAINT `careers_jobdescription_user_id_62a2c9fc_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `careers_jobdescription`
--

LOCK TABLES `careers_jobdescription` WRITE;
/*!40000 ALTER TABLE `careers_jobdescription` DISABLE KEYS */;
INSERT INTO `careers_jobdescription` VALUES (1,'TCS','Data Analyst','text','','We are looking for a Data Analyst with strong SQL, Python, Excel, Power BI and data visualization skills.','We are looking for a Data Analyst with strong SQL, Python, Excel, Power BI and data visualization skills.','2026-09-08 03:25:50.138482',1,'{\"required_skills\": [\"SQL\", \"Python\", \"Excel\", \"Power BI\", \"Data visualization\"], \"preferred_skills\": [], \"education_required\": \"\", \"experience_required\": \"\"}'),(2,'Hackit','Data Analyst','file','job_descriptions/HackIT-HR-JD-Data_Analyst-Delhi-20251128-01-00.pdf','Job Description  \nData Analyst  \n \n \nPUBLIC                                                                                                                                                              Page  1 of 2 \n JOB DESCRIPTION – DATA ANALYST  \n \nAbout HackIT  \nHackIT Technology and Advisory Services is an IT/Cyber Security company, operating since 2009. HackIT \nis an Indian Computer Emergency Response Team, CERT -IN (www.cert -in.org.in) empaneled provider \nfor IT Security Audit Services. HackIT provides a broad ran ge of security consulting and advisory \nservices to a diverse group of clients, including government organizations, corporations, Military \nestablishments, financial institutions and start -up, to name few. Our work spans multiple sectors and \nindustries, incl uding Telecommunications, Defense and Military, I TeS, Financial Services, Aviation, \nHospitality, Healthcare and Research. We work end -to-end—from diagnosis to delivery of lasting \nimpact — together generating tangible results that are improving the security posture of organizations \nworldwide.  \nWe are looking for passionate Information Security Professionals to help us keep growing. If you\'re \nexcited to be part of a winning team, HackIT Technology & Advisory Services is a perfect place to get \nahead.  \n \nJob Title                                                       •   Data Analyst  \nLocation                                                       •   Delhi  \n \nJob Overview    \nWe are seeking a detail -oriented and analytical Data Analyst to join our team. The ideal candidate will \nbe responsible for collecting, cleaning, analyzing, and interpreting large datasets to support business \ndecisions. The role requires strong technical sk ills in Python, SQL, Excel, and familiarity with data \nengineering concepts. Experience in reporting, insight generation, and social media data analysis is an \nadded advantage.  \n \nJob Responsibilities  \n• Collect, clean, and transform raw data from multiple sources for analysis.  \n• Use Python (Pandas) to manipulate, process, and analyze datasets efficiently.  \n• Extract data using SQL queries and work with MongoDB for NoSQL data operations.  \n• Perform data scraping and automation tasks using scripting tools and Python libraries.  \n• Generate meaningful business insights through exploratory data analysis (EDA).  \n• Conduct social media analytics to track trends, sentiment, and performance metrics.  \n• Collaborate with cross -functional teams to understand requirements and deliver data -driven \nsolutions.  \n• Ensure accuracy, integrity, and security of data throughout the pipeline.  \n \nJob Description  \nData Analyst  \n \n \nPUBLIC                                                                                                                                                              Page  2 of 2 \n Technical Skillsets (Mandatory)  \n• Strong proficiency in Python, especially Pandas, NumPy, Matplotlib/Seaborn.  \n• Hands -on experience with SQL (writing complex queries, joins, aggregations).  \n• Knowledge of MongoDB and working with NoSQL datasets.  \n• Advanced Excel skills (pivot tables, functions, data visualization).  \n• Experience with web scraping (Beautiful Soup, Selenium, or similar tools).  \n• Ability to perform deep data cleaning and preprocessing.  \n• Experience with report generation and narrative insight creation.  \n• Understanding of social media metrics and analytics tools.  \n• Strong problem -solving, communication, and documentation skills.  \n• Familiarity with data APIs, automation, or scripting workflows.  \n \nEducation & Certifications  \nBachelor’s degree in Computer Science, Data Science, Statistics, or related field.  \n \nExperience  \n1-3 Years of experience  \n \nSend your updated profiles to careers@hackit.co','Job Description  \nData Analyst  \n \n \nPUBLIC                                                                                                                                                              Page  1 of 2 \n JOB DESCRIPTION – DATA ANALYST  \n \nAbout HackIT  \nHackIT Technology and Advisory Services is an IT/Cyber Security company, operating since 2009. HackIT \nis an Indian Computer Emergency Response Team, CERT -IN (www.cert -in.org.in) empaneled provider \nfor IT Security Audit Services. HackIT provides a broad ran ge of security consulting and advisory \nservices to a diverse group of clients, including government organizations, corporations, Military \nestablishments, financial institutions and start -up, to name few. Our work spans multiple sectors and \nindustries, incl uding Telecommunications, Defense and Military, I TeS, Financial Services, Aviation, \nHospitality, Healthcare and Research. We work end -to-end—from diagnosis to delivery of lasting \nimpact — together generating tangible results that are improving the security posture of organizations \nworldwide.  \nWe are looking for passionate Information Security Professionals to help us keep growing. If you\'re \nexcited to be part of a winning team, HackIT Technology & Advisory Services is a perfect place to get \nahead.  \n \nJob Title                                                       •   Data Analyst  \nLocation                                                       •   Delhi  \n \nJob Overview    \nWe are seeking a detail -oriented and analytical Data Analyst to join our team. The ideal candidate will \nbe responsible for collecting, cleaning, analyzing, and interpreting large datasets to support business \ndecisions. The role requires strong technical sk ills in Python, SQL, Excel, and familiarity with data \nengineering concepts. Experience in reporting, insight generation, and social media data analysis is an \nadded advantage.  \n \nJob Responsibilities  \n• Collect, clean, and transform raw data from multiple sources for analysis.  \n• Use Python (Pandas) to manipulate, process, and analyze datasets efficiently.  \n• Extract data using SQL queries and work with MongoDB for NoSQL data operations.  \n• Perform data scraping and automation tasks using scripting tools and Python libraries.  \n• Generate meaningful business insights through exploratory data analysis (EDA).  \n• Conduct social media analytics to track trends, sentiment, and performance metrics.  \n• Collaborate with cross -functional teams to understand requirements and deliver data -driven \nsolutions.  \n• Ensure accuracy, integrity, and security of data throughout the pipeline.  \n \nJob Description  \nData Analyst  \n \n \nPUBLIC                                                                                                                                                              Page  2 of 2 \n Technical Skillsets (Mandatory)  \n• Strong proficiency in Python, especially Pandas, NumPy, Matplotlib/Seaborn.  \n• Hands -on experience with SQL (writing complex queries, joins, aggregations).  \n• Knowledge of MongoDB and working with NoSQL datasets.  \n• Advanced Excel skills (pivot tables, functions, data visualization).  \n• Experience with web scraping (Beautiful Soup, Selenium, or similar tools).  \n• Ability to perform deep data cleaning and preprocessing.  \n• Experience with report generation and narrative insight creation.  \n• Understanding of social media metrics and analytics tools.  \n• Strong problem -solving, communication, and documentation skills.  \n• Familiarity with data APIs, automation, or scripting workflows.  \n \nEducation & Certifications  \nBachelor’s degree in Computer Science, Data Science, Statistics, or related field.  \n \nExperience  \n1-3 Years of experience  \n \nSend your updated profiles to careers@hackit.co','2026-09-13 02:44:08.926809',3,'{\"required_skills\": [\"Python\", \"SQL\", \"Mongodb\", \"Excel\", \"Pandas\", \"Numpy\", \"Communication\"], \"preferred_skills\": [\"Data Analysis\"], \"education_required\": \"Bachelor’s degree in Computer Science, Data Science, Statistics, or related field.\", \"experience_required\": \"3 Years of experience\"}'),(3,'Ranjeeth political','Cosultnacy','text','','Pre-Sales Associate\r\nRajneethi Political Management Consultants\r\nLocation\r\nBangalore Urban\r\nInside Sales\r\nBusiness Development\r\nPre-Sales Associate / jobs\r\nEligibility\r\nFresher\r\nExperienced Professionals\r\nDetails\r\nRole Overview\r\n\r\nWe are looking for a dynamic and articulate Pre-Sales Associate to be the first point of contact for our prospective customers. You will be responsible for lead qualification, understanding customer needs, product/service demo, proposal coordination and supporting the sales closure process.\r\n\r\nKey Responsibilities\r\n\r\nLead Management: Handle inbound leads from website, referrals, and social media. Qualify leads through initial calls and understand requirements of customers.\r\nClient Need Analysis: Conduct discovery calls to understand expectations of the customer.\r\nPitch & Demo: Give initial presentation of our services to prospective customers virtually and in-person.\r\nProposal & Documentation: Coordinate with Research, Content and Design teams to prepare customized proposals, presentations, and MoUs.\r\nCRM & Follow-ups: Maintain lead pipeline in CRM/Google Sheets, do regular follow-ups, and ensure timely closure support for the Sales Head.\r\nMarket Research: Track potential customers and create database of prospects state-wise.\r\nCoordination: Work closely with Sales, Operations and Strategy teams for smooth handover after deal closure.\r\nRequired Skills & Qualifications\r\n\r\nExcellent communication skills in English, Hindi and Kannada (Marathi/Telugu/Tamil is an added advantage)\r\nStrong presentation and interpersonal skills\r\nProficiency in MS Office - PowerPoint, Excel, Google Suite\r\nShould be comfortable with targets and flexible with working hours.','Pre-Sales Associate\r\nRajneethi Political Management Consultants\r\nLocation\r\nBangalore Urban\r\nInside Sales\r\nBusiness Development\r\nPre-Sales Associate / jobs\r\nEligibility\r\nFresher\r\nExperienced Professionals\r\nDetails\r\nRole Overview\r\n\r\nWe are looking for a dynamic and articulate Pre-Sales Associate to be the first point of contact for our prospective customers. You will be responsible for lead qualification, understanding customer needs, product/service demo, proposal coordination and supporting the sales closure process.\r\n\r\nKey Responsibilities\r\n\r\nLead Management: Handle inbound leads from website, referrals, and social media. Qualify leads through initial calls and understand requirements of customers.\r\nClient Need Analysis: Conduct discovery calls to understand expectations of the customer.\r\nPitch & Demo: Give initial presentation of our services to prospective customers virtually and in-person.\r\nProposal & Documentation: Coordinate with Research, Content and Design teams to prepare customized proposals, presentations, and MoUs.\r\nCRM & Follow-ups: Maintain lead pipeline in CRM/Google Sheets, do regular follow-ups, and ensure timely closure support for the Sales Head.\r\nMarket Research: Track potential customers and create database of prospects state-wise.\r\nCoordination: Work closely with Sales, Operations and Strategy teams for smooth handover after deal closure.\r\nRequired Skills & Qualifications\r\n\r\nExcellent communication skills in English, Hindi and Kannada (Marathi/Telugu/Tamil is an added advantage)\r\nStrong presentation and interpersonal skills\r\nProficiency in MS Office - PowerPoint, Excel, Google Suite\r\nShould be comfortable with targets and flexible with working hours.','2026-09-14 16:47:34.926686',4,'{\"required_skills\": [], \"preferred_skills\": [\"Excel\", \"Communication\"], \"education_required\": \"\", \"experience_required\": \"\"}');
/*!40000 ALTER TABLE `careers_jobdescription` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(13,'careers','jobdescription'),(5,'contenttypes','contenttype'),(17,'interviews','interviewquestion'),(18,'interviews','interviewsession'),(14,'matching','matchresult'),(8,'profiles','certification'),(9,'profiles','education'),(7,'profiles','project'),(10,'profiles','skill'),(11,'profiles','studentprofile'),(19,'resources','communityresource'),(12,'resumes','resume'),(16,'roadmap','roadmap'),(15,'roadmap','roadmapitem'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-09-07 17:11:53.331387'),(2,'auth','0001_initial','2026-09-07 17:11:54.234217'),(3,'admin','0001_initial','2026-09-07 17:11:54.435678'),(4,'admin','0002_logentry_remove_auto_add','2026-09-07 17:11:54.445326'),(5,'admin','0003_logentry_add_action_flag_choices','2026-09-07 17:11:54.464917'),(6,'contenttypes','0002_remove_content_type_name','2026-09-07 17:11:54.638280'),(7,'auth','0002_alter_permission_name_max_length','2026-09-07 17:11:54.743666'),(8,'auth','0003_alter_user_email_max_length','2026-09-07 17:11:54.797695'),(9,'auth','0004_alter_user_username_opts','2026-09-07 17:11:54.811309'),(10,'auth','0005_alter_user_last_login_null','2026-09-07 17:11:54.929882'),(11,'auth','0006_require_contenttypes_0002','2026-09-07 17:11:54.936616'),(12,'auth','0007_alter_validators_add_error_messages','2026-09-07 17:11:54.955913'),(13,'auth','0008_alter_user_username_max_length','2026-09-07 17:11:55.105496'),(14,'auth','0009_alter_user_last_name_max_length','2026-09-07 17:11:55.298490'),(15,'auth','0010_alter_group_name_max_length','2026-09-07 17:11:55.338853'),(16,'auth','0011_update_proxy_permissions','2026-09-07 17:11:55.356474'),(17,'auth','0012_alter_user_first_name_max_length','2026-09-07 17:11:55.510796'),(18,'sessions','0001_initial','2026-09-07 17:11:55.576695'),(19,'profiles','0001_initial','2026-09-07 17:21:07.180653'),(20,'profiles','0002_alter_certification_id_alter_education_id_and_more','2026-09-07 17:43:59.241086'),(21,'careers','0001_initial','2026-09-08 03:19:48.122562'),(22,'resumes','0001_initial','2026-09-08 03:19:48.248703'),(23,'matching','0001_initial','2026-09-09 11:07:22.619143'),(24,'careers','0002_jobdescription_ai_analysis','2026-09-09 11:16:43.068612'),(25,'resumes','0002_resume_ai_analysis','2026-09-09 11:16:43.140242'),(26,'roadmap','0001_initial','2026-09-09 16:43:20.811334'),(27,'interviews','0001_initial','2026-09-09 16:53:34.623874'),(28,'interviews','0002_interviewquestion_correct_option_and_more','2026-09-13 07:43:07.204858'),(29,'roadmap','0002_roadmapitem_resources','2026-09-13 07:43:07.345468'),(30,'matching','0002_matchresult_optimization','2026-09-13 13:14:18.995427'),(31,'resources','0001_initial','2026-09-14 16:07:11.461178'),(32,'resumes','0003_resume_ats_report','2026-09-14 16:07:11.670847');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('83x2p3fcnffkp26utgenqturl3eeroid','.eJxVjDEOgzAMAP_iuYpICAlm7N43IMeOG9oKJAJT1b9XSAztene6N4y0b2Xca17HSWAAC5dfloifeT6EPGi-L4aXeVunZI7EnLaa2yL5dT3bv0GhWmAAdNwRS4eRux4lexeZmqyht9YxBvWEQTxZDRo1hSZqKx5bjS0Se4bPF_ErOFI:1x5NFo:Mrxb0Sx7Gvt9VaIMZn3rcbP3TRo5dtGRGTqDZ-g9zbs','2026-09-26 12:54:48.362015'),('cvrn5tf2j9i5ln10vahnklxwalzwvmxv','.eJxVjDEOgzAMAP_iuYpICAlm7N43IMeOG9oKJAJT1b9XSAztene6N4y0b2Xca17HSWAAC5dfloifeT6EPGi-L4aXeVunZI7EnLaa2yL5dT3bv0GhWmAAdNwRS4eRux4lexeZmqyht9YxBvWEQTxZDRo1hSZqKx5bjS0Se4bPF_ErOFI:1x3dOZ:hPhusckrfDoeuy0Sw86qOG0--jeUhhRK1jyRj5m0yJM','2026-09-21 17:44:39.832164');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interviews_interviewquestion`
--

DROP TABLE IF EXISTS `interviews_interviewquestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interviews_interviewquestion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `question` longtext NOT NULL,
  `category` varchar(30) NOT NULL,
  `related_skill` varchar(150) DEFAULT NULL,
  `expected_points` json NOT NULL,
  `answer` longtext,
  `score` decimal(5,2) DEFAULT NULL,
  `feedback` longtext,
  `improvement_tips` json NOT NULL,
  `answered_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `session_id` bigint NOT NULL,
  `correct_option` varchar(10) DEFAULT NULL,
  `explanation` longtext,
  `is_correct` tinyint(1) DEFAULT NULL,
  `language` varchar(30) DEFAULT NULL,
  `options` json NOT NULL DEFAULT (_utf8mb3'[]'),
  `question_type` varchar(20) NOT NULL,
  `sample_solution` longtext,
  `selected_option` varchar(10) DEFAULT NULL,
  `starter_code` longtext,
  PRIMARY KEY (`id`),
  KEY `interviews_interview_session_id_3e0fbe92_fk_interview` (`session_id`),
  CONSTRAINT `interviews_interview_session_id_3e0fbe92_fk_interview` FOREIGN KEY (`session_id`) REFERENCES `interviews_interviewsession` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interviews_interviewquestion`
--

LOCK TABLES `interviews_interviewquestion` WRITE;
/*!40000 ALTER TABLE `interviews_interviewquestion` DISABLE KEYS */;
INSERT INTO `interviews_interviewquestion` VALUES (1,'What is a Pivot Table and when would you use one?','technical','excel','[]','An INNER JOIN returns only records that have matching values in both tables. A LEFT JOIN returns all records from the left table and matching records from the right table. If there is no match, the right side contains NULL values. I would use LEFT JOIN when I need to retain all records from the primary table.',80.00,'Your answer has been recorded. For a stronger interview answer, include a clear explanation, an example and connect it to the job requirements.','[\"Give a structured answer.\", \"Include a practical example.\", \"Connect your answer to the target role.\"]','2026-09-09 16:55:47.040090','2026-09-09 16:54:52.953952',1,NULL,NULL,NULL,NULL,'[]','open',NULL,NULL,NULL),(2,'What is the difference between VLOOKUP and XLOOKUP?','technical','excel','[]',NULL,NULL,NULL,'[]',NULL,'2026-09-09 16:54:52.960166',1,NULL,NULL,NULL,NULL,'[]','open',NULL,NULL,NULL),(3,'How would you clean duplicate data in Excel?','technical','excel','[]',NULL,NULL,NULL,'[]',NULL,'2026-09-09 16:54:52.964891',1,NULL,NULL,NULL,NULL,'[]','open',NULL,NULL,NULL),(4,'What are conditional formatting rules used for?','technical','excel','[]',NULL,NULL,NULL,'[]',NULL,'2026-09-09 16:54:52.969498',1,NULL,NULL,NULL,NULL,'[]','open',NULL,NULL,NULL),(5,'How would you create a dashboard in Excel?','technical','excel','[]',NULL,NULL,NULL,'[]',NULL,'2026-09-09 16:54:52.974135',1,NULL,NULL,NULL,NULL,'[]','open',NULL,NULL,NULL),(6,'What is a Pivot Table and when would you use one?','technical','excel','[]','It is a excel table it is used when a large number of data needs to be filtered on any specific condition',60.00,'Your answer has been recorded. For a stronger interview answer, include a clear explanation, an example and connect it to the job requirements.','[\"Give a structured answer.\", \"Include a practical example.\", \"Connect your answer to the target role.\"]','2026-09-13 02:46:23.550683','2026-09-13 02:45:32.422224',2,NULL,NULL,NULL,NULL,'[]','open',NULL,NULL,NULL),(7,'What is the difference between VLOOKUP and XLOOKUP?','technical','excel','[]','v lookup search for the value to be found in the whole table \nxlookup only search the required area',60.00,'Your answer has been recorded. For a stronger interview answer, include a clear explanation, an example and connect it to the job requirements.','[\"Give a structured answer.\", \"Include a practical example.\", \"Connect your answer to the target role.\"]','2026-09-13 02:47:27.093852','2026-09-13 02:45:32.456557',2,NULL,NULL,NULL,NULL,'[]','open',NULL,NULL,NULL),(8,'How would you clean duplicate data in Excel?','technical','excel','[]','for cleaning duplicate data we can use function duplicate()to find duplicates and then can remove them',60.00,'Your answer has been recorded. For a stronger interview answer, include a clear explanation, an example and connect it to the job requirements.','[\"Give a structured answer.\", \"Include a practical example.\", \"Connect your answer to the target role.\"]','2026-09-13 02:48:14.365746','2026-09-13 02:45:32.462222',2,NULL,NULL,NULL,NULL,'[]','open',NULL,NULL,NULL),(9,'What are conditional formatting rules used for?','technical','excel','[]','conditional formating rule are that which can be implemented on any row or column they use specific condition according to which the colour of the cells of the row or column gets changed',70.00,'Your answer has been recorded. For a stronger interview answer, include a clear explanation, an example and connect it to the job requirements.','[\"Give a structured answer.\", \"Include a practical example.\", \"Connect your answer to the target role.\"]','2026-09-13 02:49:30.949984','2026-09-13 02:45:32.468027',2,NULL,NULL,NULL,NULL,'[]','open',NULL,NULL,NULL),(10,'How would you create a dashboard in Excel?','technical','excel','[]','for creating a dashboard in excel we needd to have the various required sheets to be included in the dashboard and after selecting the required sheets we can use them to create the dashboard',70.00,'Your answer has been recorded. For a stronger interview answer, include a clear explanation, an example and connect it to the job requirements.','[\"Give a structured answer.\", \"Include a practical example.\", \"Connect your answer to the target role.\"]','2026-09-13 02:50:55.632926','2026-09-13 02:45:32.472651',2,NULL,NULL,NULL,NULL,'[]','open',NULL,NULL,NULL),(11,'(Mongodb) Describe, step by step, how you would approach solving a problem in this skill area that you haven\'t seen before.','technical','mongodb','[]','# Describe your approach in comments, then write any code you can.\nyes for using any area which i am  new to i will try to take help of ai to complete it',65.00,'Answer recorded. Compare your approach with the sample solution below.','[\"Make sure your solution actually addresses every part of the question.\", \"Walk through an example input to check your logic.\"]','2026-09-13 07:45:39.136617','2026-09-13 07:44:42.832623',3,NULL,'Interviewers value structured problem-solving as much as the final answer.',0,'text','[]','coding','A strong answer breaks the problem into smaller steps, identifies inputs/outputs, considers edge cases, and tests incrementally.',NULL,'# Describe your approach in comments, then write any code you can.'),(12,'Describe (in formula form) how you would use XLOOKUP to find a customer\'s email in a table given their ID in cell A2, where the ID column is D:D and email column is F:F.','technical','excel','[]','=XLOOKUP(F:F)',30.00,'Answer recorded. Compare your approach with the sample solution below.','[\"Make sure your solution actually addresses every part of the question.\", \"Walk through an example input to check your logic.\"]','2026-09-13 07:46:18.292145','2026-09-13 07:44:42.840789',3,NULL,'XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found]) searches D:D for A2 and returns the matching value from F:F.',0,'excel','[]','coding','=XLOOKUP(A2, D:D, F:F, \"Not found\")',NULL,'=XLOOKUP(...)'),(13,'(Mongodb) Which of the following is generally considered a best practice when learning a new technical skill for a job?','technical','mongodb','[]','B',100.00,'Correct!','[]','2026-09-13 07:46:33.506015','2026-09-13 07:44:42.844924',3,'B','Hands-on practice with real feedback builds deeper, more durable understanding than passive reading alone.',1,NULL,'[\"Only reading theory, never practicing\", \"Building small practical projects and reviewing mistakes\", \"Avoiding documentation\", \"Memorizing answers without understanding them\"]','mcq',NULL,'B',NULL),(14,'Which Excel feature summarizes large datasets interactively without formulas?','technical','excel','[]','B',100.00,'Correct!','[]','2026-09-13 07:46:42.552447','2026-09-13 07:44:42.850322',3,'B','Pivot Tables let you summarize, group and rearrange data interactively.',1,NULL,'[\"Conditional formatting\", \"Pivot Table\", \"Data validation\", \"Freeze panes\"]','mcq',NULL,'B',NULL),(15,'Tell me about yourself.','behavioral',NULL,'[]','nothing',40.00,'Your answer has been recorded. For a stronger interview answer, include a clear explanation, an example and connect it to the job requirements.','[\"Give a structured answer.\", \"Include a practical example.\", \"Connect your answer to the target role.\"]','2026-09-13 07:46:50.799524','2026-09-13 07:44:42.853935',3,NULL,NULL,0,NULL,'[]','open',NULL,NULL,NULL),(16,'Why are you interested in this role?','behavioral',NULL,'[]','Yes beacuse u have relavnat knowledge',40.00,'Your answer has been recorded. For a stronger interview answer, include a clear explanation, an example and connect it to the job requirements.','[\"Give a structured answer.\", \"Include a practical example.\", \"Connect your answer to the target role.\"]','2026-09-13 07:47:09.255770','2026-09-13 07:44:42.856989',3,NULL,NULL,0,NULL,'[]','open',NULL,NULL,NULL),(17,'Tell me about yourself.','behavioral',NULL,'[]','strong independent individual willing to apply my knowledge on the live projects',60.00,'Your answer has been recorded. For a stronger interview answer, include a clear explanation, an example and connect it to the job requirements.','[\"Give a structured answer.\", \"Include a practical example.\", \"Connect your answer to the target role.\"]','2026-09-13 09:39:22.836095','2026-09-13 09:38:31.751677',4,NULL,NULL,0,NULL,'[]','open',NULL,NULL,NULL),(18,'Why are you interested in this role?','behavioral',NULL,'[]','yes this role suites me well because i am prior knowledge of this topic by building a project which required the knowledge to be implemented',70.00,'Your answer has been recorded. For a stronger interview answer, include a clear explanation, an example and connect it to the job requirements.','[\"Give a structured answer.\", \"Include a practical example.\", \"Connect your answer to the target role.\"]','2026-09-13 09:40:41.674082','2026-09-13 09:38:31.760630',4,NULL,NULL,1,NULL,'[]','open',NULL,NULL,NULL),(19,'Why should we hire you?','behavioral',NULL,'[]','because i am fit for this role as i have all the prerequisites required for this role and am confident for achiving what me team wants me to do the job',70.00,'Your answer has been recorded. For a stronger interview answer, include a clear explanation, an example and connect it to the job requirements.','[\"Give a structured answer.\", \"Include a practical example.\", \"Connect your answer to the target role.\"]','2026-09-13 09:42:19.679518','2026-09-13 09:38:31.766993',4,NULL,NULL,1,NULL,'[]','open',NULL,NULL,NULL),(20,'Tell me about a challenging project you worked on.','behavioral',NULL,'[]','yes i will tell about one of my project named upi fraud detection in that i was trying to predict wether my payement is valid or invalid for that i have imported 3 ml models but applying them on the relevant cases',70.00,'Your answer has been recorded. For a stronger interview answer, include a clear explanation, an example and connect it to the job requirements.','[\"Give a structured answer.\", \"Include a practical example.\", \"Connect your answer to the target role.\"]','2026-09-13 09:44:55.089771','2026-09-13 09:38:31.771640',4,NULL,NULL,1,NULL,'[]','open',NULL,NULL,NULL),(21,'Tell me about a time you had to learn something quickly.','behavioral',NULL,'[]','for creating the project i have to use streamlit browser but i am unable to do so for that i learned and i got a cear esponse very earlier',70.00,'Your answer has been recorded. For a stronger interview answer, include a clear explanation, an example and connect it to the job requirements.','[\"Give a structured answer.\", \"Include a practical example.\", \"Connect your answer to the target role.\"]','2026-09-13 09:46:31.086591','2026-09-13 09:38:31.776250',4,NULL,NULL,1,NULL,'[]','open',NULL,NULL,NULL),(22,'What are your strengths and weaknesses?','behavioral',NULL,'[]','a strength i want to mention if i am a quick learner and have the abilty to work under pressure and deliver the requiremnts on time \na weekness i want to add is its  hard for me to backoff for a task untill its complete',70.00,'Your answer has been recorded. For a stronger interview answer, include a clear explanation, an example and connect it to the job requirements.','[\"Give a structured answer.\", \"Include a practical example.\", \"Connect your answer to the target role.\"]','2026-09-13 09:48:49.000616','2026-09-13 09:38:31.781043',4,NULL,NULL,1,NULL,'[]','open',NULL,NULL,NULL),(23,'(Mongodb) Which of the following is generally considered a best practice when learning a new technical skill for a job?','technical','mongodb','[]','B',100.00,'Correct!','[]','2026-09-24 02:28:56.576100','2026-09-24 02:28:38.156326',5,'B','Hands-on practice with real feedback builds deeper, more durable understanding than passive reading alone.',1,NULL,'[\"Only reading theory, never practicing\", \"Building small practical projects and reviewing mistakes\", \"Avoiding documentation\", \"Memorizing answers without understanding them\"]','mcq',NULL,'B',NULL),(24,'Which Excel feature summarizes large datasets interactively without formulas?','technical','excel','[]','B',100.00,'Correct!','[]','2026-09-24 02:29:05.820989','2026-09-24 02:28:38.165209',5,'B','Pivot Tables let you summarize, group and rearrange data interactively.',1,NULL,'[\"Conditional formatting\", \"Pivot Table\", \"Data validation\", \"Freeze panes\"]','mcq',NULL,'B',NULL),(25,'(Pandas) Which of the following is generally considered a best practice when learning a new technical skill for a job?','technical','pandas','[]','B',100.00,'Correct!','[]','2026-09-24 02:29:16.709949','2026-09-24 02:28:38.169779',5,'B','Hands-on practice with real feedback builds deeper, more durable understanding than passive reading alone.',1,NULL,'[\"Only reading theory, never practicing\", \"Building small practical projects and reviewing mistakes\", \"Avoiding documentation\", \"Memorizing answers without understanding them\"]','mcq',NULL,'B',NULL),(26,'(Numpy) Which of the following is generally considered a best practice when learning a new technical skill for a job?','technical','numpy','[]','B',100.00,'Correct!','[]','2026-09-24 02:29:22.279474','2026-09-24 02:28:38.175465',5,'B','Hands-on practice with real feedback builds deeper, more durable understanding than passive reading alone.',1,NULL,'[\"Only reading theory, never practicing\", \"Building small practical projects and reviewing mistakes\", \"Avoiding documentation\", \"Memorizing answers without understanding them\"]','mcq',NULL,'B',NULL),(27,'(Communication) Which of the following is generally considered a best practice when learning a new technical skill for a job?','technical','communication','[]','B',100.00,'Correct!','[]','2026-09-24 02:29:28.224495','2026-09-24 02:28:38.180204',5,'B','Hands-on practice with real feedback builds deeper, more durable understanding than passive reading alone.',1,NULL,'[\"Only reading theory, never practicing\", \"Building small practical projects and reviewing mistakes\", \"Avoiding documentation\", \"Memorizing answers without understanding them\"]','mcq',NULL,'B',NULL);
/*!40000 ALTER TABLE `interviews_interviewquestion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `interviews_interviewsession`
--

DROP TABLE IF EXISTS `interviews_interviewsession`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `interviews_interviewsession` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `session_type` varchar(20) NOT NULL,
  `total_questions` int unsigned NOT NULL,
  `questions_answered` int unsigned NOT NULL,
  `overall_score` decimal(5,2) NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `job_description_id` bigint NOT NULL,
  `match_result_id` bigint NOT NULL,
  `resume_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `interviews_interview_job_description_id_295bac3b_fk_careers_j` (`job_description_id`),
  KEY `interviews_interview_match_result_id_b1dfd414_fk_matching_` (`match_result_id`),
  KEY `interviews_interview_resume_id_43378b98_fk_resumes_r` (`resume_id`),
  KEY `interviews_interviewsession_user_id_9a372824_fk_auth_user_id` (`user_id`),
  CONSTRAINT `interviews_interview_job_description_id_295bac3b_fk_careers_j` FOREIGN KEY (`job_description_id`) REFERENCES `careers_jobdescription` (`id`),
  CONSTRAINT `interviews_interview_match_result_id_b1dfd414_fk_matching_` FOREIGN KEY (`match_result_id`) REFERENCES `matching_matchresult` (`id`),
  CONSTRAINT `interviews_interview_resume_id_43378b98_fk_resumes_r` FOREIGN KEY (`resume_id`) REFERENCES `resumes_resume` (`id`),
  CONSTRAINT `interviews_interviewsession_user_id_9a372824_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `interviews_interviewsession_chk_1` CHECK ((`total_questions` >= 0)),
  CONSTRAINT `interviews_interviewsession_chk_2` CHECK ((`questions_answered` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `interviews_interviewsession`
--

LOCK TABLES `interviews_interviewsession` WRITE;
/*!40000 ALTER TABLE `interviews_interviewsession` DISABLE KEYS */;
INSERT INTO `interviews_interviewsession` VALUES (1,'mixed',5,1,80.00,'active','2026-09-09 16:54:52.927898','2026-09-09 16:55:47.062792',1,1,1,1),(2,'technical',5,5,64.00,'completed','2026-09-13 02:45:32.403990','2026-09-13 02:50:55.661398',2,2,2,3),(3,'mixed',6,6,62.50,'completed','2026-09-13 07:44:42.800775','2026-09-13 07:47:09.272787',2,2,2,3),(4,'behavioral',6,6,68.33,'completed','2026-09-13 09:38:31.694306','2026-09-13 09:48:49.018874',2,2,2,3),(5,'mcq',5,5,100.00,'completed','2026-09-24 02:28:38.101131','2026-09-24 02:29:28.256294',2,3,2,3);
/*!40000 ALTER TABLE `interviews_interviewsession` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `matching_matchresult`
--

DROP TABLE IF EXISTS `matching_matchresult`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `matching_matchresult` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `match_score` decimal(5,2) NOT NULL,
  `matched_skills` json NOT NULL,
  `skills_to_improve` json NOT NULL,
  `missing_skills` json NOT NULL,
  `preferred_skills_missing` json NOT NULL,
  `experience_match` tinyint(1) NOT NULL,
  `education_match` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `job_description_id` bigint NOT NULL,
  `resume_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  `optimization` json NOT NULL DEFAULT (_utf8mb3'{}'),
  PRIMARY KEY (`id`),
  KEY `matching_matchresult_job_description_id_80a9b00f_fk_careers_j` (`job_description_id`),
  KEY `matching_matchresult_resume_id_293477c3_fk_resumes_resume_id` (`resume_id`),
  KEY `matching_matchresult_user_id_d3a814da_fk_auth_user_id` (`user_id`),
  CONSTRAINT `matching_matchresult_job_description_id_80a9b00f_fk_careers_j` FOREIGN KEY (`job_description_id`) REFERENCES `careers_jobdescription` (`id`),
  CONSTRAINT `matching_matchresult_resume_id_293477c3_fk_resumes_resume_id` FOREIGN KEY (`resume_id`) REFERENCES `resumes_resume` (`id`),
  CONSTRAINT `matching_matchresult_user_id_d3a814da_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matching_matchresult`
--

LOCK TABLES `matching_matchresult` WRITE;
/*!40000 ALTER TABLE `matching_matchresult` DISABLE KEYS */;
INSERT INTO `matching_matchresult` VALUES (1,58.00,'[\"python\", \"sql\"]','[]','[\"data visualization\", \"excel\", \"power bi\"]','[]',1,1,'2026-09-09 16:37:07.883248','2026-09-09 16:37:07.883301',1,1,1,'{}'),(2,30.00,'[\"python\", \"sql\"]','[]','[\"mongodb\", \"excel\", \"pandas\", \"numpy\", \"communication\"]','[\"data analysis\"]',0,1,'2026-09-13 02:44:41.212024','2026-09-13 02:44:41.212077',2,2,3,'{}'),(3,30.00,'[\"python\", \"sql\"]','[]','[\"mongodb\", \"excel\", \"pandas\", \"numpy\", \"communication\"]','[\"data analysis\"]',0,1,'2026-09-13 13:14:29.486787','2026-09-13 13:14:29.486842',2,2,3,'{\"summary\": \"Your resume already reflects 2 of the role\'s key skills. Adding the missing keywords below — and quantifying your bullet points — is the fastest way to raise your ATS match score.\", \"strong_points\": [\"python\", \"sql\"], \"missing_keywords\": [\"Mongodb\", \"Pandas\", \"Numpy\", \"Data Analysis\", \"Communication\"], \"ats_keyword_score\": 38, \"bullet_suggestions\": [{\"reason\": \"Quantified bullets (with a number, %, or scale) are far more likely to pass ATS ranking and catch a recruiter\'s eye.\", \"improved_bullet\": \"I\'d rather ship a working prototype than spend a month discussing the idea — that mindset has shaped — add a measurable result (e.g. \'reducing X by Y%\' or \'for Z users/records\').\", \"original_bullet\": \"I\'d rather ship a working prototype than spend a month discussing the idea — that mindset has shaped\"}, {\"reason\": \"Quantified bullets (with a number, %, or scale) are far more likely to pass ATS ranking and catch a recruiter\'s eye.\", \"improved_bullet\": \"my MCA, four independent full stack and machine learning projects (including a deployed model for — add a measurable result (e.g. \'reducing X by Y%\' or \'for Z users/records\').\", \"original_bullet\": \"my MCA, four independent full stack and machine learning projects (including a deployed model for\"}, {\"reason\": \"Quantified bullets (with a number, %, or scale) are far more likely to pass ATS ranking and catch a recruiter\'s eye.\", \"improved_bullet\": \"UPI fraud detection), and an ongoing Python Full Stack De velopment program at QSpider. I put in the — add a measurable result (e.g. \'reducing X by Y%\' or \'for Z users/records\').\", \"original_bullet\": \"UPI fraud detection), and an ongoing Python Full Stack De velopment program at QSpider. I put in the\"}]}'),(4,95.00,'[]','[]','[]','[\"excel\"]',1,1,'2026-09-14 16:47:55.966459','2026-09-14 16:47:55.966620',3,3,4,'{\"summary\": \"Your resume already reflects 0 of the role\'s key skills. Adding the missing keywords below — and quantifying your bullet points — is the fastest way to raise your ATS match score.\", \"strong_points\": [], \"missing_keywords\": [\"Excel\"], \"ats_keyword_score\": 50, \"bullet_suggestions\": [{\"reason\": \"Quantified bullets (with a number, %, or scale) are far more likely to pass ATS ranking and catch a recruiter\'s eye.\", \"improved_bullet\": \"Aspiring Software Developer and Computer Science graduate specializing in Artificial Intelligence and Machine Learning, with — add a measurable result (e.g. \'reducing X by Y%\' or \'for Z users/records\').\", \"original_bullet\": \"Aspiring Software Developer and Computer Science graduate specializing in Artificial Intelligence and Machine Learning, with\"}, {\"reason\": \"Quantified bullets (with a number, %, or scale) are far more likely to pass ATS ranking and catch a recruiter\'s eye.\", \"improved_bullet\": \"expertise in full -stack web development and scalable application design. Skilled in problem -solving and modern development — add a measurable result (e.g. \'reducing X by Y%\' or \'for Z users/records\').\", \"original_bullet\": \"expertise in full -stack web development and scalable application design. Skilled in problem -solving and modern development\"}, {\"reason\": \"Quantified bullets (with a number, %, or scale) are far more likely to pass ATS ranking and catch a recruiter\'s eye.\", \"improved_bullet\": \"technolo gies, eager to contribute technical expertise and build innovative software solutions — add a measurable result (e.g. \'reducing X by Y%\' or \'for Z users/records\').\", \"original_bullet\": \"technolo gies, eager to contribute technical expertise and build innovative software solutions.\"}]}');
/*!40000 ALTER TABLE `matching_matchresult` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profiles_certification`
--

DROP TABLE IF EXISTS `profiles_certification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profiles_certification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `issuing_organization` varchar(200) DEFAULT NULL,
  `issue_date` date DEFAULT NULL,
  `credential_url` varchar(200) DEFAULT NULL,
  `profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `profiles_certification_profile_id_f88de370_fk` (`profile_id`),
  CONSTRAINT `profiles_certification_profile_id_f88de370_fk` FOREIGN KEY (`profile_id`) REFERENCES `profiles_studentprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profiles_certification`
--

LOCK TABLES `profiles_certification` WRITE;
/*!40000 ALTER TABLE `profiles_certification` DISABLE KEYS */;
/*!40000 ALTER TABLE `profiles_certification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profiles_education`
--

DROP TABLE IF EXISTS `profiles_education`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profiles_education` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `institution` varchar(200) NOT NULL,
  `degree` varchar(150) NOT NULL,
  `field_of_study` varchar(150) DEFAULT NULL,
  `start_year` int DEFAULT NULL,
  `end_year` int DEFAULT NULL,
  `grade` varchar(50) DEFAULT NULL,
  `profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `profiles_education_profile_id_fc3828ab_fk` (`profile_id`),
  CONSTRAINT `profiles_education_profile_id_fc3828ab_fk` FOREIGN KEY (`profile_id`) REFERENCES `profiles_studentprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profiles_education`
--

LOCK TABLES `profiles_education` WRITE;
/*!40000 ALTER TABLE `profiles_education` DISABLE KEYS */;
/*!40000 ALTER TABLE `profiles_education` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profiles_project`
--

DROP TABLE IF EXISTS `profiles_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profiles_project` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `technologies` longtext,
  `project_url` varchar(200) DEFAULT NULL,
  `github_url` varchar(200) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `profiles_project_profile_id_53728e59_fk` (`profile_id`),
  CONSTRAINT `profiles_project_profile_id_53728e59_fk` FOREIGN KEY (`profile_id`) REFERENCES `profiles_studentprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profiles_project`
--

LOCK TABLES `profiles_project` WRITE;
/*!40000 ALTER TABLE `profiles_project` DISABLE KEYS */;
/*!40000 ALTER TABLE `profiles_project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profiles_skill`
--

DROP TABLE IF EXISTS `profiles_skill`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profiles_skill` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `proficiency` varchar(20) NOT NULL,
  `years_of_experience` decimal(3,1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `profiles_skill_profile_id_069fc46b_fk` (`profile_id`),
  CONSTRAINT `profiles_skill_profile_id_069fc46b_fk` FOREIGN KEY (`profile_id`) REFERENCES `profiles_studentprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profiles_skill`
--

LOCK TABLES `profiles_skill` WRITE;
/*!40000 ALTER TABLE `profiles_skill` DISABLE KEYS */;
INSERT INTO `profiles_skill` VALUES (1,'Python','intermediate',1.0,'2026-09-08 03:14:28.316116',1),(2,'SQL','intermediate',1.0,'2026-09-08 03:14:46.936243',1),(3,'Excel','advanced',1.5,'2026-09-08 03:14:56.285534',1),(4,'Power BI','beginner',0.2,'2026-09-08 03:15:07.429856',1),(5,'python','intermediate',0.0,'2026-09-13 02:52:20.757161',2),(6,'sql','intermediate',0.0,'2026-09-13 02:52:40.496661',2),(7,'django','advanced',0.0,'2026-09-13 02:52:50.234294',2),(8,'html','beginner',20.0,'2026-09-15 15:21:21.198966',2);
/*!40000 ALTER TABLE `profiles_skill` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profiles_studentprofile`
--

DROP TABLE IF EXISTS `profiles_studentprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profiles_studentprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(150) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `college` varchar(200) DEFAULT NULL,
  `degree` varchar(100) DEFAULT NULL,
  `graduation_year` int DEFAULT NULL,
  `career_goal` varchar(150) DEFAULT NULL,
  `bio` longtext,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `profiles_studentprofile_user_id_ffee5cc8_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profiles_studentprofile`
--

LOCK TABLES `profiles_studentprofile` WRITE;
/*!40000 ALTER TABLE `profiles_studentprofile` DISABLE KEYS */;
INSERT INTO `profiles_studentprofile` VALUES (1,'Rahul Sharma','9876543210',NULL,'RSMT','BCA',2027,'Data Analyst','BCA student interested in data analytics and software development.','2026-09-08 03:11:26.694602','2026-09-08 03:11:26.731346',1),(2,'Amit','12345675','2002-11-20','rgtry','mca',2026,'Data Analyst',NULL,'2026-09-11 08:28:46.354854','2026-09-13 02:52:52.769483',3),(3,'Arsh',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'2026-09-14 16:38:11.607743','2026-09-14 16:38:11.607806',4);
/*!40000 ALTER TABLE `profiles_studentprofile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resources_communityresource`
--

DROP TABLE IF EXISTS `resources_communityresource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resources_communityresource` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `skill` varchar(150) NOT NULL,
  `title` varchar(200) NOT NULL,
  `url` varchar(500) NOT NULL,
  `note` varchar(300) NOT NULL,
  `resource_type` varchar(20) NOT NULL,
  `upvotes` int unsigned NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `submitted_by_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `resources_communityr_submitted_by_id_53be7050_fk_auth_user` (`submitted_by_id`),
  KEY `resources_communityresource_skill_b32b775f` (`skill`),
  CONSTRAINT `resources_communityr_submitted_by_id_53be7050_fk_auth_user` FOREIGN KEY (`submitted_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `resources_communityresource_chk_1` CHECK ((`upvotes` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resources_communityresource`
--

LOCK TABLES `resources_communityresource` WRITE;
/*!40000 ALTER TABLE `resources_communityresource` DISABLE KEYS */;
/*!40000 ALTER TABLE `resources_communityresource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resumes_resume`
--

DROP TABLE IF EXISTS `resumes_resume`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resumes_resume` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL,
  `file` varchar(100) NOT NULL,
  `extracted_text` longtext,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  `ai_analysis` json DEFAULT NULL,
  `ats_report` json DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `resumes_resume_user_id_0221d0a3_fk_auth_user_id` (`user_id`),
  CONSTRAINT `resumes_resume_user_id_0221d0a3_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resumes_resume`
--

LOCK TABLES `resumes_resume` WRITE;
/*!40000 ALTER TABLE `resumes_resume` DISABLE KEYS */;
INSERT INTO `resumes_resume` VALUES (1,'Aryan Jaiswal','resumes/Aryan_resume.pdf','ARYAN JAISWAL  \n     Varanasi, India |     6389766905 |      aryanjaiswal6342@gmail.com  | \nwww.linkedin.com/in/aryan -jaiswal -4491a8319  | github.com/AryanJaiswal9454  \nCAREER OBJECTIVE  \nI\'d rather ship a working prototype than spend a month discussing the idea — that mindset has shaped \nmy MCA, four independent full stack and machine learning projects (including a deployed model for \nUPI fraud detection), and an ongoing Python Full Stack De velopment program at QSpider. I put in the \nhours where they matter, but I look for the smarter route first: reusing what works, automating the \nrepetitive, and reserving real effort for what actually moves the outcome. Seeking an entry -level \nSoftware Develo per role where that mindset — building things, not just studying them — adds real \nvalue from day one, in a team that rewards ownership as much as output.  \nSKILLS  \n• Programming & Web: Python, Django, HTML, CSS, JavaScript  \n• Machine Learning: Gradient Boosting, Random Forest, Scikit -learn, Model Evaluation  \n• Databases: MySQL, SQL  \n• Tools: Advanced Excel, Tableau, Google Workspace (Docs, Sheets, Slides, Drive)  \nPROJECTS  \nUPI Fraud Detection using ML  – Built and deployed an ML model (Gradient Boosting, Random \nForest) to flag potentially fraudulent UPI transactions. Live Demo  \nEduPulse  – Django web app to track student engagement and learning progress. (Django, HTML, \nCSS)  \nPersonal Finance Tracker  – Django web app to track income, expenses, and savings goals with visual \nspending insights. (Django, HTML, CSS)  \nEvent Management System  – Django web app for creating, managing, and registering for events \nonline, with unit testing. (Django, HTML, CSS)  \nEDUCATION  \nMaster of Computer Applications (MCA) – 2026  \n   Rajarshi School of Management & Technology (RSMT), Varanasi – 8.22 CGPA (≈78.09%)  \nBachelor of Computer Applications (BCA) – 2021 to 2024  \n   Rajarshi School of Management & Technology (RSMT), Varanasi – 70.66%  \nSenior Secondary (12th, PCM) – 2021 – 79%  \nSecondary (10th) – 2019 – 80%  \nCERTIFICATIONS & TRAINING  \nPython Full Stack Development – QSpider, Noida (Ongoing)  \nData Analytics Course – Centum  — Advanced Excel, MySQL, Python, Tableau','2026-09-08 16:42:24.817841','2026-09-08 16:42:24.817886',1,'{\"skills\": [\"Python\", \"Django\", \"HTML\", \"CSS\", \"JavaScript\", \"Gradient Boosting\", \"Random Forest\", \"Scikit-learn\", \"Model Evaluation\", \"MySQL\", \"SQL\", \"Advanced Excel\", \"Tableau\", \"Google Workspace (Docs, Sheets, Slides, Drive)\"], \"projects\": [\"UPI Fraud Detection using ML – Built and deployed an ML model (Gradient Boosting, Random Forest) to flag potentially fraudulent UPI transactions. Live Demo\", \"EduPulse – Django web app to track student engagement and learning progress. (Django, HTML, CSS)\", \"Personal Finance Tracker – Django web app to track income, expenses, and savings goals with visual spending insights. (Django, HTML, CSS)\", \"Event Management System – Django web app for creating, managing, and registering for events online, with unit testing. (Django, HTML, CSS)\"], \"education\": [\"Master of Computer Applications (MCA) – 2026, Rajarshi School of Management & Technology (RSMT), Varanasi – 8.22 CGPA (≈78.09%)\", \"Bachelor of Computer Applications (BCA) – 2021 to 2024, Rajarshi School of Management & Technology (RSMT), Varanasi – 70.66%\", \"Senior Secondary (12th, PCM) – 2021 – 79%\", \"Secondary (10th) – 2019 – 80%\"], \"experience\": [], \"certifications\": [\"Python Full Stack Development – QSpider, Noida (Ongoing)\", \"Data Analytics Course – Centum — Advanced Excel, MySQL, Python, Tableau\"]}',NULL),(2,'Aryan resume','resumes/Aryan_resume_hfmeTJU.pdf','ARYAN JAISWAL  \n     Varanasi, India |     6389766905 |      aryanjaiswal6342@gmail.com  | \nwww.linkedin.com/in/aryan -jaiswal -4491a8319  | github.com/AryanJaiswal9454  \nCAREER OBJECTIVE  \nI\'d rather ship a working prototype than spend a month discussing the idea — that mindset has shaped \nmy MCA, four independent full stack and machine learning projects (including a deployed model for \nUPI fraud detection), and an ongoing Python Full Stack De velopment program at QSpider. I put in the \nhours where they matter, but I look for the smarter route first: reusing what works, automating the \nrepetitive, and reserving real effort for what actually moves the outcome. Seeking an entry -level \nSoftware Develo per role where that mindset — building things, not just studying them — adds real \nvalue from day one, in a team that rewards ownership as much as output.  \nSKILLS  \n• Programming & Web: Python, Django, HTML, CSS, JavaScript  \n• Machine Learning: Gradient Boosting, Random Forest, Scikit -learn, Model Evaluation  \n• Databases: MySQL, SQL  \n• Tools: Advanced Excel, Tableau, Google Workspace (Docs, Sheets, Slides, Drive)  \nPROJECTS  \nUPI Fraud Detection using ML  – Built and deployed an ML model (Gradient Boosting, Random \nForest) to flag potentially fraudulent UPI transactions. Live Demo  \nEduPulse  – Django web app to track student engagement and learning progress. (Django, HTML, \nCSS)  \nPersonal Finance Tracker  – Django web app to track income, expenses, and savings goals with visual \nspending insights. (Django, HTML, CSS)  \nEvent Management System  – Django web app for creating, managing, and registering for events \nonline, with unit testing. (Django, HTML, CSS)  \nEDUCATION  \nMaster of Computer Applications (MCA) – 2026  \n   Rajarshi School of Management & Technology (RSMT), Varanasi – 8.22 CGPA (≈78.09%)  \nBachelor of Computer Applications (BCA) – 2021 to 2024  \n   Rajarshi School of Management & Technology (RSMT), Varanasi – 70.66%  \nSenior Secondary (12th, PCM) – 2021 – 79%  \nSecondary (10th) – 2019 – 80%  \nCERTIFICATIONS & TRAINING  \nPython Full Stack Development – QSpider, Noida (Ongoing)  \nData Analytics Course – Centum  — Advanced Excel, MySQL, Python, Tableau','2026-09-10 01:58:38.707308','2026-09-15 02:03:52.161207',3,'{\"skills\": [\"Python\", \"Django\", \"HTML\", \"CSS\", \"JavaScript\", \"Gradient Boosting\", \"Random Forest\", \"Scikit-learn\", \"Model Evaluation\", \"MySQL\", \"SQL\", \"Advanced Excel\", \"Tableau\", \"Google Workspace (Docs, Sheets, Slides, Drive)\", \"Machine Learning\", \"Unit Testing\"], \"projects\": [\"UPI Fraud Detection using ML: Built and deployed an ML model (Gradient Boosting, Random Forest) to flag potentially fraudulent UPI transactions.\", \"EduPulse: Django web app to track student engagement and learning progress (Django, HTML, CSS).\", \"Personal Finance Tracker: Django web app to track income, expenses, and savings goals with visual spending insights (Django, HTML, CSS).\", \"Event Management System: Django web app for creating, managing, and registering for events online, with unit testing (Django, HTML, CSS).\"], \"education\": [\"Master of Computer Applications (MCA) – 2026, Rajarshi School of Management & Technology (RSMT), Varanasi – 8.22 CGPA (≈78.09%)\", \"Bachelor of Computer Applications (BCA) – 2021 to 2024, Rajarshi School of Management & Technology (RSMT), Varanasi – 70.66%\", \"Senior Secondary (12th, PCM) – 2021 – 79%\", \"Secondary (10th) – 2019 – 80%\"], \"experience\": [], \"certifications\": [\"Python Full Stack Development – QSpider, Noida (Ongoing)\", \"Data Analytics Course – Centum (Advanced Excel, MySQL, Python, Tableau)\"]}','{\"issues\": [{\"fix\": \"Add a clearly labeled section for: experience.\", \"issue\": \"Missing standard section header(s): experience\", \"why_it_matters\": \"ATS software looks for standard section headers to categorize your experience correctly.\"}], \"ats_score\": 85, \"strengths\": [\"Uses bullet points for readability.\", \"Email address is present and detectable.\", \"Resume length is in a reasonable range.\"], \"improved_summary\": \"This is a rule-based check (structure, sections, bullets, contact info, length) rather than a full AI review. Address the issues above, then re-run this check to confirm your score improved.\"}'),(3,'Amit_Tiwari_Resume','resumes/Amit_Tiwari_Resume.pdf','AMIT KUMAR TIWARI  \n Noida, Uttar Pradesh   ☎ +91-6388458422   ✉ at389012@gmail.com     linkedin.com/amit -kumar -tiwari  \nCAREER OBJECTIVE  \nAspiring Software Developer and Computer Science graduate specializing in Artificial Intelligence and Machine Learning, with \nexpertise in full -stack web development and scalable application design. Skilled in problem -solving and modern development \ntechnolo gies, eager to contribute technical expertise and build innovative software solutions.  \nEDUCATION  \nB.Tech, Computer Science Engineering (AI & ML)   |  Kashi Institute of Technology, Varanasi  2022 – 2026  \nCGPA: 7.2  \nIntermediate (12th)   |  SBBSS Inter College  2022  \nPercentage: 66.6%  \nHigh School (10th)   |  SSDUMV Chakkaulapati  2020  \nPercentage: 74%  \nTECHNICAL SKILLS  \n• Programming Languages: Python, C, SQL  \n• Web Technologies: HTML5, CSS3, JavaScript, React.js (Basic)  \n• Framework: Django  \n• Database: Oracle SQL*Plus  \n• Tools: Git, VS Code, Browser Developer Tools  \n• Core Concepts: Object -Oriented Programming, DBMS, Computer Networks  \n• Soft Skills: Problem Solving, Communication, Analytical Thinking, Time Management  \nINTERNSHIP EXPERIENCE  \nPython Full -Stack Developer Trainee   |  QSpiders, Noida  Jan 2026 – Present  \n• Gaining hands -on experience across the full stack — frontend, backend, and database integration — through live project \ndevelopment.  \n• Learning SQL database design, query optimization, and industry -standard coding practices within the software development \nlifecycle (SDLC).  \nPython Programming Virtual Intern   |  InternCertify  Aug 2024  \n• Built foundational skills in Python programming, logic -building, and problem -solving through applied scripting exercises.  \nPROJECTS  \nSmart Study Planner — Student Productivity & Task Management App  Apr 2026  \n• Built a full -stack web app for managing study schedules, task tracking, and progress monitoring using Django, HTML, CSS, and \nJavaScript.  \n• Implemented dynamic task management, reminders, and progress -tracking features with a responsive, mobile -friendly UI.  \n• Tech stack: Django, SQLite, HTML5, CSS3, JavaScript  \nArticles Management System  Mar 2025  \n• Developed a web -based Articles Management System using Python and Django, allowing users to sign up, log in, write, and \nmanage their own articles.  \n• Implemented complete CRUD (Create, Read, Update, and Delete) operations for article management.  \n• Designed responsive web pages using HTML and CSS, and used Django ORM for efficient database operations with SQL.  \n• Built the application using Django Models, Views, URL Routing, Templates, and Forms.  \n• Tech stack: Python, Django, HTML, CSS, SQL  \nPersonal Portfolio Website  May 2024  \n• Designed and built a responsive portfolio site to showcase projects, technical skills, and achievements.  \n• Implemented interactive sections and smooth navigation to improve user experience across devices.  \n• Tech stack: HTML5, CSS3, JavaScript  \nCERTIFICATIONS  \n• Getting Started with Enterprise Data Science — IBM \n• AI Tools Expert — BE10x  \n• Generative AI for Software Development — IBM','2026-09-14 16:39:21.445225','2026-09-14 16:39:36.627352',4,'{\"skills\": [\"Python\", \"Javascript\", \"SQL\", \"HTML\", \"CSS\", \"React\", \"Django\", \"Git\", \"Machine Learning\", \"Communication\", \"Problem Solving\"], \"projects\": [\"expertise in full -stack web development and scalable application design. Skilled in problem -solving and modern development\", \"• Gaining hands -on experience across the full stack — frontend, backend, and database integration — through live project\", \"• Built foundational skills in Python programming, logic -building, and problem -solving through applied scripting exercises.\", \"PROJECTS\", \"• Built a full -stack web app for managing study schedules, task tracking, and progress monitoring using Django, HTML, CSS, and\", \"Articles Management System  Mar 2025\", \"• Developed a web -based Articles Management System using Python and Django, allowing users to sign up, log in, write, and\", \"• Built the application using Django Models, Views, URL Routing, Templates, and Forms.\", \"• Designed and built a responsive portfolio site to showcase projects, technical skills, and achievements.\"], \"education\": [\"EDUCATION\", \"B.Tech, Computer Science Engineering (AI & ML)   |  Kashi Institute of Technology, Varanasi  2022 – 2026\", \"Intermediate (12th)   |  SBBSS Inter College  2022\"], \"experience\": [\"Aspiring Software Developer and Computer Science graduate specializing in Artificial Intelligence and Machine Learning, with\", \"B.Tech, Computer Science Engineering (AI & ML)   |  Kashi Institute of Technology, Varanasi  2022 – 2026\", \"• Tools: Git, VS Code, Browser Developer Tools\", \"INTERNSHIP EXPERIENCE\", \"Python Full -Stack Developer Trainee   |  QSpiders, Noida  Jan 2026 – Present\", \"• Gaining hands -on experience across the full stack — frontend, backend, and database integration — through live project\", \"Python Programming Virtual Intern   |  InternCertify  Aug 2024\", \"• Implemented interactive sections and smooth navigation to improve user experience across devices.\"], \"certifications\": [\"CERTIFICATIONS\"]}','{\"issues\": [], \"ats_score\": 100, \"strengths\": [\"Has standard Experience / Education / Skills sections.\", \"Uses bullet points for readability.\", \"Email address is present and detectable.\", \"Resume length is in a reasonable range.\"], \"improved_summary\": \"This is a rule-based check (structure, sections, bullets, contact info, length) rather than a full AI review. Address the issues above, then re-run this check to confirm your score improved.\"}');
/*!40000 ALTER TABLE `resumes_resume` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roadmap_roadmap`
--

DROP TABLE IF EXISTS `roadmap_roadmap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roadmap_roadmap` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(250) NOT NULL,
  `summary` longtext NOT NULL,
  `total_days` int unsigned NOT NULL,
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `job_description_id` bigint NOT NULL,
  `match_result_id` bigint NOT NULL,
  `resume_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `match_result_id` (`match_result_id`),
  KEY `roadmap_roadmap_job_description_id_aeeca7c4_fk_careers_j` (`job_description_id`),
  KEY `roadmap_roadmap_resume_id_34e7af0e_fk_resumes_resume_id` (`resume_id`),
  KEY `roadmap_roadmap_user_id_95418b98_fk_auth_user_id` (`user_id`),
  CONSTRAINT `roadmap_roadmap_job_description_id_aeeca7c4_fk_careers_j` FOREIGN KEY (`job_description_id`) REFERENCES `careers_jobdescription` (`id`),
  CONSTRAINT `roadmap_roadmap_match_result_id_caa2a1eb_fk_matching_` FOREIGN KEY (`match_result_id`) REFERENCES `matching_matchresult` (`id`),
  CONSTRAINT `roadmap_roadmap_resume_id_34e7af0e_fk_resumes_resume_id` FOREIGN KEY (`resume_id`) REFERENCES `resumes_resume` (`id`),
  CONSTRAINT `roadmap_roadmap_user_id_95418b98_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `roadmap_roadmap_chk_1` CHECK ((`total_days` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roadmap_roadmap`
--

LOCK TABLES `roadmap_roadmap` WRITE;
/*!40000 ALTER TABLE `roadmap_roadmap` DISABLE KEYS */;
INSERT INTO `roadmap_roadmap` VALUES (1,'Data Analyst Career Readiness Roadmap','This roadmap is personalized using your resume, the selected job description, and your match result. It focuses on 3 skill areas that can improve your readiness for the Data Analyst role.',30,'active','2026-09-09 16:48:03.686404','2026-09-09 16:48:03.686453',1,1,1,1),(2,'Data Analyst Career Readiness Roadmap','This roadmap is personalized using your resume, the selected job description, and your match result. It focuses on 6 skill areas that can improve your readiness for the Data Analyst role.',55,'active','2026-09-13 02:45:21.432811','2026-09-13 02:45:21.432881',2,2,2,3),(3,'Data Analyst Career Readiness Roadmap','This roadmap is personalized using your resume, the selected job description, and your match result. It focuses on 6 skill areas that can improve your readiness for the Data Analyst role.',55,'active','2026-09-13 13:15:31.497944','2026-09-13 13:15:31.498023',2,3,2,3),(4,'Cosultnacy Career Readiness Roadmap','This roadmap is personalized using your resume, the selected job description, and your match result. It focuses on 1 skill areas that can improve your readiness for the Cosultnacy role.',7,'active','2026-09-14 16:48:28.523030','2026-09-14 16:48:28.523081',3,4,3,4);
/*!40000 ALTER TABLE `roadmap_roadmap` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roadmap_roadmapitem`
--

DROP TABLE IF EXISTS `roadmap_roadmapitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roadmap_roadmapitem` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `skill` varchar(150) NOT NULL,
  `category` varchar(20) NOT NULL,
  `priority` varchar(20) NOT NULL,
  `current_level` varchar(50) NOT NULL,
  `target_level` varchar(50) NOT NULL,
  `reason` longtext NOT NULL,
  `learning_topics` json NOT NULL,
  `practice_tasks` json NOT NULL,
  `project_task` longtext NOT NULL,
  `estimated_days` int unsigned NOT NULL,
  `status` varchar(20) NOT NULL,
  `order` int unsigned NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `roadmap_id` bigint NOT NULL,
  `resources` json NOT NULL DEFAULT (_utf8mb3'[]'),
  PRIMARY KEY (`id`),
  KEY `roadmap_roadmapitem_roadmap_id_39a4d81c_fk_roadmap_roadmap_id` (`roadmap_id`),
  CONSTRAINT `roadmap_roadmapitem_roadmap_id_39a4d81c_fk_roadmap_roadmap_id` FOREIGN KEY (`roadmap_id`) REFERENCES `roadmap_roadmap` (`id`),
  CONSTRAINT `roadmap_roadmapitem_chk_1` CHECK ((`estimated_days` >= 0)),
  CONSTRAINT `roadmap_roadmapitem_chk_2` CHECK ((`order` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roadmap_roadmapitem`
--

LOCK TABLES `roadmap_roadmapitem` WRITE;
/*!40000 ALTER TABLE `roadmap_roadmapitem` DISABLE KEYS */;
INSERT INTO `roadmap_roadmapitem` VALUES (1,'data visualization','missing','high','Missing','Intermediate','data visualization is required for the selected job but was not found in your current skill set.','[\"Understand the fundamentals\", \"Learn the core concepts\", \"Practice common problems\", \"Work with a real-world example\"]','[\"Complete 10 beginner practice problems\", \"Complete 5 intermediate practice problems\", \"Apply the skill to a small project\"]','Build a small project demonstrating this skill.',10,'completed',1,'2026-09-09 16:48:03.696950','2026-09-09 16:58:21.261329',1,'[]'),(2,'excel','missing','high','Missing','Intermediate','excel is required for the selected job but was not found in your current skill set.','[\"Excel formulas\", \"Lookup functions\", \"Pivot tables\", \"Data cleaning\", \"Conditional formatting\", \"Charts and dashboards\"]','[\"Create a sales analysis worksheet\", \"Practice XLOOKUP/VLOOKUP\", \"Create a pivot-table report\"]','Create an interactive Excel business dashboard.',10,'not_started',2,'2026-09-09 16:48:03.701643','2026-09-09 16:48:03.701688',1,'[]'),(3,'power bi','missing','high','Missing','Intermediate','power bi is required for the selected job but was not found in your current skill set.','[\"Power BI interface\", \"Data loading\", \"Power Query\", \"Data cleaning\", \"Data modeling\", \"DAX basics\", \"Dashboard design\"]','[\"Import and clean a dataset\", \"Create relationships between tables\", \"Create calculated measures\", \"Build an interactive dashboard\"]','Build a Power BI sales or business analytics dashboard.',10,'not_started',3,'2026-09-09 16:48:03.703578','2026-09-09 16:48:03.703632',1,'[]'),(4,'mongodb','missing','high','Missing','Intermediate','mongodb is required for the selected job but was not found in your current skill set.','[\"Understand the fundamentals\", \"Learn the core concepts\", \"Practice common problems\", \"Work with a real-world example\"]','[\"Complete 10 beginner practice problems\", \"Complete 5 intermediate practice problems\", \"Apply the skill to a small project\"]','Build a small project demonstrating this skill.',10,'completed',1,'2026-09-13 02:45:21.440113','2026-09-13 07:47:49.520740',2,'[]'),(5,'excel','missing','high','Missing','Intermediate','excel is required for the selected job but was not found in your current skill set.','[\"Excel formulas\", \"Lookup functions\", \"Pivot tables\", \"Data cleaning\", \"Conditional formatting\", \"Charts and dashboards\"]','[\"Create a sales analysis worksheet\", \"Practice XLOOKUP/VLOOKUP\", \"Create a pivot-table report\"]','Create an interactive Excel business dashboard.',10,'completed',2,'2026-09-13 02:45:21.530653','2026-09-13 07:47:53.709225',2,'[]'),(6,'pandas','missing','high','Missing','Intermediate','pandas is required for the selected job but was not found in your current skill set.','[\"Understand the fundamentals\", \"Learn the core concepts\", \"Practice common problems\", \"Work with a real-world example\"]','[\"Complete 10 beginner practice problems\", \"Complete 5 intermediate practice problems\", \"Apply the skill to a small project\"]','Build a small project demonstrating this skill.',10,'completed',3,'2026-09-13 02:45:21.532605','2026-09-13 07:47:58.806164',2,'[]'),(7,'numpy','missing','high','Missing','Intermediate','numpy is required for the selected job but was not found in your current skill set.','[\"Understand the fundamentals\", \"Learn the core concepts\", \"Practice common problems\", \"Work with a real-world example\"]','[\"Complete 10 beginner practice problems\", \"Complete 5 intermediate practice problems\", \"Apply the skill to a small project\"]','Build a small project demonstrating this skill.',10,'completed',4,'2026-09-13 02:45:21.535195','2026-09-13 07:48:01.465846',2,'[]'),(8,'communication','missing','high','Missing','Intermediate','communication is required for the selected job but was not found in your current skill set.','[\"Understand the fundamentals\", \"Learn the core concepts\", \"Practice common problems\", \"Work with a real-world example\"]','[\"Complete 10 beginner practice problems\", \"Complete 5 intermediate practice problems\", \"Apply the skill to a small project\"]','Build a small project demonstrating this skill.',10,'completed',5,'2026-09-13 02:45:21.537171','2026-09-13 07:48:04.158243',2,'[]'),(9,'data analysis','preferred','low','Missing','Beginner','data analysis is preferred for the selected job. Learning it can strengthen your profile.','[\"Understand the fundamentals\", \"Learn the core concepts\", \"Practice common problems\", \"Work with a real-world example\"]','[\"Complete 10 beginner practice problems\", \"Complete 5 intermediate practice problems\", \"Apply the skill to a small project\"]','Build a small project demonstrating this skill.',5,'completed',6,'2026-09-13 02:45:21.539916','2026-09-13 07:48:07.034372',2,'[]'),(10,'mongodb','missing','high','Missing','Intermediate','mongodb is required for the selected job but was not found in your current skill set.','[\"Understand the fundamentals\", \"Learn the core concepts\", \"Practice common problems\", \"Work with a real-world example\"]','[\"Complete 10 beginner practice problems\", \"Complete 5 intermediate practice problems\", \"Apply the skill to a small project\"]','Build a small project demonstrating this skill.',10,'completed',1,'2026-09-13 13:15:31.501757','2026-09-13 13:16:35.516268',3,'[{\"url\": \"https://www.youtube.com/results?search_query=mongodb+full+course+tutorial+for+beginners\", \"type\": \"video\", \"title\": \"Mongodb — Full Course / Playlist\", \"provider\": \"YouTube\", \"ai_recommended\": false}]'),(11,'excel','missing','high','Missing','Intermediate','excel is required for the selected job but was not found in your current skill set.','[\"Excel formulas\", \"Lookup functions\", \"Pivot tables\", \"Data cleaning\", \"Conditional formatting\", \"Charts and dashboards\"]','[\"Create a sales analysis worksheet\", \"Practice XLOOKUP/VLOOKUP\", \"Create a pivot-table report\"]','Create an interactive Excel business dashboard.',10,'completed',2,'2026-09-13 13:15:31.507377','2026-09-13 13:17:00.439250',3,'[{\"url\": \"https://www.youtube.com/results?search_query=Excel+full+course+pivot+tables+VLOOKUP\", \"type\": \"video\", \"title\": \"Excel — Full Course / Playlist\", \"provider\": \"YouTube\", \"ai_recommended\": false}]'),(12,'pandas','missing','high','Missing','Intermediate','pandas is required for the selected job but was not found in your current skill set.','[\"Understand the fundamentals\", \"Learn the core concepts\", \"Practice common problems\", \"Work with a real-world example\"]','[\"Complete 10 beginner practice problems\", \"Complete 5 intermediate practice problems\", \"Apply the skill to a small project\"]','Build a small project demonstrating this skill.',10,'completed',3,'2026-09-13 13:15:31.509182','2026-09-13 13:16:40.732798',3,'[{\"url\": \"https://www.youtube.com/results?search_query=pandas+full+course+tutorial+for+beginners\", \"type\": \"video\", \"title\": \"Pandas — Full Course / Playlist\", \"provider\": \"YouTube\", \"ai_recommended\": false}]'),(13,'numpy','missing','high','Missing','Intermediate','numpy is required for the selected job but was not found in your current skill set.','[\"Understand the fundamentals\", \"Learn the core concepts\", \"Practice common problems\", \"Work with a real-world example\"]','[\"Complete 10 beginner practice problems\", \"Complete 5 intermediate practice problems\", \"Apply the skill to a small project\"]','Build a small project demonstrating this skill.',10,'completed',4,'2026-09-13 13:15:31.511429','2026-09-13 13:16:42.884373',3,'[{\"url\": \"https://www.youtube.com/results?search_query=numpy+full+course+tutorial+for+beginners\", \"type\": \"video\", \"title\": \"Numpy — Full Course / Playlist\", \"provider\": \"YouTube\", \"ai_recommended\": false}]'),(14,'communication','missing','high','Missing','Intermediate','communication is required for the selected job but was not found in your current skill set.','[\"Understand the fundamentals\", \"Learn the core concepts\", \"Practice common problems\", \"Work with a real-world example\"]','[\"Complete 10 beginner practice problems\", \"Complete 5 intermediate practice problems\", \"Apply the skill to a small project\"]','Build a small project demonstrating this skill.',10,'completed',5,'2026-09-13 13:15:31.513399','2026-09-13 13:16:44.785524',3,'[{\"url\": \"https://www.youtube.com/results?search_query=communication+full+course+tutorial+for+beginners\", \"type\": \"video\", \"title\": \"Communication — Full Course / Playlist\", \"provider\": \"YouTube\", \"ai_recommended\": false}]'),(15,'data analysis','preferred','low','Missing','Beginner','data analysis is preferred for the selected job. Learning it can strengthen your profile.','[\"Understand the fundamentals\", \"Learn the core concepts\", \"Practice common problems\", \"Work with a real-world example\"]','[\"Complete 10 beginner practice problems\", \"Complete 5 intermediate practice problems\", \"Apply the skill to a small project\"]','Build a small project demonstrating this skill.',5,'completed',6,'2026-09-13 13:15:31.516505','2026-09-13 13:16:47.267076',3,'[{\"url\": \"https://www.youtube.com/results?search_query=data+analysis+full+course+tutorial+for+beginners\", \"type\": \"video\", \"title\": \"Data Analysis — Full Course / Playlist\", \"provider\": \"YouTube\", \"ai_recommended\": false}]'),(16,'excel','preferred','low','Missing','Beginner','excel is preferred for the selected job. Learning it can strengthen your profile.','[\"Excel formulas\", \"Lookup functions\", \"Pivot tables\", \"Data cleaning\", \"Conditional formatting\", \"Charts and dashboards\"]','[\"Create a sales analysis worksheet\", \"Practice XLOOKUP/VLOOKUP\", \"Create a pivot-table report\"]','Create an interactive Excel business dashboard.',5,'not_started',1,'2026-09-14 16:48:28.529471','2026-09-14 16:48:28.529523',4,'[{\"url\": \"https://www.youtube.com/results?search_query=Excel+full+course+pivot+tables+VLOOKUP\", \"type\": \"video\", \"title\": \"Excel — Full Course / Playlist\", \"provider\": \"YouTube\", \"ai_recommended\": false}, {\"url\": \"https://support.microsoft.com/en-us/excel\", \"type\": \"doc\", \"title\": \"Excel — Official Documentation\", \"provider\": \"Official Docs\", \"ai_recommended\": false}]');
/*!40000 ALTER TABLE `roadmap_roadmapitem` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-24 18:33:36
