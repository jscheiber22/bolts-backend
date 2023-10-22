import sqlite3
from flask import Flask, jsonify
from flask_cors import CORS

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
    print(projects)
    curr.close()
    return jsonify(projects)


if __name__ == "__main__":
    app.run(ssl_context="adhoc")