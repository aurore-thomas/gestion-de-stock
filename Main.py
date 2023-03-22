from Classes.Produit import *
from Classes.Categorie import *
from Classes.Settings import *

class Main:
    def __init__(self) -> None:
        self.db = mysql.connector.connect(
                host = "localhost",
                user  = 'root',
                password = '05012001'
                )
        
        self.cursor = self.db.cursor()

        self.window()
        self.draw()
        

    def window(self):
        self.win = tk.Tk()
        self.win.geometry('800x500')
        self.win.title('Gestion de stock')

        # Theme import : 
        self.win.tk.call('source', 'Tkinter_theme/forest-dark.tcl')
        ttk.Style().theme_use('forest-dark')


    def draw(self):

        # Display the tabs : 
        self.tabs = ttk.Notebook(self.win)
        self.display_product = tk.Frame(self.tabs)
        self.add_del_product = tk.Frame(self.tabs)
        self.modify_product = tk.Frame(self.tabs)

        self.tabs.add(self.display_product, text = "Catalogue")
        self.tabs.add(self.add_del_product, text = "Ajouter/Supprimer")
        self.tabs.add(self.modify_product, text = "Modifier")
        self.tabs.pack(expand = 1, fill = "both")

        # Catalogue : 
        

    def create_database(self, name):
        self.cursor.execute("SHOW DATABASES;")
        self.list_database = []
        for x in self.cursor:
            self.list_database.append(x[0])
        
        if name in self.list_database:
            print(f"Database {name} already exists !")
        else :
            self.create_db = f"CREATE DATABASE {str(name)};"
            self.cursor.execute(self.create_db)

    def use_database(self, name):
        self.change_db = f"USE {str(name)};"
        self.cursor.execute(self.change_db)

    def show_database(self):
        self.cursor.execute("SHOW DATABASES;")
        print("Databases : ")
        for x in self.cursor:
            print(f"    - {x[0]}")

    def drop_database(self,name):
        self.cursor.execute(f"DROP DATABASE {name}")
        print(f"Database {name} deleted")
        
    def close_all(self):
        self.cursor.close()
        self.db.close()

if __name__ == '__main__':
    main = Main()
    main.win.mainloop()

# class Crud:
#     def __init__(self):
#         self.cursor = db.cursor()
        
#     def create_tables(self, table):
#         self.create_table = "CREATE " + str(table) + ";"
#         self.cursor.execute(self.create_table)
#         db.commit()
#         self.cursor.close()
#         db.close()
    
#     def insert_into_table(self, table, nb_columns):
#         self.insert_table = "INSERT INTO" + str(table) + "VALUES ("
#         for i in range (1, nb_columns):
#             exec(f"var_{i} = input('Columns ? ')") # On crée autant de variable que de colonnes
#             self.insert_table += str(exec(f"var_{i}") + ",")

#         self.insert_table += ")"
#         db.commit()
#         self.cursor.close()
#         db.close()
    
#     def read_table(self, table):
#         self.read = "SELECT * FROM " + str(table) + ";"
#         self.cursor.execute(self.read)
#         db.commit()
#         self.cursor.close()
#         db.close()

#     def delete_all(self, table):
#         self.delete = "DELETE FROM " + str(table) + ";"
#         self.cursor.execute(self.delete)
#         db.commit()
#         self.cursor.close()
#         db.close()