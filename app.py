import os
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id SERIAL PRIMARY KEY,
            titulo VARCHAR(150) NOT NULL,
            descripcion TEXT,
            completada BOOLEAN DEFAULT FALSE,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.route("/")
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM tareas ORDER BY fecha_creacion DESC;")
    tareas = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", tareas=tareas)


@app.route("/crear", methods=["GET", "POST"])
def crear_tarea():
    if request.method == "POST":
        titulo = request.form["titulo"]
        descripcion = request.form.get("descripcion", "")
        completada = "completada" in request.form

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tareas (titulo, descripcion, completada) VALUES (%s, %s, %s);",
            (titulo, descripcion, completada),
        )
        conn.commit()
        cur.close()
        conn.close()
        flash("Tarea creada correctamente", "success")
        return redirect(url_for("index"))

    return render_template("form.html", tarea=None, accion="Crear")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_tarea(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if request.method == "POST":
        titulo = request.form["titulo"]
        descripcion = request.form.get("descripcion", "")
        completada = "completada" in request.form

        cur.execute(
            "UPDATE tareas SET titulo = %s, descripcion = %s, completada = %s WHERE id = %s;",
            (titulo, descripcion, completada, id),
        )
        conn.commit()
        cur.close()
        conn.close()
        flash("Tarea actualizada correctamente", "success")
        return redirect(url_for("index"))

    cur.execute("SELECT * FROM tareas WHERE id = %s;", (id,))
    tarea = cur.fetchone()
    cur.close()
    conn.close()

    if tarea is None:
        flash("Tarea no encontrada", "error")
        return redirect(url_for("index"))

    return render_template("form.html", tarea=tarea, accion="Editar")


@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar_tarea(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tareas WHERE id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash("Tarea eliminada correctamente", "success")
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
