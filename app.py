from flask import Flask, render_template, request, url_for
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


@app.route("/BazaPokoi")
def baza_pokoi():
    cursor = mysql.connect.cursor()
    cursor.execute("SELECT * FROM rooms")
    baza_pokoi = cursor.fetchall()
    return render_template("baza_pokoi.html", baza_pokoi=baza_pokoi)


@app.route("/ArchiwumRezerwacji")
def archiwum_rezerwacji():
    cursor = mysql.connect.cursor()
    cursor.execute("SELECT * FROM previous_reservations")
    archiwum_rezerwacji = cursor.fetchall()
    return render_template(
        "archiwum_rezerwacji.html", archiwum_rezerwacji=archiwum_rezerwacji
    )


@app.route("/BazaGosci")
def baza_gosci():
    cursor = mysql.connect.cursor()
    cursor.execute("SELECT * FROM guests")
    baza_gosci = cursor.fetchall()
    return render_template("baza_gosci.html", baza_gosci=baza_gosci)


@app.route("/ObecneRezerwacje")
def obecne_rezerwacje():
    cursor = mysql.connect.cursor()
    cursor.execute("SELECT * FROM reservations")
    obecne_rezerwacje = cursor.fetchall()
    return render_template(
        "obecne_rezerwacje.html", obecne_rezerwacje=obecne_rezerwacje
    )


##Koniec stron z danymi


##Strona do wczytywania danych z mysql
@app.route("/orders", methods=["POST", "GET"])
def sikuel():
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        birth_date = request.form["birth_date"]
        arrival_date = request.form["arrival_date"]
        departure_date = request.form["departure_date"]
        email = request.form["email"]
        room_number = request.form["room_number"]
        cursor = mysql.connect.cursor()
        cursor.execute(
            """INSERT INTO guests (first_name, last_name, number_of_visits, birth_date, email) VALUES (%s, %s, 1, %s, %s)""",
            (name, surname, birth_date, email),
        )
        mysql.connection.commit()
        cursor.close()
    return render_template("orders.html")


if __name__ == "__main__":
    app.run(debug=True)
