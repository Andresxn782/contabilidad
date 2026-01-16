1. Explicacion del proyecto

Hemos creado un proyecto de contabilidad personal, tiene su login, con el que accedes con tu usuario/correo y contraseña, cuando entras tienes varias cosas, una barra a la izquierda con los apartados y luego en el centro el sueldo actual y abajo los ingresos, los gastos y un historial de tu cuenta y luego en el menu de la izquierda cada apartado.

La aplicacion esta hecha para personas jovenes, sin muchos ingresos, para que puedan ahorrar dinero y ver sus gastos e ingresos claramente, aparte de una tabla grafica y los presupuestos que tienen previstos para el siguiente mes.

2. Moddelo de datos

├── README.md
├── app.py
├── db.sql
├── inserciones.sql
├── static
│ ├── css
│ │ ├── estadisticas.css
│ │ ├── gastos.css
│ │ ├── ingresos.css
│ │ ├── login.css
│ │ ├── panel.css
│ │ ├── perfil.css
│ │ └── presupuestos.css
│ └── js
│ ├── gastos.js
│ ├── ingresos.js
│ ├── login.js
│ └── panel.js
└── templates
├── estadisticas.html
├── gastos.html
├── ingresos.html
├── login.html
├── panel.html
├── perfil.html
└── presupuestos.html

Este de aqui es el modelo de datos, como se puede ver el proyecto se divide en dos carpetas para el front, static y templates, en static se añaden los css y js en sus respectivas carpetas y en templates los html, y luego esta el app.py lo importante en este examen y lo que te voy a explicar acontinuacion, para que sirve el por que lo hemos creado y la explicacion de codigo.

El app.py sirve para hacer la comunicacion entre la base de datos y el front sin el hacer funcionar la aplicacion seria imposible, ya que estarian las dos cosas separadas y no se podrian juntar.

Lo hemos creado para que la aplicacion pudiera funcionar, para que uniera la base de datos y el front y configurarlo para que los datos de la base de datos aparzcan en el front y asi porde hacer bien las inserciones y que cuando hagamos por ejemplo un ingreso se guarde en la base de datos desde el front.

Ahora voy a explicarte el codigo :

´´´

# Importamos Flask y las funciones necesarias para renderizar plantillas

# manejar formularios redirecciones y respuestas en formato JSON

from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql

# Creamos la aplicacion Flask

app = Flask(**name**)

# ------------------ CONEXION A LA BASE DE DATOS ------------------

# Esta funcion se encarga de crear y devolver la conexion a MySQL

# Se usa cada vez que se necesita acceder a la base de datos

def obtener_db():
return pymysql.connect(
host="localhost",
user="usuario_app",
password="Contabilidad123$",
database="contabilidad",
cursorclass=pymysql.cursors.DictCursor
)

# ------------------ LOGIN ------------------

# Ruta principal de la aplicacion

# Permite acceder tanto por GET como por POST

