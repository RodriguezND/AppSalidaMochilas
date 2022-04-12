from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from Database import Database as db
import sqlite3
from ttkthemes import ThemedTk


class Stock:

    db_name = "Database\\dbstock.db"
    

    def __init__(self, ventanaPrincipal, framePadre):

        """ ventana = ThemedTk(theme="aquativo")
        
        ventana.title("Stock")
        ventana.resizable(height=False, width=False)
        ventana.wm_attributes("-topmost",True)
        # ventana.geometry("600x400") """

        #FRAME CONTAINER
        self.frame = LabelFrame(framePadre, text = "Control de Stock")
        self.frame.grid(row=0, column=2,rowspan=4, pady=10,padx=10)

        #CAMPOS
        Label(self.frame, text="Item: ", padx=20).grid(row=1, column=0)
        self.item = Entry(self.frame)
        self.item.grid(row=1, column=1,pady=5)
        
        Label(self.frame, text="Stock: ", padx=20).grid(row=2, column=0)
        self.stock = Entry(self.frame)
        self.stock.grid(row=2, column=1,pady=5)
   
        
        #TABLA
        self.tree = ttk.Treeview(self.frame, height= 7, columns=("1"))
        self.tree.grid(row = 0, column = 2, rowspan=4,padx=15)
        self.tree.heading("#0", text= "Item", anchor = CENTER)
        self.tree.column("#0", minwidth=0, width=328, anchor=CENTER)
        self.tree.heading("#1", text= "Stock", anchor = CENTER)
        self.tree.column("#1", minwidth=0, width=330, anchor=CENTER)
        
        self.Listar_Items()
        
        """ self.tree["displaycolumns"]=("1","2","3") """

        #BOTON
        self.botonRegistrar = ttk.Button(self.frame, text="Agregar", width=10, command= lambda: self.Registrar_Item(self.item.get(), self.stock.get()))
        self.botonRegistrar.grid(row=6,column=0, sticky=W+E)
        
        self.botonEliminar = ttk.Button(self.frame, text="Eliminar", width=10, command= lambda: self.Eliminar_Items())
        self.botonEliminar.grid(row=6,column=1,columnspan=3,sticky=W+E)


    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def Listar_Items(self):
        #Limpiando tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #Consultando datos en la tabla
        query = "SELECT * FROM dbstock ORDER BY idItem DESC"
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert("", 0, text = row[1], values = (row[2])) 

    def Registrar_Item(self,item, stock):
        
        self.item.delete(0,END)
        self.stock.delete(0,END)

        if item != "" and stock != "":
            query = "INSERT INTO dbstock VALUES(NULL, ? , ?)"
            parameters = (item,stock)
            self.run_query(query,parameters)    
            messagebox.showinfo("Stock","Se ha agregado un nuevo item")
        else:
            messagebox.showerror("ERROR","Debe completar los campos")

        self.Listar_Items()

    def Eliminar_Items(self):

        try:
            self.tree.item(self.tree.selection())["text"]
        except Exception as e:
            messagebox.showinfo("ALERTA","Selecciona un Item")
            return
        
        item = self.tree.item(self.tree.selection())["text"]
        print(item)
        cartel = messagebox.askyesno("ALERTA", "¿Seguro que queres eliminar?")
        if cartel == True:
            self.Confirmacion_Eliminar(item)

    def Confirmacion_Eliminar(self, dato):
        
        query =  "DELETE FROM dbstock WHERE item = ?"
        self.run_query(query, (dato,))
        messagebox.showinfo("ALERTA","El Item fue eliminado")
        
        self.Listar_Items()


    def __del__(self):
        print("objeto eliminado")

        
        
    def Destruirme(self):
        self.frame.destroy()