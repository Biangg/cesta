import datetime as dt
import os
import psycopg2
import pandas as pd

# Configura las variables de entorno
DB_HOST = os.getenv("DB_HOST", "dpg-cud4hvogph6c738lbpdg-a")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "tu_contraseña_segura")  # NO compartas esto públicamente
DB_NAME = os.getenv("DB_NAME", "nkuen")

# Función para obtener la conexión a PostgreSQL
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    
class Cargador:
    def principal(self):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM productos")
                productos = cursor.fetchall()
        finally:
            conexion.close()
        return pd.DataFrame(productos)
    
    def buscador(dato):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(f"SELECT * FROM productos WHERE nombre LIKE '%{dato}%' ")
                datos = cursor.fetchall()
        finally:
            conexion.close()
        return datos
    
    def filtrar(dato):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(f"SELECT * FROM productos WHERE id_categoria = '{dato}' ")
                datos = cursor.fetchall()
        finally:
            conexion.close()
        return datos
    
    def det(id):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(f"SELECT * FROM productos WHERE id_producto = '{id}' ")
                datos = cursor.fetchall()
        finally:
            conexion.close()
        return pd.DataFrame(datos)

class Usuarios:
    def insertar(self, nombre, apellidos, telefono, dip, password, ciudad, bario, ubicacion = '000,0', desc_ubicacion = 'no lo tengo claro'):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(f"INSERT INTO usuarios(nombre, apellidos, telefono, dip, password, ciudad, bario, ubicacion, desc_ubicacion) VALUES ('{nombre}', '{apellidos}', '{telefono}', '{dip}', '{password}', '{ciudad}', '{bario}', '{ubicacion}', '{desc_ubicacion}' )")
                conexion.commit()
        finally:
            conexion.close()

    def yo(telefono):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(f"SELECT * FROM usuarios WHERE telefono = '{telefono}' ")
                yo = cursor.fetchall()
        finally:
            conexion.close()
        return pd.DataFrame(yo)

class Pedidos:
    def simple(id_producto, id_cliente, fecha_pedido, precio, estado = 'pedido'):
        fecha = dt.datetime.now()
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(f"INSERT INTO pedidos(id_producto, id_cliente, fecha_pedido, precio, estado) VALUES ('{id_producto}', '{id_cliente}', '{fecha}', '{precio}', '{estado}')")
                conexion.commit()
        finally:
            conexion.close()
    def facturas(id):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(f"SELECT * FROM pedidos INNER JOIN productos ON pedidos.id_cliente = '{id}' and pedidos.id_producto = productos.id_producto")
                facturas = cursor.fetchall()
        finally:
            conexion.close()
        print(pd.DataFrame(facturas))
        return pd.DataFrame(facturas)

class Carro:
    def insertar(id_producto, precio, id_cliente):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(f"INSERT INTO carro(id_producto, precio, id_usuario) VALUES ('{id_producto}', '{precio}', '{id_cliente}')")
                conexion.commit()
        finally:
            conexion.close()
    def comprar(id_cliente):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(f"INSERT INTO carro(id_producto, precio, id_usuario) VALUES ('{id_producto}', '{precio}', '{id_cliente}')")
                conexion.commit()
        finally:
            conexion.close()
    def cargar(id_usuario):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(f"SELECT * FROM carro INNER JOIN productos ON carro.id_producto = productos.id_producto ")
                productos = cursor.fetchall()
        finally:
            conexion.close()
        return pd.DataFrame(productos)
    def eliminar(id_producto):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(f"DELETE FROM carro WHERE id_producto = '{id_producto}' ")
                conexion.commit()
        finally:
            conexion.close()
    def limpiar(id_usuario):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(f"DELETE FROM carro WHERE id_usuario = '{id_usuario}' ")
                conexion.commit()
        finally:
            conexion.close()
