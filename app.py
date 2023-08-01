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


class previous_reservations(db.Model):
    reservation_number = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.Integer, nullable=False)
    guest_id = db.Column(db.Integer, nullable=False)
    arrival_date = db.Column(db.Date, nullable=False)
    departure_date = db.Column(db.Date, nullable=False)


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
    # Checking if date of reservation is less or equal today, if yes than record is deleted from reservations and added to previous_reservations
    dzisiaj = date.today()
    reservations_to_move = reservations.query.filter(
        reservations.departure_date < dzisiaj
    ).all()

    for reservation in reservations_to_move:
        previous_reservation = previous_reservations(
            reservation_number=reservation.reservation_number,
            guest_id=reservation.guest_id,
            arrival_date=reservation.arrival_date,
            departure_date=reservation.departure_date,
            room_number=reservation.room_number,
        )
        db.session.add(previous_reservation)
    reservations.query.filter(reservations.departure_date < dzisiaj).delete()
    db.session.commit()

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

        # Sprawdź, czy gość już istnieje w bazie na podstawie danych identyfikujących (imię, nazwisko, data urodzenia, email).
        existing_guest = guests.query.filter_by(
            first_name=name, last_name=surname, birth_date=birth_date, email=email
        ).first()

        if existing_guest:
            # Jeśli gość już istnieje, zaktualizuj liczbę wizyt o 1.
            existing_guest.number_of_visits += 1
        else:
            # Jeśli gość nie istnieje, utwórz nowego gościa i zapisz go w bazie.
            new_guest = guests(
                first_name=name,
                last_name=surname,
                birth_date=birth_date,
                email=email,
                number_of_visits=1,
            )
            db.session.add(new_guest)

        # Utwórz rezerwację i zapisz ją w bazie.
        new_reservation = reservations(
            room_number=room_number,
            arrival_date=arrival_date,
            departure_date=departure_date,
            guest_id=existing_guest.guest_id if existing_guest else new_guest.guest_id,
        )
        db.session.add(new_reservation)

        # Zatwierdź zmiany w bazie danych.
        db.session.commit()

    return render_template("orders.html")


if __name__ == "__main__":
    app.run(debug=True)
