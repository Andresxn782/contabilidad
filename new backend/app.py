from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)

# ----------------------
# Conexión a MySQL
# ----------------------
def obtener_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Contabilidad123$",
        database="contabilidad",
        cursorclass=pymysql.cursors.DictCursor
    )

# ----------------------
# Rutas de Templates
# ----------------------
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/panel')
def panel_page():
    return render_template('panel.html')

# ----------------------
# Login API
# ----------------------
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()
    db.close()

    if user:
        return jsonify({"success": True, "usuario_id": user["id"]})
    else:
        return jsonify({"success": False, "error": "Usuario o contraseña incorrectos"})

# ----------------------
# Dashboard API
# ----------------------
@app.route('/dashboard/<int:usuario_id>')
def dashboard(usuario_id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("SELECT COALESCE(SUM(cantidad),0) AS total FROM ingresos WHERE usuario_id=%s", (usuario_id,))
    total_ingresos = cursor.fetchone()['total']
    cursor.execute("SELECT COALESCE(SUM(cantidad),0) AS total FROM gastos WHERE usuario_id=%s", (usuario_id,))
    total_gastos = cursor.fetchone()['total']
    db.close()

    saldo = total_ingresos - total_gastos
    return jsonify({"ingresos": total_ingresos, "gastos": total_gastos, "saldo": saldo})

# ----------------------
# Ingresos API
# ----------------------
@app.route('/ingresos', methods=['POST'])
def agregar_ingreso():
    data = request.json
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO ingresos (nombre, cantidad, date, nota, categoria_id, usuario_id) VALUES (%s,%s,%s,%s,%s,%s)",
        (data["nombre"], data["cantidad"], data["date"], data.get("nota"), data.get("categoria_id"), data["usuario_id"])
    )
    db.commit()
    db.close()
    return jsonify({"message": "Ingreso añadido"})

@app.route('/ingresos/<int:usuario_id>')
def obtener_ingresos(usuario_id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT i.*, c.nombre AS categoria FROM ingresos i LEFT JOIN categorias c ON i.categoria_id=c.id WHERE i.usuario_id=%s ORDER BY i.date DESC",
        (usuario_id,)
    )
    ingresos = cursor.fetchall()
    db.close()
    return jsonify(ingresos)

# ----------------------
# Gastos API
# ----------------------
@app.route('/gastos', methods=['POST'])
def agregar_gasto():
    data = request.json
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO gastos (nombre, cantidad, date, nota, categoria_id, usuario_id) VALUES (%s,%s,%s,%s,%s,%s)",
        (data["nombre"], data["cantidad"], data["date"], data.get("nota"), data.get("categoria_id"), data["usuario_id"])
    )
    db.commit()
    db.close()
    return jsonify({"message": "Gasto añadido"})

@app.route('/gastos/<int:usuario_id>')
def obtener_gastos(usuario_id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT g.*, c.nombre AS categoria FROM gastos g LEFT JOIN categorias c ON g.categoria_id=c.id WHERE g.usuario_id=%s ORDER BY g.date DESC",
        (usuario_id,)
    )
    gastos = cursor.fetchall()
    db.close()
    return jsonify(gastos)

# ----------------------
# Presupuesto API
# ----------------------
@app.route('/presupuesto', methods=['POST'])
def set_presupuesto():
    data = request.json
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO presupuestos (cantidad, periodo, usuario_id) VALUES (%s,%s,%s)",
        (data["cantidad"], data["periodo"], data["usuario_id"])
    )
    db.commit()
    db.close()
    return jsonify({"message": "Presupuesto guardado"})

# ----------------------
# Estadísticas API
# ----------------------
@app.route('/stats/gastos/<int:usuario_id>')
def stats_gastos(usuario_id):
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT c.nombre AS categoria, SUM(g.cantidad) AS total FROM gastos g JOIN categorias c ON g.categoria_id=c.id WHERE g.usuario_id=%s GROUP BY c.nombre",
        (usuario_id,)
    )
    stats = cursor.fetchall()
    db.close()
    return jsonify(stats)

# ----------------------
# Iniciar servidor
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)
