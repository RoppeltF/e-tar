CREATE TABLE `listas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nomes` varchar(30) NOT NULL,
  `link` varchar(200) DEFAULT NULL,
  `data` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
