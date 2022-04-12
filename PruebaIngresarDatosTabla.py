import sqlite3
import os


db_name = os.getcwd()+"\\Database\\dbbateria.db"

ruta = os.getcwd()

f = open(ruta + "\\Datos CSV\\Bateria.csv", "r")
lista = f.readlines()



with sqlite3.connect(db_name) as conn:
    for dato in lista:
        if(dato == lista[0]):
            continue

        datos = dato.split(";")
        
        cursor = conn.cursor()
        query = "INSERT INTO dbbateria VALUES(NULL, ? ,?, ?, ?, 0)"
        parameters = (datos[0].strip(),datos[1].strip(),datos[2].strip(),datos[3].strip())
        result = cursor.execute(query, parameters)
        conn.commit()  
    


 