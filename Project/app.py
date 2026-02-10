from flask import Flask, redirect, render_template, request, url_for
import sqlite3

app = Flask(__name__)


#DATU BĀZES IZVEIDE

conn = sqlite3.connect("passwords.db")
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        app_name TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)
conn.commit()
conn.close()


def get_db_connection():
    conn = sqlite3.connect("passwords.db")
    conn.row_factory = sqlite3.Row
    return conn



@app.route("/")
def index():
    conn = get_db_connection()
    passwords = conn.execute("SELECT * FROM passwords").fetchall()
    conn.close()
    return render_template("index.html", passwords = passwords)


@app.route("/add", methods=["GET", "POST"])
def add():
    conn = get_db_connection()
 
    if request.method == "POST":
        app_name = request.form["app_name"]
        password = request.form["password"]
 
        conn.execute(
            "INSERT INTO passwords (app_name, password) VALUES (?, ?)",
            (app_name, password)
        )
        conn.commit()
        conn.close()
        
        return redirect(url_for("index"))
    
    return render_template("add.html")


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM passwords WHERE id = ?", (id,))
    conn.commit()
    conn.close()


    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)





# # @app.route("/add")
# # def add():
# #     return render_template("add.html")


# @app.route("/add", methods = ["GET", "POST"])
# def add_new():
#     if request.method == "POST":
#         app_name = request.form["app_name"]
#         password = request.form["password"]

#         conn = get_db_connection()
#         conn.execute("INSERT INTO passwords (app_name, password) VALUES (?, ?)", (app_name, password))
#         conn.commit()
#         conn.close()
#         return redirect(url_for("index"))
#     return render_template("add.html")














if __name__ == "__main__":
    app.run(debug=True)