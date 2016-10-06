CREATE TABLE `occupation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `last_name` varchar(50) DEFAULT NULL,
  `birth` date DEFAULT NULL,
  `id_occupation` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_pessoas_1_idx` (`id_occupation`),
  CONSTRAINT `fk_users_1` FOREIGN KEY (`id_occupation`) REFERENCES `occupation` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=latin1;
