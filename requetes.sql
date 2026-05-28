-- R1. Liste de tous les pilotes triés par ordre alphabétique
-- Utilisation de la clause ORDER BY sur deux niveaux (nom puis prénom). 
-- Le mot-clé ASC garantit un tri croissant (de A à Z).
SELECT * FROM Pilote ORDER BY nom ASC, prenom ASC;

-- R2. Avions ayant une capacité strictement supérieure à 200 sièges
-- Filtrage simple avec la clause WHERE pour exclure les lignes 
-- qui ne respectent pas la condition mathématique (>).
SELECT immatriculation, capacite FROM Avion WHERE capacite > 200;

-- R3. Tous les vols partant de l'aéroport ID 1 (CDG - Paris)
-- Projection sur des colonnes spécifiques (numero_vol, date_heure_depart) 
-- et restriction (WHERE) basée directement sur une clé étrangère (id_aeroport_depart).
SELECT numero_vol, date_heure_depart FROM Vol WHERE id_aeroport_depart = 1;

-- R4. Informations combinées des avions et de leur modèle (INNER JOIN)
-- Jointure interne (INNER JOIN) pour fusionner les données de deux tables. 
-- Ne ramène que les avions qui ont une correspondance stricte avec un modèle existant.
SELECT a.immatriculation, m.constructeur, m.nom_modele, m.moteur 
FROM Avion a 
INNER JOIN Modele m ON a.id_modele = m.id_modele;

-- R5. Tous les aéroports, y compris ceux qui n'ont reçu/envoyé aucun vol (LEFT JOIN)
-- Jointure externe gauche (LEFT JOIN) pour conserver absolument tous les 
-- aéroports de la table de gauche (Aeroport), même s'ils n'ont aucune correspondance 
-- dans la table Vol (ce qui renverra des valeurs NULL pour numero_vol).
SELECT ae.code_iata, ae.ville, v.numero_vol
FROM Aeroport ae 
LEFT JOIN Vol v ON ae.id_aeroport = v.id_aeroport_depart;

-- R6. Capacité totale de la flotte par nom de compagnie
-- Utilisation d'une fonction d'agrégation (SUM) combinée à un regroupement (GROUP BY). 
-- On calcule la somme des capacités pour chaque groupe (nom de la compagnie).
SELECT c.nom AS Compagnie, SUM(a.capacite) AS Capacite_Totale
FROM Compagnie c 
INNER JOIN Avion a ON c.id_compagnie = a.id_compagnie
GROUP BY c.nom;

-- R7. Nombre d'avions par modèle, trié par ordre décroissant
-- Regroupement (GROUP BY) avec la fonction d'agrégation COUNT(). 
-- Le LEFT JOIN garantit que les modèles sans avion afficheront un total de 0 au lieu de disparaître.
SELECT m.nom_modele, COUNT(a.id_avion) AS Nombre_Avions
FROM Modele m 
LEFT JOIN Avion a ON m.id_modele = a.id_modele
GROUP BY m.id_modele, m.nom_modele
ORDER BY Nombre_Avions DESC;

-- R8. Compagnies ayant plus de 2 avions dans leur flotte
-- Utilisation de la clause HAVING. Contrairement à WHERE qui filtre les lignes brutes, 
-- HAVING filtre les données *après* leur regroupement (ici, on ne garde que les groupes ayant un COUNT > 2).
SELECT c.nom, COUNT(a.id_avion) AS Nb_Avions
FROM Compagnie c 
JOIN Avion a ON c.id_compagnie = a.id_compagnie
GROUP BY c.id_compagnie, c.nom
HAVING COUNT(a.id_avion) > 2;

-- R9. Moyenne des salaires des pilotes par compagnie, uniquement si supérieure à 6000
-- Calcul de moyenne avec AVG() et filtrage post-agrégation avec HAVING 
-- pour exclure les compagnies dont la moyenne salariale est trop basse.
SELECT id_compagnie, AVG(salaire) AS Salaire_Moyen
FROM Pilote
GROUP BY id_compagnie
HAVING AVG(salaire) > 6000;

-- R10. La capacité maximale pour chaque modèle d'avion
-- Extraction d'une valeur extrême via la fonction d'agrégation MAX(), 
-- appliquée sur des sous-ensembles créés par la clause GROUP BY (par modèle).
SELECT id_modele, MAX(capacite) AS Capacite_Max
FROM Avion
GROUP BY id_modele;

-- R11. Pilotes gagnant plus que la moyenne globale (Sous-requête scalaire)
-- Utilisation d'une sous-requête dans le WHERE. La sous-requête calcule 
-- dynamiquement la moyenne globale (valeur unique / scalaire) pour servir de seuil de comparaison.
SELECT nom, prenom, salaire 
FROM Pilote 
WHERE salaire > (SELECT AVG(salaire) FROM Pilote);

-- R12. Compagnies dont tous les avions ont une capacité > 150 (NOT EXISTS)
-- Traduction d'une contrainte universelle ("POUR TOUT avion, capacité > 150") 
-- par une double négation avec NOT EXISTS ("IL N'EXISTE PAS d'avion avec capacité <= 150"). 
-- Le second EXISTS s'assure que la compagnie possède bien au moins un avion.
SELECT c.nom 
FROM Compagnie c 
WHERE NOT EXISTS (
    SELECT 1 FROM Avion a WHERE a.id_compagnie = c.id_compagnie AND a.capacite <= 150
) AND EXISTS (
    SELECT 1 FROM Avion a WHERE a.id_compagnie = c.id_compagnie
);

-- R13. Classement des pilotes par salaire décroissant, puis par date d'embauche
-- Tri multi-critères avec ORDER BY. On trie d'abord par le salaire du plus grand 
-- au plus petit (DESC). En cas d'égalité de salaire, on départage par l'ancienneté (ASC).
SELECT nom, prenom, salaire, date_embauche 
FROM Pilote 
ORDER BY salaire DESC, date_embauche ASC;

-- R14. Pilotes ayant volé avec au moins 2 rôles différents (Sous-requête avec COUNT DISTINCT)
-- Sous-requête listant les ID avec la clause IN. Le COUNT(DISTINCT role) 
-- garantit qu'on compte bien les rôles uniques (ex: Commandant ET Copilote) et non le nombre total de vols.
SELECT p.nom, p.prenom 
FROM Pilote p
WHERE p.id_pilote IN (
    SELECT id_pilote FROM Affectation GROUP BY id_pilote HAVING COUNT(DISTINCT role) >= 2
);

-- R15. L'avion ayant la plus grande capacité par compagnie (Corrélation)
-- Sous-requête corrélée dans le WHERE. La sous-requête calcule le MAX() 
-- en faisant référence (a2.id_compagnie = a.id_compagnie) à la ligne actuellement évaluée par la requête principale.
SELECT a.id_compagnie, a.immatriculation, a.capacite
FROM Avion a
WHERE a.capacite = (
    SELECT MAX(a2.capacite) 
    FROM Avion a2 
    WHERE a2.id_compagnie = a.id_compagnie
);