import sqlite3
from flask import Flask, jsonify, request, Response
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('../db/cars_parts_database.db')
    curr = conn.cursor()
    return conn, curr


@app.route('/api/projects')
def Projects():
    conn, curr = get_db_connection()
    projects = curr.execute('SELECT * FROM Cars').fetchall()
    conn.close()
    return jsonify(projects)


@app.route('/api/new_project', methods=['POST'])
def NewProject():
    try:
        # required to appease CORS otherwise it throws a big fit
        resp = Response("0")
        resp.headers['Access-Control-Allow-Origin'] = '*'

        file = request.files.get('file')
        if file:
            file.save("pic.jpg")
        car_data = json.loads(request.form['car_details'])

        conn, curr = get_db_connection()
        curr.execute('''INSERT INTO Cars(Make, Model, Year, Misc_Info, img_Location) VALUES ('{}', '{}', {}, '{}', '{}')'''.format(car_data["Make"], car_data["Model"], int(car_data["Year"]), car_data["Description"], ""))


    except:
        resp = Response("-1")
        raise

    finally:
        resp.headers['Access-Control-Allow-Origin'] = '*'
        conn.commit()
        conn.close()
        return resp


@app.route('/api/del_project/<id>', methods=['POST'])
def DelProject(id):
    try:
        # required to appease CORS otherwise it throws a big fit
        resp = Response("0")
        resp.headers['Access-Control-Allow-Origin'] = '*'

        conn, curr = get_db_connection()

        curr.execute('''DELETE FROM Cars WHERE ID={}'''.format(id))

    except:
        resp = Response("-1")
        raise

    finally:
        resp.headers['Access-Control-Allow-Origin'] = '*'
        conn.commit()
        conn.close()
        return resp


if __name__ == "__main__":
    app.run(ssl_context="adhoc")