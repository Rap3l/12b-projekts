from flask import Flask, redirect, render_template, request, url_for
import sqlite3
import requests

app = Flask(__name__)

API_url = "https://api.npoint.io/ec052940c9bc0f580e40" #izveidotais API

#DATU BĀZES IZVEIDE

conn = sqlite3.connect("passwords.db")
c = conn.cursor()                       #izveidoju tabulu
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
    conn.row_factory = sqlite3.Row #nosaku, ka dati no datubāzes tiks saņemti kā saraksts
    return conn



@app.route("/")
def index():

    response = requests.get(API_url)

    if response.status_code == 200:
        data = response.json()
        title = data.get("title")
        description = data.get("text")      #Pievienoju API, ja tas strādā tad parādās paredzētais teksts, ja ne, tad ir nodrošināts informatīvs paziņojums
    else:
        title = "Nav pieslēguma"
        description = ""

    conn = get_db_connection()
    #nosūtot šo funkciju ar jautājumu "kāpēc man met ārā kļūdu ja visi nosaukumi ir norādīti pareizi?" MI intelekts teica, ka man pietrūks fetchall metodes
    passwords = conn.execute("SELECT * FROM passwords").fetchall()  #fetchall atgriež rindas no db 
    conn.close()

    return render_template("index.html", 
                            passwords = passwords,
                            title=title,
                            description=description)       #Parāda index.html un visus datus kuri ir vajadzīgi "indexā"




@app.route("/add", methods=["GET", "POST"])
def add():
    conn = get_db_connection()
 
    if request.method == "POST":
        app_name = request.form["app_name"] #Saņem ievadītos datus
        password = request.form["password"]
 
        conn.execute(
            "INSERT INTO passwords (app_name, password) VALUES (?, ?)",     
            (app_name, password)    #ievieto datubāzē ievadītos datus
        )
        conn.commit()
        conn.close()
        
        return redirect(url_for("index"))
    
    return render_template("add.html")



#funkcija delete ir veidota ar chatgpt palīdzību, prompt ir tāds:
# Es gribu pievienot iespēju dzēst paroles, 
# piemēram, man bija (snapchat un tās parole) un
# ēs dzēšu ārā paroli kopā ar applikācijas nosaukumu. Kā to var realizēt?

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):  
    conn = get_db_connection()
    conn.execute("DELETE FROM passwords WHERE id = ?", (id,))  #dzēš ierakstus pēc id
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
