'''
Created on 19/12/2018

@author: a16daviddss
'''

import sqlite3


# este bloque de codigo nos conecta a la base de datos
try:
    bd = 'Provincias'
    conex = sqlite3.connect(bd)
    cur = conex.cursor()
    print('Conectado a la base de datos')
except sqlite3.OperationalError as e:
    print(e)
    

def cargarCombo(list):
    """
        Anade todas las provincias al combo de provincias
    """
    
    try:
        cur.execute("select provincia from Provincias")
        res = cur.fetchall()
        list.clear()
        for row in res:
            
            list.append(row)
    except sqlite3.OperationalError as e:
        print(e)
    
def cargarmun(listmun,prov):
    """
        Anade todos los municipios de una determinada provincia al combobox de municipios
    """
    try:
        cur.execute("select municipio from municipios where provincia_id = "+str(prov+1)+" order by id")
        res = cur.fetchall()
        listmun.clear()
        for row in res:
           
            listmun.append(row)
    except sqlite3.OperationalError as e:
        print(e)
        
        
def recuperarprovincia(provincia):
    """
        Recoge el id de una provincia de la base de datos y lo devuelve restandole 1 para que pueda ser usado en el combobox
    """
    try:
        cur.execute("select id from provincias where provincia ='" + provincia + "'")

        idprovincia = cur.fetchall()

        return idprovincia[0][0]-1


    except sqlite3.OperationalError as e:
        print(e)
        conex.rollback

def recuperarmunicipio(provincia,localidad):
    """
        recibiendo un id de provincia y un municipo obtiene el id del municipio y los id maximo y minimo de municipios de esa provincia,
        con esos datos traduce el id del municipio a la posicion que este tendra en el combobox y devuelve esta posicion
    """
    try:
        cur.execute("select id from municipios where municipio='"+localidad+"' ORDER BY ID")
        print(localidad)
        idlocalidad = cur.fetchall()
        print(idlocalidad)
        cur.execute("select min(id),max(id) from municipios where provincia_id ='" + str(provincia+1) + "'")
        minmax = cur.fetchall()
        numero = minmax[0][1]-minmax[0][0] + 1 
        print(numero)
        pos=numero-(minmax[0][1]-idlocalidad[0][0])
        print(pos)

        return pos


    except sqlite3.OperationalError as e:
        print(e)
        conex.rollback
        