@app.route('/', methods=['GET', 'POST'])
def login(): # Si el formulario se envia
if request.method == 'POST': # Se recogen los datos introducidos por el usuario
email = request.form['email']
password = request.form['password']

        # Conexion a la base de datos
        db = obtener_db()
        cursor = db.cursor()

        # Consulta para comprobar si existe el usuario
        cursor.execute(
            "SELECT * FROM usuarios WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cursor.fetchone()
        db.close()

        # Si el usuario existe se redirige al panel
        if user:
            return redirect(url_for('panel', usuario_id=user['id']))
        else:
            # Si no existe se muestra un mensaje de error
            return render_template('login.html', error="Usuario o contraseña incorrectos")

    # Si se accede por GET se muestra el login
    return render_template('login.html')


    Este apartado gestiona el inicio de sesión del usuario, recoge el email y la contraseña del formulario y los compara con la base de datos si los datos son correctos redirige al usuario al panel principal y si no lo son vuelve a mostrar el login con un mensaje de error

# ------------------ PANEL ------------------

# Ruta del panel principal del usuario

@app.route('/panel/<int:usuario_id>')
def panel(usuario_id):
db = obtener_db()
cursor = db.cursor()

    # Se calcula el total de ingresos del usuario
    cursor.execute(
        "SELECT COALESCE(SUM(cantidad),0) as total FROM ingresos WHERE usuario_id=%s",
        (usuario_id,)
    )
    total_ingresos = cursor.fetchone()['total']

    # Se calcula el total de gastos del usuario
    cursor.execute(
        "SELECT COALESCE(SUM(cantidad),0) as total FROM gastos WHERE usuario_id=%s",
        (usuario_id,)
    )
    total_gastos = cursor.fetchone()['total']

    # Se calcula el saldo
    saldo = total_ingresos - total_gastos
    db.close()

    # Se envian los datos al HTML
    return render_template(
        'panel.html',
        usuario_id=usuario_id,
        ingresos=total_ingresos,
        gastos=total_gastos,
        saldo=saldo
    )


    Este apartado muestra el panel principal del usuario, se calcula el total de ingresos y gastos a partir de la base de datos y con esos datos se obtiene el saldo actual toda la información se envía al panel para mostrarse al usuario

# ------------------ INGRESOS ------------------

# Ruta para mostrar los ingresos del usuario

@app.route('/ingresos/<int:usuario_id>')
def ingresos(usuario_id):
db = obtener_db()
cursor = db.cursor()

    # Se obtienen todos los ingresos ordenados por fecha
    cursor.execute(
        "SELECT * FROM ingresos WHERE usuario_id=%s ORDER BY date DESC",
        (usuario_id,)
    )
    lista_ingresos = cursor.fetchall()
    db.close()

    return render_template(
        'ingresos.html',
        usuario_id=usuario_id,
        ingresos=lista_ingresos
    )

# Ruta para añadir un nuevo ingreso

@app.route('/ingresos/<int:usuario_id>/nuevo', methods=['POST'])
def nuevo_ingreso(usuario_id):
data = request.form
db = obtener_db()
cursor = db.cursor()

    # Se inserta el ingreso en la base de datos
    cursor.execute(
        "INSERT INTO ingresos (nombre, cantidad, date, nota, usuario_id) VALUES (%s,%s,%s,%s,%s)",
        (data['nombre'], data['cantidad'], data['date'], data.get('nota',''), usuario_id)
    )
    db.commit()
    db.close()

    # Se vuelve a la pagina de ingresos
    return redirect(url_for('ingresos', usuario_id=usuario_id))


    Este apartado gestiona los ingresos del usuario, se muestran todos los ingresos guardados en la base de datos y también permite añadir nuevos ingresos mediante un formulario que se guarda directamente en la base de datos

# ------------------ GASTOS ------------------

# Ruta para mostrar los gastos del usuario

@app.route('/gastos/<int:usuario_id>')
def gastos(usuario_id):
db = obtener_db()
cursor = db.cursor()

    # Se obtienen todos los gastos del usuario
    cursor.execute(
        "SELECT * FROM gastos WHERE usuario_id=%s ORDER BY date DESC",
        (usuario_id,)
    )
    lista_gastos = cursor.fetchall()
    db.close()

    return render_template(
        'gastos.html',
        usuario_id=usuario_id,
        gastos=lista_gastos
    )

# Ruta para añadir un nuevo gasto

@app.route('/gastos/<int:usuario_id>/nuevo', methods=['POST'])
def nuevo_gasto(usuario_id):
data = request.form
db = obtener_db()
cursor = db.cursor()

    # Inserta el gasto en la base de datos
    cursor.execute(
        "INSERT INTO gastos (nombre, cantidad, date, nota, usuario_id) VALUES (%s,%s,%s,%s,%s)",
        (data['nombre'], data['cantidad'], data['date'], data.get('nota',''), usuario_id)
    )
    db.commit()
    db.close()

    return redirect(url_for('gastos', usuario_id=usuario_id))


    Este apartado funciona igual que el de ingresos, pero aplicado a los gastos se muestran todos los gastos del usuario y se pueden añadir nuevos gastos desde el formulario

# ------------------ PRESUPUESTOS ------------------

# Ruta para mostrar los presupuestos del usuario

@app.route('/presupuestos/<int:usuario_id>')
def presupuestos(usuario_id):
db = obtener_db()
cursor = db.cursor()

    # Se obtienen los presupuestos asociados al usuario
    cursor.execute(
        "SELECT * FROM presupuestos WHERE usuario_id=%s ORDER BY id DESC",
        (usuario_id,)
    )
    lista_presupuestos = cursor.fetchall()
    db.close()

    return render_template(
        'presupuestos.html',
        usuario_id=usuario_id,
        presupuestos=lista_presupuestos
    )


    Este apartado muestra los presupuestos del usuario, obteniendo los datos desde la base de datos y mostrándolos en la página de presupuestos

# ------------------ ESTADISTICAS ------------------

# Ruta para mostrar las estadisticas

@app.route('/estadisticas/<int:usuario_id>')
def estadisticas(usuario_id):
db = obtener_db()
cursor = db.cursor()

    # Total de ingresos
    cursor.execute(
        "SELECT COALESCE(SUM(cantidad),0) AS total FROM ingresos WHERE usuario_id=%s",
        (usuario_id,)
    )
    ingresos = cursor.fetchone()['total']

    # Total de gastos
    cursor.execute(
        "SELECT COALESCE(SUM(cantidad),0) AS total FROM gastos WHERE usuario_id=%s",
        (usuario_id,)
    )
    gastos = cursor.fetchone()['total']

    db.close()

    return render_template(
        'estadisticas.html',
        usuario_id=usuario_id,
        ingresos=ingresos,
        gastos=gastos,
        saldo=ingresos - gastos
    )

    Este apartado calcula el total de ingresos y gastos del usuario y muestra un resumen general de su situación económica en la página de estadísticas

# ------------------ PERFIL ------------------

# Ruta para mostrar el perfil del usuario

@app.route('/perfil/<int:usuario_id>')
def perfil(usuario_id):
db = obtener_db()
cursor = db.cursor()

    # Se obtienen los datos del usuario
    cursor.execute(
        "SELECT id, email FROM usuarios WHERE id=%s",
        (usuario_id,)
    )
    usuario = cursor.fetchone()
    db.close()

    return render_template(
        'perfil.html',
        usuario_id=usuario_id,
        usuario=usuario
    )

    Este apartado muestra los datos básicos del usuario, como el email en la página de perfil manteniendo la coherencia visual con el resto de la aplicación

# ------------------ INICIAR SERVIDOR ------------------

# Se inicia el servidor en modo debug

if **name** == '**main**':
app.run(debug=True)

´´´ 3. Conclusion

En conclusión, este proyecto de contabilidad personal permite al usuario llevar un control claro de sus ingresos, gastos y presupuestos. Gracias a la conexión entre la base de datos y el frontend mediante Flask, la aplicación funciona de forma correcta y los datos se guardan y muestran en tiempo real. Es una aplicación sencilla, pensada para personas jóvenes, que facilita la organización del dinero y ayuda a tener una mejor visión de la situación económica personal.
