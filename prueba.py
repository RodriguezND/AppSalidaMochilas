from tkinter import *
from index import Principal
from openpyxl import load_workbook
from http import client
from win32com import client 
import os
import sqlite3


def run_query(db_name, query, parameters = ()):
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, parameters)
        conn.commit()
    return result


if __name__ == "__main__":


    db_name = "Database\\dbstock.db"
    query = "SELECT * FROM dbstock"
    db_rows = run_query(db_name,query)
    stock = {}
    for i, row in enumerate(db_rows):
        stock[row[1]] = row[2]

    print(stock)

    res = int(stock["Cargadores"]) - 1
    stock["Cargadores"] = res

    print(stock)
    lista =[]
    for key in stock:
        lista.append(key)
        lista.append(stock[key])
        print(lista)

        db_name = "Database\\dbstock.db"
        query = "UPDATE dbstock SET cantidad = ? WHERE item = ?"
        parameters = (lista[1],lista[0])
        db_rows = run_query(db_name,query,parameters)


    """ window = Tk()
    window.geometry("800x500")

    car1 = BooleanVar()
    cbCargador1 = Checkbutton(window, text="Cargador", variable=car1,onvalue=True,offvalue=False, command=lambda: prueba())
    cbCargador1.grid(row=2, column=2)


    def prueba():
        print( car1.get())

    currentDir = os.getcwd()+""
    ruta_excel = currentDir + "\\remito.xlsx"
    ruta_pdf = "C:\\Users\\rodrigne\\Desktop\\GITMochilas\\" 
    
    print(currentDir)
    #EXCEL a PDF

    xlApp = client.Dispatch("Excel.Application")
    books = xlApp.Workbooks.Open("C:\\Users\\rodrigne\\Desktop\\GITMochilas\\remito.xlsx")
    ws = books.Worksheets[0] 
    ws.Visible = 1
    ws.ExportAsFixedFormat(0,currentDir+"\\saraza.pdf") 
    books.Close()
    window.mainloop()  """