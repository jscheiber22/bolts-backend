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


@app.route('/api/projects/<id>', methods=['GET'])
def GetProjectData(id):
    conn, curr = get_db_connection()
    project_data = curr.execute('SELECT * FROM Cars WHERE ID={}'.format(id)).fetchone()
    conn.close()

    return jsonify(project_data)


@app.route('/api/projects/<id>', methods=['PATCH'])
def PatchProjectData(id):
    print("this")
    update_data = request.get_json()
    print(update_data)
    conn, curr = get_db_connection()
    for item in update_data:
        curr.execute('''UPDATE Cars SET {} = {} WHERE id={}'''.format(item, update_data[item], id))
    conn.commit()
    conn.close()

    return "0"


@app.route('/api/projects', methods=['GET'])
def GetAllProjectData():
    conn, curr = get_db_connection()
    projects = curr.execute('SELECT * FROM Cars').fetchall()
    conn.close()

    return jsonify(projects)


@app.route('/api/projects', methods=['POST'])
def PostNewProject():
    uploaded_file = request.files.get('file')
    if uploaded_file:
        image_data = uploaded_file.read()
        encoded_image_data = base64.b64encode(image_data).decode('utf-8')
    car_data = json.loads(request.form['car_details'])

    conn, curr = get_db_connection()
    # Adds new data to database, defaulting the favorite option to 0 for False
    curr.execute('''INSERT INTO Cars(Make, Model, Year, Misc_Info, Image, Favorite) VALUES ('{}', '{}', {}, '{}', '{}', 0)'''.format(car_data["Make"], car_data["Model"], int(car_data["Year"]), car_data["Description"], encoded_image_data))
    
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


# combine this with the get project data by id function
@app.route('/api/locations/<id>', methods=['GET'])
def GetLocationData(id):
    conn, curr = get_db_connection()
    project_data = curr.execute('SELECT * FROM Locations WHERE Car_ID={}'.format(id)).fetchall()
    # print(project_data)
    conn.close()

    return jsonify(project_data)


@app.route('/api/locations/<id>', methods=['POST'])
def AddLocationData(id):
    update_data = request.get_json()

    conn, curr = get_db_connection()
    # Adds new data to database, defaulting the favorite option to 0 for False
    curr.execute('''INSERT INTO Locations(Name, Description, Image, Car_ID) VALUES ('{}', '', '', '{}')'''.format(update_data["Name"], id))
    
    conn.commit()
    conn.close()

    return "0"


@app.route('/api/del_location/<location_id>', methods=['POST'])
def DelLocation(location_id):
    try:
        conn, curr = get_db_connection()
        curr.execute('''DELETE FROM Locations WHERE ID={}'''.format(location_id))

        conn.commit()
        conn.close()

    except:
        raise

    finally:
        return "0"



if __name__ == "__main__":
    app.run(ssl_context="adhoc")