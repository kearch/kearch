CREATE TABLE `webpages` (
  `url` varchar(255) NOT NULL,
  `title` text DEFAULT NULL,
  `title_words` json DEFAULT NULL,
  `summary` text DEFAULT NULL,
  `tfidf` json DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(`url`)
) CHARACTER SET=utf8mb4;
