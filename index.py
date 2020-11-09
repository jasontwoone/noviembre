import os
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session
from flask import escape 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify
from flask import g
import sqlite3
from requests import get
from Datos.receta import Receta 
import json
from Datos.Usuario import Usuario 
Usuario1 = Usuario("admin", "admin")

Usuarios = [Usuario1]

Recetas = [
    {
        "id": 1,
        "title": "1. - preparacion de alimentos"
    },
    {
        "id": 2,
        "title": "1. - preparacion de alimentos"
       
    }
        ]

Recetas_recientes = [
    {
        "id": 1,
        "title": "1. - preparacion de alimentos"
    },
    {
        "id": 2,
        "title": "1. - preparacion de alimentos"
      
    }
        ]        

dbdir = "sqlite:///" + os.path.abspath(os.getcwd()) + "/database.db"

app = Flask(__name__) #app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = dbdir


db = SQLAlchemy(app)


@app.route("/recetario")
def get_all_recetas():
    
    return jsonify({"tiprecetas": {"tipoRece": Recetas, "TipoRece2": Recetas_recientes}})


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    nombre = db.Column(db.String(80), nullable=False)
    Apellido = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(80), nullable=False)


class ListaRecetas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    autor = db.Column(db.String(80), nullable=False)
    Titulo = db.Column(db.String(80), nullable=False)




@app.before_request
def before_request():
    if "username" in session:
        g.user = session["username"]
    else: 
        g.user = None


@app.route('/')  #wrap o un decorador
def index():
    return  render_template('home.html') 



@app.route('/login', methods=['GET', 'POST'])  #wrap o un decorador
def login():  
    art=g.user
    ingreso_correcto = 'ingreso correcto'
    ingreso_incorrecto = 'ingreso correcto'
    if request.method == 'POST':
        user = Users.query.filter_by(username=request.form['uname']).first()

        if user and (user.Password, request.form['psw'] ):

            session["username"] = user.username
            return  render_template('login_status.html', ingreso_correcto = ingreso_correcto, art=art )

        return  render_template( 'login-form.html', ingreso_incorrecto = ingreso_incorrecto )

    return  render_template('login-form.html') 



@app.route("/home")
def home():
    if g.user:
        
        return "you are %s" % g.user

    return "debes iniciar primero"

@app.route("/logout")
def logout():
    session.pop('username', None)
    return render_template('login-form.html') 


app.secret_key = "12345"

@app.route('/registro', methods=['GET', 'POST'])  #wrap o un decorador
def registro():
    error = 'Contraseña invalida'
    if request.method == "POST":
        if (request.form['psw']) == (request.form['psw-repeat']):
            
            new_user = Users(username = request.form['nombre_usuario'], nombre = request.form['Nombre'] ,
            Apellido = request.form['apellido'], email = request.form['email'], Password=request.form['psw'])
            db.session.add(new_user)
            db.session.commit()
            return "Registrado correctamente"
        return render_template('register_user.html', error=error) 
    return  render_template('register_user.html') 

recetas=['pizza','pastel','pollo']

@app.route("/home_log")
def home_log():
    asl= url_for("home")
    return url_for("home", next="login")

@app.route("/google")
def ir_a_google():
    return redirect("https://www.google.com/")

@app.route ("/post/<int:id>")  
def post(id):
    return "showing post: {}".format(id)

@app.route("/today")
def today():
    return redirect(url_for("post",id=50, next="edit"))

@app.route("/receta_form")
def receta_form():
    
    return render_template('receta_form.html') 

@app.route("/acerca_de")
def acerca_de():
    return render_template('acerca_de.html')
    
@app.route("/contactenos")
def contactenos():
    return render_template('contactenos.html')



@app.route('/recuperar_contraseña',methods=['POST'])
def recuperar_contraseña():
    if request.method == "POST":
        username_recu = request.form['uname']
        usuariobuscar = Users.query.filter(Users.username==username_recu).first()
        resulta = usuariobuscar.Password
        return render_template('forget_password.html', resulta=resulta)
    return "busqueda mal"

@app.route('/forget_password.html')
def forget_password():
    resultado = Users.query.all()
    for r in resultado:
        nombreus = r.username 
        print(r.username)
    return render_template('forget_password.html',resultado = resultado, nombreus = nombreus)

@app.route('/agregar_receta', methods=['GET', 'POST'])
def agregar_recetas():
    
    new_Receta = ListaRecetas(autor = "jjjj" , Titulo = "receta")
    db.session.add(new_Receta)
    db.session.commit()

    return ( "agregado bien")
        
    



if __name__ == "__main__":  
    db.create_all()

    app.run( debug=False, port = 5000)  # esto se encarga de ejecutar en el servidors

