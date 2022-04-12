from asyncio.windows_events import NULL
from inspect import Parameter
from msilib.schema import CheckBox
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from xmlrpc.client import Boolean
from Database import Database as db
import sqlite3
from ttkthemes import ThemedTk


class Mochila:

    db_name = "Database\\dbmochila.db"
    

    def __init__(self, Mochi):

        ventana = ThemedTk(theme="aquativo")
        
        ventana.title("Armar una nueva Mochila")
        ventana.resizable(height=False, width=False)
        ventana.wm_attributes("-topmost",True)
        # ventana.geometry("600x400")

        #FRAME CONTAINER
        frame = LabelFrame(ventana, text = "Nueva Mochila")
        frame.grid(row=0, column=0, pady=10,padx=10)

        #CAMPOS
        Label(frame, text="Codigo Equipo: ", padx=20).grid(row=1, column=0)
        self.listaEquipo = ttk.Combobox(frame, width=17, state="readonly")
        self.listaEquipo.grid(row=1, column =1)
        opciones = self.Listar_Codigo_Equipo()
        self.listaEquipo['values'] = opciones
        
        Label(frame, text="Celular 1: ", padx=20).grid(row=2, column=0)
        self.listaCelular1 = ttk.Combobox(frame, width=17, state="readonly")
        self.listaCelular1.grid(row=2, column = 1)
        opciones = self.Listar_Celular()
        self.listaCelular1['values'] = opciones

        self.car1= BooleanVar()
        self.cbCargador1 = Checkbutton(frame, text="Cargador", variable=self.car1,onvalue=True, offvalue=False, command= lambda: self.Check_Boolean(self.car1))
        self.cbCargador1.grid(row=2, column=2)
        

        self.aur1= IntVar()
        self.cbAuricular1 = Checkbutton(frame, text="Auricular",variable=self.aur1,onvalue=True,offvalue=False, command= lambda: self.Check_Boolean(self.aur1))
        self.cbAuricular1.grid(row=2, column=3)

        Label(frame, text="Celular 2: ", padx=20).grid(row=3, column=0)
        self.listaCelular2 = ttk.Combobox(frame, width=17, state="readonly")
        self.listaCelular2.grid(row=3, column = 1)
        opciones = self.Listar_Celular()
        self.listaCelular2['values'] = opciones
        
        self.car2= IntVar()
        self.cbCargador2 = Checkbutton(frame, text="Cargador", variable=self.car2,onvalue=True,offvalue=False, command= lambda: self.Check_Boolean(self.car2))
        self.cbCargador2.grid(row=3, column=2)

        self.aur2= IntVar()
        self.cbAuricular2 = Checkbutton(frame, text="Auricular",variable=self.aur2,onvalue=True,offvalue=False, command= lambda: self.Check_Boolean(self.aur2))
        self.cbAuricular2.grid(row=3, column=3)

        Label(frame, text="Bateria 1: ", padx=20).grid(row=4, column=0)
        self.listaBateria1 = ttk.Combobox(frame, width=17, state="readonly")
        self.listaBateria1.grid(row=4, column = 1)
        opciones = self.Listar_Bateria()
        self.listaBateria1['values'] = opciones

        Label(frame, text="Bateria 2: ", padx=20).grid(row=5, column=0)
        self.listaBateria2 = ttk.Combobox(frame, width=17, state="readonly")
        self.listaBateria2.grid(row=5, column = 1)
        opciones = self.Listar_Bateria()
        self.listaBateria2['values'] = opciones

        Label(frame, text="Bateria 3: ", padx=20).grid(row=6, column=0)
        self.listaBateria3 = ttk.Combobox(frame, width=17, state="readonly")
        self.listaBateria3.grid(row=6, column = 1)
        opciones = self.Listar_Bateria()
        self.listaBateria3['values'] = opciones
        

        #BOTON
        self.botonRegistrar = ttk.Button(frame, text="Finalizar Armado", width=20, command= lambda: self.Armar_Mochila(self.listaEquipo.get(), self.listaCelular1.get(), self.listaCelular2.get(),
                                                                                                                    self.listaBateria1.get(),self.listaBateria2.get(),self.listaBateria3.get(),
                                                                                                                    self.car1,self.car2,self.aur1,self.aur2))
        self.botonRegistrar.grid(row=7,column=0,columnspan=2, sticky=W+E)
        self.botonEliminar = ttk.Button(frame, text="Desarmar", width=10, command= lambda: self.Desarmar_Mochila())
        self.botonEliminar.grid(row=7,column=2, columnspan=3, sticky=W+E)
        
        
        #TABLA
        self.tree = ttk.Treeview(frame, height= 10, columns=("1","2","3","4","5","6","7"))
        self.tree.grid(row = 9, column = 0, columnspan=4, pady=15)
        self.tree.heading("#0", text= "Equipo", anchor = CENTER)
        self.tree.column("#0", minwidth=0, width=100)
        self.tree.heading("#1", text= "Celular 1", anchor = CENTER)
        self.tree.column("#1", minwidth=0, width=100)
        self.tree.heading("#2", text= "Celular 2", anchor = CENTER)
        self.tree.column("#2", minwidth=0, width=100)
        self.tree.heading("#3", text= "Bateria 1", anchor = CENTER) 
        self.tree.column("#3", minwidth=0, width=100)
        self.tree.heading("#4", text= "Bateria 2", anchor = CENTER) 
        self.tree.column("#4", minwidth=0, width=100)
        self.tree.heading("#5", text= "Bateria 3", anchor = CENTER) 
        self.tree.column("#5", minwidth=0, width=100)
        self.tree.heading("#6", text= "Cargador", anchor = CENTER) 
        self.tree.column("#6", minwidth=0, width=100)
        self.tree.heading("#7", text= "Auricular", anchor = CENTER) 
        self.tree.column("#7", minwidth=0, width=100)
        """ self.tree["displaycolumns"]=("1","2","3") """
        
        self.Listar_Mochila()

        self.mochila = Mochi


    def Check_Boolean(self,valor):
        if valor.get() == False:
                valor.set(True)
        elif valor.get() == True:
                valor.set(False)
        
        return valor
        
        

    def Armar_Mochila(self, equipo, cel1, cel2, bat1,bat2,bat3,car1,car2,aur1, aur2):
        car=0
        aur=0

        if car1.get() == True:
            car = car+1
        if car2.get() == True:
            car = car+1
        if aur1.get() == True:
            aur = aur+1
        if aur2.get() == True:
            aur = aur+1

        if cel1 == "":
            cel1 = NULL
        if cel2 == "":
            cel2 = NULL
        if bat1 == "":
            bat1 = NULL
        if bat2 == "":
            bat2 = NULL
        if bat3 == "":
            bat3 = NULL

        try:
            parameters = (equipo,cel1, cel2, bat1,bat2,bat3,car,aur)
            query = "INSERT INTO dbmochila VALUES(NULL, ? ,?, ?, ?, ?, ?, ?, ?, 0)"
            self.run_query(self.db_name,query,parameters)

            self.Asignar_Elementos(equipo, cel1, cel2, bat1, bat2, bat3)

            self.listaEquipo.set("")
            self.listaCelular1.set("")
            self.listaCelular2.set("")
            self.listaBateria1.set("")
            self.listaBateria2.set("")
            self.listaBateria3.set("")

            self.listaEquipo['values'] = self.Listar_Codigo_Equipo()
            self.listaCelular1['values'] = self.Listar_Celular()
            self.listaCelular2['values'] = self.Listar_Celular()
            self.listaBateria1['values'] = self.Listar_Bateria()
            self.listaBateria2['values'] = self.Listar_Bateria()
            self.listaBateria3['values'] = self.Listar_Bateria()

            messagebox.showinfo("Mochila","La Mochila se ha armado ")

            self.mochila.Listar_Mochila_ListBox()
            self.Listar_Mochila()
        except sqlite3.IntegrityError as e:
                print(e)
                messagebox.showerror("ERROR","Algun elemento se encuentra registrado")


        #VOLVEMO A CARGAR LAS OPCIONES ACTUALIZDAS
        
    def Desarmar_Mochila(self):
        
        try:
            self.tree.item(self.tree.selection())["text"]
        except Exception as e:
            messagebox.showinfo("ALERTA","Selecciona una Mochila")
            return
        
        equipo = self.tree.item(self.tree.selection())["text"]
        
        cartel = messagebox.askyesno("ALERTA", "¿Seguro que queres eliminar?")
        if cartel == True:
            self.Confirmacion_Eliminar(equipo)

        
    def Confirmacion_Eliminar(self, dato):

        self.Desasignar_Elementos(dato)
        
        query =  "DELETE FROM dbmochila WHERE codEquipo = ?"
        self.run_query(self.db_name,query, (dato,))
        messagebox.showinfo("ALERTA","El equipo se ha desarmado")
        
        self.listaEquipo['values'] = self.Listar_Codigo_Equipo()
        self.listaCelular1['values'] = self.Listar_Celular()
        self.listaCelular2['values'] = self.Listar_Celular()
        self.listaBateria1['values'] = self.Listar_Bateria()
        self.listaBateria2['values'] = self.Listar_Bateria()
        self.listaBateria3['values'] = self.Listar_Bateria()
        
        self.mochila.Listar_Mochila_ListBox()
        self.Listar_Mochila()


    def Listar_Mochila(self):
        
        #Limpiando tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #Consultando datos en la tabla
        query = "SELECT * FROM dbmochila ORDER BY idmochila DESC"
        db_rows = self.run_query(self.db_name,query)
        for row in db_rows:
            self.tree.insert("", 0, text = row[1], values = (row[2],row[3],row[4],row[5],row[6],row[7],row[8])) 

    
    def run_query(self, db_name, query, parameters = ()):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def Listar_Codigo_Equipo(self):
        db_name= "Database\\dbequipo.db"
        #Limpiando lista
        """ self.listaEquipo.delete() """
        lista = []
        #Consultando datos en la tabla
        query = "SELECT codigoEquipo FROM dbequipo WHERE asignado = 0 ORDER BY idEquipo ASC"
        db_rows = self.run_query(db_name,query)
        for row in db_rows:
            lista.append(row[0])
        
        return lista

    def Listar_Celular(self):
        db_name= "Database\\dbcelular.db"
        #Limpiando lista
        """ self.listaEquipo.delete() """
        lista = []
        #Consultando datos en la tabla
        query = "SELECT codigoCelular FROM dbcelular WHERE asignado = 0 ORDER BY idCelular ASC"
        db_rows = self.run_query(db_name,query)
        for row in db_rows:
            lista.append(row)
        
        return lista

    def Listar_Bateria(self):
        db_name= "Database\\dbbateria.db"
        #Limpiando lista
        """ self.listaEquipo.delete() """
        lista = []
        #Consultando datos en la tabla
        query = "SELECT codigoBateria FROM dbbateria WHERE asignado = 0 ORDER BY idBateria ASC"
        db_rows = self.run_query(db_name,query)
        for row in db_rows:
            lista.append(row)
        
        return lista


    def Asignar_Elementos(self, equipo, cel1, cel2, bat1, bat2, bat3):
        db_name= "Database\\dbequipo.db"
        query = "UPDATE dbequipo SET asignado = 1 WHERE codigoEquipo = ?"
        self.run_query(db_name,query,(equipo,))

        db_name= "Database\\dbcelular.db"
        query = "UPDATE dbcelular SET asignado = 1 WHERE (codigoCelular = ?) OR (codigoCelular = ?)"
        parameters = (cel1,cel2)
        self.run_query(db_name,query,parameters)

        db_name= "Database\\dbbateria.db"
        query = "UPDATE dbbateria SET asignado = 1 WHERE (codigoBateria = ?) OR (codigoBateria = ?) OR (codigoBateria = ?)"
        parameters = (bat1,bat2,bat3)
        self.run_query(db_name,query,parameters)

    def Desasignar_Elementos(self, equipo):
        
        lista = ()
        query = "SELECT * FROM dbmochila WHERE codEquipo = ?"
        
        db_rows = self.run_query(self.db_name,query,(equipo,))
        
        for row in db_rows:
            lista = row
            
        
        db_name= "Database\\dbequipo.db"
        query = "UPDATE dbequipo SET asignado = 0 WHERE codigoEquipo = ?"
        self.run_query(db_name,query,(equipo,))

        db_name= "Database\\dbcelular.db"
        query = "UPDATE dbcelular SET asignado = 0 WHERE (codigoCelular = ?) OR (codigoCelular = ?)"
        parameters = (lista[2],lista[3])
        self.run_query(db_name,query,parameters)

        db_name= "Database\\dbbateria.db"
        query = "UPDATE dbbateria SET asignado = 0 WHERE (codigoBateria = ?) OR (codigoBateria = ?) OR (codigoBateria = ?)"
        parameters = (lista[4],lista[5],lista[6])
        self.run_query(db_name,query,parameters)
        


        