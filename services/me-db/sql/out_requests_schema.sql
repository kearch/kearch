CREATE TABLE `out_requests` (
  `id` int NOT NULL AUTO_INCREMENT,
  `host_id` int NOT NULL,
  `is_approved` bool NOT NULL DEFAULT false,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(`id`),
  FOREIGN KEY (`host_id`) REFERENCES `sp_hosts` (`id`) ON UPDATE CASCADE ON DELETE CASCADE,
  UNIQUE KEY `index_out_requests_on_host_id` (`host_id`)
) ENGINE=InnoDB CHARACTER SET=utf8mb4;
