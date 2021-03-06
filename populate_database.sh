INSERT INTO `families` VALUES \
	(45,'Apocynacea'),
	(65,'Araceae'),
	(616,'Asphodelaceae'),
	(54,'Crassulaceae'),
	(218,'Marantaceae'),
	(149,'Moraceae'),
	(32,'Orchidaceae'),
	(69,'Rubiaceae'),
	(495,'Strelitziaceae');
INSERT INTO `genera` VALUES \
	(279,'Aloe',616),
	(1926,'Coffea',69),
	(2083,'Crassula',54),
	(2794,'Epipremnum',65),
	(2795,'Philodendron',65),
	(3630,'Hoya',45),
	(4700,'Monstera',65),
	(6381,'Strelitzia',495),
	(6850,'Vanilla',32),
	(8147,'Raphidophora',65),
	(13632,'Goeppertia',218),
	(13633,'Stromanthe',218),
	(43615,'Ficus',149);
INSERT INTO `species` VALUES \
	(122300,'arabica',1926),
	(123796,'ovata',2083),
	(132808,'pinnatum',2794),
	(132809,'aureum',2794),
	(143475,'carnosa',3630),
	(157552,'adansonii',4700),
	(157554,'deliciosa',4700),
	(165585,'hederaceum',2795),
	(184915,'reginae',6381),
	(191077,'planifolia',6850),
	(222369,'erubescens',2795),
	(222644,'burle-marxii',2795),
	(699609,'thalia',13633),
	(780168,'ornata',13632),
	(780214,'kegeljanii',13632),
	(780423,'elliptica',13632),
	(780486,'majestica',13632),
	(780646,'concinna',13632),
	(780719,'makoyana',13632),
	(780835,'orbifolia',13632),
	(1234157,'elastica',43615),
	(99999905,'lyrata',43615),
	(99999937,'natalensis',43615),
	(99999939,'tetrasperma',8147);

INSERT INTO `varieties` VALUES \
	('4pWgM','\"Manjula\"',132809),
	('B2VWb','\"Golden\"',132809),
	('Ba8qS','\"Peacock\"',780719),
	('E6gXD','\"Triostar\"',699609),
	('EVGtK','\"Network\"',780214),
	('JZo99','\"Chelsea\"',143475),
	('RoGG4','\"Thai Constellation\"',157554),
	('SzVbb','\"Marble Queen\"',132809),
	('UxVn2','\"Triangularis\"',99999937),
	('V9XKH','\"Cebu Blue\"',132808),
	('Y473K','\"Jade\"',123796);

INSERT INTO `contacts` VALUES \
	('94J5R','George','Tully','george@tullysgreenhouse.com',2486898735),
	('NinFG','Hank','Scorpio','hankscorpio@globex.com',8001418533),
	('TWrXN','Yosemite','Sam','y.sam@acme.com',5055571941);

INSERT INTO `suppliers` VALUES \
	('ZJ9Mz','Globex Corporation','533 Globex Dr','Canfield','OH',44406,'NinFG'),
	('TGKmf','Tully\'s Greenhouse','3103 John R. Rd.','Troy','MI',48083,'94J5R'),
	('TAGda','Acme Argricultural Supply','101 Cayote Dr','Albuquerque','NM',87104,'TWrXN');
