import models.sqlmodel as execSql
from flask import current_app


def insert_user(name, age):
    statement = "INSERT INTO users(Name, Age) VALUES (?, ?)"
    result = execSqlCmd(statement, [name, age])

    if result:
        response = "success"
    else:
        response = "fail"
    return response


def bulk_insert_user(data):
    statement = "INSERT INTO users(Name, Age) VALUES (?, ?)"
    result = execmanySqlCmd(statement, data)

    if result:
        response = "success"
    else:
        response = "fail"
    return response


def update_user(id, name, age):
    statement = "UPDATE users SET Name = ?, Age = ? WHERE Id = ?"
    result = execSqlCmd(statement, [name, age, id])

    if result:
        response = "success"
    else:
        response = "fail"
    return response


def delete_user(id):
    statement = "DELETE FROM users WHERE Id = ?"
    result = execSqlCmd(statement, [id])

    if result:
        response = "success"
    else:
        response = "fail"
    return response


def get_by_id(id):
    query = "SELECT Id, Name, Age FROM users WHERE Id = ?"
    result = querySqlCmd(query, [id])
    return result


def get_users():
    query = "SELECT Id, Name, Age FROM users"
    result = querySqlCmd(query, [])
    return result


def querySqlCmd(query, args):
    with current_app.app_context():
        try:
            db = execSql.connect_db()
            cursor = db.cursor()
            query = query
            cursor.execute(query, args)
            result = cursor.fetchall()
            return result
        except AssertionError as err:
            db.close()
            return err


def execSqlCmd(statement, args):
    with current_app.app_context():
        try:
            db = execSql.connect_db()
            cursor = db.cursor()
            statement = statement
            # Fill the table
            cursor.execute(statement, args)
            db.commit()
            return True
        except AssertionError as err:
            db.close()
            return err


# bulk insert
def execmanySqlCmd(statement, data):
    with current_app.app_context():
        try:
            db = execSql.connect_db()
            # If Exists fill the table or create table
            data.to_sql("users", db, if_exists="append", index=False)
            return True
        except AssertionError as err:
            db.close()
            return err
