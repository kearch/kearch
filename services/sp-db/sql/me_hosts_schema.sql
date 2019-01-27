CREATE TABLE `me_hosts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `scheme` varchar(255) DEFAULT 'http',
  `name` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(`id`),
  UNIQUE KEY `index_me_hosts_on_name` (`name`)
) ENGINE=InnoDB CHARACTER SET=utf8mb4;
