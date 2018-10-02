CREATE TABLE `words` (
  `id` int NOT NULL AUTO_INCREMENT,
  `str` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY `index_words_on_str` (`str`)
) ENGINE=InnoDB CHARACTER SET=utf8mb4;
