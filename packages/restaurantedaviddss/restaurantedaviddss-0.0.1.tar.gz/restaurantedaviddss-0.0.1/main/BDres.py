'''
Created on 10/01/2019

@author: a16daviddss
'''
from passlib.hash import pbkdf2_sha256
import sqlite3
import GestionClientes
import locale
import GestionProd
import GestionMesas
import GestionFacturas
from gi.overrides.Gtk import Gtk

# este bloque de codigo nos conecta a la base de datos
try:
    bd = 'Restaurante'
    conex = sqlite3.connect(bd)
    cur = conex.cursor()
    print('Conectado a la base de datos')
except sqlite3.OperationalError as e:
    print(e)
    
    
def altaCliente(listclientes, treeclientes, row):
    try:
        cur.execute("insert into clientes (dni,nombre,apellidos,direccion,provincia,ciudad) values(?,?,?,?,?,?)", row)
        conex.commit()
        GestionClientes.altacli(listclientes, treeclientes, row)
    except sqlite3.OperationalError as e:
        print (e)

        
def cargarCli(listclientes, treeclientes):
    try:
        cur.execute("select * from clientes")
        listclientes.clear()
        rows = cur.fetchall()
        for row in rows:
            GestionClientes.altacli(listclientes, treeclientes, row)
    except sqlite3.OperationalError as e:
        print(e)

        
def login(user, ps):
    """
        Recibe un usuario y contraseña de la ventana de login, busca el usuario y la contraseña en la base de datos,
        comprueba lo que recibe coincide lo que hay en la base de datos mediante el metodo pbkdf2_sha256.verify("texto",hash),
        de la libreria passlib y devuelve True y el id del camarero si es correcto o False si el login no es correcto.
    """
    try:
        cur.execute("select id,pass from camareros where nombre = '" + user + "'")
        rows = cur.fetchall()
        
        for row in rows:
            # if pbkdf2_sha256.verify(user,row[1]):
            if pbkdf2_sha256.verify(ps, row[1]):
                return (True, row[0])
                
        return False
    except sqlite3.OperationalError as e:
        print(e)


def registrar(user, pwd, listcamarero, treecamareros):
    """
        obtiene el hash de la contraseña que recibe y añade al camarero a la base de datos si no existe ya
    """
    try:
        passwd = pbkdf2_sha256.hash(pwd) 
        fila = (user, passwd)
        cur.execute("insert into camareros (nombre,pass) values(?,?)", fila)
        conex.commit()
        cargarcamareros(listcamarero, treecamareros)
    except sqlite3.OperationalError as e:
        print(e)


def getcamarero(idfactura):
    try:
        cur.execute("select nombre from camareros where id = (select camarero from facturas where id ='" + str(idfactura) + "')")
        res = cur.fetchall()
        
        return res[0][0]
    except sqlite3.OperationalError as e:
        print(e)
                

def cargarcamareros(listcamarero, treecamareros):
    try:
        listcamarero.clear()
        cur.execute("select id, nombre from camareros order by id")
        rows = cur.fetchall()
        for row in rows:
            listcamarero.append(row)
            treecamareros.show()
    except sqlite3.OperationalError as e:
        print(e)
    
        
def altaserv(listserv, treeserv, row):
    try:
        cur.execute("insert into servicios (servicio,precio) values(?,?)", row)
        conex.commit()
        cur.execute("select count(*) from servicios")
        fila = []
        filas = cur.fetchall()
        for f in filas:
            fila.append(f[0])
        fila.append(row[0])
        locale.setlocale(locale.LC_ALL, '')
        fila.append(locale.currency(row[1]))
        GestionProd.altaserv(listserv, treeserv, fila)
    except sqlite3.OperationalError as e:
        print(e)
        
        
def cargaserv(listserv, treeserv):
    try:
        cur.execute("select * from servicios")
        rows = cur.fetchall()
        for row in rows:
            fila = []
            fila.append(row[0])
            fila.append(row[1])
            locale.setlocale(locale.LC_MONETARY, '')
            fila.append(locale.currency(row[2]))
            GestionProd.altaserv(listserv, treeserv, fila)
    except sqlite3.OperationalError as e:
        print(e)
        
        
