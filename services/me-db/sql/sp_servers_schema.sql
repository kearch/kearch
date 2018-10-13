CREATE TABLE `sp_servers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `word` varchar(255) NOT NULL,
  `host` varchar(255) NOT NULL,
  `frequency` INTEGER DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(`id`),
  UNIQUE KEY index_sp_servers_on_word_and_host UNIQUE (word, host)
) ENGINE=InnoDB CHARACTER SET=utf8mb4;
