from inspect import Parameter

import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry



class Faltante():


    def __init__(self, ventanaPrincipal, framePadre):

        """ ventana = Tk()

        ventana.title("Registro de Faltantes")
        ventana.resizable(height=False, width=False)
        ventana.wm_attributes("-topmost",True) """

        #FRAME CONTAINER
        self.frame = LabelFrame(framePadre, text= "Faltantes")
        self.frame.grid(row=0, column=1, rowspan=2,pady=10,padx=10)

        #CAMPOS PARA FILTRAR
        Label(self.frame, text="Elemento: ", padx=20).grid(row=0, column=0)
        self.listaelemento= ttk.Combobox(self.frame, width=17)
        self.listaelemento.grid(row=0, column =1, columnspan=2)
        opciones= self.Lista_Elemento()
        self.listaelemento['values'] = opciones

        Label(self.frame, text="Productor: ", padx=20).grid(row=1, column=0)
        self.productor = Entry(self.frame)
        self.productor.grid(row=1, column = 1, columnspan=2)

        Label(self.frame, text="Cobertura: ", padx=20).grid(row=2, column=0)
        self.cobertura = Entry(self.frame)
        self.cobertura.grid(row=2, column=1, columnspan=2)

        """ Label(frame, text="Fecha Entrega: ", padx=20).grid(row=1, column=2)
        today = datetime.date.today()
        self.fechaEntrega = DateEntry(frame, width=17, locale="es_AR", year= today.year, month = today.month, day = today.day)
        self.fechaEntrega.grid(row=1, column=3, padx=15)

        Label(frame, text="Fecha Regreso: ", padx=20).grid(row=2, column=2)
        today = datetime.date.today()
        self.fechaRegreso = DateEntry(frame, width=17, locale="es_AR", year = today.year, month = today.month, day = today.day)
        self.fechaRegreso.grid(row=2, column=3, padx=15) """


        #TABLA (EN ANCHO DE LAS COLUMNAS DEBEN SUMAR 600)
        self.tree = ttk.Treeview(self.frame, height= 7, columns=("1","2","3","4"))
        self.tree.grid(row = 0, column = 3, rowspan=3, padx=15)
        self.tree.heading("#0", text= "Elemento", anchor = CENTER)
        self.tree.column("#0", minwidth=0, width=135, anchor=CENTER)
        self.tree.heading("#1", text= "Productor", anchor = CENTER)
        self.tree.column("#1", minwidth=0, width=135, anchor=CENTER)
        self.tree.heading("#2", text= "Cobertura", anchor = CENTER)
        self.tree.column("#2", minwidth=0, width=135, anchor=CENTER)
        self.tree.heading("#3", text= "Fecha de Entrega", anchor = CENTER)
        self.tree.column("#3", minwidth=0, width=135, anchor=CENTER)
        self.tree.heading("#4", text= "Fecha de Regreso", anchor = CENTER)
        self.tree.column("#4", minwidth=0, width=135, anchor=CENTER)

        botonFiltrar = ttk.Button(self.frame,text="Buscar", command= lambda: self.Filtrar_Elemento())
        botonFiltrar.grid(row=3,column=0, sticky=W+E)

        botonFiltrar = ttk.Button(self.frame,text="Item Recuperado", command= lambda: self.Recuperar_Faltante())
        botonFiltrar.grid(row=3,column=1,columnspan=3,sticky=W+E)

        self.Listar_Faltantes()
       

    def run_query(self, db_name, query, parameters = ()):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result  



    def Listar_Faltantes(self):
        #Limpiando tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        db_name = "Database\\dbfaltante.db"
        query = "SELECT * FROM dbfaltante ORDER BY idFaltante ASC"
        db_rows = self.run_query(db_name,query)

        for row in db_rows:
            self.tree.insert("", 0, text = row[1], values = (row[2],row[3],row[4],row[5])) 


    def Lista_Elemento(self):
        db_name = "Database\\dbfaltante.db"
        query= "SELECT codigoFaltante FROM dbfaltante"

        db_rows = self.run_query(db_name,query)
        listaS =[]
        
        for row in db_rows:
            listaS.append(row[0])
        
        nuevaListaS = []

        for elem in listaS:
            if elem not in nuevaListaS:
                nuevaListaS.append(elem)

        return nuevaListaS
    
    def Filtrar_Elemento(self):
        db_name = "Database\\dbfaltante.db"

        if len(self.listaelemento.get()) != 0 or len(self.productor.get()) != 0 or len(self.cobertura.get()) != 0:
        #Limpiando tabla
            records = self.tree.get_children()
            for element in records:
                self.tree.delete(element)

        #Consultando datos en la tabla
            query = "SELECT * FROM dbfaltante WHERE (codigoFaltante LIKE ?) AND (productor LIKE ?) AND (cobertura LIKE ?)"

            parameters = ('%'+self.listaelemento.get().strip()+'%','%'+self.productor.get().strip()+'%','%'+self.cobertura.get().strip()+'%')
            print(query)
            print(parameters)

            db_rows = self.run_query(db_name,query,parameters)
            
            for row in db_rows:
                self.tree.insert("", 0, text = row[1], values = (row[2],row[3],row[4],row[5]))
        else:
            self.Listar_Faltantes()

    def Recuperar_Faltante(self):

        try:
            item = self.tree.item(self.tree.selection())["text"]

            #RECUPERA CELULARES Y BUSCA SI COINCIDE CON LO SELECCIONADO
            db_name= "Database\\dbcelular.db"
            query = "SELECT codigoCelular FROM dbcelular"
            db_rows = self.run_query(db_name,query)
            lista = []
            for row in db_rows:
                lista.append(row[0])
            if item in lista:
                db_name= "Database\\dbcelular.db"
                query = "UPDATE dbcelular SET asignado = 0 WHERE codigoCelular = ?"
                self.run_query(db_name,query,(item,))

            #RECUPERA BATERIAS Y BUSCA SI COINCIDE CON LO SELECCIONADO
            db_name= "Database\\dbbateria.db"
            query = "SELECT codigobateria FROM dbbateria"
            db_rows = self.run_query(db_name,query)
            lista = []
            for row in db_rows:
                lista.append(row[0])
            if item in lista:
                db_name= "Database\\dbbateria.db"
                query = "UPDATE dbbateria SET asignado = 0 WHERE codigoBateria = ?"
                self.run_query(db_name,query,(item,))

            #ELIMINA FALTANTE DE LA LISTA
            db_name= "Database\\dbfaltante.db"
            query = "DELETE FROM dbfaltante WHERE codigoFaltante = ?"
            db_rows = self.run_query(db_name,query,(item,))

            #RECUPERA STOCK Y BUSCA SI COINCIDE CON LO SELECCIONADO
            item2 = item.split()

            db_name= "Database\\dbstock.db"
            query = "SELECT item FROM dbstock"
            db_rows = self.run_query(db_name,query)
            lista = []
            for row in db_rows:
                lista.append(row[0])
                print(row[0])
                print(item2[0])
            if item2[1] in lista:
                print("Hola me  meti en el if, o sea que estoy en la lista y esto deberia salir bien")
                db_name= "Database\\dbstock.db"
                query = "UPDATE dbstock SET cantidad = cantidad + ? WHERE item = ?"
                parameters = (item2[0],item2[1])
                self.run_query(db_name,query,parameters)


            messagebox.showinfo("ALERTA","El elemento faltante fue recuperado")
            self.Listar_Faltantes()

        except Exception as e:
            print(e)
            messagebox.showinfo("ALERTA","Selecciona un Elemento")
            return

        

    def __del__(self):
        print("objeto eliminado")

        
        
    def Destruirme(self):
        self.frame.destroy()    