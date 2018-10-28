CREATE TABLE `connection_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `host` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(`id`),
) ENGINE=InnoDB CHARACTER SET=utf8mb4;
