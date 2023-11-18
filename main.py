import base64
import sqlite3
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('../db/cars_parts_database.db')
    curr = conn.cursor()
    return conn, curr


@app.route('/api/projects', methods=['GET'])
def Projects():
    conn, curr = get_db_connection()
    projects = curr.execute('SELECT * FROM Cars').fetchall()
    conn.close()

    return jsonify(projects)


@app.route('/api/projects', methods=['POST'])
def NewProject():
    uploaded_file = request.files.get('file')
    if uploaded_file:
        image_data = uploaded_file.read()
        encoded_image_data = base64.b64encode(image_data).decode('utf-8')
    car_data = json.loads(request.form['car_details'])

    conn, curr = get_db_connection()
    curr.execute('''INSERT INTO Cars(Make, Model, Year, Misc_Info, Image) VALUES ('{}', '{}', {}, '{}', '{}')'''.format(car_data["Make"], car_data["Model"], int(car_data["Year"]), car_data["Description"], encoded_image_data))
    
    conn.commit()
    conn.close()

    return "0"


@app.route('/api/del_project/<id>', methods=['POST'])
def DelProject(id):
    try:
        conn, curr = get_db_connection()
        curr.execute('''DELETE FROM Cars WHERE ID={}'''.format(id))

        conn.commit()
        conn.close()

    except:
        raise

    finally:
        return "0"


if __name__ == "__main__":
    app.run(ssl_context="adhoc")