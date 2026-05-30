CREATE DATABASE IF NOT EXISTS AeroDB;
USE AeroDB;

DROP VIEW IF EXISTS Vue_Details_Vols;
DROP TABLE IF EXISTS Affectation;
DROP TABLE IF EXISTS Vol;
DROP TABLE IF EXISTS Pilote;
DROP TABLE IF EXISTS Avion;
DROP TABLE IF EXISTS Modele;
DROP TABLE IF EXISTS Aeroport;
DROP TABLE IF EXISTS Compagnie;
CREATE TABLE Compagnie (
    id_compagnie INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL UNIQUE,
    pays_origine VARCHAR(100) NOT NULL
);

CREATE TABLE Aeroport (
    id_aeroport INT AUTO_INCREMENT PRIMARY KEY,
    code_iata VARCHAR(3) NOT NULL UNIQUE,
    ville VARCHAR(100) NOT NULL,
    pays VARCHAR(100) NOT NULL
);

CREATE TABLE Modele (
    id_modele INT AUTO_INCREMENT PRIMARY KEY,
    constructeur VARCHAR(50) NOT NULL,
    nom_modele VARCHAR(50) NOT NULL,
    moteur VARCHAR(100) NOT NULL
);

CREATE TABLE Avion (
    id_avion INT AUTO_INCREMENT PRIMARY KEY,
    immatriculation VARCHAR(10) NOT NULL UNIQUE,
    capacite INT CHECK (capacite > 0),
    id_compagnie INT NOT NULL,
    id_modele INT NOT NULL,
    FOREIGN KEY (id_compagnie) REFERENCES Compagnie(id_compagnie) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_modele) REFERENCES Modele(id_modele) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE Pilote (
    id_pilote INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    salaire DECIMAL(10,2) CHECK (salaire > 0),
    date_embauche DATE NOT NULL,
    id_compagnie INT NOT NULL,
    FOREIGN KEY (id_compagnie) REFERENCES Compagnie(id_compagnie) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Vol (
    id_vol INT AUTO_INCREMENT PRIMARY KEY,
    numero_vol VARCHAR(10) NOT NULL,
    date_heure_depart DATETIME NOT NULL,
    date_heure_arrivee DATETIME NOT NULL,
    id_avion INT NOT NULL,
    id_aeroport_depart INT NOT NULL,
    id_aeroport_arrivee INT NOT NULL,
    FOREIGN KEY (id_avion) REFERENCES Avion(id_avion) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_aeroport_depart) REFERENCES Aeroport(id_aeroport) ON DELETE RESTRICT ON UPDATE RESTRICT,
    FOREIGN KEY (id_aeroport_arrivee) REFERENCES Aeroport(id_aeroport) ON DELETE RESTRICT ON UPDATE RESTRICT,
    CHECK (id_aeroport_depart != id_aeroport_arrivee)
);

CREATE TABLE Affectation (
    id_vol INT NOT NULL,
    id_pilote INT NOT NULL,
    role VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_vol, id_pilote),
    FOREIGN KEY (id_vol) REFERENCES Vol(id_vol) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_pilote) REFERENCES Pilote(id_pilote) ON DELETE CASCADE ON UPDATE CASCADE
);

-- Vue pour simplifier les requêtes de l'interface Python
CREATE VIEW Vue_Details_Vols AS
SELECT 
    p.id_pilote, p.nom, p.prenom, 
    v.numero_vol, v.date_heure_depart, v.date_heure_arrivee,
    a.role, 
    dep.code_iata AS depart_iata, 
    arr.code_iata AS arrivee_iata
FROM Pilote p
JOIN Affectation a ON p.id_pilote = a.id_pilote
JOIN Vol v ON a.id_vol = v.id_vol
JOIN Aeroport dep ON v.id_aeroport_depart = dep.id_aeroport
JOIN Aeroport arr ON v.id_aeroport_arrivee = arr.id_aeroport;




INSERT INTO Compagnie (nom, pays_origine) VALUES 
('Air France', 'France'), 
('Lufthansa', 'Allemagne'), 
('Emirates', 'EAU'),
('Delta Airlines', 'USA'),
('Qatar Airways', 'Qatar'),
('All Nippon Airways', 'Japon');

INSERT INTO Aeroport (code_iata, ville, pays) VALUES 
('CDG', 'Paris', 'France'), 
('FRA', 'Francfort', 'Allemagne'), 
('DXB', 'Dubai', 'EAU'), 
('JFK', 'New York', 'USA'),
('LHR', 'Londres', 'Royaume-Uni'),
('HND', 'Tokyo', 'Japon'),
('LAX', 'Los Angeles', 'USA'),
('DOH', 'Doha', 'Qatar'),
('ATL', 'Atlanta', 'USA');

