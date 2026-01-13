from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)

"""
=====================================================
CONFIGURACIÓN Y CONEXIÓN A BASE DE DATOS
=====================================================
"""

def obtener_db():
    """
    Devuelve una conexión activa a la base de datos MySQL
    usando PyMySQL y diccionarios como resultado.
    """
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Contabilidad123$",
        database="contabilidad",
        cursorclass=pymysql.cursors.DictCursor
    )


"""
=====================================================
FUNCIONES AUXILIARES
=====================================================
"""

def es_admin(usuario_id):
    """
    Comprueba si un usuario tiene permisos de administrador.
    """
    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("SELECT is_admin FROM usuarios WHERE id=%s", (usuario_id,))
    result = cursor.fetchone()
    db.close()

    return result and result["is_admin"] == 1


"""
=====================================================
RUTAS DE TEMPLATES (FRONTEND)
=====================================================
"""

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/panel')
def panel_page():
    return render_template('panel.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')


"""
=====================================================
AUTENTICACIÓN
=====================================================
"""

@app.route("/register", methods=["POST"])
def register():
    """
    Registro simple de usuario.
    """
    data = request.json
    db = obtener_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO usuarios (usuario, email, password) VALUES (%s,%s,%s)",
        (data["usuario"], data["email"], data["password"])
    )

    db.commit()
    db.close()

    return jsonify({"message": "Usuario creado"})


@app.route('/login', methods=['POST'])
def login():
    """
    Login simple sin hashing ni tokens.
    Devuelve usuario_id e is_admin.
    """
    data = request.json

    db = obtener_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT id, is_admin FROM usuarios WHERE email=%s AND password=%s",
        (data["email"], data["password"])
    )
    user = cursor.fetchone()
    db.close()

    if user:
        return jsonify({
            "success": True,
            "usuario_id": user["id"],
            "is_admin": user["is_admin"]
        })
    else:
        return jsonify({"success": False, "error": "Credenciales incorrectas"})


"""
=====================================================
DASHBOARD
=====================================================
"""

@app.route("/dashboard/<int:usuario_id>")
def dashboard(usuario_id):
    """
    Devuelve ingresos, gastos y saldo del usuario.
    """
    db = obtener_db()
    cursor = db.cursor()

    cursor.execute("SELECT COALESCE(SUM(cantidad),0) AS total FROM ingresos WHERE usuario_id=%s", (usuario_id,))
    total_ingresos = cursor.fetchone()["total"]

    cursor.execute("SELECT COALESCE(SUM(cantidad),0) AS total FROM gastos WHERE usuario_id=%s", (usuario_id,))
    total_gastos = cursor.fetchone()["total"]

    db.close()

    saldo = total_ingresos - total_gastos

    return jsonify({
        "ingresos": total_ingresos,
        "gastos": total_gastos,
        "saldo": saldo
    })


"""
=====================================================
INGRESOS
=====================================================
"""

@app.route('/ingresos', methods=['POST'])
def agregar_ingreso():
    data = request.json

    db = obtener_db()
    cursor = db.cursor()

    cursor.execute(
        """INSERT INTO ingresos (nombre,cantidad,date,nota,categoria_id,usuario_id)
           VALUES (%s,%s,%s,%s,%s,%s)""",
        (data["nombre"], data["cantidad"], data["date"],
         data.get("nota"), data.get("categoria_id"), data["usuario_id"])
    )

    db.commit()
    db.close()

    return jsonify({"message": "Ingreso añadido"})


