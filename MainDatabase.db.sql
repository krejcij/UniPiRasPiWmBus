BEGIN TRANSACTION;
CREATE TABLE "TELEGRAMS" (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`DATETIME`	TEXT,
	`PRE`	TEXT,
	`HEADER`	TEXT,
	`DATA`	TEXT,
	`POST`	TEXT,
	`AESKEY`	TEXT
);
INSERT INTO `TELEGRAMS` VALUES (1,'2017-03-13 22:35','0000','2A44016A4493671201027244936712','016A0102000000208610830076238501000086208300973192000000','1234','-');
INSERT INTO `TELEGRAMS` VALUES (2,'2017-03-13 22:35','0000','2A44016A4742750101027247427501','016A01020000002086108300B80B0000000086208300F82A00000000','9658','-');
INSERT INTO `TELEGRAMS` VALUES (3,'2017-03-13 22:35','2e00','2a44016a4742750101027247427501','016a01021b00002086108300b80b0000000086208300f82a00000000','8cd4','-');
INSERT INTO `TELEGRAMS` VALUES (4,'2017-03-13 22:35','3200','2E44B05C11000000021B7A92080000','2F2F0A6667020AFB1A560402FD971D01002F2F2F2F2F2F2F2F2F2F2F2F2F2F2F','1234','-');
INSERT INTO `TELEGRAMS` VALUES (5,'2017-03-13 22:35','3200','2e44b05c10000000021b7a66080000','2f2f0a6690010afb1a090302fd971d01002f2f2f2f2f2f2f2f2f2f2f2f2f2f2f','8769','-');
INSERT INTO `TELEGRAMS` VALUES (6,'2017-03-13 22:35','0000','5E442D2C9643636013047AD2100000','2F2F0422BA11000004140F000000043B0000000002FD1700100259A50A026CB316426CBF1544140F000000040F02000000025DAF0A04FF070600000004FF0802000000440F020000002F2F2F2F2F2F2F','1234','-');
INSERT INTO `TELEGRAMS` VALUES (7,'2017-03-13 22:35','0000','2A44016A4493671201027244936712','016A0102000000208610830076238501000086208300973192000000','1234','-');
INSERT INTO `TELEGRAMS` VALUES (8,'2017-03-13 22:35','0000','2A44016A4742750101027247427501','016A01020000002086108300B80B0000000086208300F82A00000000','9658','-');
INSERT INTO `TELEGRAMS` VALUES (9,'2017-03-13 22:35','2e00','2a44016a4742750101027247427501','016a01021b00002086108300b80b0000000086208300f82a00000000','8cd4','-');
INSERT INTO `TELEGRAMS` VALUES (10,'2017-03-13 22:35','3200','2E44B05C11000000021B7A92080000','2F2F0A6667020AFB1A560402FD971D01002F2F2F2F2F2F2F2F2F2F2F2F2F2F2F','1234','-');
INSERT INTO `TELEGRAMS` VALUES (11,'2017-03-13 22:35','3200','2e44b05c10000000021b7a66080000','2f2f0a6690010afb1a090302fd971d01002f2f2f2f2f2f2f2f2f2f2f2f2f2f2f','8769','-');
INSERT INTO `TELEGRAMS` VALUES (12,'2017-03-13 22:35','0000','5E442D2C9643636013047AD2100000','2F2F0422BA11000004140F000000043B0000000002FD1700100259A50A026CB316426CBF1544140F000000040F02000000025DAF0A04FF070600000004FF0802000000440F020000002F2F2F2F2F2F2F','1234','-');
INSERT INTO `TELEGRAMS` VALUES (13,'2017-03-13 22:35','0000','2A44016A4493671201027244936712','016A0102000000208610830076238501000086208300973192000000','1234','-');
INSERT INTO `TELEGRAMS` VALUES (14,'2017-03-13 22:35','0000','2A44016A4742750101027247427501','016A01020000002086108300B80B0000000086208300F82A00000000','9658','-');
INSERT INTO `TELEGRAMS` VALUES (15,'2017-03-13 22:35','2e00','2a44016a4742750101027247427501','016a01021b00002086108300b80b0000000086208300f82a00000000','8cd4','-');
INSERT INTO `TELEGRAMS` VALUES (16,'2017-03-13 22:35','3200','2E44B05C11000000021B7A92080000','2F2F0A6667020AFB1A560402FD971D01002F2F2F2F2F2F2F2F2F2F2F2F2F2F2F','1234','-');
INSERT INTO `TELEGRAMS` VALUES (17,'2017-03-13 22:35','3200','2e44b05c10000000021b7a66080000','2f2f0a6690010afb1a090302fd971d01002f2f2f2f2f2f2f2f2f2f2f2f2f2f2f','8769','-');
INSERT INTO `TELEGRAMS` VALUES (18,'2017-03-13 22:35','0000','5E442D2C9643636013047AD2100000','2F2F0422BA11000004140F000000043B0000000002FD1700100259A50A026CB316426CBF1544140F000000040F02000000025DAF0A04FF070600000004FF0802000000440F020000002F2F2F2F2F2F2F','1234','-');
INSERT INTO `TELEGRAMS` VALUES (19,'2017-03-13 22:35','0000','2A44016A4493671201027244936712','016A0102000000208610830076238501000086208300973192000000','1234','-');
INSERT INTO `TELEGRAMS` VALUES (20,'2017-03-13 22:35','0000','2A44016A4742750101027247427501','016A01020000002086108300B80B0000000086208300F82A00000000','9658','-');
INSERT INTO `TELEGRAMS` VALUES (21,'2017-03-13 22:35','2e00','2a44016a4742750101027247427501','016a01021b00002086108300b80b0000000086208300f82a00000000','8cd4','-');
INSERT INTO `TELEGRAMS` VALUES (22,'2017-03-13 22:35','3200','2E44B05C11000000021B7A92080000','2F2F0A6667020AFB1A560402FD971D01002F2F2F2F2F2F2F2F2F2F2F2F2F2F2F','1234','-');
INSERT INTO `TELEGRAMS` VALUES (23,'2017-03-13 22:35','3200','2e44b05c10000000021b7a66080000','2f2f0a6690010afb1a090302fd971d01002f2f2f2f2f2f2f2f2f2f2f2f2f2f2f','8769','-');
INSERT INTO `TELEGRAMS` VALUES (24,'2017-03-13 22:35','0000','5E442D2C9643636013047AD2100000','2F2F0422BA11000004140F000000043B0000000002FD1700100259A50A026CB316426CBF1544140F000000040F02000000025DAF0A04FF070600000004FF0802000000440F020000002F2F2F2F2F2F2F','1234','-');
INSERT INTO `TELEGRAMS` VALUES (25,'2017-03-13 22:35','0000','2A44016A4493671201027244936712','016A0102000000208610830076238501000086208300973192000000','1234','-');
INSERT INTO `TELEGRAMS` VALUES (26,'2017-03-13 22:35','0000','2A44016A4742750101027247427501','016A01020000002086108300B80B0000000086208300F82A00000000','9658','-');
INSERT INTO `TELEGRAMS` VALUES (27,'2017-03-13 22:35','2e00','2a44016a4742750101027247427501','016a01021b00002086108300b80b0000000086208300f82a00000000','8cd4','-');
INSERT INTO `TELEGRAMS` VALUES (28,'2017-03-13 22:35','3200','2E44B05C11000000021B7A92080000','2F2F0A6667020AFB1A560402FD971D01002F2F2F2F2F2F2F2F2F2F2F2F2F2F2F','1234','-');
INSERT INTO `TELEGRAMS` VALUES (29,'2017-03-13 22:35','3200','2e44b05c10000000021b7a66080000','2f2f0a6690010afb1a090302fd971d01002f2f2f2f2f2f2f2f2f2f2f2f2f2f2f','8769','-');
INSERT INTO `TELEGRAMS` VALUES (30,'2017-03-13 22:35','0000','5E442D2C9643636013047AD2100000','2F2F0422BA11000004140F000000043B0000000002FD1700100259A50A026CB316426CBF1544140F000000040F02000000025DAF0A04FF070600000004FF0802000000440F020000002F2F2F2F2F2F2F','1234','-');
CREATE TABLE "MEASURES" (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`DATETIME`	TEXT,
	`DEVICE`	TEXT,
	`RSSI`	INTEGER,
	`TYPE1`	TEXT,
	`VALUE1`	INTEGER,
	`TYPE2`	TEXT,
	`VALUE2`	INTEGER
);
INSERT INTO `MEASURES` VALUES (1,'2017-03-13 22:35','016A449367120102',-121,'Wh',44,'Wh',9731920000);
INSERT INTO `MEASURES` VALUES (2,'2017-03-13 22:35','016A474275010102',-55,'Wh','B80B00000000','Wh','F82A000000');
INSERT INTO `MEASURES` VALUES (3,'2017-03-13 22:35','016A474275010102',-60,'Wh','b80b00000000','Wh','f82a000000');
INSERT INTO `MEASURES` VALUES (4,'2017-03-13 22:35','B05C11000000021B',-121,'°C',26.7,'%',45.6);
INSERT INTO `MEASURES` VALUES (5,'2017-03-13 22:35','B05C10000000021B',-62.5,'°C',22.1,'%',30.9);
INSERT INTO `MEASURES` VALUES (6,'2017-03-13 22:35','016A449367120102',-125,'Wh',34,'Wh',9731920000);
INSERT INTO `MEASURES` VALUES (7,'2017-03-13 22:35','016A474275010102',-55,'Wh','B80B00000000','Wh','F82A000000');
INSERT INTO `MEASURES` VALUES (8,'2017-03-13 22:35','016A474275010102',-60,'Wh','b80b00000000','Wh','f82a000000');
INSERT INTO `MEASURES` VALUES (9,'2017-03-13 22:35','B05C11000000021B',-121,'°C',26.7,'%',45.6);
INSERT INTO `MEASURES` VALUES (10,'2017-03-13 22:35','B05C10000000021B',-62.5,'°C',20.1,'%',30.9);
INSERT INTO `MEASURES` VALUES (11,'2017-03-13 22:35','016A449367120102',-122,'Wh',23,'Wh',9731920000);
INSERT INTO `MEASURES` VALUES (12,'2017-03-13 22:35','016A474275010102',-55,'Wh','B80B00000000','Wh','F82A000000');
INSERT INTO `MEASURES` VALUES (13,'2017-03-13 22:35','016A474275010102',-60,'Wh','b80b00000000','Wh','f82a000000');
INSERT INTO `MEASURES` VALUES (14,'2017-03-13 22:35','B05C11000000021B',-121,'°C',26.7,'%',45.6);
INSERT INTO `MEASURES` VALUES (15,'2017-03-13 22:35','B05C10000000021B',-62.5,'°C',19.2,'%',30.9);
INSERT INTO `MEASURES` VALUES (16,'2017-03-13 22:35','016A449367120102',-110,'Wh',44,'Wh',9731920000);
INSERT INTO `MEASURES` VALUES (17,'2017-03-13 22:35','016A474275010102',-55,'Wh','B80B00000000','Wh','F82A000000');
INSERT INTO `MEASURES` VALUES (18,'2017-03-13 22:35','016A474275010102',-60,'Wh','b80b00000000','Wh','f82a000000');
INSERT INTO `MEASURES` VALUES (19,'2017-03-13 22:35','B05C11000000021B',-121,'°C',26.7,'%',45.6);
INSERT INTO `MEASURES` VALUES (20,'2017-03-13 22:35','B05C10000000021B',-62.5,'°C',19.2,'%',30.9);
INSERT INTO `MEASURES` VALUES (21,'2017-03-13 22:35','016A449367120102',-88,'Wh',23,'Wh',9731920000);
INSERT INTO `MEASURES` VALUES (22,'2017-03-13 22:35','016A474275010102',-55,'Wh','B80B00000000','Wh','F82A000000');
INSERT INTO `MEASURES` VALUES (23,'2017-03-13 22:35','016A474275010102',-60,'Wh','b80b00000000','Wh','f82a000000');
INSERT INTO `MEASURES` VALUES (24,'2017-03-13 22:35','B05C11000000021B',-121,'°C',26.7,'%',45.6);
INSERT INTO `MEASURES` VALUES (25,'2017-03-13 22:35','B05C10000000021B',-62.5,'°C',19.1,'%',30.9);
INSERT INTO `MEASURES` VALUES (26,'2017-03-13 22:35','B05C10000000021B',-67.9,'°C',22.3,'%',22.1);
INSERT INTO `MEASURES` VALUES (27,'2017-03-13 22:35','B05C10000000021B',-67.9,'°C',22.3,'%',22.1);
INSERT INTO `MEASURES` VALUES (28,'2017-03-13 22:35','B05C10000000021B',-67.9,'°C',27.1,'%',22.1);
INSERT INTO `MEASURES` VALUES (29,'2017-03-13 22:35','B05C10000000021B',-67.9,'°C',18.3,'%',22.1);
INSERT INTO `MEASURES` VALUES (30,'2017-03-13 22:35','B05C10000000021B',-67.9,'°C',17.3,'%',22.1);
INSERT INTO `MEASURES` VALUES (31,'2017-03-13 22:35','B05C10000000021B',-67.9,'°C',16.1,'%',18.7);
INSERT INTO `MEASURES` VALUES (32,'2017-03-13 22:35','B05C10000000021B',-67.9,'°C',-1.1,'%',11.6);
INSERT INTO `MEASURES` VALUES (33,'2017-03-13 22:35','B05C10000000021B',-112,'°C',0,'%',17.8);
INSERT INTO `MEASURES` VALUES (34,'2017-03-13 22:35','B05C10000000021B',-123,'°C',2,'%',20);
CREATE TABLE `ERRORS` (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`DATETIME`	INTEGER,
	`TYPE`	TEXT,
	`ERROR`	TEXT
);
CREATE TABLE "DEVICES" (
	`ID`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`DEVICE_INFO`	TEXT,
	`DEVICE_ADDRESS`	TEXT UNIQUE,
	`DEVICE_AES`	TEXT
);
INSERT INTO `DEVICES` VALUES (1,'Weptech OMSF-868A (teplota a vlhkost)','B05C10000000021B','000102030405060708090A0B0C0D0E0F');
INSERT INTO `DEVICES` VALUES (3,'Bonega SA-E/15 (studená voda)','EE09210100000106','2B7E151628AED2A6ABF7158809CF4F3C');
INSERT INTO `DEVICES` VALUES (5,'Bonega TA-E/15 (teplá voda)','EE09210100000107','2B7E151628AED2A6ABF7158809CF4F3C');
INSERT INTO `DEVICES` VALUES (6,'Kamstrup Multical 402 (elektroměr)','2D2C964363601304','D8F378729241F6883DA548881A5524F6');
INSERT INTO `DEVICES` VALUES (7,'ZPA ZE.310 (elektroměr)','016A449367120102','');
COMMIT;
