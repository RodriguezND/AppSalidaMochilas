from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from turtle import width
from Database import Database as db
import sqlite3
from ttkthemes import ThemedTk


class Equipo:

    db_name = "Database\\dbequipo.db"

    def __init__(self, ventanaPrincipal, framePadre):

        """ ventana = ThemedTk(theme="aquativo") """
        """ self.ventana = ThemedTk(theme="aquativo") 
        self.ventana.title("Agregar un nuevo equipo")
        self.ventana.resizable(height=False, width=False)
        self.ventana.wm_attributes("-topmost",True) """
        # ventana.geometry("600x400")

        #FRAME CONTAINER
        self.frame = LabelFrame(framePadre, text = "Nuevo Equipo")
        self.frame.grid(row=0, column=3, rowspan=4, pady=10,padx=10)

        #CAMPOS
        Label(self.frame, text="Equipo: ", padx=20).grid(row=1, column=0)
        self.listaEquipo = ttk.Combobox(self.frame, width=17, state="readonly")
        self.listaEquipo.grid(row=1, column =1,pady=5, columnspan=2)
        opciones=["LiveU", "Dejero", "Teradek", "Aviwest","Otro"]
        self.listaEquipo['values'] = opciones
        
        Label(self.frame, text="Modelo: ", padx=20).grid(row=2, column=0)
        self.modelo = Entry(self.frame)
        self.modelo.grid(row=2, column=1,pady=5, columnspan=2)
        Label(self.frame, text="Numero de Serie: ", padx=20).grid(row=3, column=0)
        self.serial = Entry(self.frame)
        self.serial.grid(row=3, column=1,pady=5, columnspan=2)
        Label(self.frame, text="Codigo: ", padx=20).grid(row=4, column=0)
        self.codigo = Entry(self.frame)
        self.codigo.grid(row=4, column=1,pady=5, columnspan=2)
        
        #TABLA
        self.tree = ttk.Treeview(self.frame, height= 7,columns=("1","2","3"))
        self.tree.grid(row = 1, column = 3,rowspan=4, padx=15)
        self.tree.heading("#0", text= "Equipo", anchor = CENTER)
        self.tree.column("#0", minwidth=0, width=100, anchor=CENTER)
        self.tree.heading("#1", text= "Modelo", anchor = CENTER)
        self.tree.column("#1", minwidth=0, width=100, anchor=CENTER)
        self.tree.heading("#2", text= "Numero de Serie", anchor = CENTER)
        self.tree.column("#2", minwidth=0, width=100, anchor=CENTER)
        self.tree.heading("#3", text= "Codigo", anchor = CENTER) 
        self.tree.column("#3", minwidth=0, width=100, anchor=CENTER)
        
        """ self.tree["displaycolumns"]=("1","2","3") """

        #BOTON
        self.botonRegistrar = ttk.Button(self.frame, text="Registrar", width=10, command= lambda: self.Registrar_Equipo(self.listaEquipo.get(), self.modelo.get(), self.serial.get(),self.codigo.get()))
        self.botonRegistrar.grid(row=6,column=0, sticky=W+E)
        
        self.botonEliminar = ttk.Button(self.frame, text="Eliminar", width=10, command=self.Eliminar_Equipo)
        self.botonEliminar.grid(row=6,column=1,columnspan=3,sticky=W+E)

        self.Listar_Equipos()

    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def Registrar_Equipo(self, equipo, modelo, serial, codigo):

        self.modelo.delete(0,END)
        self.serial.delete(0,END)
        self.codigo.delete(0,END)

        try:
            parameters = (equipo,modelo, serial, codigo)
            query = "INSERT INTO dbequipo VALUES(NULL, ? ,?, ?, ?, 0)"
            self.run_query(query,parameters)
            messagebox.showinfo("Equipo","El equipo se ha registrado")

            self.Listar_Equipos()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("ERROR","Numero de Serie o Codigo ya se encuentra registrado")

    def Eliminar_Equipo(self):
        print("saraza")
        try:
            self.tree.item(self.tree.selection())["values"][2]
        except Exception as e:
            messagebox.showinfo("ALERTA","Selecciona un equipo")
            return
        
        equipo = self.tree.item(self.tree.selection())["values"][2]

        cartel = messagebox.askyesno("ALERTA", "¿Seguro que queres eliminar?")
        if cartel == True:
            self.Confirmacion_Eliminar(equipo)

        
    def Confirmacion_Eliminar(self, dato):
        
        query =  "DELETE FROM dbequipo WHERE codigoEquipo = ?"
        self.run_query(query, (dato,))
        messagebox.showinfo("ALERTA","El equipo fue eliminado")
        
        self.Listar_Equipos()

    def Listar_Equipos(self):
        
        #Limpiando tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #Consultando datos en la tabla
        query = "SELECT * FROM dbequipo ORDER BY idEquipo DESC"
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert("", 0, text = row[1], values = (row[2],row[3],row[4])) 

    def __del__(self):
        print("objeto eliminado")
        
        
    def Destruirme(self):
        self.frame.destroy()
        
        
        
        
        