@app.route('/ingresos/<int:usuario_id>')
def obtener_ingresos(usuario_id):
    db = obtener_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT i.*, c.nombre AS categoria
        FROM ingresos i
        LEFT JOIN categorias c ON i.categoria_id=c.id
        WHERE i.usuario_id=%s
        ORDER BY i.date DESC
    """, (usuario_id,))

    data = cursor.fetchall()
    db.close()

    return jsonify(data)


"""
=====================================================
GASTOS
=====================================================
"""

@app.route('/gastos', methods=['POST'])
def agregar_gasto():
    data = request.json

    db = obtener_db()
    cursor = db.cursor()

    cursor.execute(
        """INSERT INTO gastos (nombre,cantidad,date,nota,categoria_id,usuario_id)
           VALUES (%s,%s,%s,%s,%s,%s)""",
        (data["nombre"], data["cantidad"], data["date"],
         data.get("nota"), data.get("categoria_id"), data["usuario_id"])
    )

    db.commit()
    db.close()

    return jsonify({"message": "Gasto añadido"})


@app.route('/gastos/<int:usuario_id>')
def obtener_gastos(usuario_id):
    db = obtener_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT g.*, c.nombre AS categoria
        FROM gastos g
        LEFT JOIN categorias c ON g.categoria_id=c.id
        WHERE g.usuario_id=%s
        ORDER BY g.date DESC
    """, (usuario_id,))

    data = cursor.fetchall()
    db.close()

    return jsonify(data)


"""
=====================================================
PRESUPUESTOS
=====================================================
"""

@app.route('/presupuesto', methods=['POST'])
def set_presupuesto():
    data = request.json

    db = obtener_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO presupuestos (cantidad,periodo,usuario_id) VALUES (%s,%s,%s)",
        (data["cantidad"], data["periodo"], data["usuario_id"])
    )

    db.commit()
    db.close()

    return jsonify({"message": "Presupuesto guardado"})


"""
=====================================================
ESTADÍSTICAS
=====================================================
"""

@app.route('/stats/gastos/<int:usuario_id>')
def stats_gastos(usuario_id):
    db = obtener_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT c.nombre AS categoria, SUM(g.cantidad) AS total
        FROM gastos g
        JOIN categorias c ON g.categoria_id=c.id
        WHERE g.usuario_id=%s
        GROUP BY c.nombre
    """, (usuario_id,))

    data = cursor.fetchall()
    db.close()

    return jsonify(data)


"""
=====================================================
PANEL DE ADMINISTRACIÓN
=====================================================
"""

@app.route("/admin/usuarios/<int:admin_id>")
def admin_usuarios(admin_id):
    if not es_admin(admin_id):
        return jsonify({"error": "Acceso denegado"}), 403

    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, usuario, email, is_admin FROM usuarios")
    data = cursor.fetchall()
    db.close()

    return jsonify(data)


@app.route("/admin/tablas/<int:admin_id>")
def admin_tablas(admin_id):
    if not es_admin(admin_id):
        return jsonify({"error": "Acceso denegado"}), 403

    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("SHOW TABLES")
    data = cursor.fetchall()
    db.close()

    return jsonify(data)


@app.route("/admin/ingresos/<int:admin_id>/<int:usuario_id>")
def admin_ingresos(admin_id, usuario_id):
    if not es_admin(admin_id):
        return jsonify({"error": "Acceso denegado"}), 403

    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ingresos WHERE usuario_id=%s", (usuario_id,))
    data = cursor.fetchall()
    db.close()

    return jsonify(data)


@app.route("/admin/usuario/<int:admin_id>/<int:usuario_id>", methods=["DELETE"])
def eliminar_usuario(admin_id, usuario_id):
    if not es_admin(admin_id):
        return jsonify({"error": "Acceso denegado"}), 403

    db = obtener_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id=%s", (usuario_id,))
    db.commit()
    db.close()

    return jsonify({"message": "Usuario eliminado"})


"""
=====================================================
INICIAR SERVIDOR
=====================================================
"""

if __name__ == "__main__":
    app.run(debug=True)


"""
=====================================================
NOTAS
=====================================================

- Backend educativo y simple
- Sin hashing de contraseñas
- Sin tokens
- Cálculos dinámicos
- Roles básicos (admin / usuario)
- Panel administrativo funcional

=====================================================
"""
