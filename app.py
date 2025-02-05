

from flask import Flask, session, jsonify
from flask import render_template, request
from flask import make_response
import datetime as dt
#from flask_wtf import CsrfProtect

import json
import numpy as np
import pandas as pd

import models


app = Flask(__name__)
app.config['SECRET_KEY'] = 'APOCALIPTO'
# csrf = CsrfProtect(app)

@app.route('/')
def init():
    if 'telefono' in session:
        print(session['telefono'])
    return render_template('init.html')

@app.route('/yo')
def yo():
    if 'password' in session and 'telefono' in session:
        yo = models.Usuarios.yo(session['telefono'])
        return make_response(render_template('yo.html', yo = yo))
    return make_response(render_template('login.html'))

@app.route('/facturas')
def facturas():
    if 'password' in session and 'telefono' in session:
        yo = models.Usuarios.yo(session['telefono'])
        facturas = models.Pedidos.facturas(int(yo['id_usuario'][0]))
        return make_response(render_template('facturas.html', yo = yo, facturas = facturas))
    return make_response(render_template('login.html'))

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        usuario = models.Usuarios()
        try:
            nombre = request.form["nombre"]
            apellidos = request.form["apellidos"]
            telefono = request.form["telefono"]
            dip = request.form["dip"]
            password = request.form["clave"]
            ciudad = request.form["ciudad"]
            bario = request.form["bario"]
            usuario.insertar(nombre,apellidos,telefono,dip,password,ciudad,bario)
        finally:
            print(request.form)
            session["telefono"] = telefono
            session["password"] = password
            response = { 'status' : 200, 'usuario' : 'nombre'}
            return json.dumps(response)
    if 'password' in session and 'telefono' in session:
        yo = models.Usuarios.yo(session['telefono'])
        modelo = models.Cargador()
        productos = modelo.principal()
        categoria = ['Electronica','Higiene','Ropas','Electricidad','Educacion','Decoracion']
        return make_response(render_template('index.html', productos = productos, yo = yo, categoria = categoria))
    return make_response(render_template('login.html'))


@app.route('/carro', methods = ['POST', 'GET'])
def carro():
    if 'password' not in session and 'telefono' not in session:
        return make_response(render_template('login.html'))
    if request.method == 'POST':
        estado = request.form['estado']
        if estado == 'eliminar':
            id_producto = int(request.form['id_producto'])
            models.Carro.eliminar(id_producto)
            return json.dumps({ 'estado' : 1 })
        elif estado == 'comprar':
            models.Carro.comprar()
            return json.dumps({ 'estado' : 1 })
        elif estado == 'efectuar':
            y = models.Usuarios.yo(session['telefono'])
            productos = models.Carro.cargar(y['id_usuario'][0])
            for i,e in enumerate(productos['id_producto']):
                models.Pedidos.simple(productos['id_producto'][i], productos['id_usuario'][i], productos['pecha_agregado'][i], productos['precio'][i])
            models.Carro.limpiar(y['id_usuario'][0])
        return json.dumps({ 'estado' : 0 })
    yo = models.Usuarios.yo(session['telefono'])
    productos = models.Carro.cargar(yo['id_usuario'][0])
    total = 0
    try:
        for i,e in enumerate(productos['id_producto']):
            total += float(productos['precio'][i])
    except:
        pass
    return make_response(render_template('carro.html', productos = productos, yo = yo, total = total))


@app.route('/index', methods = ['POST', 'GET'])
def index():
    if 'password' not in session and 'telefono' not in session:
        return make_response(render_template('login.html'))
    yo = models.Usuarios.yo(session['telefono'])
    if request.method == 'POST':
        estado = request.form['estado']
        id_producto = int(request.form['id_producto'])
        precio = float(request.form['precio'])
        id_usuario = int(yo['id_usuario'][0])
        fecha_pedido = dt.datetime.now()
        if estado == 'comprado':
            models.Pedidos.simple(id_producto, id_usuario, fecha_pedido, precio)
    cargador = models.Cargador()
    productos = cargador.principal()
    categoria = ['Electronica','Higiene','Ropas','Electricidad','Educacion','Decoracion']
    return make_response(render_template('index.html', productos = productos, yo = yo, categoria = categoria))


@app.route('/buscar', methods = ['POST', 'GET'])
def buscar():
    tabla = pd.DataFrame()
    if request.method == 'POST':
        dato = str(request.form['dato'])
        resultado = models.Cargador.buscador(dato)
        tabla = resultado
        print(resultado)
        return jsonify(resultado)
    yo = models.Usuarios.yo(session['telefono'])
    categoria = ['Electronica','Higiene','Ropas','Electricidad','Educacion','Decoracion']
    return make_response(render_template('buscar.html', yo = yo, tabla = tabla, categoria = categoria))

@app.route('/f', methods = ['POST'])
def f():
    tabla = pd.DataFrame()
    if request.method == 'POST':
        dato = str(request.form['dato'])
        categoria = ['Electronica','Higiene','Ropas','Electricidad','Educacion','Decoracion']
        resultado = models.Cargador.filtrar(categoria.index(dato))
        tabla = resultado
        print(resultado)
        return jsonify(resultado)

@app.route('/buscar/<id>', methods = ['POST', 'GET'])
def elemento(id):
    idl = int(id) + 1
    telefono = session['telefono']
    yo = models.Usuarios.yo(telefono)
    datos = models.Cargador.det(idl)
    return make_response(render_template('elemento.html', datos = datos, yo = yo))


@app.route('/usr_test', methods = ['POST'])
def test():
    if request.method == 'POST':
        telefono = request.form['telefono']
        try:
            yo = models.Usuarios.yo(telefono)
        finally:
            if yo['id_usuario'][0]:
                return json.dumps({'estado' : 1 })
        return json.dumps({'estado' : 0 })

@app.route('/enter', methods = ['POST'])
def enter():
    if request.method == 'POST':
        telefono = request.form['telefono']
        clave = request.form['pass']
        yo = models.Usuarios.yo(telefono)
        if yo['password'][0] == clave:
            session["telefono"] = telefono
            session["password"] = clave
            return json.dumps({'estado' : 1 })
        return json.dumps({'estado' : 0 })

@app.route('/dcarro', methods = ['POST'])
def dcarro():
    if request.method == 'POST':
        yo = models.Usuarios.yo(session['telefono'])
        id_producto = request.form['id_producto']
        precio = float(request.form['precio'])
        models.Carro.insertar(id_producto, precio, id_cliente = yo['id_usuario'][0])
        return json.dumps({'estado' : 1 })


if __name__ == '__main__':
    app.run(debug = True, port = 1000)
