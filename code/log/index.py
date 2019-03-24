#import libs
from flask import Flask, render_template, jsonify, Response
import sqlite3
import json

app = Flask(__name__)

# get most recent count
@app.route("/")
def index():
    con = sqlite3.connect("room.db")
    cur = con.cursor()
    #cur.execute("SELECT * FROM rooms")
    #result = cur.fetchone()
    #print(result[2])
    return render_template('index.html')


# get the most recent data
@app.route("/catch")
def data():
    con = sqlite3.connect("room.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM rooms LIMIT 10")

    entry = cur.fetchall()
    data = []
    for row in entry:
        data.append(list(row))

    return Response(json.dumps(data),  mimetype='application/json')

#get number of database entries
@app.route("/count")
def dbcount():
    con = sqlite3.connect("room.db")
    cur = con.cursor()
    cur.execute("SELECT count(*) from rooms")
    count = cur.fetchall()
    return Response(json.dumps({"data" : count[0][0]}), mimetype='application/json')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
