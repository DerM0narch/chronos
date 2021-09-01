
DROP DATABASE ChronosDB;

CREATE DATABASE ChronosDB;
USE chronosdb;

CREATE TABLE nutzer (
	
	id INT AUTO_INCREMENT,
	nname varchar(50),
	vname VARCHAR(50),
	nutzername VARCHAR(20),
	email VARCHAR(50),
	passwort VARCHAR(50),
	personalnr INT,
	kartennr VARCHAR(100),
	benutzerStatus VARCHAR(10) DEFAULT 'abwesend',
	PRIMARY KEY (id)
	
);

CREATE TABLE buchungen (
	buchung_id INT AUTO_INCREMENT,
	buchung_art VARCHAR(20),
	n_kartennr VARCHAR(100),
	uhrzeit DATETIME,
	PRIMARY KEY (buchung_id),
	FOREIGN KEY (n_kartennr) REFERENCES nutzer(kartennr)
	
)