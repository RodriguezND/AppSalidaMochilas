import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from setuptools import Command
from tkcalendar import Calendar, DateEntry
from tkinter import messagebox
import datetime
from ttkthemes import ThemedTk

ListaSistema = ["Nico","Daniel-san","Dante","Ezequiel","Juan","German","Martin","Kam","Aquiles"]


class Devolucion():

    def __init__(self,entregaRev,codMochilaRev, productorRev,coberturaRev,fechaEntregaRev,cel1,cel2,bat1,bat2,bat3, obser,obj):

        self.ventana = ThemedTk(theme="aquativo")
        self.ventana.title = "Completa la revision"
        """ ventana.geometry("350x500") """
        self.ventana.resizable(height=False, width=False)
        
        #FRAME CONTAINER
        self.frameRevision = LabelFrame(self.ventana,text="")
        self.frameRevision.grid(row=0, column=0, pady=15, padx=15) 

        #NOMBRE MOCIHLA
        Label(self.frameRevision, text = "Mochila: " + codMochilaRev + "\nSelecciona todos los elementos que volvieron").grid(row = 0, column = 0, padx = 15, pady= 15,columnspan=3)
        """ nuevo_nombre = Entry(self.revision, textvariable=StringVar(self.revision, value = codMochila), state="readonly")
        nuevo_nombre.grid(row=0, column=1) """

        """ self.listaEleme = [cel1,cel2,bat1,bat2,bat3]
        listaCheck= []
        self.listaBool =[self.cel1,self.cel2,self.bat1,self.bat2,self.bat3]
        
        i=0
        r=1
        
        for elem in self.listaEleme:   
            if elem != 0:        
                listaCheck.append(Checkbutton(self.frameRevision, text=f"{elem}", variable=self.listaBool[i],onvalue=True, offvalue=False, command= lambda: self.Check_Boolean()).grid(row=r, column=0))
                i =i+1
                r =r+1 """
        
        #CEL1
        self.cel1= BooleanVar()
        self.cbCel1 = Checkbutton(self.frameRevision, text=f"{cel1}", variable=self.cel1,onvalue=True, offvalue=False, command= lambda: self.Check_Boolean(self.cel1,cel1))
        self.cbCel1.grid(row=1, column=0)

        #CEL2
        self.cel2= BooleanVar()
        self.cbCel2 = Checkbutton(self.frameRevision, text=f"{cel2}", variable=self.cel2,onvalue=True, offvalue=False, command= lambda: self.Check_Boolean(self.cel2,cel2))
        self.cbCel2.grid(row=2, column=0)

        #BAT1
        self.bat1= BooleanVar()
        self.cbBat1 = Checkbutton(self.frameRevision, text=f"{bat1}", variable=self.bat1,onvalue=True, offvalue=False, command= lambda: self.Check_Boolean(self.bat1,bat1))
        self.cbBat1.grid(row=3, column=0)

        #BAT2
        self.bat2= BooleanVar()
        self.cbBat2 = Checkbutton(self.frameRevision, text=f"{bat2}", variable=self.bat2,onvalue=True, offvalue=False, command= lambda: self.Check_Boolean(self.bat2,bat2))
        self.cbBat2.grid(row=4, column=0)

        #BAT3
        self.bat3= BooleanVar()
        self.cbBat3 = Checkbutton(self.frameRevision, text=f"{bat3}", variable=self.bat3,onvalue=True, offvalue=False, command= lambda: self.Check_Boolean(self.bat3,bat3))
        self.cbBat3.grid(row=5, column=0)

        listaCheck= [self.cbCel1,self.cbCel2,self.cbBat1,self.cbBat2,self.cbBat3]
        self.listaEleme = [cel1,cel2,bat1,bat2,bat3]
        self.listaBool = [self.cel1,self.cel2,self.bat1,self.bat2,self.bat3]
        i=0
        for elem in self.listaEleme:   
            if elem == 0:        
                listaCheck[i].destroy()
            i =i+1
        
        self.mochi = codMochilaRev
        self.listaDeFaltantes = []
        self.listaDeFaltantes2 = []
        listaCargadorAuricular= self.GetAuricularCargador(codMochilaRev)

        #CARGADOR Y AURICULAR CON SPINBOX

        Label(self.frameRevision, text="Lista de Items: ", padx=20).grid(row=1, column=1, columnspan=2,padx=10,sticky=W)
        self.items = ttk.Combobox(self.frameRevision, width=17, state="readonly")
        self.items.grid(row=1, column =2,pady=5, columnspan=2)
        opciones= self.Listar_Items()
        self.items['values'] = opciones

        Label(self.frameRevision, text="Cantidad: ", padx=20).grid(row=2, column=1, columnspan=2,padx=10,sticky=W)
        self.spinItems = ttk.Spinbox(self.frameRevision, from_=0 ,to=2,width=10)
        self.spinItems.grid(row=2, column=2,pady=5,padx=10,sticky=E)
        self.spinItems.set(0)

        """ Label(self.frameRevision, text="Cargador: ", padx=20).grid(row=2, column=1, columnspan=2,padx=10,sticky=W)
        self.spinCargador = ttk.Spinbox(self.frameRevision, from_=0 ,to=listaCargadorAuricular[0],width=10)
        self.spinCargador.grid(row=2, column=1,pady=5,padx=10,sticky=E)
        self.spinCargador.set(0)
        
        Label(self.frameRevision, text="Auricular: ", padx=20).grid(row=3, column=1, columnspan=2,padx=10,sticky=W)
        self.spinAuricular = ttk.Spinbox(self.frameRevision, from_=0 ,to=listaCargadorAuricular[1],width=10)
        self.spinAuricular.grid(row=3, column=3,pady=5,padx=10,sticky=E)
        self.spinAuricular.set(0) """

        self.bool = False
        self.botonConfirmarInsumo = Button(self.frameRevision, text="Agregar", width=7,height=1, command= lambda: self.Confirmar_Auricular_Cargador())
        self.botonConfirmarInsumo.grid(row=4, column=1, columnspan=2,sticky=W+E)
        self.botonConfirmarInsumo = Button(self.frameRevision, text="Eliminar", width=7,height=1, command= lambda: self.Eliminar_Auricular_Cargador() )
        self.botonConfirmarInsumo.grid(row=5, column=1, columnspan=2,sticky=W+E)


        #LISTA FINAL DE ELEMENTOS FALTANTES
        """ self.listabox = Listbox(self.frameRevision,height=5)
        self.listabox.grid(row=5, column=1, pady=5, padx=5) """


        self.recibio = Label(self.frameRevision, text = "Recibe: ", padx=15, pady=15)
        self.recibio.grid(row = 7, column = 0)
        self.listaRecibe = ttk.Combobox(self.frameRevision, width=17)
        self.listaRecibe.grid(row=7, column = 1)
        self.listaRecibe['values'] = ListaSistema


        #OTROS
        self.var= BooleanVar()
        self.cbVar = Checkbutton(self.frameRevision, text=f"¿Queres notificar algun elemento dañado o perdido?", variable=self.var,onvalue=True, offvalue=False, command= lambda: self.Check_Boolean2(self.var,9))
        self.cbVar.grid(row=8, column=0, columnspan=2)

        self.varMotivoLabel = Label(self.frameRevision, text = "Motivo: ")
        self.varMotivoLabel.grid(row = 9, column = 0)
        self.varMotivo = Entry(self.frameRevision, state="readonly")
        self.varMotivo.grid(row=9, column=1)

        Button(self.frameRevision, text="Confirmar", width=15, command= lambda: self.Confirmar_Devolucion(self.listaDeFaltantes,entregaRev,codMochilaRev,productorRev,coberturaRev,fechaEntregaRev,cel1,cel2,bat1,bat2,bat3,self.listaRecibe,self.varMotivo,obser,obj)).grid(row=10, column=0, columnspan=3, pady=10, padx=10)



    def Confirmar_Devolucion(self,lista,entre,codmochi,pro,cob,fe,c1,c2,b1,b2,b3,rec,mov,obser,obj):
        db_name= "Database\\dbfaltante.db"
        ahora = datetime.datetime.now()
        ahoraFormat = ahora.strftime("%d/%m/%y - %I:%M")
        fechaDevolucion = ahoraFormat

        #RESTAMOS LOS FALTANTES EN EL STOCK
        self.listaDeFaltantes3 = self.Restar_Stock(self.listaDeFaltantes2, codmochi)

        print("Este es la lista final")
        print(self.listaDeFaltantes3)
        """ lista = lista  """
        self.listaEleme = self.listaEleme + self.listaDeFaltantes3
        n = len(self.listaEleme)
        
        i=0
        print(self.listaEleme)
        print(lista)
        for elem in range(n):
            print(self.listaEleme[i])
            if self.listaEleme[i] not in lista:
                try: 
                    print("se disparo el elemento faltante " + self.listaEleme[i])
                    query = "INSERT INTO dbfaltante VALUES(NULL, ?,?,?,?,?)"
                    parameters = (self.listaEleme[i],pro,cob,fe,fechaDevolucion)
                    self.run_query(db_name,query,parameters)
                except:
                    pass
            i = i + 1   
        
        #MAXIMO SOLICITADOS
        ListaStock = self.Listar_Items()
        TotalCarAur = self.GetAuricularCargador(codmochi)
        TotalCar = TotalCarAur[0]
        TotalAur = TotalCarAur[1]
        TotalSDI = 2
        longitudStock = len(ListaStock)

        for i in range(longitudStock):
            if ListaStock[i] not in self.listaDeFaltantes2:
                pass
            

        #DATOS EN HISTORIAL DE MOCHILAS
        print("ESTA ES UNA PRUEBA " + mov.get())
        db_name= "Database\\dbhistorial.db"
        listaEquip = f"{c1}, {c2}, {b1}, {b2}, {b3}"
        query = "INSERT INTO dbhistorial VALUES(NULL, ?,?,?,?,?,?,?,?,?)"
        parameters = (entre,codmochi,pro,cob,listaEquip,fe,fechaDevolucion,rec.get(),mov.get() + " // " + obser)
        self.run_query(db_name,query,parameters) 
        
        #ELIMINA DATOS EN MOCHILAS ARMADAS Y SALIDA MOCHILAS
        db_name= "Database\\dbsalidamochilas.db"
        query =  "DELETE FROM dbsalidamochilas WHERE codigoMochila = ?"
        self.run_query(db_name,query, (codmochi,))

        db_name= "Database\\dbmochila.db"
        query =  "DELETE FROM dbmochila WHERE codEquipo = ?"
        parameters = (codmochi,)
        self.run_query(db_name,query,parameters) 

        #SE DESASIGNA EQUIPAMIENTO
        db_name= "Database\\dbequipo.db"
        query = "UPDATE dbequipo SET asignado = 0 WHERE codigoEquipo = ?"
        self.run_query(db_name,query,(codmochi,))

        contador=0
        listaP = [] 
        listaConfirmadas = lista
        if c1 in listaConfirmadas:
            listaP.append(c1)
            contador += 1
        if c2 in listaConfirmadas:
            listaP.append(c2)
            contador += 1
        tuplaP = tuple(listaP)

        if contador != 0:
            db_name= "Database\\dbcelular.db"
            query = "UPDATE dbcelular SET asignado = 0"
            j=1
            for elem in range(contador):
                if j == 1:
                    query = query + " WHERE (codigoCelular = ?)"
                else: 
                    query = query + " OR (codigoCelular = ?)" 
                j +=1
            print(query)
            parameters = tuplaP
            self.run_query(db_name,query,parameters)

        contador=0
        listaP = [] 
        listaConfirmadas = lista
        if b1 in lista:
            listaP.append(b1)
            contador += 1
        if b2 in lista:
            listaP.append(b2)
            contador += 1
        if b3 in lista:
            listaP.append(b3)
            contador += 1
        tuplaP = tuple(listaP)

        if contador != 0:
            db_name= "Database\\dbbateria.db"
            query = "UPDATE dbbateria SET asignado = 0 "
            j=1
            for elem in range(contador):
                if j == 1:
                    query = query + " WHERE (codigoBateria = ?)"
                else: 
                    query = query + " OR (codigoBateria = ?)" 
                j +=1
            parameters = tuplaP
            self.run_query(db_name,query,parameters)

        messagebox.showinfo("Informacion","Se confirma el regreso de la mochila")

        obj.Listar_SalidaMochila()

        self.ventana.destroy()
        

    def Confirmar_Auricular_Cargador(self):
        
        item  = self.items.get()
        print(item)
        print(self.spinItems.get())

        carAur = self.GetAuricularCargador(self.mochi)

        if self.items.get() == "Cargadores":
            if int(self.spinItems.get()) > carAur[0]:
                messagebox.showerror("Error","La cantidad seleccionada supera el maximo de Cargadores que salieron")
                return
        elif self.items.get() == "Auriculares":
            if int(self.spinItems.get()) > carAur[1]:
                messagebox.showerror("Error","La cantidad seleccionada supera el maximo de Auriculares que salieron")
                return
                
        if len(self.listaDeFaltantes2) == 0:
                self.listaDeFaltantes2.append(f"{self.spinItems.get()} {item}")
        else:
            for element in self.listaDeFaltantes2:
                e = element.split()
                if e[1] == item:
                    messagebox.showerror("Error","El Item seleccionado ya fue agregado")
                    break  
            else:
                self.listaDeFaltantes2.append(f"{self.spinItems.get()} {item}")
   
        print(self.listaDeFaltantes2)
        return self.listaDeFaltantes2
        
        
            
    def Eliminar_Auricular_Cargador(self):

        self.listaDeFaltantes2.clear()
        """ self.cel1.set(False)
        self.cel2.set(False)
        self.bat1.set(False)
        self.bat2.set(False)
        self.bat3.set(False) """
        self.bool=False

    def GetAuricularCargador(self, equipo):
        db_name = "Database\\dbmochila.db"
        query = "SELECT cargador, auricular FROM dbmochila WHERE codEquipo = ?"
        parameters = (equipo,)
        db_rows = self.run_query(db_name,query,parameters)
        for row in db_rows:
            tupla = row

        lista = []
        lista.append(tupla[0])
        lista.append(tupla[1])

        return lista


    #FUNCIONES DE BASE DE DATOS
    def run_query(self,db_name, query, parameters = ()):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result


    #FUNCIONES PARA CHEQUEAR BOOLEANOS CON CHECKBOX
    def Check_Boolean(self,valor,elem):

        if valor.get() == False:
            valor.set(True)
            self.listaDeFaltantes.append(elem)
        
        elif valor.get() == True:
            valor.set(False)
            self.listaDeFaltantes.remove(elem)

        print(self.listaDeFaltantes)
    
    def Check_Boolean2(self,valor, fila):
        print(valor.get())
        if valor.get() == False:
            valor.set(True)
            self.varMotivo = Entry(self.frameRevision)
            self.varMotivo.grid(row=fila,column=1)
        elif valor.get() == True:
            valor.set(False)
            self.varMotivo = Entry(self.frameRevision, state="readonly")
            self.varMotivo.grid(row=fila,column=1)
            
        return valor, self.varMotivo

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

    def Restar_Stock(self,listaStock, mochi):
        #TRAEMOS LA INFORMACION DE LA TABLA EN UN DICCIONARIO
        db_name = "Database\\dbstock.db"
        query = "SELECT * FROM dbstock"
        db_rows = self.run_query(db_name,query)

        stock = {}
        for i, row in enumerate(db_rows):
            stock[row[1]] = row[2]

        
        #USAMOS LA LISTA FALTANTES PARA RESTAR EN EL STOCK
        
        print(stock)
        listaItem = []
        faltanteOficial = []
        
        dicci = {}
        maxCarAur = self.GetAuricularCargador(mochi)
        dicCarAurTotal = {}
        dicCarAurTotal["Cargadores"] = maxCarAur[0]
        dicCarAurTotal["Auriculares"] = maxCarAur[1]
        dicCarAurTotal["SDI"] = 2

        for i in listaStock:
            item = i.split()
            listaItem.append(item[1])
            dicci[item[1]] = item[0]
        
        print("Esta es la lista de elementos que volvieron")
        print(listaStock)

        for e in stock:
            if e not in listaItem:
                res = int(stock[e]) - 2
                stock[e] = res
                faltanteOficial.append(f"{str(2)} {e}")
            else:
                if int(dicci[e]) == int(dicCarAurTotal[e]):
                    print("No hacer nada")
                else:
                    if int(dicci[e]) == 0:
                        res = int(stock[e]) - 2
                        stock[e] = res
                        faltanteOficial.append(f"{str(2)} {e}")
                    else: 
                        res = int(stock[e]) - int(dicci[e])
                        stock[e] = res
                        faltanteOficial.append(f"{dicci[e]} {e}")


        #CARGAMOS EL DICCIONARIO RESULTANTE NUEVAMENTE A LA BASE DE DATOS
        lista = []
        for key in stock:
            lista.append(key)
            lista.append(stock[key])
            print(lista)

            db_name = "Database\\dbstock.db"
            query = "UPDATE dbstock SET cantidad = ? WHERE item = ?"
            parameters = (lista[1],lista[0])
            db_rows = self.run_query(db_name,query,parameters)
            lista.clear()

        return faltanteOficial


        