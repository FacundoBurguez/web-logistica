from flask import Flask, render_template, session , request, redirect, flash, url_for
import smtplib , sqlite3 , io
from flask import send_file
import openpyxl

app = Flask(__name__)
app.secret_key = "clave_super_secreta"  # Necesaria para usar flash()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        email = request.form["email"].strip()
        mensaje = request.form["mensaje"].strip()

        # VALIDACIÓN BACKEND
        errores = []

        if len(nombre) < 2 or not nombre.replace(" ", "").isalpha():
            errores.append("El nombre debe tener al menos 2 letras y solo puede contener letras y espacios.")

        if "@" not in email or "." not in email or len(email) > 100:
            errores.append("El correo electrónico no es válido.")

        if len(mensaje) < 10:
            errores.append("El mensaje debe tener al menos 10 caracteres.")

        if errores:
            for error in errores:
                flash(error, "danger")
            return redirect(url_for("index.html"))

        # SI TODO ESTÁ OK, ENVÍA EL CORREO
        enviar_mail(nombre, email, mensaje)
        flash("Gracias por tu mensaje. Te responderé pronto!", "success")
        return render_template("index.html")

    return render_template("index.html")


def enviar_mail(nombre, email, mensaje):
    remitente = "loginovadev@gmail.com"
    contraseña = "mnasfzohusebspyq"  # Contraseña de aplicación Gmail

    # ➤ Correo que recibís vos
    destinatario_empresa = "loginovadev@gmail.com"
    cuerpo_empresa = f"Nombre: {nombre}\nEmail: {email}\nMensaje:\n{mensaje}"
    mensaje_empresa = f"From: {remitente}\nTo: {destinatario_empresa}\nSubject: Consulta desde la web\n\n{cuerpo_empresa}"

    # ➤ Correo que recibe el usuario
    destinatario_usuario = email
    cuerpo_usuario = f"""
Hola {nombre},

Gracias por contactarme. Recibí tu mensaje y te responderé pronto.

Este es un resumen de tu consulta:

------------------------------------------------
Nombre: {nombre}
Email: {email}
Mensaje:
{mensaje}
------------------------------------------------

Saludos,
Facundo – Soluciones Logísticas
    """
    mensaje_usuario = f"From: {remitente}\nTo: {destinatario_usuario}\nSubject: Gracias por tu mensaje\n\n{cuerpo_usuario}"

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(remitente, contraseña)
            # Enviar a vos
            smtp.sendmail(remitente, destinatario_empresa, mensaje_empresa.encode("utf-8"))
            # Enviar al usuario
            smtp.sendmail(remitente, destinatario_usuario, mensaje_usuario.encode("utf-8"))

        print("✅ Correos enviados correctamente")
    except Exception as e:
        print("❌ Error al enviar correos:", e)

def guardar_consulta(nombre, email, mensaje):
    conn = sqlite3.connect("consultas.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO consultas (nombre, email, mensaje)
        VALUES (?, ?, ?)
    """, (nombre, email, mensaje))
    conn.commit()
    conn.close()

def inicializar_bd():
    conn = sqlite3.connect("consultas.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT NOT NULL,
            mensaje TEXT NOT NULL,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


@app.route("/exportar-consultas")
def exportar_consultas():
    if not session.get("admin"):
        flash("Acceso restringido. Iniciá sesión.", "danger")
        return redirect(url_for("login"))
 
    conn = sqlite3.connect("consultas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email, mensaje, fecha FROM consultas")
    filas = cursor.fetchall()
    conn.close()

    # Crear archivo Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Consultas"

    # Agregar encabezados
    ws.append(["ID", "Nombre", "Email", "Mensaje", "Fecha"])

    # Agregar datos
    for fila in filas:
        ws.append(fila)

    # Guardar archivo
    output = io.BytesIO()
    wb.save(output)
    output.seek(0)
    
     # Enviamos el archivo al navegador
    return send_file(
        output,
        download_name="consultas.xlsx",
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        clave_ingresada = request.form["clave"]
        if clave_ingresada == "admin123":  # 👈 Cambiá esto por tu contraseña secreta
            session["admin"] = True
            flash("Acceso concedido ✅", "success")
            return redirect(url_for("index"))
        else:
            flash("Clave incorrecta ❌", "danger")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("admin", None)
    flash("Sesión cerrada", "info")
    return redirect(url_for("index"))

@app.route("/admin/consultas")
def ver_consultas():
    if not session.get("admin"):
        flash("Acceso restringido. Iniciá sesión primero.", "danger")
        return redirect(url_for("login"))

    conn = sqlite3.connect("consultas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, email, mensaje, fecha FROM consultas ORDER BY fecha DESC")
    consultas = cursor.fetchall()
    conn.close()

    return render_template("admin_consultas.html", consultas=consultas)


if __name__ == "__main__":
    inicializar_bd()
    app.run(debug=True, host="0.0.0.0")

