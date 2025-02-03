
import os
import psycopg2
import pandas as pd

# Configura las variables de entorno
DB_HOST = os.getenv("DB_HOST", "dpg-cud4hvogph6c738lbpdg-a")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "ca0JZkCQyssnhLgzyUKi08Z5FdKt9ozf")  # Reemplaza con tu contraseña
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
        """Obtiene todos los productos de la base de datos."""
        try:
            with get_connection() as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT * FROM productos")
                    productos = cursor.fetchall()
                    columnas = [desc[0] for desc in cursor.description]  # Obtiene nombres de columnas
            return pd.DataFrame(productos, columns=columnas)
        except psycopg2.Error as e:
            print(f"Error en la base de datos: {e}")
            return pd.DataFrame()

    def buscador(self, dato):
        """Busca productos por nombre (evita inyección SQL)."""
        try:
            with get_connection() as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT * FROM productos WHERE nombre ILIKE %s", (f"%{dato}%",))
                    datos = cursor.fetchall()
                    columnas = [desc[0] for desc in cursor.description]
            return pd.DataFrame(datos, columns=columnas)
        except psycopg2.Error as e:
            print(f"Error en la base de datos: {e}")
            return pd.DataFrame()

    def filtrar(self, id_categoria):
        """Filtra productos por categoría."""
        try:
            with get_connection() as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT * FROM productos WHERE id_categoria = %s", (id_categoria,))
                    datos = cursor.fetchall()
                    columnas = [desc[0] for desc in cursor.description]
            return pd.DataFrame(datos, columns=columnas)
        except psycopg2.Error as e:
            print(f"Error en la base de datos: {e}")
            return pd.DataFrame()

    def det(self, id_producto):
        """Obtiene detalles de un producto por ID."""
        try:
            with get_connection() as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT * FROM productos WHERE id_producto = %s", (id_producto,))
                    datos = cursor.fetchall()
                    columnas = [desc[0] for desc in cursor.description]
            return pd.DataFrame(datos, columns=columnas)
        except psycopg2.Error as e:
            print(f"Error en la base de datos: {e}")
            return pd.DataFrame()


class Usuarios:
    def insertar(self, nombre, apellidos, telefono, dip, password, ciudad, barrio, ubicacion="000,0", desc_ubicacion="No definido"):
        """Inserta un nuevo usuario en la base de datos."""
        try:
            with get_connection() as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute(
                        """INSERT INTO usuarios (nombre, apellidos, telefono, dip, password, ciudad, barrio, ubicacion, desc_ubicacion)
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (nombre, apellidos, telefono, dip, password, ciudad, barrio, ubicacion, desc_ubicacion),
                    )
                    conexion.commit()
        except psycopg2.Error as e:
            print(f"Error en la base de datos: {e}")

    def yo(self, telefono):
        """Obtiene la información de un usuario por su número de teléfono."""
        try:
            with get_connection() as conexion:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT * FROM usuarios WHERE telefono = %s", (telefono,))
                    usuario = cursor.fetchall()
                    columnas = [desc[0] for desc in cursor.description]
            return pd.DataFrame(usuario, columns=columnas)
        except psycopg2.Error as e:
            print(f"Error en la base de datos: {e}")
            return pd.DataFrame()


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
