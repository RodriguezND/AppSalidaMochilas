from cProfile import label
from tkinter import *
from tkinter import messagebox
from tkinter.font import BOLD
from turtle import width
from bateria import Bateria
from celular import Celular
from equipo import Equipo
from faltante import Faltante
from general import Stock
from imprimir import Imprimir
from mochila import Mochila
from historial import Historial
from tkinter import ttk
import sqlite3
import datetime
from Devolucion import Devolucion
from ttkthemes import ThemedTk

ListaSistema = ["Nico","Daniel-san","Dante","Ezequiel","Juan","German","Martin","Kam","Aquiles"]


class Principal:
    
    def __init__(self,windows):

        self.window = windows
        
        """ self.window.option_add("*TCombobox*Listbox*selectBackground", 'red')
        style = ttk.Style() 
        # Lista de Temas para usar: alt,clam, classic,default, vista,winnative,xpnative
        style.theme_use('adapta')
        style.configure("TCombobox", selectbackground= "red",highlightbackground="red") 

        style.configure("Treeview",
                background="#E1E1E1",
                fieldbackground="#E1E1E1")
        style.map('Treeview', background=[('selected', 'red')])

        style.configure('TButton', background='#D2D2D2', foreground='black')
        style.map('TButton', background=[('active', '#FF8888')]) """
        

        # window.geometry("800x500")
        self.window.title("Aplicacion Mochilas ESPN - DISNEY")
        self.window.resizable(height=False, width=False)
        """self.window.configure(bg="#FF6C6C")
        titulo = Label(self.window, text="ESPN")
        titulo.grid(row=0,column=0,pady=10)
        titulo.configure(fg="white",
                        bg="red",
                        font="Verdana 50 bold italic") """
                        
        #FRAME CONTAINER --------------------------------------------------------------
        framePrincipal = LabelFrame(self.window)
        framePrincipal.grid(row=1, column=0, rowspan=2, padx=20,pady=10)
        framePrincipal.configure(bg="#8A8A8A")
        
        #NOTEBOOK
        notebook = ttk.Notebook(framePrincipal)
        notebook.grid(row=0,column=0,columnspan=2,sticky=W+E)

        frame1 = ttk.Frame(notebook, width=800, height=280)
        frame2 = ttk.Frame(notebook, width=800, height=280)
        frame3 = ttk.Frame(notebook, width=800, height=280)
        frame4 = ttk.Frame(notebook, width=800, height=280)

        notebook.add(frame1, text='INVENTARIO')
        notebook.add(frame2, text='MOCHILAS')
        notebook.add(frame4, text='PRESTAMOS')
        notebook.add(frame3, text='HISTORIAL')
        

            #FRAME CONTAINER INVENTARIO --------------------------------------------------------------
        self.frame = LabelFrame(frame1)
        self.frame.pack(pady=20)
        """ frame.grid(row=0, column=0, pady=20, padx=20,sticky="") """

        ttk.Button(self.frame, text = "Equipo", width=15, command= lambda: self.Abrir_Equipo()).grid(row = 0, column=0, pady=5, padx=5, sticky= W + E)
        ttk.Button(self.frame, text = "Celular", width=15, command= lambda: self.Abrir_Celular()).grid(row = 1, column=0, pady=5, padx=5, sticky= W + E)
        ttk.Button(self.frame, text = "Bateria", width=15, command= lambda: self.Abrir_Bateria()).grid(row = 2, column=0, pady=5, padx=5, sticky= W + E)
        ttk.Button(self.frame, text = "Stock General", width=15, command= lambda: self.Abrir_Stock()).grid(row = 3, column=0, pady=5, padx=5, sticky= W + E)

        """ Label(frame, text="Lista de Equipos").grid(row=0,column=0)
        self.listaEquipos = Listbox(frame,height=10,width=50)
        self.listaEquipos.grid(row=1, column=0, pady=5,padx=5)
        self.listaEquipos.configure(highlightbackground="red",selectbackground="red")
        items = self.Listar_Equipos()
        self.listaEquipos.insert(0,*items)

        Label(frame, text="Lista de Celulares").grid(row=0,column=1)
        self.listaCelulares = Listbox(frame,height=10,width=50)
        self.listaCelulares.grid(row=1, column=1, pady=5,padx=5)
        self.listaCelulares.configure(highlightbackground="red",selectbackground="red")
        items = self.Listar_Equipos()
        self.listaEquipos.insert(0,*items) """


            #FRAME CONTAINER MOCHILA --------------------------------------------------------------
        frameMochila = LabelFrame(frame2)
        frameMochila.pack(pady=20, padx=10)

        ttk.Button(frameMochila, text="Preparar Mochila", width=15, command= lambda: Mochila(self)).grid(row=1, column=0,rowspan=3, pady=10, padx=10)
        ttk.Button(frameMochila, text="Asignar Mochila", width=15, command= lambda: self.Asignar_Mochila(self.listaEntrega.get(),self.productor.get(),self.cobertura.get(),self.obs.get())).grid(row=5, column=3, pady=10, padx=10)
        botonDesasignar = ttk.Button(frameMochila, text="Desasignar Mochila", command= lambda: self.Desasignar_Mochila())
        botonDesasignar.grid(row=5, column=4, pady=10, padx=10)
        botonChequeoMochila = ttk.Button(frameMochila, text="Revisar Mochila", command = lambda: self.Revisar_Mochila())
        botonChequeoMochila.grid(row=1, column=5, pady=10, padx=10)
        botonImprimir = ttk.Button(frameMochila, text="Imprimir", width=15, command= lambda: self.Imprimir())
        botonImprimir.grid(row=3, column=5, pady=10, padx=10)
        """ self.tree["displaycolumns"]=("1","2","3") """

        Label(frameMochila, text = "Mochilas preparadas").grid(row=0, column= 3,columnspan=2)

        self.lstbox = Listbox(frameMochila,height=7)
        self.lstbox.grid(row=1, column=3, pady=5,columnspan=2, rowspan=4,padx=5)
        self.lstbox.configure(highlightbackground="red",selectbackground="red")

        Label(frameMochila, text = "Entrega").grid(row=1, column= 1)
        self.listaEntrega = ttk.Combobox(frameMochila, width=18)
        self.listaEntrega.grid(row=1, column = 2)
        
        self.listaEntrega['values'] = ListaSistema
        Label(frameMochila, text = "Productor").grid(row=2, column= 1)
        self.productor = Entry(frameMochila)
        self.productor.grid(row=2, column=2)

        Label(frameMochila, text = "Cobertura").grid(row=3, column= 1)
        self.cobertura = Entry(frameMochila)
        self.cobertura.grid(row=3, column=2)

        Label(frameMochila, text = "Observaciones").grid(row=4, column= 1)
        self.obs = Entry(frameMochila)
        self.obs.grid(row=4, column=2)

        """ frameAnteFinal = Frame(frame2)
        frameAnteFinal.pack(side=RIGHT,pady=20, padx=10) """


            #FRAME CONTAINER PRESTAMOS --------------------------------------------------------------
        framePrestamos = LabelFrame(frame4)
        framePrestamos.pack(pady=20, padx=10)

        Label(framePrestamos, text = "Entrega").grid(row=1, column= 1)
        self.listaEntregaPrestamo = ttk.Combobox(framePrestamos, width=18)
        self.listaEntregaPrestamo.grid(row=1, column = 2)
        self.listaEntregaPrestamo['values'] = ListaSistema

        Label(framePrestamos, text = "Productor").grid(row=2, column= 1)
        self.productorPrestamo = Entry(framePrestamos)
        self.productorPrestamo.grid(row=2, column=2)

        Label(framePrestamos, text = "Produccion").grid(row=3, column= 1)
        self.produccionPrestamo = Entry(framePrestamos)
        self.produccionPrestamo.grid(row=3, column=2)

        Label(framePrestamos, text = "Evento").grid(row=4, column= 1)
        self.eventoPrestamo = Entry(framePrestamos)
        self.eventoPrestamo.grid(row=4, column=2)

        Label(framePrestamos, text="Celular: ", padx=20).grid(row=5, column=1)
        self.listaCelular1 = ttk.Combobox(framePrestamos, width=18, state="readonly")
        self.listaCelular1.grid(row=5, column = 2)
        opciones = self.Listar_Celular()
        self.listaCelular1['values'] = opciones

        Label(framePrestamos, text="Lista de Items: ", padx=20).grid(row=6, column=1)
        self.items = ttk.Combobox(framePrestamos, width=18, state="readonly")
        self.items.grid(row=6, column=2)
        opciones= self.Listar_Items()
        self.items['values'] = opciones


            #FRAME CONTAINER HISTORIAL --------------------------------------------------------------
        self.frameHistorial = LabelFrame(frame3)
        self.frameHistorial.pack(pady=20)
        
        botonHistorlaMochilas = ttk.Button(self.frameHistorial, text="Historial Mochilas", width=15, command= lambda: self.Abrir_Historial())
        botonHistorlaMochilas.grid(row = 0, column=0, pady=5, padx=5, sticky= W + E)
        botonHistorialFaltantes = ttk.Button(self.frameHistorial, text="Historial Faltantes", width=15, command= lambda: self.Abrir_Faltantes())
        botonHistorialFaltantes.grid(row = 1, column=0, pady=5, padx=5, sticky= W + E)

        Label(framePrincipal, text = "LISTA DE MOCHILAS ENTREGADAS").grid(row=1,column=1, columnspan=2, sticky=W+E)

        self.tree = ttk.Treeview(framePrincipal, height= 15, columns=("1","2","3","4","5","6","7","8","9","10"))
        self.tree.grid(row = 2, column = 1,sticky=W+E)  
        self.tree.heading("#0", text= "Entrega", anchor = CENTER)
        self.tree.column("#0", minwidth=0, width=100, anchor=CENTER)
        self.tree.heading("#1", text= "Mochila", anchor = CENTER)
        self.tree.column("#1", minwidth=0, width=100, anchor=CENTER)
        self.tree.heading("#2", text= "Productor", anchor = CENTER)
        self.tree.column("#2", minwidth=0, width=100, anchor=CENTER)
        self.tree.heading("#3", text= "Cobertura", anchor = CENTER) 
        self.tree.column("#3", minwidth=0, width=100, anchor=CENTER)
        self.tree.heading("#4", text= "Fecha Entrega", anchor = CENTER)   
        self.tree.column("#4", minwidth=0, width=100, anchor=CENTER)
        self.tree.heading("#5", text= "Celular 1", anchor = CENTER)   
        self.tree.column("#5", minwidth=0, width=100, anchor=CENTER)
        self.tree.heading("#6", text= "Celular 2", anchor = CENTER)   
        self.tree.column("#6", minwidth=0, width=100, anchor=CENTER)
        self.tree.heading("#7", text= "Bateria 1", anchor = CENTER)   
        self.tree.column("#7", minwidth=0, width=100, anchor=CENTER)
        self.tree.heading("#8", text= "Bateria 2", anchor = CENTER)   
        self.tree.column("#8", minwidth=0, width=100, anchor=CENTER)
        self.tree.heading("#9", text= "Bateria 3", anchor = CENTER)   
        self.tree.column("#9", minwidth=0, width=100, anchor=CENTER)
        self.tree.heading("#10", text= "Observaciones", anchor = CENTER)   
        self.tree.column("#10", minwidth=0, width=100, anchor=CENTER)
        
        #FRAME FINAL --------------------------------------------------------------
        framePie = LabelFrame(self.window)
        framePie.grid(row=2,column=0, sticky=W+S+E)
        pie = Label(framePie,text="Desarrollado por Daniel san - Version 0.0.5")
        pie.grid(row=0,column=0)

        self.ventanaEquipo = None
        self.ventanaCelular = None
        self.ventanaBateria = None
        self.ventanaStock = None
        self.ventanaFalta = None
        self.ventanaHisto = None

        self.Listar_Mochila_ListBox()
        self.Listar_SalidaMochila()

    #BOTON PARA REVISAR MOCHILA
    def Revisar_Mochila(self):
        
        try:
            self.tree.item(self.tree.selection())["values"][1]
        except Exception as e:
            messagebox.showinfo("ALERTA","Selecciona una Mochila")
            return

        self.entregaRevision= self.tree.item(self.tree.selection())["text"]
        self.codMochilaRevision= self.tree.item(self.tree.selection())["values"][0]
        self.productorRevision= self.tree.item(self.tree.selection())["values"][1]
        self.coberturaRevision=self.tree.item(self.tree.selection())["values"][2]
        self.fechaEntregaRevision=self.tree.item(self.tree.selection())["values"][3]
        cel1=self.tree.item(self.tree.selection())["values"][4]
        cel2=self.tree.item(self.tree.selection())["values"][5]
        bat1 = self.tree.item(self.tree.selection())["values"][6]
        bat2 = self.tree.item(self.tree.selection())["values"][7]
        bat3 =self.tree.item(self.tree.selection())["values"][8]
        obser =self.tree.item(self.tree.selection())["values"][9]

        ventanaDevolver = Devolucion(self.entregaRevision,self.codMochilaRevision,self.productorRevision,self.coberturaRevision,self.fechaEntregaRevision,cel1,cel2,bat1,bat2,bat3,obser,self)
        

    #FUNCIONES DE BASE DE DATOS
    def run_query(self,db_name, query, parameters = ()):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result


    #ASIGNACION Y DESASIGNACION DE MOCHILAS
    def Asignar_Mochila(self,entrega,productor,cobertura, observacion):
        
        if entrega != "" and productor != "" and cobertura != "":
            db_name= "Database\\dbmochila.db"

            lista=[]
            lista.append(entrega)
            try:
                item = self.lstbox.get(self.lstbox.curselection())
            except:
                messagebox.showerror("ERROR","Selecciona una mochila armada")
                return

            lista.append(item)
            lista.append(productor)
            lista.append(cobertura)
            
            """ today = datetime.date.today()
            hour = datetime.datetime.today() """
            ahora = datetime.datetime.now()
            ahoraFormat = ahora.strftime("%d/%m/%y - %I:%M")
            """ lista.append(f"{str(today.day)}/{str(today.month)}/{str(today.year)} - {hour.hour}:{hour.minute}") """
            lista.append(ahoraFormat)

            query= "SELECT codCelular1, codCelular2, codBateria1, codBateria2, codBateria3 FROM dbmochila WHERE codEquipo = ?"
            db_rows = self.run_query(db_name,query,(item,))
            for row in db_rows:
                tupla = row
            
            lista.append(tupla[0])
            lista.append(tupla[1])
            lista.append(tupla[2])
            lista.append(tupla[3])
            lista.append(tupla[4])
            lista.append(observacion)
            
            db_name= "Database\\dbsalidamochilas.db"

            try:
                parameters = tuple(lista)
                query = "INSERT INTO dbsalidamochilas VALUES(NULL, ? ,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)"
                self.run_query(db_name,query,parameters)
                messagebox.showinfo("Mochila","La Mochila fue asignada a " + productor)

                self.Asignar_Elementos(item)
                self.Listar_SalidaMochila() 
                self.Listar_Mochila_ListBox()
                self.listaEntrega.set("")
                self.productor.delete(0,END)
                self.cobertura.delete(0,END)
                self.obs.delete(0,END)


            except sqlite3.IntegrityError as e:
                messagebox.showerror("ERROR","Mochila ya se encuentra asignada")
        else:
            messagebox.showerror("ERROR","Debe completar los campos")
            
    
    def Desasignar_Mochila(self):

        try:
            self.tree.item(self.tree.selection())["values"][0]
        except Exception as e:
            messagebox.showinfo("ALERTA","Selecciona una Mochila")
            return
        
        mochila = self.tree.item(self.tree.selection())["values"][0]

        cartel = messagebox.askyesno("ALERTA", "¿Seguro que queres eliminar?")
        if cartel == True:
            self.Confirmacion_Eliminar(mochila)

        
    def Confirmacion_Eliminar(self, dato):
        db_name= "Database\\dbsalidamochilas.db"
        query =  "DELETE FROM dbsalidamochilas WHERE codigoMochila = ?"
        self.run_query(db_name,query, (dato,))
        messagebox.showinfo("ALERTA",f"La mochila {dato} se desasigna")
        
        self.Desasignar_Elementos(dato)
        self.Listar_Mochila_ListBox()
        self.Listar_SalidaMochila()

        

    #FUNCIONES PARA LISTAR MOCHILAS
    def Listar_SalidaMochila(self):
        db_name= "Database\\dbsalidamochilas.db"
        #Limpiando tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #Consultando datos en la tabla
        query = "SELECT * FROM dbsalidamochilas ORDER BY idSalidaMochila DESC"
        db_rows = self.run_query(db_name,query)
        for row in db_rows:
            self.tree.insert("", 0, text = row[1], values = (row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11])) 

    def Listar_Mochila_ListBox(self):
        db_name= "Database\\dbmochila.db"
        #Limpiando tabla
        self.lstbox.delete(0, END)
        #Consultando datos en la tabla
        query = "SELECT codEquipo FROM dbmochila WHERE asignado = 0 ORDER BY idmochila DESC"
        db_rows = self.run_query(db_name,query)
        for row in db_rows:
            self.lstbox.insert(0, *row)

    #FUNCIONES PARA ASIGNAR O DESASIGNAR ELEMENTOS
    def Asignar_Elementos(self, equipo):
        db_name= "Database\\dbmochila.db"
        query = "UPDATE dbmochila SET asignado = 1 WHERE codEquipo = ?"
        self.run_query(db_name,query,(equipo,))


    def Desasignar_Elementos(self, equipo):
        
        db_name= "Database\\dbmochila.db"
        query = "UPDATE dbmochila SET asignado = 0 WHERE codEquipo = ?"
        self.run_query(db_name,query,(equipo,))

    def Abrir_Historial(self):

        if self.ventanaFalta is not None:
            self.ventanaFalta.Destruirme()
            self.ventanaFalta = None    


        if self.ventanaHisto is None:
            self.ventanaHisto = Historial(self.window, self.frameHistorial)

    def Abrir_Faltantes(self):

        if self.ventanaHisto is not None:
            self.ventanaHisto.Destruirme()
            self.ventanaHisto = None    
        
        if self.ventanaFalta is None:
            self.ventanaFalta = Faltante(self.window, self.frameHistorial)
        
        

    def Imprimir(self):

        entrega = self.tree.item(self.tree.selection())["text"]
        equipo = self.tree.item(self.tree.selection())["values"][0]
        productor = self.tree.item(self.tree.selection())["values"][1]
        cobertura = self.tree.item(self.tree.selection())["values"][2]
        fechaEntrega =self.tree.item(self.tree.selection())["values"][3]
        c1 = self.tree.item(self.tree.selection())["values"][4]
        c2 = self.tree.item(self.tree.selection())["values"][5]
        b1 = self.tree.item(self.tree.selection())["values"][6]
        b2 = self.tree.item(self.tree.selection())["values"][7]
        b3 = self.tree.item(self.tree.selection())["values"][8]
        ob = self.tree.item(self.tree.selection())["values"][9]

        imprimir = Imprimir(entrega, equipo,productor,cobertura,fechaEntrega,c1,c2,b1,b2,b3,ob)

    def Listar_Equipos(self):
        #Consultando datos en la tabla
        db_name= "Database\\dbequipo.db"
        query = "SELECT * FROM dbequipo ORDER BY idEquipo ASC"
        db_rows = self.run_query(db_name, query)
        lista =[]
        for row in db_rows:
            lista.append(f"Equipo: {row[1]} - Modelo: {row[2]} - Codigo: {row[4]}")

        return lista

    def Abrir_Equipo(self):
        if self.ventanaCelular is not None:
            self.ventanaCelular.Destruirme()
            self.ventanaCelular = None

        if self.ventanaBateria is not None:        
            self.ventanaBateria.Destruirme()
            self.ventanaBateria = None

        if self.ventanaStock is not None:
            self.ventanaStock.Destruirme()
            self.ventanaStock = None
        
        if self.ventanaEquipo is None:
                self.ventanaEquipo = Equipo(self.window, self.frame)

    def Abrir_Celular(self):
        
        if self.ventanaEquipo is not None:
            self.ventanaEquipo.Destruirme()
            self.ventanaEquipo = None

        if self.ventanaBateria is not None:
            self.ventanaBateria.Destruirme()
            self.ventanaBateria = None

        if self.ventanaStock is not None:
            self.ventanaStock.Destruirme()
            self.ventanaStock = None    
        
        if self.ventanaCelular is None:
            self.ventanaCelular= Celular(self.window, self.frame)

    def Abrir_Bateria(self):
        
        if self.ventanaEquipo is not None:
            self.ventanaEquipo.Destruirme()
            self.ventanaEquipo = None

        if self.ventanaCelular is not None:
            self.ventanaCelular.Destruirme()
            self.ventanaCelular = None

        if self.ventanaStock is not None:
            self.ventanaStock.Destruirme()
            self.ventanaStock = None

        if self.ventanaBateria is None:
            self.ventanaBateria= Bateria(self.window, self.frame)
    
    def Abrir_Stock(self):
        if self.ventanaEquipo is not None:
            self.ventanaEquipo.Destruirme()
            self.ventanaEquipo = None

        if self.ventanaCelular is not None:
            self.ventanaCelular.Destruirme()
            self.ventanaCelular = None

        if self.ventanaBateria is not None:
            self.ventanaBateria.Destruirme()
            self.ventanaBateria = None

        if self.ventanaStock is None:
            self.ventanaStock = Stock(self.window, self.frame)
        
        pass
            
    def Listar_Items(self):
        #Limpiando tabla
        
        #Consultando datos en la tabla
        listaItems = []
        db_name = "Database\\dbstock.db"
        query = "SELECT * FROM dbstock ORDER BY idItem ASC"
        db_rows = self.run_query(db_name,query)
        for row in db_rows:
            listaItems.append(row[1])

        return listaItems


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