from flask import Flask, render_template, jsonify, Response
import sqlite3 as sql
import json
#temp
app = Flask(__name__)
@app.route("/")
def ap():
    #set last entry equal to temp
    conn = sql.connect("./temperature.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM tempData ORDER BY rowid DESC LIMIT 1")
    result = cur.fetchone()
    temp = result[1]
    print(result[2])
    temp = result[2]
    return render_template('index.html', temp = temp)

#data
@app.route("/fetch")
def data():
    conn = sql.connect("./temperature.db")
    conn.row_factory = sql.Row
   
    cur = conn.cursor()
    cur.execute("SELECT * FROM tempData")

    entry = cur.fetchall()
    data = []
    for row in entry:
        data.append(list(row))

    return Response(json.dumps(data),  mimetype='application/json')
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
