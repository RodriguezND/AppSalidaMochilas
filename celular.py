import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk


class Celular:

    db_name = "Database\\dbcelular.db"

    def __init__(self, ventanaPrincipal, framePadre):

        """ self.ventana = ventanaPrincipal
        
        self.ventana.title("Agregar un nuevo Celular")
        self.ventana.resizable(height=False, width=False)
        self.ventana.wm_attributes("-topmost",True)
        # ventana.geometry("600x400") """

        #FRAME CONTAINER
        self.frame = LabelFrame(framePadre, text = "Nuevo Celular")
        self.frame.grid(row=0, column=3,rowspan=4, pady=10,padx=10)

        #CAMPOS
        Label(self.frame, text="Marca: ", padx=20).grid(row=1, column=0)
        self.marca = Entry(self.frame)
        self.marca.grid(row=1, column=1, columnspan=2)
        Label(self.frame, text="Modelo: ", padx=20).grid(row=2, column=0)
        self.modelo = Entry(self.frame)
        self.modelo.grid(row=2, column=1, columnspan=2)
        Label(self.frame, text="Numero de Serie: ", padx=20).grid(row=3, column=0)
        self.serial = Entry(self.frame)
        self.serial.grid(row=3, column=1, columnspan=2)
        Label(self.frame, text="Linea: ", padx=20).grid(row=4, column=0)
        self.linea = Entry(self.frame)
        self.linea.grid(row=4, column=1, columnspan=2)

        Label(self.frame, text="Empresa: ", padx=20).grid(row=5, column=0)
        self.listaEmpresa = ttk.Combobox(self.frame, width=17, state="readonly")
        self.listaEmpresa.grid(row=5, column =1, columnspan=2)
        opciones=["Personal", "Claro", "Movistar"]
        self.listaEmpresa['values'] = opciones

        Label(self.frame, text="Codigo: ", padx=20).grid(row=6, column=0)
        self.codigo = Entry(self.frame)
        self.codigo.grid(row=6, column=1, columnspan=2)

        
        
        #TABLA
        self.tree = ttk.Treeview(self.frame, height= 7, columns=("1","2","3","4","5"))
        self.tree.grid(row = 1, column = 3,rowspan=6, padx=15)
        self.tree.heading("#0", text= "Marca", anchor = CENTER)
        self.tree.column("#0", minwidth=0, width=100, anchor=CENTER)
        self.tree.heading("#1", text= "Modelo", anchor = CENTER)
        self.tree.column("#1", minwidth=0, width=100, anchor=CENTER)
        self.tree.heading("#2", text= "Numero de Serie", anchor = CENTER)
        self.tree.column("#2", minwidth=0, width=100, anchor=CENTER)
        self.tree.heading("#3", text= "Linea", anchor = CENTER) 
        self.tree.column("#3", minwidth=0, width=100, anchor=CENTER)
        self.tree.heading("#4", text= "Empresa", anchor = CENTER) 
        self.tree.column("#4", minwidth=0, width=100, anchor=CENTER)
        self.tree.heading("#5", text= "Codigo", anchor = CENTER) 
        self.tree.column("#5", minwidth=0, width=100, anchor=CENTER)
        """ self.tree["displaycolumns"]=("1","2","3") """

        #BOTON
        self.botonRegistrar = ttk.Button(self.frame, text="Registrar",width=10, command= lambda: self.Registrar_Celular(self.marca.get(), self.modelo.get(), self.serial.get(),self.linea.get(),self.listaEmpresa.get(),self.codigo.get()))
        self.botonRegistrar.grid(row=8,column=0,columnspan=2, sticky=W+E)
        self.botonEliminar = ttk.Button(self.frame, text="Eliminar",width=10, command= self.Eliminar_Celular)
        self.botonEliminar.grid(row=8,column=2,columnspan=4,sticky=W+E)


        self.Listar_Celular()


    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def Listar_Celular(self):
        
        #Limpiando tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #Consultando datos en la tabla
        query = "SELECT * FROM dbcelular ORDER BY idCelular DESC"
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert("", 0, text = row[1], values = (row[2],row[3],row[4],row[5],row[6])) 

        
    def Registrar_Celular(self, marca, modelo, serial, linea, empresa, codigo):
        
        self.marca.delete(0,END)
        self.modelo.delete(0,END)
        self.serial.delete(0,END)
        self.linea.delete(0,END)
        self.codigo.delete(0,END)

        try:
            parameters = (marca,modelo, serial, linea, empresa,codigo)
            query = "INSERT INTO dbcelular VALUES(NULL, ? ,?, ?, ?, ?, ?, 0)"
            self.run_query(query,parameters)
            messagebox.showinfo("Celular","El Celular se ha registrado")

            self.Listar_Celular()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("ERROR","Numero de Serie o Codigo ya se encuentra registrado")

    def Eliminar_Celular(self):
        print("saraza")
        try:
            self.tree.item(self.tree.selection())["values"][4]
        except Exception as e:
            messagebox.showinfo("ALERTA","Selecciona un equipo")
            return
        
        equipo = self.tree.item(self.tree.selection())["values"][4]

        cartel = messagebox.askyesno("ALERTA", "¿Seguro que queres eliminar?")
        if cartel == True:
            self.Confirmacion_Eliminar(equipo)

    def Confirmacion_Eliminar(self, dato):
        
        query =  "DELETE FROM dbcelular WHERE codigoCelular = ?"
        self.run_query(query, (dato,))
        messagebox.showinfo("ALERTA","El celular fue eliminado")
        
        self.Listar_Celular()

    def __del__(self):
        print("objeto eliminado")

        
        
    def Destruirme(self):
        self.frame.destroy()