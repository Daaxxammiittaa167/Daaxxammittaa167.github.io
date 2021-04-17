from flask import Flask
import sqlite3
from sqlite3 import Error
import os

class conexion:
    def sql_conexion():
        try:
            con=sqlite3.connect('..\\bd\\Cafeteria.db')
            print("Connection is established: Database is created in memory")
            cones=con.cursor()
            print("ntro")
            cones.execute('select nombrep from usuario')
            print("entro")
            rows=cones.fetchall()
            for row in rows:
                print(row)
            return True

        except Error:

            print(Error)
            return False

        finally:

            con.close()

    def sql_insercion(init,datos):
        try:
            con=sqlite3.connect('..\\bd\\Cafeteria.db')
            cones=con.cursor()
            cones.execute(datos)
            con.commit()
            return True
        except Error:
            return False
        finally:
            con.close()

    def sql_actualizar(init,datos):
        try:
            con=sqlite3.connect('..\\bd\\Cafeteria.db')
            cones=con.cursor()
            cones.execute(datos)
            con.commit()
            return True
        except Error:
            return False
        finally:
            con.close()
        return True

    def sql_Eliminacion(init,datos):
        try:
            con=sqlite3.connect('..\\bd\\Cafeteria.db')
            cones=con.cursor()
            cones.execute(datos)
            con.commit()
            return True

        except Error:
            return False
        finally:
            con.close()

    def sql_actualizacion(query,datos):
        try:
            con=sqlite3.connect('..\\bd\\Cafeteria.db')
            cones=con.cursor()
            cones.execute(query,datos)
            cones.commit()
            return True

        except Error:
            return False
        finally:
            con.close()
    
    def sql_ObtenerDatos(init,query):
        try:
            con=sqlite3.connect('..\\bd\\Cafeteria.db')
            cones=con.cursor()
            cones.execute(query)
            rows=cones.fetchall()
            return rows

        except Error:
            return "error"
        finally:
            con.close()


    def sql_ObtenerContador(init,query):
        try:
            con=sqlite3.connect('..\\bd\\Cafeteria.db')
            cones=con.cursor()
            cones.execute(query).rowcount
            rows=cones.fetchone()
            return rows

        except Error:
            return "error"
        finally:
            con.close()
    
#obj=conexion()
#s="select * from estatus"
#val=obj.sql_ObtenerDatos(s)
#sa=val


