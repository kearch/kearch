CREATE TABLE `url_queue` (
  `id` int NOT NULL AUTO_INCREMENT,
  `url` varchar(255) NOT NULL,
  `crawled_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(`id`),
  UNIQUE KEY `index_url_queue_on_url` (`url`),
  INDEX `index_url_queue_on_crawled_at_and_updated_at` (`crawled_at`, `updated_at`)
) ENGINE=InnoDB CHARACTER SET=utf8mb4;
