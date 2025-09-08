PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE categories (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
INSERT INTO categories VALUES(1,'piscinas');
INSERT INTO categories VALUES(2,'limpieza');
INSERT INTO categories VALUES(3,'pintura');
INSERT INTO categories VALUES(4,'fontanería');
INSERT INTO categories VALUES(5,'decoración');
INSERT INTO categories VALUES(6,'cocina');
INSERT INTO categories VALUES(7,'carpintería');
INSERT INTO categories VALUES(8,'jardinería');
INSERT INTO categories VALUES(9,'albañilería');
INSERT INTO categories VALUES(10,'cuidado infantil');
INSERT INTO categories VALUES(11,'cuidado de mayores');
CREATE TABLE user (
	id INTEGER NOT NULL, 
	name VARCHAR(80) NOT NULL, 
	email VARCHAR(120), 
	phone VARCHAR(20), 
	password VARCHAR(255) NOT NULL, 
	role VARCHAR(20) NOT NULL, 
	photo_url VARCHAR(255), 
	is_active BOOLEAN NOT NULL, last_name VARCHAR(80), average_rating FLOAT, total_reviews INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (email), 
	UNIQUE (phone)
);
INSERT INTO user VALUES(2,'Judith','judith@email.com','+34639528417','password','proveedor',NULL,1,'Ramírez Pachón',4.90000000000000035,6);
INSERT INTO user VALUES(5,'Maria','mduarte@email.com','+34612345789','password','proveedor',NULL,1,'Fernanda Duarte',3.79999999999999982,2);
INSERT INTO user VALUES(6,'Carlos','carloren@email.com','+34676310141','scrypt:32768:8:1$KaWM8axizKoQpb6N$615399d7fe84f35b6d11cb98024958766371661479477a2b9f72054ff119827d87af351f50f9eb058f530f8c59c8b92fc06518bd9feaa64d5b8bc0a320893d6f','cliente','https://lh3.googleusercontent.com/a/ACg8ocINLEe6QWDfxFDhXabGGf-SKVl7bAbUz7uWy69Ac7u18l6EtBK4=s288-c-no',1,'Lorenzo Moreno',3.5,6);
INSERT INTO user VALUES(7,'Eduardo','eduardo@email.com','+5760123456789','scrypt:32768:8:1$pphPK80UO5z0ru5V$e1edd2f9b27a9aad5a9e82b42916a03dd3e20dbd6a6ff0ada69a059756c113f06fc0ecf2a74f04223aec40ad978a71e9244f90b32cc3f655addb68dd04b80c38','proveedor',NULL,1,'García Valverde',4.20000000000000017,4);
INSERT INTO user VALUES(8,'Daniela','euladaniela@email.com','693582471','scrypt:32768:8:1$4rhzNCjkHgudTsUV$66752cafdba2aaa70facd5a915c692591174e3d5517de29d937e32d7c4f1168842612d73578b4ec1ef23f5a13bbdbabd6951a4a21a232d65b02b93297618227e','proveedor','https://i.etsystatic.com/31548528/r/il/ffde13/5804742914/il_300x300.5804742914_ap2d.jpg',1,'Eula',4.70000000000000017,3);
INSERT INTO user VALUES(9,'AAAA','asfsd@email.com','60123456789','scrypt:32768:8:1$X1u1pf4sI9OAxxZ7$809e1f20e480485dbbae9846d2c5d7aafb404941217a4d99e80df36bae22f1cce8e66f2e021f06553a19ee5c9b8308b7cfe7a72ac388c07afa25bfacd73285d6','proveedor','',1,'BBB CCC',0.0,0);
INSERT INTO user VALUES(10,'Eduardo','edu@gmail.com','666666666','scrypt:32768:8:1$p7NVh5PGDGnMTZdQ$dc6be00b8ded93b2ce4b2e9a621682a71c15dba9657105eb4b90dcbe06314117cba99138b60aac56f9a206300da739c9dfd01914d7721e164bc124d1f202e29e','cliente','',1,'GV',0.0,0);
INSERT INTO user VALUES(11,'Carlos ','carlos@gmail.com','777777777','scrypt:32768:8:1$vuGTb2pYifEdmA2m$ecb6c54d2e58f78e9990ddceb6b0e1386036b1cca37e0bf039834678c0feb385fb43d770259918f59f5ce636ce1c56c3503b3b467466aebd4b5b436d2e7e7ed1','cliente','',1,'Lorenzo ',0.0,0);
INSERT INTO user VALUES(12,'Daniela','daniela@gmail.com','888888888','scrypt:32768:8:1$T4RAkKBOK1KxDew6$6aeabeb78ea5abe49b0d5a25c8e441f9b07fcf56ab73511e8cbf56dd1f0656df62402f1d11fdffd1f794adafe8538f58c41ae57382b35d85acb630fea97a61f9','proveedor','',1,'Eula',0.0,0);
CREATE TABLE services (
	id INTEGER NOT NULL, 
	title VARCHAR(150) NOT NULL, 
	description TEXT NOT NULL, 
	price FLOAT NOT NULL, 
	provider_id INTEGER NOT NULL, 
	category_id INTEGER NOT NULL, photo_url VARCHAR(255), 
	PRIMARY KEY (id), 
	FOREIGN KEY(category_id) REFERENCES categories (id), 
	FOREIGN KEY(provider_id) REFERENCES user (id)
);
INSERT INTO services VALUES(1,'Te arreglo la ducha','Experta en mantenimiento y reparación de bañeras, placas de ducha, mamparas y grifería',45000.0,2,4,NULL);
INSERT INTO services VALUES(2,'Pinta tu casa','15 años de experiencia pintando todo tipo de paredes para que vuelvas a sentir tu hogar limpio, nuevo y acogedor',70000.0,7,3,NULL);
INSERT INTO services VALUES(3,'Tu piscina siempre a punto','Mantén tu piscina siempre en óptimas condiciones. Mantenimiento de depuradora, limpiado y calibrado del ph del agua, reparación de fugas y mucho más',90000.0,8,1,NULL);
INSERT INTO services VALUES(4,'Niñera','Tus peques son la parte más importante de tu vida, por eso me comprometo a cuidar de ellos y mantenerlos a salvo, bien alimentados y ¡sobre todo felices!',40000.0,5,10,NULL);
INSERT INTO services VALUES(5,'Limpieza profunda','Tu hogar más limpio que nunca. Puedo ir a hacer limpieza general semanalmente o a realizar una limpieza en profundidad. ¡Contáctame!',42500.0,8,2,NULL);
INSERT INTO services VALUES(6,'Cocino por ti','¿Tienes poco tiempo para cocinar o necesitas ayuda para algún evento? ¡No te preocupes! Relájate y disfruta de un gran festín en tu propia casa',65300.0,2,6,NULL);
INSERT INTO services VALUES(7,'Carpintería Dani','Todo tipo de trabajo con madera: restauraciones, muebles personalizados, parqués...',80000.0,8,7,NULL);
INSERT INTO services VALUES(8,'Tus mayores en buenas manos','¡Hola! Soy María. Sé que no hay nadie para cuidar a tus seres queridos mejor que uno mismo, pero no siempre se puede. ¡Yo intentaré hacerlo igual de bien!',37800.0,5,11,NULL);
CREATE TABLE contracts (
	id INTEGER NOT NULL, 
	start_date DATETIME NOT NULL, 
	status VARCHAR(50) NOT NULL, 
	client_id INTEGER NOT NULL, 
	provider_id INTEGER NOT NULL, 
	service_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(client_id) REFERENCES user (id), 
	FOREIGN KEY(provider_id) REFERENCES user (id), 
	FOREIGN KEY(service_id) REFERENCES services (id)
);
INSERT INTO contracts VALUES(1,'2025-09-05 04:32:53.000000','completado',6,8,3);
INSERT INTO contracts VALUES(2,'2025-09-05 04:33:25.000000','cancelado',6,8,5);
INSERT INTO contracts VALUES(3,'2025-09-05 04:33:38.000000','completado',6,8,3);
INSERT INTO contracts VALUES(4,'2025-09-05 04:36:45.000000','completado',6,8,7);
INSERT INTO contracts VALUES(5,'2025-09-05 08:06:24.785910','esperando confirmación',8,2,1);
INSERT INTO contracts VALUES(6,'2025-09-05 11:42:13.092269','esperando confirmación',6,2,1);
CREATE TABLE reviews (
	id INTEGER NOT NULL, 
	rating INTEGER NOT NULL, 
	comment TEXT, 
	created_at DATETIME NOT NULL, 
	contract_id INTEGER NOT NULL, 
	author_id INTEGER NOT NULL, 
	recipient_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(author_id) REFERENCES user (id), 
	FOREIGN KEY(contract_id) REFERENCES contracts (id), 
	FOREIGN KEY(recipient_id) REFERENCES user (id)
);
INSERT INTO reviews VALUES(1,5,'Un fantástico servicio','2025-09-05 04:36:01.000000',3,6,8);
INSERT INTO reviews VALUES(2,3,'Hizo un trabajo excelente con la puerta, pero al barniz se le notan algunos goterones','2025-09-05 04:37:30.000000',4,6,8);
INSERT INTO reviews VALUES(3,3,'afwfverqve','2025-09-05 11:42:57.191468',1,8,6);
COMMIT;
