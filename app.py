from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:6133@127.0.0.1/rooms"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class rooms(db.Model):
    room_number = db.Column(db.Integer, primary_key=True)
    floor = db.Column(db.Integer, nullable=False)
    guests_capacity = db.Column(db.Integer, nullable=False)


class previous_reservations(db.Model):
    reservation_number = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.Integer, nullable=False)
    guest_id = db.Column(db.Integer, nullable=False)
    arrival_date = db.Column(db.Date, nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.String(50), nullable=False)


class guests(db.Model):
    guest_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    number_of_visits = db.Column(db.Integer, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), nullable=False)


class reservations(db.Model):
    reservation_number = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.Integer, nullable=False)
    guest_id = db.Column(db.Integer, nullable=False)
    arrival_date = db.Column(db.Date, nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    paid = db.Column(db.String(50), nullable=False)


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
    baza_pokoi = rooms.query.all()
    return render_template("baza_pokoi.html", baza_pokoi=baza_pokoi)


@app.route("/ArchiwumRezerwacji")
def archiwum_rezerwacji():
    archiwum_rezerwacji = previous_reservations.query.all()
    return render_template(
        "archiwum_rezerwacji.html", archiwum_rezerwacji=archiwum_rezerwacji
    )


@app.route("/BazaGosci")
def baza_gosci():
    baza_gosci = guests.query.all()
    return render_template("baza_gosci.html", baza_gosci=baza_gosci)


@app.route("/ObecneRezerwacje")
def obecne_rezerwacje():
    obecne_rezerwacje = reservations.query.all()
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

        # Create and add the new Guest to the database
        new_guest = guests(
            first_name=name,
            last_name=surname,
            birth_date=birth_date,
            email=email,
        )
        db.session.add(new_guest)
        db.session.commit()

    return render_template("orders.html")


if __name__ == "__main__":
    app.run(debug=True)
