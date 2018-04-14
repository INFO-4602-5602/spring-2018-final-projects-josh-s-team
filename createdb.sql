/* Evan James
MySQL create database and tables for J Dilla visualization
*/

CREATE DATABASE IF NOT EXISTS dilla;
CREATE USER IF NOT EXISTS 'dillaUser' IDENTIFIED BY 'DillaPW123';
GRANT ALL PRIVILEGES on dilla.* TO 'dillaUser'@localhost;

USE dilla;

CREATE TABLE IF NOT EXISTS Artists (
	ID smallint unsigned NOT NULL AUTO_INCREMENT,
	Name char(255) NOT NULL,
	PRIMARY KEY(ID),
	UNIQUE(ID)
);

CREATE TABLE IF NOT EXISTS Songs (
	ID smallint unsigned NOT NULL AUTO_INCREMENT,
 	Title char(255) NOT NULL ,
	ReleaseYear smallint(4) unsigned,
	Artist smallint unsigned NOT NULL,
	Producer smallint unsigned,
	DillaBit tinyint(1) NOT NULL DEFAULT 1,
	PABit tinyint(1) NOT NULL DEFAULT 1,
	PRIMARY KEY (ID),
	UNIQUE(ID),
	FOREIGN KEY (Artist) REFERENCES Artists(ID),
	FOREIGN KEY (Producer) REFERENCES Artists(ID)
);

CREATE TABLE IF NOT EXISTS Rel (
	ID smallint unsigned NOT NULL AUTO_INCREMENT,
	Song smallint unsigned NOT NULL, 
	SampledIn smallint unsigned NOT NULL,
	Sampled smallint unsigned NOT NULL,
	PRIMARY KEY(ID),
	UNIQUE(ID),
	FOREIGN KEY (SampledIn) REFERENCES Songs(ID),
	FOREIGN KEY (Sampled) REFERENCES Songs(ID)
);

CREATE VIEW IF NOT EXISTS DillaSongs AS
	SELECT *
	FROM Songs
	WHERE DillaBit = 1;

