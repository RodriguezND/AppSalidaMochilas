from inspect import Parameter
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from ttkthemes import ThemedTk


class Historial:


    def __init__(self, ventanaPrincipal, framePadre):

        """ ventana = ThemedTk(theme="aquativo")
    
        ventana.title("Historial de Mochilas")
        ventana.resizable(height=False, width=False)
        ventana.wm_attributes("-topmost",True)
 """
        #FRAME CONTAINER
        self.frame = LabelFrame(framePadre, text= "Historial")
        self.frame.grid(row=0, column=1, rowspan=2, pady=10,padx=10)

        #CAMPOS PARA FILTRAR
        Label(self.frame, text="Mochila: ", padx=20).grid(row=0, column=0)
        self.listamochila= ttk.Combobox(self.frame, width=17)
        self.listamochila.grid(row=0, column =1)
        opciones= self.Lista_Mochila()
        self.listamochila['values'] = opciones

        Label(self.frame, text="Productor: ", padx=20).grid(row=1, column=0)
        self.productor = Entry(self.frame)
        self.productor.grid(row=1, column = 1)

        Label(self.frame, text="Cobertura: ", padx=20).grid(row=2, column=0)
        self.cobertura = Entry(self.frame)
        self.cobertura.grid(row=2, column=1)

        """ Label(frame, text="Fecha Entrega: ", padx=20).grid(row=1, column=2)
        today = datetime.date.today()
        self.fechaEntrega = DateEntry(frame, width=17, locale="es_AR", year= today.year, month = today.month, day = today.day)
        self.fechaEntrega.grid(row=1, column=3, padx=15)

        Label(frame, text="Fecha Regreso: ", padx=20).grid(row=2, column=2)
        today = datetime.date.today()
        self.fechaRegreso = DateEntry(frame, width=17, locale="es_AR", year = today.year, month = today.month, day = today.day)
        self.fechaRegreso.grid(row=2, column=3, padx=15) """


        #TABLA (EN ANCHO DE LAS COLUMNAS DEBEN SUMAR 600)
        self.tree = ttk.Treeview(self.frame, height= 7, columns=("1","2","3","4","5","6","7","8"))
        self.tree.grid(row = 0, column = 3, rowspan=3, padx=15)
        self.tree.heading("#0", text= "Entrega", anchor = CENTER)
        self.tree.column("#0", minwidth=0, width=75, anchor=CENTER)
        self.tree.heading("#1", text= "Mochila", anchor = CENTER)
        self.tree.column("#1", minwidth=0, width=75, anchor=CENTER)
        self.tree.heading("#2", text= "Productor", anchor = CENTER)
        self.tree.column("#2", minwidth=0, width=75, anchor=CENTER)
        self.tree.heading("#3", text= "Cobertura", anchor = CENTER)
        self.tree.column("#3", minwidth=0, width=75, anchor=CENTER)
        self.tree.heading("#4", text= "Equipamiento", anchor = CENTER)
        self.tree.column("#4", minwidth=0, width=75, anchor=CENTER)
        self.tree.heading("#5", text= "Fecha de Entrega", anchor = CENTER)
        self.tree.column("#5", minwidth=0, width=65, anchor=CENTER)
        self.tree.heading("#6", text= "Fecha de Regreso", anchor = CENTER)
        self.tree.column("#6", minwidth=0, width=65, anchor=CENTER)
        self.tree.heading("#7", text= "Recibio", anchor = CENTER)
        self.tree.column("#7", minwidth=0, width=70, anchor=CENTER)
        self.tree.heading("#8", text= "Observaciones", anchor = CENTER)
        self.tree.column("#8", minwidth=0, width=100, anchor=CENTER)

        botonFiltrar = ttk.Button(self.frame,text="Filtrar", command= lambda: self.Filtrar_Mochila())
        botonFiltrar.grid(row=3,column=0, columnspan=3, sticky=W+E)

        self.Listar_Historial()  

    def Listar_Historial(self):
        #Limpiando tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
            
        db_name = "Database\\dbhistorial.db"
        query = "SELECT * FROM dbhistorial ORDER BY idHistorialMochila ASC"
        db_rows = self.run_query(db_name,query)

        for row in db_rows:
            i=0
            datofinal = ""
            equipo = row[5]
            lista = equipo.split(",")
            
            for elem in lista:
                if elem != "0":
                    if i == 0:
                        datofinal = elem
                    else:
                        datofinal = datofinal + ", " + elem
                    i = i+1

            self.tree.insert("", 0, text = row[1], values = (row[2],row[3],row[4],datofinal,row[6],row[7],row[8],row[9])) 


    def run_query(self, db_name, query, parameters = ()):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result  

    def Lista_Mochila(self):
        db_name = "Database\\dbhistorial.db"
        query= "SELECT codigoMochila FROM dbhistorial"

        db_rows = self.run_query(db_name,query)
        listaS =[]
        
        for row in db_rows:
            listaS.append(row[0])
        
        nuevaListaS = []

        for elem in listaS:
            if elem not in nuevaListaS:
                nuevaListaS.append(elem)

        return nuevaListaS

    def Filtrar_Mochila(self):
        db_name = "Database\\dbhistorial.db"

        if len(self.listamochila.get()) != 0 or len(self.productor.get()) != 0 or len(self.cobertura.get()) != 0:
        #Limpiando tabla
            records = self.tree.get_children()
            for element in records:
                self.tree.delete(element)

        #Consultando datos en la tabla
            query = "SELECT * FROM dbhistorial WHERE (codigoMochila LIKE ?) AND (productor LIKE ?) AND (cobertura LIKE ?)"
            
            parameters = ('%'+self.listamochila.get().strip()+'%','%'+self.productor.get().strip()+'%','%'+self.cobertura.get().strip()+'%')
            print(query)
            print(parameters)

            db_rows = self.run_query(db_name,query,parameters)
            
            for row in db_rows:
                self.tree.insert("", 0, text = row[1], values = (row[2],row[3],row[4],row[5], row[6]))
        else:
            self.Listar_Historial()
    
    def __del__(self):
        print("objeto eliminado")

        
        
    def Destruirme(self):
        self.frame.destroy()