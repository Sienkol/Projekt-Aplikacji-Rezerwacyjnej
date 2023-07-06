from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)


app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "6133"
app.config["MYSQL_DB"] = "sql_store"
mysql = MySQL(app)


##Strona główna
@app.route("/")
def hello():
    return "Witaj, świecie!"


##Strona do wczytywania danych z mysql
@app.route("/sql")
def sikuel():
    cursor = mysql.connect.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    return render_template("orders.html", orders=orders)
