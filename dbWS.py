import psycopg2
from flask import Flask, request
from flask import render_template
from flask import redirect

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

#retrive data from DB
@app.route("/program")
def get_data(program):
    connection =psycopg2.connect(host = "localhost", database="Washtags", user="postgres", password="pippi2802")
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM programswm WHERE number = %s", (program,))
    single_program = cursor.fetchone()

    print(single_program)
    cursor.close()
    connection.close()
    return render_template("program.html", prog = single_program)

#add program to app
@app.route("/program/add", methods=["GET", "POST"])
def add_program():
    if request.method == "GET":
        return render_template("add.html")

    if request.method == "POST":

        connection = psycopg2.connect(host="localhost", database="Washtags", user="postgres", password="pippi2802")
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute("INSERT INTO programswm (number, name, temperature, spin, typeCloth, duration, ecosaver, prewash VALUES (%s, %s, %s, %s, %s, %s, %s, %s))", (program, name, temp, sping, tc, time, eco, pre))
        cursor.close()
        connection.close()
    
    return redirect("/program")


if __name__ == "__main__": 
    app.run(host="0.0.0.0", port = 8080, threaded = True, debug=True)