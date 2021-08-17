from flask import request, jsonify
from flask import Blueprint
from flasgger.utils import swag_from
import models.sqlmodel as execSql
import models.user_controller as user_controller
import pandas as pd

users = Blueprint("user", __name__)


@users.route("/users", methods=["GET"])
@swag_from("getlist.yml")
def get_users():
    users = user_controller.get_users()
    result = []
    for obj in users:
        dct = dict(zip(["id", "name", "age"], obj))
        result.append(dct)
    result = sorted(result, key=lambda k: k["id"])
    return jsonify(result)


@users.route("/users", methods=["POST"])
@swag_from("importlist.yml")
def add_users():
    user_details = request.get_json()
    name = user_details["name"]
    age = user_details["age"]
    result = user_controller.insert_user(name, age)
    return jsonify(result)


@users.route("/users/<int:id>", methods=["GET"])
@swag_from("getbyid.yml")
def get_user_by_id(id):
    user = user_controller.get_by_id(id)[0]
    result = dict(zip(["id", "name", "age"], user))
    return jsonify(result)


@users.route("/users/<int:id>", methods=["PUT"])
@swag_from("updatebyid.yml")
def update_user(id):
    user_details = request.get_json()
    name = user_details["name"]
    age = user_details["age"]
    result = user_controller.update_user(id, name, age)
    return jsonify(result)


@users.route("/users/<int:id>", methods=["DELETE"])
@swag_from("deletebyid.yml")
def delete_user(id):
    result = user_controller.delete_user(id)
    return jsonify(result)


@users.route("/batch-users-import", methods=["POST"])
@swag_from("batchImport.yml")
def batch_import_users():
    file = request.files["file"]
    if not file:
        return "No file"

    csv_input = pd.read_csv(file, header=0)
    data = pd.DataFrame(csv_input, columns=["Name", "Age"])
    print(type(data))
    result = user_controller.bulk_insert_user(csv_input)

    if result:
        response = "success"
    else:
        response = "fail"
    return response
