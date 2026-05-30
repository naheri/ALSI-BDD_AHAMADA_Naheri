# ALSI-BDD_AHAMADA_Naheri
Gestion d'un système de gestion d'avions et de pilotes


Bienvenue dans le dépôt de mon projet de Base de Données (ALSI61). Ce projet modélise le système d'information d'une compagnie aérienne et inclut une simple interface graphique développée en Python (PyQt6) pour gérer les données.

---

## 1. Description du domaine

Le domaine choisi est la **gestion d'une flotte aérienne et des vols commerciaux**.
Ce système permet de gérer les compagnies, les avions, les modèles d'appareils, les pilotes, et la planification des vols. Il assure le suivi opérationnel : savoir quel avion effectue quel vol, entre quels aéroports, et quel est l'équipage affecté.

## 2. Règles métiers

Afin de modéliser ce système de manière cohérente, les règles métiers suivantes ont été définies :
1. Un avion appartient à une et une seule compagnie aérienne.
2. Un avion correspond à un seul modèle (ex: Airbus A320), mais plusieurs avions peuvent être du même modèle.
3. Un vol possède un aéroport de départ et un aéroport d'arrivée qui doivent obligatoirement être distincts.
4. Un vol est opéré par un seul et unique avion.
5. Un pilote est rattaché à une seule compagnie aérienne.
6. Un pilote peut être affecté à plusieurs vols. Pour chaque vol auquel il est affecté, il occupe un rôle spécifique (ex: "Commandant" ou "Copilote"). **Il s'agit d'une association porteuse d'attributs.**

## 3. Dictionnaire des données

| Table | Attribut | Type SQL | Contraintes | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Compagnie** | `id_compagnie` | INT | PK, AUTO_INCREMENT | Identifiant unique |
| **Compagnie** | `nom` | VARCHAR(100) | NOT NULL, UNIQUE | Nom de la compagnie |
| **Compagnie** | `pays_origine`| VARCHAR(100) | NOT NULL | Pays d'origine |
| **Aeroport** | `id_aeroport` | INT | PK, AUTO_INCREMENT | Identifiant unique |
| **Aeroport** | `code_iata` | VARCHAR(3) | NOT NULL, UNIQUE | Code IATA (ex: CDG) |
| **Aeroport** | `ville` | VARCHAR(100) | NOT NULL | Ville de l'aéroport |
| **Aeroport** | `pays` | VARCHAR(100) | NOT NULL | Pays de l'aéroport |
| **Modele** | `id_modele` | INT | PK, AUTO_INCREMENT | Identifiant unique |
| **Modele** | `constructeur` | VARCHAR(50) | NOT NULL | Nom du constructeur |
| **Modele** | `nom_modele` | VARCHAR(50) | NOT NULL | Nom de l'appareil (ex: A350) |
| **Modele** | `moteur` | VARCHAR(100) | NOT NULL | Motorisation |
| **Avion** | `id_avion` | INT | PK, AUTO_INCREMENT | Identifiant unique |
| **Avion** | `immatriculation` | VARCHAR(10) | NOT NULL, UNIQUE | Numéro d'immatriculation |
| **Avion** | `capacite` | INT | CHECK(capacite > 0) | Nombre de sièges passagers |
| **Pilote** | `id_pilote` | INT | PK, AUTO_INCREMENT | Identifiant unique |
| **Pilote** | `nom` | VARCHAR(100) | NOT NULL | Nom de famille |
| **Pilote** | `prenom` | VARCHAR(100) | NOT NULL | Prénom |
| **Pilote** | `salaire` | DECIMAL(10,2) | CHECK(salaire > 0) | Salaire mensuel (en €) |
| **Pilote** | `date_embauche` | DATE | NOT NULL | Date de début de contrat |
| **Vol** | `id_vol` | INT | PK, AUTO_INCREMENT | Identifiant unique |
| **Vol** | `numero_vol` | VARCHAR(10) | NOT NULL | Numéro de vol (ex: AF123) |
| **Vol** | `date_heure_depart` | DATETIME | NOT NULL | Heure de décollage |
| **Vol** | `date_heure_arrivee`| DATETIME | NOT NULL | Heure d'atterrissage |
| **Affectation**| `role` | VARCHAR(50) | NOT NULL | Rôle du pilote sur ce vol |

*(Les clés étrangères ne sont pas listées ici mais sont détaillées dans le script DDL et le rapport PDF).*

---

## 4. Instructions de lancement

### Prérequis
* Un serveur MySQL local (WAMP, XAMPP, MAMP, ou natif).
* Python 3.8+ installé.

### Étape 1 : Initialisation de la Base de Données
1. Lancez votre serveur MySQL.
2. Ouvrez votre SGBD (ex: MySQL Workbench, phpMyAdmin).
3. Exécutez l'intégralité du fichier `script_creation.sql`. Cela va créer la base `AeroDB`, générer les 7 tables, créer la vue SQL et insérer le jeu d'essai.
4. Vous pouvez exécuter le fichier `requetes.sql` pour visualiser le comportement des 15 requêtes métier complexes.

### Étape 2 : Lancement de l'Application (Interface Graphique)
Pour éviter tout conflit de dépendances (notamment sur macOS/Anaconda), il est recommandé d'utiliser un environnement virtuel.

Ouvrez un terminal à la racine du projet et tapez les commandes suivantes :

```bash
# 1. Création de l'environnement virtuel
python3 -m venv env_aero

# 2. Activation de l'environnement
# Sur macOS / Linux :
source env_aero/bin/activate
# Sur Windows :
env_aero\Scripts\activate

# 3. Installation des dépendances requises
pip install PyQt6 mysql-connector-python

# 4. Lancement de l'interface
python gui_projetBDML_AHAMADA_Naheri.py
