import datetime as dt
import psycopg2
import pandas as pd

# Configura las variables de entorno
URL = "postgresql://postgres.aaayhwqxqyklufnvpqnj:#Admin_root0@aws-0-us-west-1.pooler.supabase.com:6543/postgres"

# Función para obtener la conexión a PostgreSQL
def get_connection():
    conn = psycopg2.connect(URL)
    return conn 

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
    
    def buscador(self, dato):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM productos WHERE nombre LIKE %s", ('%' + dato + '%',))
                datos = cursor.fetchall()
        finally:
            conexion.close()
        return datos
    
    def filtrar(self, dato):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM productos WHERE id_categoria = %s", (dato,))
                datos = cursor.fetchall()
        finally:
            conexion.close()
        return datos
    
    def det(self, id):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,))
                datos = cursor.fetchall()
        finally:
            conexion.close()
        return pd.DataFrame(datos)

class Usuarios:
    def insertar(self, nombre, apellidos, telefono, dip, password, ciudad, bario, ubicacion='000,0', des_ubicacion='no lo tengo claro'):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO usuarios (nombre, apellidos, telefono, dip, password, ciudad, bario, ubicacion, desc_ubicacion)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (nombre, apellidos, telefono, dip, password, ciudad, bario, ubicacion, des_ubicacion))
                conexion.commit()
        finally:
            conexion.close()

    def yo( telefono):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE telefono = %s", (telefono,))
                yo = cursor.fetchall()
        finally:
            conexion.close()
        return(yo)
        
class Pedidos:
    def simple(self, id_producto, id_cliente, precio, estado='pedido'):
        fecha = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Aseguramos que la fecha esté en el formato correcto
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO pedidos (id_producto, id_cliente, fecha_pedido, precio, estado)
                    VALUES (%s, %s, %s, %s, %s)
                """, (id_producto, id_cliente, fecha, precio, estado))
                conexion.commit()
        finally:
            conexion.close()

    def facturas(self, id):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM pedidos
                    INNER JOIN productos ON pedidos.id_producto = productos.id_producto
                    WHERE pedidos.id_cliente = %s
                """, (id,))
                facturas = cursor.fetchall()
        finally:
            conexion.close()
        
        return pd.DataFrame(facturas)

class Carro:
    def insertar(self, id_producto, precio, id_cliente):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO carro (id_producto, precio, id_usuario)
                    VALUES (%s, %s, %s)
                """, (id_producto, precio, id_cliente))
                conexion.commit()
        finally:
            conexion.close()

    def comprar(self, id_producto, precio, id_cliente):
        # Este método es similar a insertar, por lo que lo unificamos con insertar
        self.insertar(id_producto, precio, id_cliente)

    def cargar(self, id_usuario):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    SELECT productos.nombre, productos.precio
                    FROM carro
                    INNER JOIN productos ON carro.id_producto = productos.id_producto
                    WHERE carro.id_usuario = %s
                """, (id_usuario,))
                productos = cursor.fetchall()
        finally:
            conexion.close()
        
        return pd.DataFrame(productos)

    def eliminar(self, id_producto):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM carro WHERE id_producto = %s", (id_producto,))
                conexion.commit()
        finally:
            conexion.close()

    def limpiar(self, id_usuario):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM carro WHERE id_usuario = %s", (id_usuario,))
                conexion.commit()
        finally:
            conexion.close()
