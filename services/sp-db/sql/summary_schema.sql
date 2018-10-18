CREATE TABLE `summary` (
  `id` int NOT NULL AUTO_INCREMENT,
  `word` varchar(255) NOT NULL,
  `frequency` int NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(`id`),
  UNIQUE KEY `index_summary_on_word` (`word`)
) ENGINE=InnoDB CHARACTER SET=utf8mb4;
