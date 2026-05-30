import sys
import mysql.connector
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
                             QLabel, QLineEdit, QMessageBox, QHeaderView, QGroupBox, 
                             QFormLayout, QTabWidget)
from PyQt6.QtCore import Qt

DB_CONFIG = {
    'host': '',
    'user': '',      
    'password': '',      
    'database': ''
}

class AeroApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion de Flotte Aérienne - ALSI61 (Naheri AHAMADA)")
        self.resize(1100, 700)
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.tab_pilotes = QWidget()
        self.tab_compagnies = QWidget()
        self.tab_avions = QWidget()
        self.tab_vols = QWidget()
        
        self.tabs.addTab(self.tab_pilotes, "Pilotes")
        self.tabs.addTab(self.tab_compagnies, "Compagnies")
        self.tabs.addTab(self.tab_avions, "Avions")
        self.tabs.addTab(self.tab_vols, "Vols")
        
        self.setup_pilotes()
        self.setup_compagnies()
        self.setup_avions()
        self.setup_vols()
        
        self.refresh_all_tables()

    def connect_db(self):
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Erreur BDD", f"Impossible de se connecter: {err}")
            return None

    def charger_donnees_generique(self, table_widget, query, params=None):
        conn = self.connect_db()
        if not conn: return
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        records = cursor.fetchall()
        table_widget.setRowCount(0)
        for row_number, row_data in enumerate(records):
            table_widget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                table_widget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        conn.close()

    def refresh_all_tables(self):
        # On met à jour tous les tableaux en même temps pour que l'interface reflète 
        # instantanément les suppressions en cascade (ON DELETE CASCADE)
        self.charger_donnees_generique(self.table_pilotes, "SELECT * FROM Pilote")
        self.charger_donnees_generique(self.table_compagnies, "SELECT * FROM Compagnie")
        self.charger_donnees_generique(self.table_avions, "SELECT * FROM Avion")
        self.charger_donnees_generique(self.table_vols, "SELECT * FROM Vol")

    def setup_pilotes(self):
        layout = QHBoxLayout(self.tab_pilotes)
        left_panel = QVBoxLayout()
        
        form_group = QGroupBox("Informations Pilote")
        form_layout = QFormLayout()
        self.p_nom = QLineEdit()
        self.p_prenom = QLineEdit()
        self.p_salaire = QLineEdit()
        self.p_date = QLineEdit()
        self.p_date.setPlaceholderText("YYYY-MM-DD")
        self.p_comp = QLineEdit()
        
        form_layout.addRow("Nom :", self.p_nom)
        form_layout.addRow("Prénom :", self.p_prenom)
        form_layout.addRow("Salaire :", self.p_salaire)
        form_layout.addRow("Date embauche :", self.p_date)
        form_layout.addRow("ID Compagnie :", self.p_comp)
        form_group.setLayout(form_layout)
        left_panel.addWidget(form_group)
        
        self.btn_add_p = QPushButton("Ajouter Pilote")
        self.btn_mod_p = QPushButton("Modifier Salaire")
        self.btn_del_p = QPushButton("Supprimer Pilote")
        self.btn_details_p = QPushButton("Détails des vols (Sélectionnez un pilote)")
        
        self.btn_add_p.clicked.connect(self.ajouter_pilote)
        self.btn_mod_p.clicked.connect(self.modifier_pilote)
        self.btn_del_p.clicked.connect(self.supprimer_pilote)
        self.btn_details_p.clicked.connect(self.afficher_details_pilote)
        
        left_panel.addWidget(self.btn_add_p)
        left_panel.addWidget(self.btn_mod_p)
        left_panel.addWidget(self.btn_del_p)
        left_panel.addWidget(self.btn_details_p)
        left_panel.addStretch()
        layout.addLayout(left_panel, 1)
        
        self.table_pilotes = QTableWidget()
        self.table_pilotes.setColumnCount(6)
        self.table_pilotes.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "Salaire", "Embauche", "ID Comp."])
        self.table_pilotes.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_pilotes.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table_pilotes, 3)

    def ajouter_pilote(self):
        if not all([self.p_nom.text(), self.p_prenom.text(), self.p_salaire.text(), self.p_date.text(), self.p_comp.text()]):
            QMessageBox.warning(self, "Erreur", "Tous les champs sont requis.")
            return
        conn = self.connect_db()
        if conn:
            try:
                c = conn.cursor()
                c.execute("INSERT INTO Pilote (nom, prenom, salaire, date_embauche, id_compagnie) VALUES (%s, %s, %s, %s, %s)",
                          (self.p_nom.text(), self.p_prenom.text(), self.p_salaire.text(), self.p_date.text(), self.p_comp.text()))
                conn.commit()
                self.refresh_all_tables()
            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Erreur SQL", str(err))
            finally:
                conn.close()

    def modifier_pilote(self):
        row = self.table_pilotes.currentRow()
        if row < 0: return
        id_p = self.table_pilotes.item(row, 0).text()
        if not self.p_salaire.text():
            QMessageBox.warning(self, "Erreur", "Entrez le nouveau salaire dans le formulaire.")
            return
        conn = self.connect_db()
        if conn:
            c = conn.cursor()
            c.execute("UPDATE Pilote SET salaire = %s WHERE id_pilote = %s", (self.p_salaire.text(), id_p))
            conn.commit()
            conn.close()
            self.refresh_all_tables()

    def supprimer_pilote(self):
        row = self.table_pilotes.currentRow()
        if row < 0: return
        id_p = self.table_pilotes.item(row, 0).text()
        conn = self.connect_db()
        if conn:
            c = conn.cursor()
            c.execute("DELETE FROM Pilote WHERE id_pilote = %s", (id_p,))
            conn.commit()
            conn.close()
            self.refresh_all_tables()

    def afficher_details_pilote(self):
        row = self.table_pilotes.currentRow()
        if row < 0: return
        
        id_pilote = self.table_pilotes.item(row, 0).text()
        nom = self.table_pilotes.item(row, 1).text()
        prenom = self.table_pilotes.item(row, 2).text()
        
        conn = self.connect_db()
        if conn:
            cursor = conn.cursor()
            # Utilisation de la vue SQL pour s'épargner les jointures complexes côté Python
            sql = """SELECT numero_vol, role, date_heure_depart, depart_iata, arrivee_iata 
                     FROM Vue_Details_Vols 
                     WHERE id_pilote = %s"""
            cursor.execute(sql, (id_pilote,))
            vols = cursor.fetchall()
            conn.close()
            
            if not vols:
                msg = f"Le pilote {prenom} {nom} n'est affecté à aucun vol."
            else:
                msg = f"Vols de {prenom} {nom} :\n\n"
                for v in vols:
                    msg += f"- Vol {v[0]} : {v[1]} (Départ : {v[2]})\n  Trajet : {v[3]} -> {v[4]}\n\n"
            
            QMessageBox.information(self, "Détails du Pilote", msg)

    def setup_compagnies(self):
        layout = QHBoxLayout(self.tab_compagnies)
        left_panel = QVBoxLayout()
        
        form_group = QGroupBox("Informations Compagnie")
        form_layout = QFormLayout()
        self.c_nom = QLineEdit()
        self.c_pays = QLineEdit()
        form_layout.addRow("Nom :", self.c_nom)
        form_layout.addRow("Pays :", self.c_pays)
        form_group.setLayout(form_layout)
        left_panel.addWidget(form_group)
        
        self.btn_add_c = QPushButton("Ajouter Compagnie")
        self.btn_mod_c = QPushButton("Modifier Compagnie")
        self.btn_del_c = QPushButton("Supprimer Compagnie")
        
        self.btn_add_c.clicked.connect(self.ajouter_compagnie)
        self.btn_mod_c.clicked.connect(self.modifier_compagnie)
        self.btn_del_c.clicked.connect(self.supprimer_compagnie)
        
        left_panel.addWidget(self.btn_add_c)
        left_panel.addWidget(self.btn_mod_c)
        left_panel.addWidget(self.btn_del_c)
        left_panel.addStretch()
        layout.addLayout(left_panel, 1)
        
        self.table_compagnies = QTableWidget()
        self.table_compagnies.setColumnCount(3)
        self.table_compagnies.setHorizontalHeaderLabels(["ID", "Nom", "Pays d'origine"])
        self.table_compagnies.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_compagnies.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table_compagnies, 3)

    def ajouter_compagnie(self):
        if not self.c_nom.text() or not self.c_pays.text(): return
        conn = self.connect_db()
        if conn:
            try:
                c = conn.cursor()
                c.execute("INSERT INTO Compagnie (nom, pays_origine) VALUES (%s, %s)", (self.c_nom.text(), self.c_pays.text()))
                conn.commit()
                self.refresh_all_tables()
            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Erreur SQL", str(err))
            finally:
                conn.close()

    def modifier_compagnie(self):
        row = self.table_compagnies.currentRow()
        if row < 0: return
        id_c = self.table_compagnies.item(row, 0).text()
        if not self.c_nom.text() or not self.c_pays.text():
            QMessageBox.warning(self, "Erreur", "Veuillez remplir Nom et Pays pour la modification.")
            return
        conn = self.connect_db()
        if conn:
            c = conn.cursor()
            c.execute("UPDATE Compagnie SET nom = %s, pays_origine = %s WHERE id_compagnie = %s", 
                      (self.c_nom.text(), self.c_pays.text(), id_c))
            conn.commit()
            conn.close()
            self.refresh_all_tables()

    def supprimer_compagnie(self):
        row = self.table_compagnies.currentRow()
        if row < 0: return
        id_c = self.table_compagnies.item(row, 0).text()
        rep = QMessageBox.question(self, "Attention", "Supprimer cette compagnie supprimera ses avions, ses pilotes et ses vols (CASCADE). Continuer ?")
        if rep == QMessageBox.StandardButton.Yes:
            conn = self.connect_db()
            if conn:
                c = conn.cursor()
                c.execute("DELETE FROM Compagnie WHERE id_compagnie = %s", (id_c,))
                conn.commit()
                conn.close()
                self.refresh_all_tables()

    def setup_avions(self):
        layout = QHBoxLayout(self.tab_avions)
        left_panel = QVBoxLayout()
        
        form_group = QGroupBox("Informations Avion")
        form_layout = QFormLayout()
        self.a_imm = QLineEdit()
        self.a_cap = QLineEdit()
        self.a_comp = QLineEdit()
        self.a_mod = QLineEdit()
        form_layout.addRow("Immatriculation :", self.a_imm)
        form_layout.addRow("Capacité :", self.a_cap)
        form_layout.addRow("ID Compagnie :", self.a_comp)
        form_layout.addRow("ID Modèle :", self.a_mod)
        form_group.setLayout(form_layout)
        left_panel.addWidget(form_group)
        
        self.btn_add_a = QPushButton("Ajouter Avion")
        self.btn_del_a = QPushButton("Supprimer Avion")
        self.btn_add_a.clicked.connect(self.ajouter_avion)
        self.btn_del_a.clicked.connect(self.supprimer_avion)
        
        left_panel.addWidget(self.btn_add_a)
        left_panel.addWidget(self.btn_del_a)
        left_panel.addStretch()
        layout.addLayout(left_panel, 1)
        
        self.table_avions = QTableWidget()
        self.table_avions.setColumnCount(5)
        self.table_avions.setHorizontalHeaderLabels(["ID", "Immatriculation", "Capacité", "ID Comp.", "ID Mod."])
        self.table_avions.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_avions.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table_avions, 3)

    def ajouter_avion(self):
        if not all([self.a_imm.text(), self.a_cap.text(), self.a_comp.text(), self.a_mod.text()]): return
        conn = self.connect_db()
        if conn:
            try:
                c = conn.cursor()
                c.execute("INSERT INTO Avion (immatriculation, capacite, id_compagnie, id_modele) VALUES (%s, %s, %s, %s)", 
                          (self.a_imm.text(), self.a_cap.text(), self.a_comp.text(), self.a_mod.text()))
                conn.commit()
                self.refresh_all_tables()
            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Erreur SQL", str(err))
            finally:
                conn.close()

    def supprimer_avion(self):
        row = self.table_avions.currentRow()
        if row < 0: return
        id_a = self.table_avions.item(row, 0).text()
        conn = self.connect_db()
        if conn:
            c = conn.cursor()
            c.execute("DELETE FROM Avion WHERE id_avion = %s", (id_a,))
            conn.commit()
            conn.close()
            self.refresh_all_tables()

    def setup_vols(self):
        layout = QHBoxLayout(self.tab_vols)
        left_panel = QVBoxLayout()
        
        form_group = QGroupBox("Informations Vol")
        form_layout = QFormLayout()
        self.v_num = QLineEdit()
        self.v_dep = QLineEdit()
        self.v_dep.setPlaceholderText("YYYY-MM-DD HH:MM:00")
        self.v_arr = QLineEdit()
        self.v_arr.setPlaceholderText("YYYY-MM-DD HH:MM:00")
        self.v_avion = QLineEdit()
        self.v_aero_d = QLineEdit()
        self.v_aero_a = QLineEdit()
        
        form_layout.addRow("Numéro :", self.v_num)
        form_layout.addRow("Départ :", self.v_dep)
        form_layout.addRow("Arrivée :", self.v_arr)
        form_layout.addRow("ID Avion :", self.v_avion)
        form_layout.addRow("ID Aéro Dép :", self.v_aero_d)
        form_layout.addRow("ID Aéro Arr :", self.v_aero_a)
        form_group.setLayout(form_layout)
        left_panel.addWidget(form_group)
        
        self.btn_add_v = QPushButton("Ajouter Vol")
        self.btn_del_v = QPushButton("Annuler (Supprimer) Vol")
        self.btn_add_v.clicked.connect(self.ajouter_vol)
        self.btn_del_v.clicked.connect(self.supprimer_vol)
        
        left_panel.addWidget(self.btn_add_v)
        left_panel.addWidget(self.btn_del_v)
        left_panel.addStretch()
        layout.addLayout(left_panel, 1)
        
        self.table_vols = QTableWidget()
        self.table_vols.setColumnCount(7)
        self.table_vols.setHorizontalHeaderLabels(["ID", "Numéro", "Départ", "Arrivée", "ID Avion", "Aéro Dép", "Aéro Arr"])
        self.table_vols.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_vols.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table_vols, 3)

    def ajouter_vol(self):
        if not all([self.v_num.text(), self.v_dep.text(), self.v_arr.text(), self.v_avion.text(), self.v_aero_d.text(), self.v_aero_a.text()]):
            QMessageBox.warning(self, "Erreur", "Tous les champs sont requis.")
            return
        conn = self.connect_db()
        if conn:
            try:
                c = conn.cursor()
                c.execute("INSERT INTO Vol (numero_vol, date_heure_depart, date_heure_arrivee, id_avion, id_aeroport_depart, id_aeroport_arrivee) VALUES (%s, %s, %s, %s, %s, %s)", 
                          (self.v_num.text(), self.v_dep.text(), self.v_arr.text(), self.v_avion.text(), self.v_aero_d.text(), self.v_aero_a.text()))
                conn.commit()
                self.refresh_all_tables()
            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Erreur SQL", str(err))
            finally:
                conn.close()

    def supprimer_vol(self):
        row = self.table_vols.currentRow()
        if row < 0: return
        id_v = self.table_vols.item(row, 0).text()
        conn = self.connect_db()
        if conn:
            c = conn.cursor()
            c.execute("DELETE FROM Vol WHERE id_vol = %s", (id_v,))
            conn.commit()
            conn.close()
            self.refresh_all_tables()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AeroApp()
    window.show()
    sys.exit(app.exec())