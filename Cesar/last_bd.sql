-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: paidosett
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `associacao`
--

DROP TABLE IF EXISTS `associacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `associacao` (
  `ID_ASSOCIACAO` int NOT NULL AUTO_INCREMENT,
  `GRAU` varchar(25) NOT NULL,
  `PAIS_ATUACAO` varchar(30) NOT NULL,
  `CAMPO_INFO_ASSOCIACAO` text,
  `SEDE_ASSOCIACAO` varchar(40) DEFAULT NULL,
  `DATA_FECHAMENTO_ASSOCIACAO` date DEFAULT NULL,
  `DATA_ABERTURA_ASSOCIACAO` date DEFAULT NULL,
  `NOME_ASSOCIACAO` varchar(70) NOT NULL,
  `IMAGEM_PERFIL_URL` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID_ASSOCIACAO`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `associacao`
--

LOCK TABLES `associacao` WRITE;
/*!40000 ALTER TABLE `associacao` DISABLE KEYS */;
INSERT INTO `associacao` VALUES (1,'Continental','Brasil','Coordena 50 centros de prática em 12 paísesa','São Paulo',NULL,'1987-05-21','Associação Zen Latinoamericana','/uploads/associacao_1_perfil_204c950307dd4354b2cb4ab438224226.jpg'),(2,'Continental','Argentina','Foco na preservação das tradições do budismo primitivo','Mendoza',NULL,'2001-09-14','Rede Theravada Continental',NULL),(3,'Global','Nepal','Autoridade máxima na transmissão de linhagens tântricas','Katmandu',NULL,'1975-03-02','Aliança Global Vajrayana',NULL),(4,'Nacional','Brasil','Certifica instrutores e coordena eventos nacionais','Curitiba',NULL,'1995-11-30','Sociedade Budista Brasileira',NULL),(5,'Regional','Chile','Iniciativa de mindfulness em favelas - registros perdidos após 2020','Santiago','0001-01-01','2015-07-04','Projeto Dharma Urbano',NULL),(8,'Global','Nepal','Autoridade máxima na transmissão de linhagens tântricas','Katmandu',NULL,'1975-03-02','Aliança Global Vajrayana',NULL),(9,'Nacional','Brasil','Certifica instrutores e coordena eventos nacionais','Curitiba',NULL,'1995-11-30','Sociedade Budista Brasileira',NULL),(10,'Regional','Chile','Iniciativa de mindfulness em favelas - registros perdidos após 2020','Santiago','0001-01-01','2015-07-04','Projeto Dharma Urbano',NULL),(13,'Global','Nepal','Autoridade máxima na transmissão de linhagens tântricas','Katmandu',NULL,'1975-03-02','Aliança Global Vajrayana',NULL),(14,'Nacional','Brasil','Certifica instrutores e coordena eventos nacionais','Curitiba',NULL,'1995-11-30','Sociedade Budista Brasileira',NULL),(15,'Regional','Chile','Iniciativa de mindfulness em favelas - registros perdidos após 2020','Santiago','0001-01-01','2015-07-04','Projeto Dharma Urbano',NULL);
/*!40000 ALTER TABLE `associacao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `associacao_visita`
--

DROP TABLE IF EXISTS `associacao_visita`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `associacao_visita` (
  `ID_ASSOCIACAO_VISITA` int NOT NULL AUTO_INCREMENT,
  `ID_AV_ASSOCIACAO_FK` int NOT NULL,
  `ID_AV_VISITA_FK` int NOT NULL,
  PRIMARY KEY (`ID_ASSOCIACAO_VISITA`),
  KEY `ID_ASSOCIACAO_idx` (`ID_AV_ASSOCIACAO_FK`),
  KEY `ID_VISITA_idx` (`ID_AV_VISITA_FK`),
  CONSTRAINT `fk_associacao_visita_associacao` FOREIGN KEY (`ID_AV_ASSOCIACAO_FK`) REFERENCES `associacao` (`ID_ASSOCIACAO`),
  CONSTRAINT `fk_associacao_visita_visita` FOREIGN KEY (`ID_AV_VISITA_FK`) REFERENCES `visita` (`ID_VISITA`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `associacao_visita`
--

LOCK TABLES `associacao_visita` WRITE;
/*!40000 ALTER TABLE `associacao_visita` DISABLE KEYS */;
INSERT INTO `associacao_visita` VALUES (1,1,1),(2,1,3),(3,2,2),(4,3,4),(5,4,5),(6,5,6),(7,1,7),(8,2,8),(9,3,9),(10,4,10),(11,1,1),(12,1,3),(13,2,2),(14,3,4),(15,4,5),(16,5,6),(17,1,7),(18,2,8),(19,3,9),(20,4,10),(21,1,1),(22,1,3),(23,2,2),(24,3,4),(25,4,5),(26,5,6),(27,1,7),(28,2,8),(29,3,9),(30,4,10),(31,1,11),(32,2,12),(33,3,13),(34,4,14),(35,5,15),(36,1,16),(37,2,17),(38,3,18),(39,4,19),(40,5,20);
/*!40000 ALTER TABLE `associacao_visita` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imagem_associacao`
--

DROP TABLE IF EXISTS `imagem_associacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `imagem_associacao` (
  `ID_IMAGEM` int NOT NULL AUTO_INCREMENT,
  `URL_IMAGEM` varchar(255) NOT NULL,
  `LEGENDA` varchar(255) DEFAULT NULL,
  `ID_ASSOCIACAO_FK` int NOT NULL,
  PRIMARY KEY (`ID_IMAGEM`),
  KEY `fk_imagem_associacao_idx` (`ID_ASSOCIACAO_FK`),
  CONSTRAINT `fk_imagem_associacao` FOREIGN KEY (`ID_ASSOCIACAO_FK`) REFERENCES `associacao` (`ID_ASSOCIACAO`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imagem_associacao`
--

LOCK TABLES `imagem_associacao` WRITE;
/*!40000 ALTER TABLE `imagem_associacao` DISABLE KEYS */;
INSERT INTO `imagem_associacao` VALUES (1,'/uploads/associacao_1_carrossel_9187081c70684721945e43a9f6ec59ad.png','Ss',1);
/*!40000 ALTER TABLE `imagem_associacao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imagem_personalidade`
--

DROP TABLE IF EXISTS `imagem_personalidade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `imagem_personalidade` (
  `ID_IMAGEM` int NOT NULL AUTO_INCREMENT,
  `URL_IMAGEM` varchar(255) NOT NULL,
  `LEGENDA` varchar(255) DEFAULT NULL,
  `ID_PERSONALIDADE_FK` int NOT NULL,
  PRIMARY KEY (`ID_IMAGEM`),
  KEY `fk_imagem_personalidade_idx` (`ID_PERSONALIDADE_FK`),
  CONSTRAINT `fk_imagem_personalidade` FOREIGN KEY (`ID_PERSONALIDADE_FK`) REFERENCES `personalidade` (`ID_PERSONALIDADE`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imagem_personalidade`
--

LOCK TABLES `imagem_personalidade` WRITE;
/*!40000 ALTER TABLE `imagem_personalidade` DISABLE KEYS */;
INSERT INTO `imagem_personalidade` VALUES (1,'/uploads/personalidade_58_carrossel_f6bcff44fd0c4d179113011ef2a91d31.jpg','ÓCLOS',58),(2,'/uploads/personalidade_58_carrossel_4cf6c795a1b34209b33fee5728d84f65.jpg','Pesnas',58);
/*!40000 ALTER TABLE `imagem_personalidade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imagem_produto`
--

DROP TABLE IF EXISTS `imagem_produto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `imagem_produto` (
  `ID_IMAGEM` int NOT NULL AUTO_INCREMENT,
  `URL_IMAGEM` varchar(255) NOT NULL,
  `LEGENDA` varchar(255) DEFAULT NULL,
  `ID_PRODUTO_FK` int NOT NULL,
  PRIMARY KEY (`ID_IMAGEM`),
  KEY `fk_imagem_produto_idx` (`ID_PRODUTO_FK`),
  CONSTRAINT `fk_imagem_produto` FOREIGN KEY (`ID_PRODUTO_FK`) REFERENCES `produto` (`ID_PRODUTO`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imagem_produto`
--

LOCK TABLES `imagem_produto` WRITE;
/*!40000 ALTER TABLE `imagem_produto` DISABLE KEYS */;
INSERT INTO `imagem_produto` VALUES (1,'/uploads/produto_1_carrossel_bcd4b164c7c046c5a498c5c329f07898.jpg','',1);
/*!40000 ALTER TABLE `imagem_produto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `imagem_templo`
--

DROP TABLE IF EXISTS `imagem_templo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `imagem_templo` (
  `ID_IMAGEM` int NOT NULL AUTO_INCREMENT,
  `URL_IMAGEM` varchar(255) NOT NULL,
  `LEGENDA` varchar(255) DEFAULT NULL,
  `ID_TEMPLO_FK` int NOT NULL,
  PRIMARY KEY (`ID_IMAGEM`),
  KEY `fk_imagem_templo_idx` (`ID_TEMPLO_FK`),
  CONSTRAINT `fk_imagem_templo` FOREIGN KEY (`ID_TEMPLO_FK`) REFERENCES `templo` (`ID_TEMPLO`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `imagem_templo`
--

LOCK TABLES `imagem_templo` WRITE;
/*!40000 ALTER TABLE `imagem_templo` DISABLE KEYS */;
INSERT INTO `imagem_templo` VALUES (4,'/uploads/templo_7_carrossel_38155f9cfb20458d9c4d32b534347c2e.jpg','Braum',7),(5,'/uploads/templo_7_carrossel_d9b8b01f92fa480da7dd745c604891e9.png','Bruxo',7);
/*!40000 ALTER TABLE `imagem_templo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personalidade`
--

DROP TABLE IF EXISTS `personalidade`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personalidade` (
  `ID_PERSONALIDADE` int NOT NULL AUTO_INCREMENT,
  `DATA_NASCIMENTO` date DEFAULT NULL,
  `PAIS_ORIGEM_PERSONALIDADE` varchar(100) DEFAULT NULL,
  `CAMPO_INFO_PERSONALIDADE` text,
  `NIVEL` varchar(50) NOT NULL,
  `GENERO` varchar(20) DEFAULT NULL,
  `DATA_MORTE` date DEFAULT NULL,
  `RACA` varchar(20) NOT NULL,
  `NOME_PERSONALIDADE` varchar(40) NOT NULL,
  `IMAGEM_PERFIL_URL` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID_PERSONALIDADE`)
) ENGINE=InnoDB AUTO_INCREMENT=160 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personalidade`
--

LOCK TABLES `personalidade` WRITE;
/*!40000 ALTER TABLE `personalidade` DISABLE KEYS */;
INSERT INTO `personalidade` VALUES (58,'1975-03-22','Argentina','É o shacas','Instrutora','Feminino',NULL,'Branco','Monochaco','/uploads/personalidade_58_perfil_61e0556e18ad4cfb81e67559b2168b9d.png'),(59,'1926-10-11','Vietnã','Renomado monge zen, pacifista e pioneiro na introdução do budismo engajado no Ocidente.','Monge','Masculino','2022-01-22','Asiático','Thich Nhat Hanh',NULL),(60,'1988-07-15','México','Responsável pelo Templo Tzintzuntzan, especialista em cerimônias tradicionais.','Cuidador de Templo','Masculino',NULL,'Mestiço','Carlos Gutierrez',NULL),(61,NULL,'Índia','Estudiosa do budismo tântrico, desaparecida em 1999 durante pesquisa de campo no Tibete.','Pesquisadora','Feminino','0001-01-01','Asiático','Priya Sharma',NULL),(62,'1950-12-01','Japão','Discípulo direto de Shunryu Suzuki, lidera retiros anuais no Chile.','Mestre Zen','Masculino',NULL,'Asiático','Hiroshi Yamamoto',NULL),(63,'1990-11-05','Brasil','Coordenadora do projeto \"Budismo nas Periferias\" em São Paulo.','Ativista','Feminino',NULL,'Negro','Mariana Costa',NULL),(64,'1945-05-30','Tibet','Refugiado político que estabeleceu o primeiro templo Gelug na Colômbia.','Lama','Masculino','2019-02-14','Asiático','Lobsang Tenzin',NULL),(65,'1982-09-18','Chile','Pioneira na adaptação de técnicas de mindfulness para ambientes corporativos.','Instrutora','Feminino',NULL,'Branco','Fernanda Morales',NULL),(66,'1978-04-09','Índia','Leciona história do budismo na Universidade Nacional da Costa Rica.','Professor Universitário','Masculino',NULL,'Asiático','Rajiv Kapoor',NULL),(67,'1995-06-25','Peru','Organiza cerimônias inter-religiosas na região de Cusco.','Líder Comunitário','Não-binário',NULL,'Indígena','Amara Silva',NULL),(68,'1987-03-12','Brasil','Responsável pela tradução dos sutras para o português brasileiro contemporâneo.','Tradutor','Masculino',NULL,'Branco','Diego Almeida',NULL),(69,'1932-07-07','Japão','Integrou a cerimônia do chá com práticas meditativas no Peru.','Mestra de Cerimônia do Chá','Feminino','2020-11-19','Asiático','Sakura Takahashi',NULL),(70,'1991-08-30','Colômbia','Criadora de mandalas contemporâneas usando materiais reciclados.','Artista','Feminino',NULL,'Negro','Luciana Pérez',NULL),(71,'1980-02-29','Butão','Combina medicina tradicional tibetana com práticas de atenção plena.','Médica','Feminino',NULL,'Asiático','Tenzin Wangmo',NULL),(72,'1973-10-31','México','Especialista em sítios arqueológicos budistas na América Central.','Arqueólogo','Masculino',NULL,'Mestiço','Ricardo Juárez',NULL),(73,'1984-12-24','Japão','Organiza peregrinações aos principais templos da América do Sul.','Coordenadora de Caravanas','Feminino',NULL,'Asiático','Yumi Nakano',NULL),(74,'1965-06-15','Nigéria','Autor de \"O Budismo na Diáspora Africana\", residente na Bahia.','Escritor','Masculino',NULL,'Negro','Kwame Achebe',NULL),(75,NULL,'Peru','Integrou práticas andinas com meditação Vipassana.','Curandeiro','Masculino','0001-01-01','Indígena','Eduardo Vilca',NULL),(76,'1993-04-05','China','Desenvolveu app de meditação com mais de 1 milhão de usuários na AL.','Programadora','Feminino',NULL,'Asiático','Sofia Chang',NULL),(77,'1989-09-17','Argentina','Pioneiro na integração de terapias cognitivas com práticas Zen.','Psicólogo','Masculino',NULL,'Branco','Rafael Otero',NULL),(78,'1970-11-03','Índia','Responsável pelo intercâmbio Brasil-Índia em estudos budistas.','Embaixadora Cultural','Feminino',NULL,'Asiático','Amita Patel',NULL),(79,'2000-01-08','Brasil','Coordena o centro de visitantes do Templo Zu Lai em Cotia.','Atendente','Masculino',NULL,'Negro','Lucas Mendes',NULL),(80,'1955-05-05','Chile','Curadora do maior acervo de textos budistas da América do Sul.','Bibliotecária','Feminino',NULL,'Branco','Hilda Fernández',NULL),(81,'1948-08-22','Japão','Mestre em shodō (caligrafia Zen), realizou workshops em 15 países.','Calígrafo','Masculino','2023-03-15','Asiático','Kenji Sato',NULL),(82,'1986-07-19','Colômbia','Desenvolveu programa de mindfulness para escolas públicas.','Educadora','Feminino',NULL,'Mestiço','Camila Rojas',NULL),(83,'1979-12-01','Vietnã','Fundador do primeiro templo Theravada no Nordeste brasileiro.','Monge','Masculino',NULL,'Asiático','Nguyen Van Hung',NULL),(84,'1998-02-14','Portugal','Coordenadora de projetos sociais no Templo Kadampa em Lisboa.','Voluntária','Feminino',NULL,'Branco','Isabela Costa',NULL),(85,'1962-09-09','Japão','Projetou 23 templos budistas modernos na América Latina.','Arquiteto','Masculino',NULL,'Asiático','Takashi Ono',NULL),(86,'1983-10-10','Guatemala','Luta pela preservação de sítios sagrados maias-budistas.','Ativista','Feminino',NULL,'Indígena','Adriana Mejía',NULL),(87,'1971-06-30','Peru','Editor-chefe da revista \"Buddha Magazine\" em espanhol.','Jornalista','Masculino',NULL,'Mestiço','Javier Morales',NULL),(88,'1992-03-03','China','Canal sobre budismo moderno com 500k seguidores.','Youtuber','Não-binário',NULL,'Asiático','Li Wei',NULL),(89,'1968-04-18','Espanha','Integra cuidados paliativos com filosofia budista no México.','Enfermeira','Feminino',NULL,'Branco','Carmen Díaz',NULL),(90,'1985-11-11','Brasil','Compositor de mantras contemporâneos em português.','Músico','Masculino',NULL,'Negro','Samuel Oliveira',NULL),(91,'1939-05-05','Japão','Especialista em ikebana para espaços meditativos.','Florista','Feminino','2015-08-08','Asiático','Aiko Tanaka',NULL),(92,'1977-07-07','Bolívia','Pioneiro em agricultura consciente baseada em princípios budistas.','Agricultor','Masculino',NULL,'Indígena','Raúl Quispe',NULL),(93,'1994-09-23','Uruguai','Pesquisa o uso de psilocibina combinada com meditação.','Psiquiatra','Feminino',NULL,'Branco','Natalia Gómez',NULL),(94,'1980-02-28','China','Financia a construção de stupas em áreas carentes.','Empresário','Masculino',NULL,'Asiático','Chen Wei',NULL),(95,'1988-12-12','Cuba','Desenvolveu coreografias baseadas em movimentos meditativos.','Bailarina','Feminino',NULL,'Negro','Lucía Ramírez',NULL),(96,'1973-01-15','Índia','Defensor dos direitos dos templos budistas na América Latina.','Advogado','Masculino',NULL,'Asiático','Arjun Patel',NULL),(97,'1999-05-01','Costa Rica','Mais jovem professora de dharma certificada na América Central.','Estudante','Feminino',NULL,'Mestiço','Valeria Castro',NULL),(98,'1940-11-25','Japão','Integrou o zen às práticas de aikido no Brasil.','Mestre de Artes Marciais','Masculino','2010-09-09','Asiático','Haruto Suzuki',NULL),(99,'1965-08-17','Paraguai','Utiliza técnicas de respiração budista em partos humanizados.','Parteira','Feminino',NULL,'Indígena','Marisol Herrera',NULL),(100,'1982-04-04','Argentina','Autor do livro \"Cozinha Consciente: Gastronomia e Dharma\".','Chef','Masculino',NULL,'Branco','Oscar Martínez',NULL),(101,'1990-10-31','Bangladesh','Documentou comunidades budistas em 12 países latino-americanos.','Fotógrafa','Feminino',NULL,'Asiático','Ananya Das',NULL),(102,'1978-03-08','Brasil','Primeiro deputado federal a propor leis baseadas no princípio da compaixão.','Político','Masculino',NULL,'Negro','Felipe Costa',NULL),(103,'1987-06-21','Nepal','Lidera peregrinações ao Lago Titicaca com enfoque meditativo.','Guia de Trekking','Feminino',NULL,'Asiático','Suni Sharma',NULL),(104,'1955-12-25','El Salvador','Especialista na rota do budismo desde a Ásia até a AL.','Historiador','Masculino',NULL,'Mestiço','Roberto Salinas',NULL),(105,'1969-02-14','China','Desenvolveu modelo de microcrédito baseado em ética budista.','Economista','Feminino',NULL,'Asiático','Mei Lin',NULL),(106,'1995-07-04','Brasil','Divulga o budismo através de memes e linguagem jovem.','Influenciador Digital','Masculino',NULL,'Branco','Gabriel Santos',NULL),(107,'1984-09-09','Sri Lanka','Traduziu o cânone Pali para o espanhol diretamente do original.','Tradutora','Feminino',NULL,'Asiático','Priyanka Rao',NULL),(108,'1976-10-22','Equador','Fundador da \"Sangha Verde\" - ambientalismo budista.','Ecologista','Masculino',NULL,'Mestiço','Juan Pablo Ruiz',NULL),(109,'2002-11-02','Brasil','Criadora do podcast \"Dharma Gen-Z\" com 100k ouvintes/mês.','Estudante','Feminino',NULL,'Negro','Yara Lima',NULL),(110,'1947-12-31','México','Sincronizou rituais toltecas com meditação Zen.','Xamã','Masculino','2021-01-01','Indígena','Héctor Gómez',NULL),(111,'1981-04-13','Taiwan','Estuda os efeitos da meditação em cérebros bilíngues.','Neurocientista','Feminino',NULL,'Asiático','Lila Chen',NULL),(112,'1993-03-30','Chile','Cria estátuas de budas com material reciclado de computadores.','Escultor','Masculino',NULL,'Branco','Carlos Andrade',NULL),(113,'1979-07-07','Paquistão','Mediadora de conflitos usando técnicas de comunicação não-violenta.','Diplomata','Feminino',NULL,'Asiático','Nadia Khan',NULL),(114,'1960-05-05','Panamá','Especialista em projetar jardins zen para pequenos espaços.','Jardineiro','Masculino',NULL,'Negro','Pedro Vargas',NULL),(115,'1948-03-15','Japão','Pioneiro do Zen no Brasil desde 1975','Monge Chefe','Masculino','2021-12-01','Asiático','Daigo Watanabe',NULL),(116,'1980-07-22','México','Criadora do método \"Meditação Ativa\"','Instrutora Sênior','Feminino',NULL,'Mestiço','Mariana Flores',NULL),(117,'1965-11-30','Tibet','Refugiado político, mestre em filosofia Madhyamaka','Lama','Masculino',NULL,'Asiático','Lobsang Tenpa',NULL),(118,'1992-02-14','Índia','Doutora em estudos budistas pela USP','Pesquisadora','Feminino',NULL,'Asiático','Amita Gupta',NULL),(119,'1973-09-05','Brasil','Responsável pela BSGI Brasil','Presidente','Masculino',NULL,'Amarelo','Carlos Yamato',NULL),(120,'1950-12-25','Butão','Introduziu práticas tântricas femininas','Mestra','Feminino','2020-08-08','Asiático','Tharpa Dolma',NULL),(121,'1985-04-18','Portugal','Gestor do maior centro de retiros do Chile','Coordenador','Masculino',NULL,'Branco','Ricardo Sampaio',NULL),(122,'2000-01-09','Japão','Mais jovem instrutora certificada','Monja','Feminino',NULL,'Asiático','Sakura Nakamura',NULL),(123,'1991-06-30','Gana','Fundador do Budismo Afrocentrado','Ativista','Não-binário',NULL,'Negro','Kwame Adjoa',NULL),(124,'1978-08-12','Brasil','Integra mindfulness em tratamentos de câncer','Médica','Feminino',NULL,'Negro','Fernanda Silva',NULL),(125,'1935-05-05','Japão','Mestre responsável pela linhagem Rinzai','Roshi','Masculino','2010-10-10','Asiático','Tenzen Kobayashi',NULL),(126,'1995-11-21','Brasil','Primeira brasileira ordenada no Sri Lanka','Estudante','Feminino',NULL,'Branco','Ananda Pereira',NULL),(127,'1968-02-28','Índia','Especialista em diálogo inter-religioso','Professor','Masculino',NULL,'Asiático','Surya Das',NULL),(128,'1989-09-07','Brasil','Combina xamanismo com práticas Zen','Líder','Feminino',NULL,'Indígena','Yara Santos',NULL),(129,'1942-07-04','Japão','Fundador do primeiro templo Soto Zen','Pioneiro','Masculino','2019-03-03','Asiático','Hiroshi Matsuda',NULL),(130,'1948-03-15','Japão','Pioneiro do Zen no Brasil desde 1975','Monge Chefe','Masculino','2021-12-01','Asiático','Daigo Watanabe',NULL),(131,'1980-07-22','México','Criadora do método \"Meditação Ativa\"','Instrutora Sênior','Feminino',NULL,'Mestiço','Mariana Flores',NULL),(132,'1965-11-30','Tibet','Refugiado político, mestre em filosofia Madhyamaka','Lama','Masculino',NULL,'Asiático','Lobsang Tenpa',NULL),(133,'1992-02-14','Índia','Doutora em estudos budistas pela USP','Pesquisadora','Feminino',NULL,'Asiático','Amita Gupta',NULL),(134,'1973-09-05','Brasil','Responsável pela BSGI Brasil','Presidente','Masculino',NULL,'Amarelo','Carlos Yamato',NULL),(135,'1950-12-25','Butão','Introduziu práticas tântricas femininas','Mestra','Feminino','2020-08-08','Asiático','Tharpa Dolma',NULL),(136,'1985-04-18','Portugal','Gestor do maior centro de retiros do Chile','Coordenador','Masculino',NULL,'Branco','Ricardo Sampaio',NULL),(137,'2000-01-09','Japão','Mais jovem instrutora certificada','Monja','Feminino',NULL,'Asiático','Sakura Nakamura',NULL),(138,'1991-06-30','Gana','Fundador do Budismo Afrocentrado','Ativista','Não-binário',NULL,'Negro','Kwame Adjoa',NULL),(139,'1978-08-12','Brasil','Integra mindfulness em tratamentos de câncer','Médica','Feminino',NULL,'Negro','Fernanda Silva',NULL),(140,'1935-05-05','Japão','Mestre responsável pela linhagem Rinzai','Roshi','Masculino','2010-10-10','Asiático','Tenzen Kobayashi',NULL),(141,'1995-11-21','Brasil','Primeira brasileira ordenada no Sri Lanka','Estudante','Feminino',NULL,'Branco','Ananda Pereira',NULL),(142,'1968-02-28','Índia','Especialista em diálogo inter-religioso','Professor','Masculino',NULL,'Asiático','Surya Das',NULL),(143,'1989-09-07','Brasil','Combina xamanismo com práticas Zen','Líder','Feminino',NULL,'Indígena','Yara Santos',NULL),(144,'1942-07-04','Japão','Fundador do primeiro templo Soto Zen','Pioneiro','Masculino','2019-03-03','Asiático','Hiroshi Matsuda',NULL),(145,'1948-03-15','Japão','Pioneiro do Zen no Brasil desde 1975','Monge Chefe','Masculino','2021-12-01','Asiático','Daigo Watanabe',NULL),(146,'1980-07-22','México','Criadora do método \"Meditação Ativa\"','Instrutora Sênior','Feminino',NULL,'Mestiço','Mariana Flores',NULL),(147,'1965-11-30','Tibet','Refugiado político, mestre em filosofia Madhyamaka','Lama','Masculino',NULL,'Asiático','Lobsang Tenpa',NULL),(148,'1992-02-14','Índia','Doutora em estudos budistas pela USP','Pesquisadora','Feminino',NULL,'Asiático','Amita Gupta',NULL),(149,'1973-09-05','Brasil','Responsável pela BSGI Brasil','Presidente','Masculino',NULL,'Amarelo','Carlos Yamato',NULL),(150,'1950-12-25','Butão','Introduziu práticas tântricas femininas','Mestra','Feminino','2020-08-08','Asiático','Tharpa Dolma',NULL),(151,'1985-04-18','Portugal','Gestor do maior centro de retiros do Chile','Coordenador','Masculino',NULL,'Branco','Ricardo Sampaio',NULL),(152,'2000-01-09','Japão','Mais jovem instrutora certificada','Monja','Feminino',NULL,'Asiático','Sakura Nakamura',NULL),(153,'1991-06-30','Gana','Fundador do Budismo Afrocentrado','Ativista','Não-binário',NULL,'Negro','Kwame Adjoa',NULL),(154,'1978-08-12','Brasil','Integra mindfulness em tratamentos de câncer','Médica','Feminino',NULL,'Negro','Fernanda Silva',NULL),(155,'1935-05-05','Japão','Mestre responsável pela linhagem Rinzai','Roshi','Masculino','2010-10-10','Asiático','Tenzen Kobayashi',NULL),(156,'1995-11-21','Brasil','Primeira brasileira ordenada no Sri Lanka','Estudante','Feminino',NULL,'Branco','Ananda Pereira',NULL),(157,'1968-02-28','Índia','Especialista em diálogo inter-religioso','Professor','Masculino',NULL,'Asiático','Surya Das',NULL),(158,'1989-09-07','Brasil','Combina xamanismo com práticas Zen','Líder','Feminino',NULL,'Indígena','Yara Santos',NULL),(159,'1942-07-04','Japão','Fundador do primeiro templo Soto Zen','Pioneiro','Masculino','2019-03-03','Asiático','Hiroshi Matsuda',NULL);
/*!40000 ALTER TABLE `personalidade` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personalidade_associacao`
--

DROP TABLE IF EXISTS `personalidade_associacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personalidade_associacao` (
  `ID_PERSONALIDADE_ASSOCIACAO` int NOT NULL AUTO_INCREMENT,
  `ID_PA_PERSONALIDADE_FK` int NOT NULL,
  `ID_PA_ASSOCIACAO_FK` int NOT NULL,
  PRIMARY KEY (`ID_PERSONALIDADE_ASSOCIACAO`),
  KEY `ID_PERSONALIDADE_idx` (`ID_PA_PERSONALIDADE_FK`),
  KEY `ID_ASSOCIACAO_idx` (`ID_PA_ASSOCIACAO_FK`),
  CONSTRAINT `fk_personalidade_assoc_associacao` FOREIGN KEY (`ID_PA_ASSOCIACAO_FK`) REFERENCES `associacao` (`ID_ASSOCIACAO`),
  CONSTRAINT `fk_personalidade_assoc_personalidade` FOREIGN KEY (`ID_PA_PERSONALIDADE_FK`) REFERENCES `personalidade` (`ID_PERSONALIDADE`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personalidade_associacao`
--

LOCK TABLES `personalidade_associacao` WRITE;
/*!40000 ALTER TABLE `personalidade_associacao` DISABLE KEYS */;
INSERT INTO `personalidade_associacao` VALUES (31,58,1),(32,59,2);
/*!40000 ALTER TABLE `personalidade_associacao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personalidade_produto`
--

DROP TABLE IF EXISTS `personalidade_produto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personalidade_produto` (
  `ID_PERSONALIDADE_PRODUTO` int NOT NULL AUTO_INCREMENT,
  `ID_PP_PERSONALIDADE_FK` int NOT NULL,
  `ID_PP_PRODUTO_FK` int NOT NULL,
  PRIMARY KEY (`ID_PERSONALIDADE_PRODUTO`),
  KEY `ID_PERSONALIDADE_idx` (`ID_PP_PERSONALIDADE_FK`),
  KEY `ID_PRODUTO_idx` (`ID_PP_PRODUTO_FK`),
  CONSTRAINT `fk_personalidade_produto_personalidade` FOREIGN KEY (`ID_PP_PERSONALIDADE_FK`) REFERENCES `personalidade` (`ID_PERSONALIDADE`),
  CONSTRAINT `fk_personalidade_produto_produto` FOREIGN KEY (`ID_PP_PRODUTO_FK`) REFERENCES `produto` (`ID_PRODUTO`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personalidade_produto`
--

LOCK TABLES `personalidade_produto` WRITE;
/*!40000 ALTER TABLE `personalidade_produto` DISABLE KEYS */;
INSERT INTO `personalidade_produto` VALUES (1,58,1),(2,59,2),(5,63,3),(6,64,4);
/*!40000 ALTER TABLE `personalidade_produto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personalidade_templo`
--

DROP TABLE IF EXISTS `personalidade_templo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personalidade_templo` (
  `ID_PERSONALIDADE_TEMPLO` int NOT NULL AUTO_INCREMENT,
  `ID_PT_PERSONALIDADE_FK` int NOT NULL,
  `ID_PT_TEMPLO_FK` int NOT NULL,
  `FUNCAO` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`ID_PERSONALIDADE_TEMPLO`),
  KEY `ID_TEMPLO_idx` (`ID_PT_TEMPLO_FK`),
  KEY `ID_PERSONALIDADE_idx` (`ID_PT_PERSONALIDADE_FK`),
  CONSTRAINT `fk_personalidade_templo_personalidade` FOREIGN KEY (`ID_PT_PERSONALIDADE_FK`) REFERENCES `personalidade` (`ID_PERSONALIDADE`),
  CONSTRAINT `fk_personalidade_templo_templo` FOREIGN KEY (`ID_PT_TEMPLO_FK`) REFERENCES `templo` (`ID_TEMPLO`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personalidade_templo`
--

LOCK TABLES `personalidade_templo` WRITE;
/*!40000 ALTER TABLE `personalidade_templo` DISABLE KEYS */;
INSERT INTO `personalidade_templo` VALUES (31,58,51,'Abade Chefe'),(32,59,52,'Instrutor Chefe'),(33,60,53,'Cuidador de Templo'),(34,61,54,'Pesquisadora'),(35,62,55,'Mestre Zen'),(36,58,7,'Escudo');
/*!40000 ALTER TABLE `personalidade_templo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personalidade_visita`
--

DROP TABLE IF EXISTS `personalidade_visita`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `personalidade_visita` (
  `ID_PERSONALIDADE_VISITA` int NOT NULL AUTO_INCREMENT,
  `ID_PV_PERSONALIDADE_FK` int NOT NULL,
  `ID_PV_VISITA_FK` int NOT NULL,
  PRIMARY KEY (`ID_PERSONALIDADE_VISITA`),
  KEY `ID_PERSONALIDADE_idx` (`ID_PV_PERSONALIDADE_FK`),
  KEY `ID_VISITA_idx` (`ID_PV_VISITA_FK`),
  CONSTRAINT `fk_personalidade_visita_personalidade` FOREIGN KEY (`ID_PV_PERSONALIDADE_FK`) REFERENCES `personalidade` (`ID_PERSONALIDADE`),
  CONSTRAINT `fk_personalidade_visita_visita` FOREIGN KEY (`ID_PV_VISITA_FK`) REFERENCES `visita` (`ID_VISITA`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personalidade_visita`
--

LOCK TABLES `personalidade_visita` WRITE;
/*!40000 ALTER TABLE `personalidade_visita` DISABLE KEYS */;
INSERT INTO `personalidade_visita` VALUES (21,58,1),(22,59,2),(23,60,3),(24,61,4),(25,62,5),(36,58,11),(37,59,12),(38,60,13),(39,61,14),(40,62,15),(41,63,16),(42,64,17),(43,65,18),(44,66,19),(45,67,20);
/*!40000 ALTER TABLE `personalidade_visita` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produto`
--

DROP TABLE IF EXISTS `produto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produto` (
  `ID_PRODUTO` int NOT NULL AUTO_INCREMENT,
  `NOME_PRODUTO` varchar(50) NOT NULL,
  `DATA_LANCAMENTO` date DEFAULT NULL,
  `TIPO_PRODUTO` varchar(20) NOT NULL,
  `IMAGEM_PERFIL_URL` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID_PRODUTO`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produto`
--

LOCK TABLES `produto` WRITE;
/*!40000 ALTER TABLE `produto` DISABLE KEYS */;
INSERT INTO `produto` VALUES (1,'Livro \"Mindfulness Moderno\"1',NULL,'Livro','/uploads/produto_1_perfil_dcfed13ba3f745fcb5be8225fd2c190a.png'),(2,'Estatueta Buda de Madeira',NULL,'Arte Religiosa',NULL),(3,'Curso Online de Meditação',NULL,'Curso',NULL),(4,'Incenso Artesanal',NULL,'Acessório',NULL);
/*!40000 ALTER TABLE `produto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `templo`
--

DROP TABLE IF EXISTS `templo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `templo` (
  `ID_TEMPLO` int NOT NULL AUTO_INCREMENT,
  `NOME` varchar(40) NOT NULL,
  `VEICULO` varchar(15) NOT NULL,
  `PAIS` varchar(25) NOT NULL,
  `ESCOLA` varchar(25) NOT NULL,
  `DATA_FECHAMENTO_TEMPLO` date DEFAULT NULL,
  `DATA_ABERTURA_TEMPLO` date DEFAULT NULL,
  `ESTADO` varchar(5) DEFAULT NULL,
  `MUNICIPIO` varchar(50) DEFAULT NULL,
  `CODIGO_POSTAL` varchar(10) DEFAULT NULL,
  `CAMPO_INFO_TEMPLO` text,
  `PUBLICO_ALVO` varchar(15) DEFAULT NULL,
  `IMAGEM_PERFIL_URL` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID_TEMPLO`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `templo`
--

LOCK TABLES `templo` WRITE;
/*!40000 ALTER TABLE `templo` DISABLE KEYS */;
INSERT INTO `templo` VALUES (1,'Rodrigow','Teravada','Brasil','Zn',NULL,NULL,'NDs','Lake Curtis','11896','Campo enformacional','0',NULL),(2,'James','Não Sectário','El Salvadorea','SaD',NULL,NULL,'AsdD','Cassandraton','70785','Camp','0',NULL),(3,'Jackson, Daniel and Martin','Não Sectário','Venezuela','Zn','1212-12-12','1212-12-12','','Nelsonside','29286','','0',NULL),(4,'Davis-Williams','Mahayana','Honduras','Mahayana',NULL,'1977-01-27','CA','East Courtneychester','50933','Telefone: +1-784-801-8451x462\nEmail: mckaynancy@yahoo.com\nWeb: http://www.evans.com/','0',NULL),(5,'Farmer-Rya','Teravada','Republica Don','Sa',NULL,'1974-07-15','','New Mariotown','15163','Telefone: 303-911-7182x2782\nEmail: ibrandt@hotmail.com\nWeb: http://carney-santos.info/','1',NULL),(6,'Hayes, Wright and Brown','Mahayana','Argentina','Fo','0001-01-01','1934-10-19','AL','New Angelashire',NULL,'Telefone: 001-031-051-8347x382\nEmail: kristenaguirre@gmail.com\nWeb: http://www.jordan.com/','0',NULL),(7,'BRAUM ESTA AQUIa','Vajrayana','Bolívias','Khs','1222-12-11','1212-11-11','IDs','Laurenville','25432','Sim essas são as informações adicionais','1','/uploads/templo_7_perfil_a491c57b41de4569bab7a17466389b41.jpg'),(8,'Henderson-Bernard','Mahayana','El Salvador','SG','0001-01-01','1998-12-05','AR','Mooreport','76415','Telefone: 5009788208\nEmail: caseyjones@powell.com\nWeb: http://www.sandoval-cunningham.com/','0',NULL),(9,'Harris-Moran','Teravada','Guiana Francesa','Fo','0001-01-01','2012-12-27',NULL,'West Randy','88540','Telefone: 751-079-9118x3842\nEmail: suarezmike@gmail.com\nWeb: https://riggs.net/','0',NULL),(10,'Huynh-Garcia','Vajrayana','Venezuela','Etib',NULL,'2000-06-05','WA','West Darrell',NULL,'Telefone: (449)353-4874\nEmail: waltersmaria@smith.com\nWeb: http://thornton.com/','1',NULL),(11,'Johnson, Wood and Tran','Vajrayana','Porto Rico','Gg',NULL,NULL,NULL,'Andersonport','48296','Telefone: 5331586923\nEmail: nicolejohnson@middleton.com\nWeb: https://www.rodriguez.com/','0',NULL),(12,'Velasquez Group','Teravada','Colômbia','Sg',NULL,'1951-06-03','AK','Kevinbury','87012','Telefone: (541)458-6850x1429\nEmail: rodriguezryan@hotmail.com\nWeb: https://joyce.com/','1',NULL),(13,'Williams-Graham','Não Sectário','Peru','Ch',NULL,'1967-11-10','MA','West Ryan','82179','Telefone: +1-148-465-6482x36629\nEmail: akelley@yahoo.com\nWeb: https://www.floyd-lawson.com/','1',NULL),(14,'Ramos-Lowe','Não Sectário','Haiti','Ch',NULL,NULL,NULL,'Leonburgh',NULL,'Telefone: +1-148-951-3433x20037\nEmail: operry@lee.com\nWeb: http://www.osborne.com/','1',NULL),(15,'Holmes, Williams and Wright','Teravada','Equador','Teravada',NULL,'2006-03-06','NC','South Dennismouth','73760','Telefone: 798-687-2774x34873\nEmail: sjones@gmail.com\nWeb: https://orozco-miller.com/','0',NULL),(16,'Reyes and Sons','Teravada','Guiana','Etib',NULL,'1988-07-19','ND','North Robert',NULL,'Telefone: (036)690-9670x54668\nEmail: brobinson@johnson-rogers.biz\nWeb: http://hooper.com/','1',NULL),(17,'Vargas-Alvarado','Teravada','Paraguai','Etib',NULL,'1949-11-13',NULL,'Lake Roymouth',NULL,'Telefone: 4653755646\nEmail: ruizkaitlyn@gmail.com\nWeb: https://www.jones.com/','0',NULL),(18,'Gonzalez Inc','Mahayana','Guiana','Gg',NULL,'2016-03-31',NULL,'East David',NULL,'Telefone: 937-452-9912\nEmail: lanesarah@hotmail.com\nWeb: https://gonzalez.com/','0',NULL),(19,'Terry LLC','Vajrayana','Uruguai','Nk',NULL,'2015-03-03','ND','Port Tonyaton','56649','Telefone: (185)067-1657x262\nEmail: umarshall@hotmail.com\nWeb: https://rivas.com/','1',NULL),(20,'Sanchez-Marshall','Mahayana','Paraguai','Fo',NULL,'1949-11-19','MD','Rogersfort',NULL,'Telefone: 354.549.4808x3136\nEmail: hannahbrewer@yahoo.com\nWeb: https://www.phillips.com/','1',NULL),(21,'Beck-Wood','Não Sectário','Uruguai','Td',NULL,NULL,'','Ronaldside',NULL,'ass','1',NULL),(22,'Ferguson, Hill and Mccann','Mahayana','Brasil','Gg','0001-01-01','1939-02-05','WV','Heidiberg','64841','Telefone: 9477752047\nEmail: moralescharles@parks.com\nWeb: http://www.grant.org/','0',NULL),(23,'Gibbs, Perez and Mills','Teravada','Guatemala','Ny',NULL,'1983-07-02',NULL,'Kerrport','77640','Telefone: 990-913-3412x3281\nEmail: ortizhannah@carter-hall.com\nWeb: https://www.hall.org/','0',NULL),(24,'Lara, Gonzalez and Wilson','Mahayana','Brasil','SG','0001-01-01','1944-06-29',NULL,'Lake Edward','35317','Telefone: 024-994-7174\nEmail: vincent77@gmail.com\nWeb: http://morris.org/','0',NULL),(25,'Sampson, Key and Chambers','Teravada','Belize','Teravada','0001-01-01','1995-10-07',NULL,'Barbaraburgh','62170','Telefone: +1-742-967-1756x5512\nEmail: ssteele@hotmail.com\nWeb: https://www.miller-king.com/','1',NULL),(26,'Hancock-Bryan','Mahayana','Costa Rica','Sk',NULL,'1950-08-31','AR','Lake Mollymouth',NULL,'Telefone: 597.703.4824x77109\nEmail: lancesmith@davis-gay.com\nWeb: https://www.collier.net/','1',NULL),(27,'Hill, Davenport and Baird','Não Sectário','Porto Rico','Bo',NULL,'1994-04-22','ID','South Andrea','79062','Telefone: 001-214-658-4044x9972\nEmail: jreed@hotmail.com\nWeb: https://kane-pollard.com/','0',NULL),(28,'Reyes, Chase and Jenkins','Não Sectário','Paraguai','Ni',NULL,'1945-11-02','TN','Juliefurt','85962','Telefone: 028.951.7187x0262\nEmail: qharrington@hanson-sanders.com\nWeb: https://sims-clay.info/','0',NULL),(29,'Johnson, Jones and Welch','Não Sectário','Cuba','SG',NULL,'2020-12-07','CT','Wendyland','83567','Telefone: 724-005-0455\nEmail: johnjenkins@hotmail.com\nWeb: http://www.miller.org/','0',NULL),(30,'Allen, Durham and Thomas','Vajrayana','Equador','Vajrayana','1222-12-11','1111-12-11','TN','Littlemouth',NULL,'asd','0',NULL),(31,'Knight Ltd','Vajrayana','Suriname','Sh',NULL,'1973-01-31','IN','New Julieport','80070','Telefone: 394.210.4709\nEmail: christopherphillips@hotmail.com\nWeb: https://www.anderson.com/','0',NULL),(32,'Shaw, Nelson and Martin','Mahayana','República Dominicana','Mahayana',NULL,'1971-03-27',NULL,'Coffeyport',NULL,'Telefone: 712-368-5160\nEmail: gibsonemily@hotmail.com\nWeb: https://bentley.com/','1',NULL),(33,'Henson, Hoffman and Herman','Vajrayana','Guiana','Ch',NULL,NULL,'NH','Lake Bryan','92392','Telefone: 612-004-7113x8267\nEmail: umatthews@gmail.com\nWeb: https://www.gilbert-crosby.com/','0',NULL),(34,'Vaughn and Sons','Teravada','Guatemala','Td',NULL,'2018-06-16','MN','Wallacebury','13523','Telefone: (850)643-1713x900\nEmail: vanessabuchanan@gmail.com\nWeb: http://www.robinson.com/','1',NULL),(35,'Smith, Garrison and Thomas','Não Sectário','República Dominicana','Fo',NULL,'1928-08-23','DE','New John','87147','Telefone: (053)950-2402\nEmail: reesethomas@yahoo.com\nWeb: http://walker.net/','1',NULL),(36,'Ellis-Maynard','Vajrayana','Honduras','Nk','0001-01-01','2022-02-03','CT','South Melaniechester','64761','Telefone: 115.921.2499x856\nEmail: bwagner@gmail.com\nWeb: http://www.hayes-perez.com/','0',NULL),(37,'Ross-Blair','Mahayana','Venezuela','Kg',NULL,'1989-09-06','FL','Ronaldview','90524','Telefone: 111-615-2809\nEmail: jenkinsmorgan@yahoo.com\nWeb: http://edwards.com/','0',NULL),(38,'Olson, Boone and Bell','Vajrayana','Costa Rica','SG',NULL,NULL,'IN','Dannyview','56745','Telefone: +1-998-094-0244\nEmail: adam29@hotmail.com\nWeb: https://www.figueroa.com/','1',NULL),(39,'Moreno, Bennett and Chavez','Mahayana','Cuba','Mahayana','0001-01-01','1969-04-14',NULL,'West Larry',NULL,'Telefone: 001-991-022-9014x76797\nEmail: jason81@yahoo.com\nWeb: https://www.gregory-watkins.net/','0',NULL),(40,'Parker, Walker and Joyce','Mahayana','Brasil','Sg','0001-01-01','1964-07-12','DC','North Jamesborough','33992','Telefone: 107-622-6838x85160\nEmail: stevenschristian@yahoo.com\nWeb: https://bowman.com/','1',NULL),(41,'Solis PLC','Vajrayana','Chile','SG','0001-01-01','1958-04-02','NE','Collierstad','14376','Telefone: (968)164-5352x18188\nEmail: michael23@thomas.com\nWeb: http://www.bean.info/','1',NULL),(42,'Webster-Wolf','Vajrayana','Guiana Francesa','Sk',NULL,NULL,'SC','Maldonadoshire',NULL,'Telefone: +1-552-717-7449x058\nEmail: steven00@decker-jones.com\nWeb: https://spencer.info/','1',NULL),(43,'Pearson, Morris and Alvarez','Mahayana','República Dominicana','Zn',NULL,'1936-08-12','MA','North Shannon','94127','Telefone: 203.778.8925x54665\nEmail: cameron18@hughes.org\nWeb: http://aguilar.com/','1',NULL),(44,'Ponce-Hale','Teravada','Peru','N2','0001-01-01','1976-05-26','OH','Andersonland',NULL,'Telefone: +1-528-168-5054x2357\nEmail: zoemoore@richard-garcia.net\nWeb: http://anderson.org/','0',NULL),(45,'Griffith Inc','Mahayana','Uruguai','Sh',NULL,'1985-08-04',NULL,'Diazbury',NULL,'Telefone: +1-473-834-7359x774\nEmail: mburch@hotmail.com\nWeb: http://davidson.net/','1',NULL),(46,'Dawson PLC','Vajrayana','Haiti','Ny',NULL,'1945-03-10','NV','West Christopherburgh','67787','Telefone: (137)506-0685x36153\nEmail: sarah52@johnson.com\nWeb: https://smith.com/','0',NULL),(47,'Bentley, Lynch and Henderson','Mahayana','Bolívia','Bo',NULL,'1982-04-10','IA','Johnville',NULL,'Telefone: +1-971-179-8089x3246\nEmail: john62@barnett.net\nWeb: http://williams-hughes.com/','1',NULL),(48,'Burgess-Kelly','Vajrayana','Paraguai','Nk',NULL,'1970-05-23','OR','West Johnville','96863','Telefone: (058)527-7221\nEmail: carterbradley@gmail.com\nWeb: http://robertson-hays.net/','0',NULL),(49,'King-Mullins','Vajrayana','Uruguai','SG',NULL,'1970-04-24','AR','West Michael','86449','Telefone: 156-676-5277x584\nEmail: mmiller@gardner.com\nWeb: http://phillips.com/','0',NULL),(50,'Wallace, West and Acosta','Teravada','Colômbia','N2',NULL,'2012-03-02',NULL,'Christinachester','36487','Telefone: 1658202970\nEmail: youngdeanna@reyes-bradley.org\nWeb: http://watson-hines.org/','1',NULL),(51,'Templo Paz Interior','Mahayana','Brasil','Zen',NULL,'2005-04-12','SP','Cotia','06700','Primeiro templo zen do Brasil com arquitetura tradicional','1',NULL),(52,'Monastério Sakya','Vajrayana','Argentina','Sakya',NULL,'1992-08-18','ME','Mendo','5500','Único centro Sakya na América do Sul','0',NULL),(53,'Centro Vipassana','Theravada','Chile','Therevada',NULL,'2010-02-28','RM','Santi','8320','Retiros silenciosos na cordilheira','1',NULL),(54,'Templo Lótus Dourado','Mahayana','Peru','Terra Pura',NULL,'1980-12-05','CU','Cusc','08002','Famoso por seu jardim de estátuas','1',NULL),(55,'Monte Koya do Brasil','Vajrayana','Brasil','Shingon',NULL,'2018-09-22','PR','Curi','80000','Réplica do templo japonês de Koyasan','0',NULL),(56,'Templo da Compaixão','Mahayana','Argentina','Gelug','2015-11-30','2003-07-15','BA','Buen','C1428','Fechado após incêndio em 2015','1',NULL),(57,'Bosque Dharma','Theravada','Chile','Therevada',NULL,'2021-03-10','LL','Pucon','4920','Construído com técnicas de bioconstrução','1',NULL),(58,'Templo Nichiren','Mahayana','Brasil','Nichiren',NULL,'1999-01-09','RJ','Nité','24000','Sede da BSGI no Brasil','0',NULL),(59,'Retiro das Montanhas','Vajrayana','Bolívia','Kagyu',NULL,'2015-06-06','LP','La Pa','0000','Altitude 3.640m - práticas avançadas','1',NULL),(60,'Templo da Juventude','Mahayana','Brasil','Zen',NULL,'2020-08-08','MG','Belo','30000','Foco em programas para jovens','1',NULL),(61,'Centro Rinzai','Mahayana','Paraguai','Rinzai',NULL,'1988-10-30','AS','Asun','00123','Único centro Rinzai autêntico na AL','0',NULL),(62,'Templo Tara Verde','Vajrayana','Uruguai','Nyingma',NULL,'2007-04-04','MO','Mont','11200','Especializado em práticas femininas','1',NULL),(63,'Casa de Meditação','Theravada','Colômbia','Therevada',NULL,'2012-12-12','BO','Bogo','11001','Programas urbanos de mindfulness','0',NULL),(64,'Templo do Amanhecer','Mahayana','Brasil','Soto',NULL,'1975-05-15','RS','Port','90000','Primeiro templo Soto Zen no país','1',NULL),(65,'Montanha Sagrada','Vajrayana','Equador','Kagyu','2023-01-01','1990-09-19','PI','Quit','170135','Fechado para reformas estruturais','1',NULL),(66,'Templo Paz Interior','Mahayana','Brasil','Zen',NULL,'2005-04-12','SP','Cotia','06700','Primeiro templo zen do Brasil com arquitetura tradicional','1',NULL),(67,'Monastério Sakya','Vajrayana','Argentina','Sakya',NULL,'1992-08-18','ME','Mendo','5500','Único centro Sakya na América do Sul','0',NULL),(68,'Centro Vipassana','Theravada','Chile','Therevada',NULL,'2010-02-28','RM','Santi','8320','Retiros silenciosos na cordilheira','1',NULL),(69,'Templo Lótus Dourado','Mahayana','Peru','Terra Pura',NULL,'1980-12-05','CU','Cusc','08002','Famoso por seu jardim de estátuas','1',NULL),(70,'Monte Koya do Brasil','Vajrayana','Brasil','Shingon',NULL,'2018-09-22','PR','Curi','80000','Réplica do templo japonês de Koyasan','0',NULL),(71,'Templo da Compaixão','Mahayana','Argentina','Gelug','2015-11-30','2003-07-15','BA','Buen','C1428','Fechado após incêndio em 2015','1',NULL),(72,'Bosque Dharma','Theravada','Chile','Therevada',NULL,'2021-03-10','LL','Pucon','4920','Construído com técnicas de bioconstrução','1',NULL),(73,'Templo Nichiren','Mahayana','Brasil','Nichiren',NULL,'1999-01-09','RJ','Nité','24000','Sede da BSGI no Brasil','0',NULL),(74,'Retiro das Montanhas','Vajrayana','Bolívia','Kagyu',NULL,'2015-06-06','LP','La Pa','0000','Altitude 3.640m - práticas avançadas','1',NULL),(75,'Templo da Juventude','Mahayana','Brasil','Zen',NULL,'2020-08-08','MG','Belo','30000','Foco em programas para jovens','1',NULL),(76,'Centro Rinzai','Mahayana','Paraguai','Rinzai',NULL,'1988-10-30','AS','Asun','00123','Único centro Rinzai autêntico na AL','0',NULL),(77,'Templo Tara Verde','Vajrayana','Uruguai','Nyingma',NULL,'2007-04-04','MO','Mont','11200','Especializado em práticas femininas','1',NULL),(78,'Casa de Meditação','Theravada','Colômbia','Therevada',NULL,'2012-12-12','BO','Bogo','11001','Programas urbanos de mindfulness','0',NULL),(79,'Templo do Amanhecer','Mahayana','Brasil','Soto',NULL,'1975-05-15','RS','Port','90000','Primeiro templo Soto Zen no país','1',NULL),(80,'Montanha Sagrada','Vajrayana','Equador','Kagyu','2023-01-01','1990-09-19','PI','Quit','170135','Fechado para reformas estruturais','1',NULL),(81,'Templo Paz Interior','Mahayana','Brasil','Zen',NULL,'2005-04-12','SP','Cotia','06700','Primeiro templo zen do Brasil com arquitetura tradicional','1',NULL),(82,'Monastério Sakya','Vajrayana','Argentina','Sakya',NULL,'1992-08-18','ME','Mendo','5500','Único centro Sakya na América do Sul','0',NULL),(83,'Centro Vipassana','Theravada','Chile','Therevada',NULL,'2010-02-28','RM','Santi','8320','Retiros silenciosos na cordilheira','1',NULL),(84,'Templo Lótus Dourado','Mahayana','Peru','Terra Pura',NULL,'1980-12-05','CU','Cusc','08002','Famoso por seu jardim de estátuas','1',NULL),(85,'Monte Koya do Brasil','Vajrayana','Brasil','Shingon',NULL,'2018-09-22','PR','Curi','80000','Réplica do templo japonês de Koyasan','0',NULL),(86,'Templo da Compaixão','Mahayana','Argentina','Gelug','2015-11-30','2003-07-15','BA','Buen','C1428','Fechado após incêndio em 2015','1',NULL),(87,'Bosque Dharma','Theravada','Chile','Therevada',NULL,'2021-03-10','LL','Pucon','4920','Construído com técnicas de bioconstrução','1',NULL),(88,'Templo Nichiren','Mahayana','Brasil','Nichiren',NULL,'1999-01-09','RJ','Nité','24000','Sede da BSGI no Brasil','0',NULL),(89,'Retiro das Montanhas','Vajrayana','Bolívia','Kagyu',NULL,'2015-06-06','LP','La Pa','0000','Altitude 3.640m - práticas avançadas','1',NULL),(90,'Templo da Juventude','Mahayana','Brasil','Zen',NULL,'2020-08-08','MG','Belo','30000','Foco em programas para jovens','1',NULL),(91,'Centro Rinzai','Mahayana','Paraguai','Rinzai',NULL,'1988-10-30','AS','Asun','00123','Único centro Rinzai autêntico na AL','0',NULL),(92,'Templo Tara Verde','Vajrayana','Uruguai','Nyingma',NULL,'2007-04-04','MO','Mont','11200','Especializado em práticas femininas','1',NULL),(94,'Templo do Amanhecer','Mahayana','Brasil','Soto',NULL,'1975-05-15','RS','Port','90000','Primeiro templo Soto Zen no país','1',NULL);
/*!40000 ALTER TABLE `templo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `templo_associacao`
--

DROP TABLE IF EXISTS `templo_associacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `templo_associacao` (
  `ID_TEMPLO_ASSOCIAÇÃO` int NOT NULL AUTO_INCREMENT,
  `ID_TA_TEMPLO_FK` int NOT NULL,
  `ID_TA_ASSOCIACAO_FK` int NOT NULL,
  PRIMARY KEY (`ID_TEMPLO_ASSOCIAÇÃO`),
  KEY `ID_TEMPLO_idx` (`ID_TA_TEMPLO_FK`),
  KEY `ID_ASSOCIAÇÃO_idx` (`ID_TA_ASSOCIACAO_FK`),
  CONSTRAINT `fk_templo_assoc_associacao` FOREIGN KEY (`ID_TA_ASSOCIACAO_FK`) REFERENCES `associacao` (`ID_ASSOCIACAO`),
  CONSTRAINT `fk_templo_assoc_templo` FOREIGN KEY (`ID_TA_TEMPLO_FK`) REFERENCES `templo` (`ID_TEMPLO`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `templo_associacao`
--

LOCK TABLES `templo_associacao` WRITE;
/*!40000 ALTER TABLE `templo_associacao` DISABLE KEYS */;
INSERT INTO `templo_associacao` VALUES (1,1,1),(2,2,2),(3,3,3),(4,4,4),(5,5,5),(8,8,3),(9,9,4),(10,10,5),(12,2,2),(13,3,3),(14,4,4),(15,5,5),(18,8,3),(19,9,4),(20,10,5),(22,1,8),(23,7,3),(24,7,9),(26,5,8),(27,2,9),(29,53,1);
/*!40000 ALTER TABLE `templo_associacao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `templo_visita`
--

DROP TABLE IF EXISTS `templo_visita`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `templo_visita` (
  `ID_TEMPLO_VISITA` int NOT NULL AUTO_INCREMENT,
  `ID_TV_VISITA_FK` int NOT NULL,
  `ID_TV_TEMPLO_FK` int NOT NULL,
  PRIMARY KEY (`ID_TEMPLO_VISITA`),
  KEY `ID_VISITA_idx` (`ID_TV_VISITA_FK`),
  KEY `ID_TEMPLO_idx` (`ID_TV_TEMPLO_FK`),
  CONSTRAINT `fk_templo_visita_templo` FOREIGN KEY (`ID_TV_TEMPLO_FK`) REFERENCES `templo` (`ID_TEMPLO`),
  CONSTRAINT `fk_templo_visita_visita` FOREIGN KEY (`ID_TV_VISITA_FK`) REFERENCES `visita` (`ID_VISITA`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `templo_visita`
--

LOCK TABLES `templo_visita` WRITE;
/*!40000 ALTER TABLE `templo_visita` DISABLE KEYS */;
INSERT INTO `templo_visita` VALUES (1,1,1),(2,2,2),(3,3,3),(4,4,4),(5,5,5),(6,6,6),(7,7,7),(8,8,8),(9,9,9),(10,10,10),(11,1,1),(12,2,2),(13,3,3),(14,4,4),(15,5,5),(16,6,6),(17,7,7),(18,8,8),(19,9,9),(20,10,10),(21,11,1),(22,12,2),(23,13,3),(24,14,4),(25,15,5),(26,16,6),(27,17,7),(28,18,8),(29,19,9),(30,20,10),(31,11,11),(32,12,12),(33,13,13),(34,14,14),(35,15,15);
/*!40000 ALTER TABLE `templo_visita` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `ID_USUARIO` int NOT NULL AUTO_INCREMENT,
  `NOME` varchar(255) NOT NULL,
  `SENHA` varchar(255) NOT NULL,
  `TIPO_CONTA` enum('admin','moderador') NOT NULL,
  PRIMARY KEY (`ID_USUARIO`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'Frank Usarski','Budismo123','admin'),(2,'Cesar Augusto','1','moderador'),(6,'André','André','moderador'),(7,'A','1','moderador');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visita`
--

DROP TABLE IF EXISTS `visita`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `visita` (
  `ID_VISITA` int NOT NULL AUTO_INCREMENT,
  `DATA_VISITA` date DEFAULT NULL,
  `CAMPO_INFO_VISITA` text,
  PRIMARY KEY (`ID_VISITA`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visita`
--

LOCK TABLES `visita` WRITE;
/*!40000 ALTER TABLE `visita` DISABLE KEYS */;
INSERT INTO `visita` VALUES (1,'2023-05-15','Inspeção anual de manutenção no Templo Paz Interior'),(2,'2022-09-22','Retiro de liderança para 30 monges'),(3,'2023-03-30','Workshop de arquitetura sagrada'),(4,'2021-12-08','Celebração do Bodhi Day com 500 participantes'),(5,'2020-07-19','Visita de intercâmbio com monges tailandeses'),(6,'2023-08-01','Capacitação de segurança contra incêndios'),(7,'2022-11-11','Cerimônia de consagração da nova biblioteca'),(8,'2021-04-09','Documentário sobre práticas tântricas'),(9,'2020-10-30','Mutirão de limpeza ecológica'),(10,'2023-01-15','Conferência sobre neurociência e meditação'),(11,'2023-05-15','Inspeção anual de manutenção no Templo Paz Interior'),(12,'2022-09-22','Retiro de liderança para 30 monges'),(13,'2023-03-30','Workshop de arquitetura sagrada'),(14,'2021-12-08','Celebração do Bodhi Day com 500 participantes'),(15,'2020-07-19','Visita de intercâmbio com monges tailandeses'),(16,'2023-08-01','Capacitação de segurança contra incêndios'),(17,'2022-11-11','Cerimônia de consagração da nova biblioteca'),(18,'2021-04-09','Documentário sobre práticas tântricas'),(19,'2020-10-30','Mutirão de limpeza ecológica'),(20,'2023-01-15','Conferência sobre neurociência e meditação'),(21,'2023-05-15','Inspeção anual de manutenção no Templo Paz Interior'),(22,'2022-09-22','Retiro de liderança para 30 monges'),(23,'2023-03-30','Workshop de arquitetura sagrada'),(24,'2021-12-08','Celebração do Bodhi Day com 500 participantes'),(25,'2020-07-19','Visita de intercâmbio com monges tailandeses'),(26,'2023-08-01','Capacitação de segurança contra incêndios'),(27,'2022-11-11','Cerimônia de consagração da nova biblioteca'),(28,'2021-04-09','Documentário sobre práticas tântricas'),(29,'2020-10-30','Mutirão de limpeza ecológica'),(30,'2023-01-15','Conferência sobre neurociência e meditação'),(31,'2024-01-10','Retiro de Ano Novo com 100 participantes'),(32,'2023-06-15','Workshop de jardinagem zen para iniciantes'),(33,'2024-02-22','Inspeção de segurança elétrica'),(34,'2023-09-05','Celebração do Equinócio de Primavera'),(35,'2024-03-18','Curso de filosofia budista básica'),(36,'2023-11-11','Cerimônia de memória aos mestres falecidos'),(37,'2024-04-05','Treinamento de primeiros socorros para monges'),(38,'2023-07-19','Festival cultural de danças sagradas'),(39,'2024-05-01','Mutirão de limpeza dos jardins'),(40,'2023-12-08','Palestra sobre ecodharma e sustentabilidade'),(41,'2024-06-14','Workshop de caligrafia japonesa'),(42,'2023-10-30','Preparação para retiro de inverno'),(43,'2024-07-07','Celebração do aniversário do templo'),(44,'2023-08-22','Visita de estudantes de arquitetura'),(45,'2024-08-30','Capacitação em gestão de riscos'),(46,'2023-04-14','Cerimônia de plantio de árvores nativas'),(47,'2024-09-09','Simpósio de medicina tradicional'),(48,'2023-05-21','Workshop de alimentação consciente'),(49,'2024-10-10','Festival de lanternas flutuantes'),(50,'2023-02-28','Inspeção anual de infraestrutura');
/*!40000 ALTER TABLE `visita` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-27 20:42:35
