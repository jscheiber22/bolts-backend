import sqlite3
from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('../db/cars_parts_database.db')
    curr = conn.cursor()
    return curr


@app.route('/api/projects')
def Projects():
    curr = get_db_connection()
    projects = curr.execute('SELECT * FROM Cars').fetchall()
    # print(projects)
    curr.close()
    return jsonify(projects)

@app.route('/api/new_project', methods=['POST'])
def NewProject():
    resp = Response("0")
    resp.headers['Access-Control-Allow-Origin'] = '*'

    print("text")
    file = request.files.get('file')
    file.save("pic.jpg")
    car_data = request.form['car_details']
    print(file)
    print(car_data)

    return resp


if __name__ == "__main__":
    app.run(ssl_context="adhoc")