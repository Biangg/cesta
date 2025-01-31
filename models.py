
import os
import psycopg2
import pandas as pd

# Configura las variables de entorno
DB_HOST = os.getenv("DB_HOST", "db.aaayhwqxqyklufnvpqnj.supabase.co")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "[YOUR-PASSWORD]")  # Reemplaza con tu contraseña
DB_NAME = os.getenv("DB_NAME", "postgres")

# Función para obtener la conexión a PostgreSQL
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Función para filtrar productos por categoría
def filtrar(dato):
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM productos WHERE id_categoria = %s", (dato,))
            datos = cursor.fetchall()
    finally:
        conexion.close()
    return datos

# Función para obtener detalles de un producto por ID
def det(id):
    conexion = get_connection()
    try:
        with conexion.cursor() as cursor:
            cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id,))
            datos = cursor.fetchall()
    finally:
        conexion.close()
    return pd.DataFrame(datos)

class Usuarios:
    # Función para insertar un nuevo usuario
    def insertar(self, nombre, apellidos, telefono, dip, password, ciudad, bario, ubicacion='000,0', desc_ubicacion='no lo tengo claro'):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO usuarios(nombre, apellidos, telefono, dip, password, ciudad, bario, ubicacion, desc_ubicacion) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (nombre, apellidos, telefono, dip, password, ciudad, bario, ubicacion, desc_ubicacion)
                )
                conexion.commit()
        finally:
            conexion.close()

    # Función para obtener datos de un usuario por teléfono
    def yo(telefono):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM usuarios WHERE telefono = %s", (telefono,))
                yo = cursor.fetchall()
        finally:
            conexion.close()
        return pd.DataFrame(yo)

class Pedidos:
    # Función para crear un pedido simple
    def simple(id_producto, id_cliente, fecha_pedido, precio, estado='pedido'):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO pedidos(id_producto, id_cliente, fecha_pedido, precio, estado) "
                    "VALUES (%s, %s, %s, %s, %s)",
                    (id_producto, id_cliente, fecha_pedido, precio, estado)
                )
                conexion.commit()
        finally:
            conexion.close()

    # Función para obtener facturas de un cliente
    def facturas(id):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM pedidos INNER JOIN productos ON pedidos.id_cliente = %s AND pedidos.id_producto = productos.id_producto",
                    (id,)
                )
                facturas = cursor.fetchall()
        finally:
            conexion.close()
        return pd.DataFrame(facturas)

class Carro:
    # Función para insertar un producto en el carro
    def insertar(id_producto, precio, id_cliente):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO carro(id_producto, precio, id_usuario) VALUES (%s, %s, %s)",
                    (id_producto, precio, id_cliente)
                )
                conexion.commit()
        finally:
            conexion.close()

    # Función para comprar productos en el carro (necesita corrección)
    def comprar(id_cliente):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                # Aquí deberías implementar la lógica de compra
                cursor.execute(
                    "INSERT INTO pedidos(id_producto, precio, id_cliente) "
                    "SELECT id_producto, precio, %s FROM carro WHERE id_usuario = %s",
                    (id_cliente, id_cliente)
                )
                conexion.commit()
        finally:
            conexion.close()

    # Función para cargar productos en el carro de un usuario
    def cargar(id_usuario):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM carro INNER JOIN productos ON carro.id_producto = productos.id_producto WHERE id_usuario = %s",
                    (id_usuario,)
                )
                productos = cursor.fetchall()
        finally:
            conexion.close()
        return pd.DataFrame(productos)

    # Función para eliminar un producto del carro
    def eliminar(id_producto):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM carro WHERE id_producto = %s", (id_producto,))
                conexion.commit()
        finally:
            conexion.close()

    # Función para limpiar el carro de un usuario
    def limpiar(id_usuario):
        conexion = get_connection()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("DELETE FROM carro WHERE id_usuario = %s", (id_usuario,))
                conexion.commit()
        finally:
            conexion.close()
