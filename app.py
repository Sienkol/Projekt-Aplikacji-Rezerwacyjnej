from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "6133"
app.config["MYSQL_DB"] = "rooms"
mysql = MySQL(app)


##Strona główna
@app.route("/")
def hello():
    return render_template("base.html")


##Strona glowna
@app.route("/glowna")
def glowna():
    return render_template("glowna.html")


##Strona z bazami danych SQL
@app.route("/tabele")
def tabele():
    return render_template("tabele.html")


@app.route("/tabele/BazaPokoi")
def baza_pokoi():
    return render_template("baza_pokoi.html")


@app.route("/tabele/ArchiwumRezerwacji")
def archiwum_rezerwacji():
    return render_template("archiwum_rezerwacji.html")


@app.route("/tabele/BazaGosci")
def baza_gosci():
    return render_template("baza_gosci.html")


@app.route("/tabele/ObecneRezerwacje")
def obecne_rezerwacje():
    return render_template("obecne_rezerwacje.html")


##Koniec stron z danymi


##Strona do wczytywania danych z mysql
@app.route("/orders")
def sikuel():
    cursor = mysql.connect.cursor()
    cursor.execute("SELECT * FROM rooms")
    orders = cursor.fetchall()
    return render_template("orders.html", orders=orders)


if __name__ == "__main__":
    app.run(debug=True)
