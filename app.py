from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import re
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key")

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Saisri@143",
        database="employee_db"
    )

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        department = request.form.get("department", "").strip()
        phone = request.form.get("phone", "").strip()

        if not all([name, email, department, phone]):
            flash("All fields are required.", "danger")
            return redirect(url_for("index"))
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            flash("Please enter a valid email address.", "danger")
            return redirect(url_for("index"))
        if not re.fullmatch(r"[0-9+\-\s()]{7,20}", phone):
            flash("Please enter a valid phone number.", "danger")
            return redirect(url_for("index"))

        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO employees (name, email, department, phone) VALUES (%s, %s, %s, %s)",
                (name, email, department, phone)
            )
            conn.commit()
            flash("Employee registered successfully.", "success")
        except mysql.connector.Error as error:
            if getattr(error, "errno", None) == 1062:
                flash("That email address is already registered.", "warning")
            else:
                app.logger.exception("Database operation failed")
                flash("Could not save employee. Check database settings and try again.", "danger")
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
        return redirect(url_for("index"))

    employees = []
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, department, phone FROM employees ORDER BY id DESC")
        employees = cursor.fetchall()
    except mysql.connector.Error:
        app.logger.exception("Could not retrieve employees")
        flash("Could not load employee records. Check that MySQL is running and configured.", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    return render_template("index.html", employees=employees)

@app.route("/delete/<int:employee_id>", methods=["POST"])
def delete_employee(employee_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
        conn.commit()
        flash("Employee deleted successfully." if cursor.rowcount else "Employee record not found.", "success")
    except mysql.connector.Error:
        app.logger.exception("Could not delete employee")
        flash("Could not delete employee. Please try again.", "danger")
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