def cargamesas(dicmesas, treemesas, listmesas):
    try:
        cur.execute("select * from mesas")
        rows = cur.fetchall()
        listmesas.clear()
        ocupada = "no"
        for row in rows:
            if row[2] == 1:
                ocupada = "si"
                dicmesas[row[0]].set_sensitive(False)
                if row[1] == 4:
                    dicmesas[row[0]].get_image().set_from_file("./mesa4oc.png")
                elif row[1] == 8:
                    dicmesas[row[0]].get_image().set_from_file("./mesa8ocv2.png")
                else:
                    dicmesas[row[0]].get_image().set_from_file("./mesa10oc.png")
            else:
                ocupada = "no"
                dicmesas[row[0]].set_sensitive(True)
                if row[1] == 4:
                    dicmesas[row[0]].get_image().set_from_file("./mesa4vacia.png")
                elif row[1] == 8:
                    dicmesas[row[0]].get_image().set_from_file("./mesa8vaciav2.png")
                else:
                    dicmesas[row[0]].get_image().set_from_file("./mesa10vacia.png")
            fila = (row[0], row[1], ocupada)
            GestionMesas.insertarmesa(treemesas, listmesas, fila)
        
    except sqlite3.OperationalError as e:
        print (e)

        
def insmesa(dicmesas, treemesas, listmesas, fila):
    try:
        cur.execute("update mesas set ocupada = 1 where id = " + fila[2] + "")
        cur.execute("insert into facturas (cliente,camarero,mesa,fecha) values(?,?,?,?)", fila)
        conex.commit()
        listmesas.clear()
        cargamesas(dicmesas, treemesas, listmesas)
    except sqlite3.OperationalError as e:
        print (e) 

        
def checkOcupada(mesa):
    try:
        cur.execute("select ocupada from mesas where id = " + str(mesa))
        rows = cur.fetchall()
        if rows[0][0] == 1:
            return True
        return False
    except sqlite3.OperationalError as e:
        print(e)

        
def checkfacturas(treefact, listfact, id):
    try:
        cur.execute("select * from facturas where mesa=" + str(id))
        rows = cur.fetchall()
        listfact.clear()
        for row in rows:
            if row[5] == 0:
                fila = (row[0], row[1], row[2], row[3], row[4], "NO")
                print(fila)
                GestionFacturas.insfact(treefact, listfact, fila)
            else:
                fila = (row[0], row[1], row[2], row[3], row[4], "SI")
                GestionFacturas.insfact(treefact, listfact, fila)
    except sqlite3.OperationalError as e:
        print(e)
        
       
def verlineas(treelineas, listlineas, id):
    try:
        cur.execute("select idventa,factura,(select servicio from servicios where id = producto),cantidad from lineasfactura where factura=" + str(id)) 
        rows = cur.fetchall()
        listlineas.clear()
        for row in rows:
            print(row)
            listlineas.append(row)
            treelineas.show()
    except sqlite3.OperationalError as e:
        print(e)   


def addlinea(treelineas, listlineas, fila):
    try:
        cur.execute("select * from lineasfactura where factura = "+str(fila[0])+" and producto = "+str(fila[1]))
        lin = cur.fetchall()
        print("a")
        if lin !=[]:
            print(str(lin[0][2]+fila[2]))
            cur.execute("update lineasfactura set cantidad = "+str(lin[0][3]+fila[2]) +" where producto ="+str(fila[1]))
            conex.commit()
        else:    
            cur.execute("insert into lineasfactura (factura,producto,cantidad) values(?,?,?)", fila)
            conex.commit()
        listlineas.clear()
        verlineas(treelineas, listlineas, fila[0])
    except sqlite3.OperationalError as e:
        print(e)

        
def getfact(id):
    try:
        cur.execute("select * from facturas where id =" + str(id))
        f = cur.fetchall()
        return f[0]
    except sqlite3.OperationalError as e:
        print(e)    
        
        
def getlineas(id):
    try:
        cur.execute("select * from lineasfactura where factura=" + str(id))
        f = cur.fetchall()
        return f
    except sqlite3.OperationalError as e:
        print(e)

        
def getnompre(idp):
    try:
        cur.execute("select servicio,precio from servicios where id=" + str(idp))
        f = cur.fetchone()
        return f
    except sqlite3.OperationalError as e:
        print(e) 


def pagar(id, mesa, listfact, treefact, listcom):
    try:
        cur.execute("update facturas set pagada=1 where id =" + str(id))
        cur.execute("update mesas set ocupada=0 where id=" + str(mesa))
        conex.commit()
        checkfacturas(treefact, listfact, mesa)
        listcom.clear()
    except sqlite3.OperationalError as e:
        print(e)

        
