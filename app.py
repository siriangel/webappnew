from flask import Flask, request, jsonify, render_template
import mysql.connector
import os

app = Flask(__name__)

# Configure the database connection
db_config = {
    'user': os.environ['DB_USER'],
    'password': os.environ['DB_PASSWORD'],
    'host': os.environ['DB_HOST'],
    'database': os.environ['DB_NAME']
}

conn = mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save_value():
    value = request.json['value']
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Values (Value) VALUES (%s)", (value,))
    conn.commit()
    return jsonify(success=True)

@app.route('/values', methods=['GET'])
def get_values():
    cursor = conn.cursor()
    cursor.execute("SELECT Value FROM Values")
    rows = cursor.fetchall()
    values = [row[0] for row in rows]
    return jsonify(values=values)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
