CREATE TABLE `webpages` (
  `url` varchar(255) NOT NULL,
  `title` text DEFAULT NULL,
  `title_words` json DEFAULT NULL,
  `summary` text DEFAULT NULL,
  `tfidf` json DEFAULT NULL,
  PRIMARY KEY(`url`)
);
