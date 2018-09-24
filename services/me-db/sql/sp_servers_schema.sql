CREATE TABLE `sp_servers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `word` varchar(255) NOT NULL,
  `host` varchar(255) NOT NULL,
  `frequency` INTEGER DEFAULT 0,
  PRIMARY KEY(`id`),
  CONSTRAINT word_host UNIQUE (word, host)
) ENGINE=InnoDB CHARACTER SET=utf8mb4;
