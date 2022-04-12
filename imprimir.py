from importlib.resources import path
from tkinter import *
from openpyxl import load_workbook
from openpyxl.drawing.image import Image

import sqlite3
from win32com import client 
from os import system
import os


class Imprimir:

    patha = 'remito.xlsx'
    
    id=0

    def __init__(self, entrega, equipo, productor, cobertura, fechaEntrega,c1,c2,b1,b2,b3, observaciones):
        currentDir = os.getcwd()
        book = load_workbook(self.patha)
        hoja1=book["REMITO_IMP"]
        image = Image(currentDir+'\\Image\\disney.png')
        hoja1.add_image(image,"B3")
        image2 = Image(currentDir+'\\Image\\espn.png')
        hoja1.add_image(image2,"D3")

        #FECHA ENTREGA
        fechaMes = self.cambiar_mes(fechaEntrega)
        hoja1['C15'] = f"{fechaMes[0]} de {fechaMes[1]} de {fechaMes[2]}"
        
        lista = self.Recuperar_Equipo(equipo)

        #DESCRIPCION EQUIPO
        hoja1['B27'] = "Mochila: " + lista[0]
        hoja1['D27'] = lista[1]
        hoja1['E27'] = lista[2]

        lista = self.Recuperar_Celular(c1)
        #DESCRIPCION CEL1
        hoja1['B28'] = f"Telefono Modelo: {lista[0]}, Linea Nro: {lista[1]}, Codigo: {lista[2]}"
        hoja1['D28'] = lista[3]
        hoja1['E28'] = lista[4]

        lista = self.Recuperar_Celular(c2)
        #DESCRIPCION CEL2
        hoja1['B29'] = f"Telefono Modelo: {lista[0]}, Linea Nro: {lista[1]}, Codigo: {lista[2]}"
        hoja1['D29'] = lista[3]
        hoja1['E29'] = lista[4]

        lista = self.Recuperar_Bateria(b1)
        #DESCRIPCION BAT1
        hoja1['B30'] = f"Bateria: {lista[0]}"
        hoja1['D30'] = lista[1]
        hoja1['E30'] = lista[2]

        lista = self.Recuperar_Bateria(b2)
        #DESCRIPCION BAT2
        hoja1['B31'] = f"Bateria: {lista[0]}"
        hoja1['D31'] = lista[1]
        hoja1['E31'] = lista[2]

        lista = self.Recuperar_Bateria(b3)
        #DESCRIPCION BAT3
        hoja1['B32'] = f"Bateria: {lista[0]}"
        hoja1['D32'] = lista[1]
        hoja1['E32'] = lista[2]

        lista = self.Recuperar_CargadorAuricular(equipo)
        #CARGADOR
        hoja1['B33'] = f"Cargador: {lista[0]}"
        #AURICULAR 
        hoja1['B34'] = f"Auricular: {lista[1]}"

        lista = self.Recuperar_ID(equipo)
        #ID SALIDA MOCHILA
        hoja1['C44'] = lista[0]

        #COBERTURA
        hoja1['B47'] = "Cobertura: " + cobertura

        #OBSERVACIONES
        hoja1['B49'] = "Observaciones: " + observaciones

        #ENTREGA
        hoja1['C53'] = f"Preparada por {entrega}"

        #PRODUCTOR
        hoja1['C59'] = productor

        book.save(self.patha)
        
        
        """ ruta_excel = currentDir + "\\remito.xlsx"
        ruta_pdf = "C:\\Users\\rodrigne\\Desktop\\GITMochilas\\"  """

        system('md "C:\\remito"')
        system('copy remito.xlsx C:\\remito')  
        
        print(currentDir)
        #EXCEL a PDF

        xlApp = client.Dispatch("Excel.Application")
        books = xlApp.Workbooks.Open("C:\\remito\\remito.xlsx")
        ws = books.Worksheets[0] 
        ws.Visible = 1
        ws.ExportAsFixedFormat(0,"C:\\remito\\saraza.pdf") 
        books.Close()

        os.startfile("C:\\remito\\remito.xlsx", "print")

        """ system('timeout 3')
        system('NET USE LPT1 \\fsfnprp76c01b\Print-B4 /PERSISTENT:YES')
        system('timeout 3')
        system('print /d:LPT1 C:\\remito\\saraza.pdf') """

        print("Abierto")

    
    def run_query(self, db_name, query, parameters = ()):
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result
    
    def Recuperar_Equipo(self,equipo):
        
        db_name = "Database\\dbequipo.db"

        query = "SELECT codigoEquipo, equipo, serialNumber FROM dbequipo WHERE codigoEquipo = ? "
        parameters = (equipo,)

        db_rows = self.run_query(db_name, query, parameters)

        lista = []
        for row in db_rows:
            lista.append(row[0])
            lista.append(row[1])
            lista.append(row[2])

        return lista

    def Recuperar_Celular(self,c):
        
        if c != 0:
            db_name = "Database\\dbcelular.db"

            query = "SELECT modelo, linea, codigoCelular, marca, serialNumber FROM dbcelular WHERE codigoCelular = ? "
            parameters = (c,)

            db_rows = self.run_query(db_name, query, parameters)

            lista = []
            for row in db_rows:
                lista.append(row[0])
                lista.append(row[1])
                lista.append(row[2])
                lista.append(row[3])
                lista.append(row[4])

            return lista
        else:
            lista = ["-","-","-","-","-"]
            return lista

    def Recuperar_Bateria(self,b):
        
        if b != 0:
            db_name = "Database\\dbbateria.db"

            query = "SELECT codigoBateria, marca, serialNumber FROM dbbateria WHERE codigoBateria = ? "
            parameters = (b,)

            db_rows = self.run_query(db_name, query, parameters)

            lista = []
            for row in db_rows:
                lista.append(row[0])
                lista.append(row[1])
                lista.append(row[2])

            return lista
        else:
            lista = ["-","-","-"]
            return lista

    def Recuperar_CargadorAuricular(self, equipo):
        
        db_name = "Database\\dbmochila.db"

        query = "SELECT cargador, auricular FROM dbmochila WHERE codEquipo = ? "
        parameters = (equipo,)

        db_rows = self.run_query(db_name, query, parameters)

        lista = []
        for row in db_rows:
            lista.append(row[0])
            lista.append(row[1])

        return lista

    def Recuperar_ID(self, equipo):
        
        db_name = "Database\\dbsalidamochilas.db"

        query = "SELECT idSalidaMochila FROM dbsalidaMochilas WHERE codigoMochila = ? "
        parameters = (equipo,)

        db_rows = self.run_query(db_name, query, parameters)

        lista = []
        for row in db_rows:
            lista.append(row[0])

        return lista

    def cambiar_mes(self, fechaarg):
        fechahora = fechaarg.split("-")
        fecha = fechahora[0].split("/")

        if fecha[1] == "01":
            fecha[1] = "Enero"
        if fecha[1]== "02":
            fecha[1] = "Febrero"
        if fecha[1] == "03":
            fecha[1] = "Marzo"
        if fecha[1] == "04":
            fecha[1] = "Abril"
        if fecha[1] == "05":
            fecha[1] = "Mayo"
        if fecha[1] == "06":
            fecha[1] = "Junio"
        if fecha[1] == "07":
            fecha[1] = "Julio"
        if fecha[1] == "08":
            fecha[1] = "Agosto"
        if fecha[1] == "09":
            fecha[1] = "Septiembre"
        if fecha[1] == "10":
            fecha[1] = "Octubre"
        if fecha[1] == "11":
            fecha[1] = "Noviembre"
        if fecha[1] == "12":
            fecha[1] = "Diciembre"

        fecha[2] = "20"+fecha[2]

        fecha.append(fechahora[1])

        return fecha