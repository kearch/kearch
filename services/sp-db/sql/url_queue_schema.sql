CREATE TABLE `url_queue` (
  `id` int NOT NULL auto_increment,
  `url` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(`id`),
  CONSTRAINT `url_unique` UNIQUE (`url`)
) ENGINE=InnoDB CHARACTER SET=utf8mb4;
