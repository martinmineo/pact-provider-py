from dataclasses import dataclass
from typing import Optional

from flask import Flask, jsonify

app = Flask(__name__)

FAKE_DB = {
    1: {"id": 1, "name": "Alice", "age": 78, "email": "alice@mail.com"},
    2: {"id": 2, "name": "Bob", "age": 25, "email": "bob@mail.com"},
    3: {"id": 3, "name": "Charlie", "age": 6, "email": "charlie@mail.com"},
}


@dataclass()
class User:
    id: int
    name: str
    age: Optional[int]
    email: str


@app.route('/users', methods=['GET'])
def get_all_users():
    return jsonify(list(FAKE_DB.values()))


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = FAKE_DB.get(user_id)
    if user is None:
        return jsonify({"detail": "User not found"}), 404
    return jsonify(user)


if __name__ == '__main__':
    app.run(debug=True)
