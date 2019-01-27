CREATE TABLE `title_words` (
  `id` int NOT NULL AUTO_INCREMENT,
  `webpage_id` int NOT NULL,
  `word_id` int NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(`id`),
  FOREIGN KEY (`webpage_id`) REFERENCES `webpages` (`id`) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (`word_id`) REFERENCES `words` (`id`) ON UPDATE CASCADE ON DELETE CASCADE,
  UNIQUE KEY `index_title_words_on_webpage_id_and_word_id` (`webpage_id`, `word_id`)
) ENGINE=InnoDB CHARACTER SET=utf8mb4;
