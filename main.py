import mysql.connector
from flask import Flask, request, jsonify

from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="flask_db"
    )

@app.route("/get-user/<user_id>", methods=["GET"])
def get_user(user_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    db.close()

    if user_data:
        return jsonify(user_data), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()
    user_id = data.get("user_id")
    name = data.get("name")
    email = data.get("email")
    extra = data.get("extra")

    db = get_db_connection()
    cursor = db.cursor()
    query = "INSERT INTO users (user_id, name, email, extra) VALUES (%s, %s, %s, %s)"
    values = (user_id, name, email, extra)

    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"message": "User created successfully!"}), 201

@app.route("/update-user/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    print(    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
              )
    if cursor.fetchone() is None:
        return jsonify({"error": "User not found"}), 404

    query = "UPDATE users SET name = %s, email = %s, extra = %s WHERE user_id = %s"
    values = (data.get("name"), data.get("email"), data.get("extra"), user_id)

    cursor.execute(query, values)
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"message": "User updated successfully!"}), 200

@app.route("/delete-user/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    if cursor.fetchone() is None:
        return jsonify({"error": "User not found"}), 404

    cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"message": f"User {user_id} deleted successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
