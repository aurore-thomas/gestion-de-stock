import mysql.connector

class Categorie:
    def __init__(self) -> None:
        self.db = mysql.connector.connect(
                host = "localhost",
                user  = 'root',
                password = '05012001',
                database = 'boutique'
        )
        
        self.cursor = self.db.cursor()
    
        self.create_table()
        self.create_categorie("T-Shirt")
        self.create_categorie("Jeans")
        self.create_categorie("Pull")
        self.create_categorie("Chemises")
        self.join_inner()
        self.close_all()
    

    def create_table(self):
        self.cursor.execute("CREATE TABLE categorie (id INT PRIMARY KEY AUTO_INCREMENT, nom VARCHAR(255));")

    def create_categorie(self, nom):
        self.cursor.execute(f"INSERT INTO categorie(nom) VALUES ('{nom}');")
        self.db.commit()
    
    def show_tables(self):
        self.cursor.execute("SHOW TABLES FROM boutique;")

    def close_all(self):
        self.cursor.close()
        self.db.close()

    def join_inner(self):
        self.cursor.execute("SELECT * FROM produit INNER JOIN categorie ON produit.id_categorie = categorie.id;")

    def list_categorie(self):
        self.cursor.execute("SELECT nom FROM categorie;")
        results = self.cursor.fetchall()
        self.all_categorie = []

        for i in range(0, len(results)):
            self.all_categorie.append(results[i][0])
