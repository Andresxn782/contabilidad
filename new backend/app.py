from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql

app = Flask(__name__)

# Conexión a MySQL
def obtener_db():
    return pymysql.connect(
        host="localhost",
        user="usuario_app",  # usuario que creaste en MySQL
        password="Contabilidad123$",
        database="contabilidad",
        cursorclass=pymysql.cursors.DictCursor
    )

# ------------------ LOGIN ------------------
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        db = obtener_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()
        db.close()

        if user:
            # Guardar usuario_id en sesión o redirigir directamente
            return redirect(url_for('panel', usuario_id=user['id']))
        else:
            return render_template('login.html', error="Usuario o contraseña incorrectos")

    return render_template('login.html')


# ------------------ PANEL ------------------
@app.route('/panel/<int:usuario_id>')
def panel(usuario_id):
    db = obtener_db()
    cursor = db.cursor()

    # Obtener total ingresos
    cursor.execute("SELECT COALESCE(SUM(cantidad),0) as total FROM ingresos WHERE usuario_id=%s", (usuario_id,))
    total_ingresos = cursor.fetchone()['total']

    # Obtener total gastos
    cursor.execute("SELECT COALESCE(SUM(cantidad),0) as total FROM gastos WHERE usuario_id=%s", (usuario_id,))
    total_gastos = cursor.fetchone()['total']

    saldo = total_ingresos - total_gastos

    db.close()
    return render_template(
        'panel.html',
        usuario_id=usuario_id,
        ingresos=total_ingresos,
        gastos=total_gastos,
        saldo=saldo
    )


# ------------------ INGRESOS ------------------
@app.route('/ingresos/<int:usuario_id>')
def ingresos(usuario_id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ingresos WHERE usuario_id=%s ORDER BY date DESC", (usuario_id,))
    lista_ingresos = cursor.fetchall()
    db.close()
    return render_template('ingresos.html', usuario_id=usuario_id, ingresos=lista_ingresos)


@app.route('/ingresos/<int:usuario_id>/nuevo', methods=['POST'])
def nuevo_ingreso(usuario_id):
    data = request.form
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO ingresos (nombre, cantidad, date, nota, usuario_id) VALUES (%s,%s,%s,%s,%s)",
        (data['nombre'], data['cantidad'], data['date'], data.get('nota',''), usuario_id)
    )
    db.commit()
    db.close()
    return redirect(url_for('ingresos', usuario_id=usuario_id))


# ------------------ GASTOS ------------------
@app.route('/gastos/<int:usuario_id>')
def gastos(usuario_id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM gastos WHERE usuario_id=%s ORDER BY date DESC", (usuario_id,))
    lista_gastos = cursor.fetchall()
    db.close()
    return render_template('gastos.html', usuario_id=usuario_id, gastos=lista_gastos)


@app.route('/gastos/<int:usuario_id>/nuevo', methods=['POST'])
def nuevo_gasto(usuario_id):
    data = request.form
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO gastos (nombre, cantidad, date, nota, usuario_id) VALUES (%s,%s,%s,%s,%s)",
        (data['nombre'], data['cantidad'], data['date'], data.get('nota',''), usuario_id)
    )
    db.commit()
    db.close()
    return redirect(url_for('gastos', usuario_id=usuario_id))


# =========================================================
# ================== NUEVOS APARTADOS =====================
# =========================================================

# ------------------ PRESUPUESTOS ------------------
@app.route('/presupuestos/<int:usuario_id>')
def presupuestos(usuario_id):
    db = obtener_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM presupuestos WHERE usuario_id=%s ORDER BY fecha_inicio DESC",
        (usuario_id,)
    )
    lista_presupuestos = cursor.fetchall()

    db.close()
    return render_template(
        'presupuestos.html',
        usuario_id=usuario_id,
        presupuestos=lista_presupuestos
    )


# ------------------ ESTADÍSTICAS ------------------
@app.route('/estadisticas/<int:usuario_id>')
def estadisticas(usuario_id):
    db = obtener_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT COALESCE(SUM(cantidad),0) AS total FROM ingresos WHERE usuario_id=%s",
        (usuario_id,)
    )
    ingresos = cursor.fetchone()['total']

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


# ------------------ PERFIL ------------------
@app.route('/perfil/<int:usuario_id>')
def perfil(usuario_id):
    db = obtener_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT id, email, nombre FROM usuarios WHERE id=%s",
        (usuario_id,)
    )
    usuario = cursor.fetchone()

    db.close()

    return render_template(
        'perfil.html',
        usuario_id=usuario_id,
        usuario=usuario
    )


# ------------------ INICIAR SERVIDOR ------------------
if __name__ == '__main__':
    app.run(debug=True)
