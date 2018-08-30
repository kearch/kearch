CREATE TABLE `sp_servers` (
  `word` varchar(255) NOT NULL,
  `ip` varchar(255) NOT NULL,
  `frequency` INTEGER DEFAULT 0,
  PRIMARY KEY(`word`)
);
