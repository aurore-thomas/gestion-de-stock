import mysql.connector

class Produit:
    def __init__(self) -> None:
        self.db = mysql.connector.connect(
                host = "localhost",
                user  = 'root',
                password = '05012001',
                database = 'boutique'
        )
        
        self.cursor = self.db.cursor()

    def create_table(self):
        self.cursor("CREATE TABLE produit (id INT PRIMARY KEY AUTO_INCREMENT, nom VARCHAR(255), DESCRIPTION TEXT, prix INT, quantite INT, id_categorie INT)")

    def create_product(self, nom, description, quantite, id_categorie):
        self.cursor.execute(f"INSERT INTO produit(nom, DESCRIPTION, quantite, id_categorie) VALUES ('{nom}, {description}, {quantite}, {id_categorie}');")
        self.db.commit()

    def delete_products(self, name):
        self.delete = f"DELETE FROM produit WHERE nom = {name};"
        self.cursor.execute(self.delete)
        self.db.commit()