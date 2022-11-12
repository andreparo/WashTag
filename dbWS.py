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
def get_data():
    connection =psycopg2.connect(host = "localhost", database="Washtags", user="postgres", password="pippi2802")
    connection.autocommit = True
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM programswm;")
    programs = cursor.fetchall()

    print(programs)
    cursor.close()
    connection.close()
    return render_template("program.html", progs = programs)

#add program to app



if __name__ == "__main__": 
    app.run(host="0.0.0.0", port = 8080, threaded = True, debug=True)