INSERT INTO Modele (constructeur, nom_modele, moteur) VALUES 
('Airbus', 'A320', 'CFM56'), 
('Airbus', 'A350', 'Rolls-Royce Trent XWB'), 
('Boeing', '737', 'CFM LEAP-1B'), 
('Boeing', '777', 'General Electric GE90'),
('Airbus', 'A380', 'Rolls-Royce Trent 900'),
('Airbus', 'A330', 'Rolls-Royce Trent 700'),
('Boeing', '787', 'General Electric GEnx'),
('Boeing', '747', 'General Electric GEnx-2B67');

INSERT INTO Avion (immatriculation, capacite, id_compagnie, id_modele) VALUES 
('F-GZNA', 180, 1, 1), 
('F-HTYA', 324, 1, 2),
('F-HRBA', 290, 1, 6),
('F-GZNB', 174, 1, 1),
('D-AIPA', 160, 2, 1), 
('D-ABYA', 364, 2, 4),
('D-ABYC', 371, 2, 8),
('A6-EGA', 354, 3, 4),
('A6-EUA', 515, 3, 5),
('A6-EUB', 515, 3, 5),
('N-101DL', 160, 4, 3),
('N-202DL', 288, 4, 4),
('N-303DL', 160, 4, 3),
('A7-ALA', 283, 5, 2),
('A7-BCA', 254, 5, 7),
('JA-801A', 246, 6, 7),
('JA-802A', 246, 6, 7);

INSERT INTO Pilote (nom, prenom, salaire, date_embauche, id_compagnie) VALUES 
('Dupont', 'Jean', 6500.00, '2015-06-01', 1), 
('Martin', 'Alice', 4200.00, '2020-03-15', 1),
('Bernard', 'Luc', 7200.00, '2010-09-01', 1),
('Petit', 'Sophie', 4000.00, '2021-11-20', 1),
('Muller', 'Thomas', 7000.00, '2012-11-01', 2), 
('Schmidt', 'Hans', 4500.00, '2019-08-20', 2),
('Weber', 'Klaus', 8100.00, '2008-04-12', 2),
('Al Maktoum', 'Omar', 8000.00, '2010-02-10', 3),
('Hassan', 'Zayed', 8200.00, '2011-05-15', 3),
('Rashid', 'Fatima', 5500.00, '2018-01-25', 3),
('Smith', 'John', 6800.00, '2014-07-11', 4),
('Johnson', 'Emily', 4300.00, '2022-02-01', 4),
('Williams', 'Michael', 7500.00, '2011-10-30', 4),
('Al Thani', 'Tariq', 7900.00, '2013-06-18', 5),
('Farooq', 'Aisha', 5100.00, '2019-09-10', 5),
('Tanaka', 'Kenji', 6700.00, '2016-03-05', 6),
('Suzuki', 'Yumi', 4600.00, '2020-08-14', 6);

INSERT INTO Vol (numero_vol, date_heure_depart, date_heure_arrivee, id_avion, id_aeroport_depart, id_aeroport_arrivee) VALUES 
('AF123', '2026-06-01 08:00:00', '2026-06-01 10:30:00', 1, 1, 2),
('AF456', '2026-06-02 14:00:00', '2026-06-02 16:30:00', 2, 1, 4),
('AF789', '2026-06-05 23:00:00', '2026-06-06 06:00:00', 3, 1, 5),
('LH789', '2026-06-03 09:00:00', '2026-06-03 11:30:00', 5, 2, 1),
('LH101', '2026-06-06 13:00:00', '2026-06-06 16:45:00', 7, 2, 4),
('EK001', '2026-06-04 07:00:00', '2026-06-04 15:00:00', 8, 3, 1),
('EK002', '2026-06-05 08:30:00', '2026-06-05 13:15:00', 9, 3, 5),
('DL404', '2026-06-07 10:00:00', '2026-06-07 13:00:00', 11, 4, 9),
('DL505', '2026-06-08 18:00:00', '2026-06-08 21:30:00', 12, 7, 4),
('QR101', '2026-06-09 06:00:00', '2026-06-09 14:00:00', 14, 8, 1),
('NH202', '2026-06-10 11:00:00', '2026-06-10 23:30:00', 16, 6, 4),
('NH203', '2026-06-11 09:00:00', '2026-06-11 20:00:00', 17, 6, 1);

INSERT INTO Affectation (id_vol, id_pilote, role) VALUES 
(1, 1, 'Commandant'), (1, 2, 'Copilote'),
(2, 3, 'Commandant'), (2, 4, 'Copilote'),
(3, 1, 'Commandant'), (3, 4, 'Copilote'),
(4, 5, 'Commandant'), (4, 6, 'Copilote'),
(5, 7, 'Commandant'), (5, 6, 'Copilote'),
(6, 8, 'Commandant'), (6, 10, 'Copilote'),
(7, 9, 'Commandant'), (7, 10, 'Copilote'),
(8, 11, 'Commandant'), (8, 12, 'Copilote'),
(9, 13, 'Commandant'), (9, 12, 'Copilote'),
(10, 14, 'Commandant'), (10, 15, 'Copilote'),
(11, 16, 'Commandant'), (11, 17, 'Copilote'),
(12, 16, 'Commandant'), (12, 17, 'Copilote');

