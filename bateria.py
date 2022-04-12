import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk

class Bateria:

    db_name = "Database\\dbbateria.db"

    def __init__(self, ventanaPrincipal, framePadre):

        """ ventana = ventanaPrincipal
        
        ventana.title("Agregar una nueva Bateria")
        ventana.resizable(height=False, width=False)
        ventana.wm_attributes("-topmost",True)
        # ventana.geometry("600x400") """

        #FRAME CONTAINER
        self.frame = LabelFrame(framePadre, text = "Nueva Bateria")
        self.frame.grid(row=0, column=3, rowspan=4, pady=10,padx=10)

        #CAMPOS
        Label(self.frame, text="Marca: ", padx=20).grid(row=1, column=0)
        self.marca = Entry(self.frame)
        self.marca.grid(row=1, column=1,pady=5, columnspan=2)

        Label(self.frame, text="Dueño: ", padx=20).grid(row=2, column=0)
        self.listaDueño = ttk.Combobox(self.frame, width=17, state="readonly")
        self.listaDueño.grid(row=2, column =1,pady=5, columnspan=2)
        opciones=["ESPN", "Dejero", "Otro"]
        self.listaDueño['values'] = opciones

        Label(self.frame, text="Numero de Serie: ", padx=20).grid(row=3, column=0)
        self.serialNumber = Entry(self.frame)
        self.serialNumber.grid(row=3, column=1,pady=5, columnspan=2)

        Label(self.frame, text="Codigo: ", padx=20).grid(row=4, column=0)
        self.codigo = Entry(self.frame)
        self.codigo.grid(row=4, column=1,pady=5, columnspan=2)
        
        #TABLA
        self.tree = ttk.Treeview(self.frame, height= 7, columns=("1","2","3"))
        self.tree.grid(row = 1, column = 3, rowspan=4, padx=15)
        self.tree.heading("#0", text= "Marca", anchor = CENTER)
        self.tree.column("#0", minwidth=0, width=150, anchor=CENTER)
        self.tree.heading("#1", text= "Dueño", anchor = CENTER)
        self.tree.column("#1", minwidth=0, width=150, anchor=CENTER)
        self.tree.heading("#2", text= "Numero de Serie", anchor = CENTER)
        self.tree.column("#2", minwidth=0, width=150, anchor=CENTER)
        self.tree.heading("#3", text= "Codigo", anchor = CENTER)
        self.tree.column("#3", minwidth=0, width=150, anchor=CENTER)
  
        """ self.tree["displaycolumns"]=("1","2","3") """

        #BOTON
        self.botonRegistrar = ttk.Button(self.frame, text="Registrar",width=10, command= lambda: self.Registrar_Bateria(self.marca.get(), self.listaDueño.get(),self.serialNumber.get(),self.codigo.get()))
        self.botonRegistrar.grid(row=7,column=0, sticky=W+E)
        self.botonEliminar = ttk.Button(self.frame, text="Eliminar",width=10, command= self.Eliminar_Bateria)
        self.botonEliminar.grid(row=7,column=1,columnspan=3,sticky=W+E)
        
        self.Listar_Bateria()


    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def Listar_Bateria(self):
        
        #Limpiando tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #Consultando datos en la tabla
        query = "SELECT * FROM dbbateria ORDER BY idBateria DESC"
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert("", 0, text = row[1], values = (row[2],row[3],row[4]) )

        
    def Registrar_Bateria(self, marca, dueño,serial, codigo):
        
        self.serialNumber.delete(0,END)
        self.marca.delete(0,END)
        self.codigo.delete(0,END)

        try:
            parameters = (marca,dueño,serial,codigo)
            query = "INSERT INTO dbbateria VALUES(NULL, ? ,?, ?, ?, 0)"
            self.run_query(query,parameters)
            messagebox.showinfo("Bateria","La Bateria se ha registrado")

            self.Listar_Bateria()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("ERROR","Codigo ya se encuentra registrado")

    def Eliminar_Bateria(self):
        print("saraza")
        try:
            self.tree.item(self.tree.selection())["values"][2]
        except Exception as e:
            messagebox.showinfo("ALERTA","Selecciona una bateria")
            return
        
        equipo = self.tree.item(self.tree.selection())["values"][2]

        cartel = messagebox.askyesno("ALERTA", "¿Seguro que queres eliminar?")
        if cartel == True:
            self.Confirmacion_Eliminar(equipo)

    def Confirmacion_Eliminar(self, dato):
        
        query =  "DELETE FROM dbbateria WHERE codigoBateria = ?"
        self.run_query(query, (dato,))
        messagebox.showinfo("ALERTA","La bateria fue eliminada")
        
        self.Listar_Bateria()

    def __del__(self):
        print("objeto eliminado")

        
    def Destruirme(self):
        self.frame.destroy()