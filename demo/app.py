from flask import Flask
from flask_cors import CORS  # cross-origin
from api.users import users

from models.sqlmodel import execSql, create_tables
from flasgger import Swagger

# demo\Scripts\activate 啟用虛擬環境
# deactivate 停止虛擬環境
swagger_template = {
    "title": "FlaskAPI",
    "description": "Demo",
    "version": "0.9.5",
    "termsOfService": "",
    "servers": [
        {
            "url": "localhost",
            "description": "Optional server description, e.g. Main (production) server",
        }
    ],
}

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["SWAGGER"] = swagger_template

CORS(app)
Swagger(app)

app.register_blueprint(users, url_prefix="/api/v1")  # using Blueprint manage web
app.register_blueprint(execSql)

# 主程式
if __name__ == "__main__":
    create_tables(app)
    app.run(host="0.0.0.0", port=80, debug=True)  # Starts the debugger
