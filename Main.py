from Classes.Produit import *
from Classes.Categorie import *
from Classes.Settings import *

class Main:
    def __init__(self) -> None:
        self.db = mysql.connector.connect(
                host = "localhost",
                user  = 'root',
                password = '05012001',
                database = 'boutique'
                )
        
        self.cursor = self.db.cursor()

        self.window()
        self.use_database("boutique")
        self.draw()
        

    def window(self):
        self.win = ctk.CTk()
        self.win.geometry('800x500')
        self.win.title('Gestion de stock')
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")

        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', font=BIG, padding=[20, 5, 20, 2])
        self.style.configure('Treeview', font=MEDIUM, rowheight=50)
        self.style.configure('Treeview.Heading', font = MEDIUM, background=BLUE)


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
        self.draw_catalogue()
        self.draw_add_del_tab()

    def draw_catalogue(self):
        choice_frame = tk.Frame(self.display_product)
        choice_frame.pack()
        text_catalogue = tk.Label(choice_frame, text='Choisissez la catégorie à afficher', font=BIG)
        text_catalogue.pack(side='left', pady=80, padx=20)

        # We put all the categories in a list to display them in the optionmenu widget.
        self.cursor.execute("SELECT nom FROM categorie")
        results = self.cursor.fetchall()
        self.category_list = []

        for i in range(0, len(results)):
            self.category_list.append(results[i][0])

        # OptionMenu widget :
        self.text_inside_optionmenu = tk.StringVar(choice_frame)
        self.text_inside_optionmenu.set('Liste des catégories')

        choice_category = tk.OptionMenu(choice_frame, self.text_inside_optionmenu, *self.category_list, command=self.display_selected)
        choice_category.config(font=BIG, bd = 1)
        choice_category['menu'].config(font = BIG)
        choice_category.pack(pady=80, padx=20)

        self.board_frame = tk.Frame(self.display_product)
        self.board_frame.pack()

    def display_selected(self, args):
        category_selected = self.text_inside_optionmenu.get()

        self.cursor.execute(f"SELECT id FROM categorie WHERE nom='{str(category_selected)}'")
        results = self.cursor.fetchall()
        self.id_selected = results[0][0]

        self.clear_board_frame()
        self.display_products()

    def display_products(self):
        board = ttk.Treeview(self.board_frame, columns=('ID', 'Nom', 'Description', 'Prix', 'Quantité'), )
        board.heading('ID', text='ID')
        board.heading('Nom', text='Nom')
        board.heading('Description', text='Description')
        board.heading('Prix', text='Prix (€)')
        board.heading('Quantité', text='Quantité')
        board.column('ID', width=100, anchor=CENTER)
        board.column('Nom', width=400)
        board.column('Description', width=750)
        board.column('Prix', width=120, anchor=CENTER)
        board.column('Quantité', width=150, anchor=CENTER)
        board['show'] = 'headings'
        board.pack()

        self.cursor.execute(f"SELECT id, nom, DESCRIPTION, prix, quantite FROM produit WHERE id_categorie = {self.id_selected}")
        results = self.cursor.fetchall()

        if len(results):
            for i in results:
                board.insert('', 'end', values=(i[0], i[1], i[2], i[3], i[4]))

    def clear_board_frame(self):
        for element in self.board_frame.winfo_children():
            element.destroy()

    def draw_add_del_tab(self):
        add_frame = ctk.CTkFrame(self.add_del_product, width=500)
        add_frame.pack(side='left')

        del_frame = ctk.CTkFrame(self.add_del_product, width=300)
        del_frame.pack()

        # ---------ADD PRODUCTS-------------------------
        add_label = ctk.CTkLabel(add_frame, text="AJOUTER UN PRODUIT", font=LITTLE)
        add_label.pack(pady=15)

        # OptionMenu widget :
        self.category_new_product = tk.StringVar(add_frame)
        self.category_new_product.set('Catégorie')

        self.add_category = tk.OptionMenu(add_frame, self.category_new_product, *self.category_list, command=self.add_new_product_database())
        self.add_category.config(font=BIG, bd = 1)
        self.add_category['menu'].config(font = BIG)
        self.add_category.pack(pady=15, padx=20)

        self.name_new_product = ctk.CTkEntry(add_frame, placeholder_text='Nom', width=250)
        self.name_new_product.pack(padx=100, pady=5)

        self.price_new_product = ctk.CTkEntry(add_frame, placeholder_text='Prix en €', width=250)
        self.price_new_product.pack(pady=5)

        self.quantity_new_product = ctk.CTkEntry(add_frame, placeholder_text='Quantité', width=250)
        self.quantity_new_product.pack(pady=5)

        self.description_new_product = ctk.CTkTextbox(add_frame, width = 250, corner_radius=10, height=100)
        self.description_new_product.pack(pady=10)

        self.button_new_product = ctk.CTkButton(add_frame, text="Enregistrer")
        self.button_new_product.pack(pady=5)

        # ---------DELETE PRODUCTS-------------------------
        delete_label = ctk.CTkLabel(del_frame, text="SUPPRIMER UN PRODUIT", font=LITTLE)
        delete_label.pack(pady=15)

        choice_category = tk.OptionMenu(del_frame, self.text_inside_optionmenu, *self.category_list, command=self.display_selected)
        choice_category.config(font=BIG, bd = 1)
        choice_category['menu'].config(font = BIG)
        choice_category.pack(pady=15, padx=20)

        self.button_del_product = ctk.CTkButton(del_frame, text="Supprimer")
        self.button_del_product.pack(pady=5)

    def add_new_product_database(self):
        name_new_product = self.name_new_product.get()
        price_new_product = self.price_new_product.get()
        quantity_new_product = self.quantity_new_product.get()
        description_new_product = self.description_new_product.get()
        category_new_product = self.category_new_product.get()

        for i in range(0, self.category_list):
            if category_new_product == self.category_list[i]:
                index_category_new_product = i + 1

        print(name_new_product)
        print(price_new_product)
        print(quantity_new_product)
        print(description_new_product)
        print(index_category_new_product)

        # self.insert_into_table('produit', ('nom', 'DESCRIPTION', 'prix', 'quantite', 'id_categorie'), (name_new_product, description_new_product, price_new_product, quantity_new_product, index_category_new_product))


    def insert_into_table(self, table_name, col_tuple, data_tuple):
        self.my_cursor.execute("USE boutique")

        columns = ", ".join(f"{col}" for col in col_tuple)
        values = ", ".join(f"'{value}'" for value in data_tuple)
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"

        self.cursor.execute(query)
        self.db.commit()

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