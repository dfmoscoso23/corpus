CREATE DATABASE corpus;

CREATE TABLE tipo_documento (
	id serial, 
	tipo varchar(35),
	PRIMARY KEY (tipo)
);

CREATE TABLE fuente (
	id serial, 
	fuente varchar(35),
	link varchar(200),
	referencia varchar(150),
	PRIMARY KEY (id)
);
CREATE TABLE zonas (
	id serial, 
	zona varchar(35),
	PRIMARY KEY (zona)
);
CREATE TABLE subzonas (
	id serial, 
	zona varchar(35) references zonas(zona),
	subzona varchar(35),
	PRIMARY KEY (subzona)
);
CREATE TABLE temas (
	id serial, 
	tema varchar(35),
	PRIMARY KEY (tema)
);

CREATE TABLE documentos(
	id serial,
	titulo varchar(150),
	tipo_documento varchar(35) references tipo_documento(tipo),
	fuente int references fuente(id),
	fecha_incorporacion date, 
	fecha_publicacion date,
	zona varchar(35) references zonas(zona),
	subzona varchar(35) references subzonas(subzona),
	tema varchar(35) references temas(tema),
	parrafos int,
	extension int,
	documento varchar(25000),
	PRIMARY KEY(id)

);
CREATE TABLE lemas (
	id serial, 
	lema varchar(30),
	PRIMARY KEY (lema)
);
CREATE TABLE clases_de_palabras (
	id serial, 
	clase varchar(30),
	determinante_1 varchar(30),
	determinante_2 varchar(30),
	determinante_3 varchar(30),
	PRIMARY KEY (clase)
);
CREATE TABLE determinante_1 (
	id serial, 
	determinante varchar(45),
	tipo varchar(30),
	PRIMARY KEY (determinante)
);
CREATE TABLE determinante_2 (
	id serial, 
	determinante varchar(45),
	tipo varchar(30),
	PRIMARY KEY (determinante)
);
CREATE TABLE determinante_3 (
	id serial, 
	determinante varchar(45),
	tipo varchar(30),
	PRIMARY KEY (determinante)
);

CREATE TABLE casos (
	id serial,
	documento int references documentos(id),
	caso varchar(35),
	lema varchar(30) references lemas(lema),
	mayuscula boolean,
	posicion int,
	lema_anterior varchar(30) references lemas(lema),
	lema_posterior varchar(30) references lemas(lema),
	desinencia varchar(5),
	prefijos varchar(5),
	clase_de_palabra varchar(30) references clases_de_palabras(clase),
	determinante_1 varchar(45) references determinante_1(determinante),
	determinante_2 varchar(45) references determinante_2(determinante),
	determinante_3 varchar(45) references determinante_3(determinante)

);