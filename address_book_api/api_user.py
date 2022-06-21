"""
:author: riccardo mei
:encoding: utf-8
"""
import flask, flask_cors
import json
import traceback
from functools import wraps
from db_handler import * # local library

APIKEY = "secret_psw"

app = flask.Flask(__name__)
flask_cors.CORS(app=app)


def send_json(result=None, status=200, error=None):
    """Sends the default response model common to all APIs.
    """
    dati_da_inviare = {
        'error': error,
        'status': status,
        'result': result
    }
    return flask.Response(
        json.dumps(dati_da_inviare),
        status,
        content_type="application/json"
    )


# this is a decorator function
def only_with_apikey(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_apikey = flask.request.form.get("apiKey")
        if user_apikey != APIKEY:
            return send_json(error="Invalid APIKEY", status=401)
        data = flask.request.form.get("data")
        data = json.loads(data)
        return f(data, *args, **kwargs)
    return decorated_function


#--------- error handling ---------#
@app.errorhandler(Exception)
def error_handler(e):
    print(traceback.print_exc())
    return send_json(
        error=str(e),
        status=500
    )


@app.errorhandler(404)
def error_handler(_):
    return send_json(
        error="The API does not exist.",
        status=500
    )
#--------- error handling ---------#


@app.route("/list", methods=["POST", "GET"])
@only_with_apikey
def list_users(data):
    limit = data.get("limit", 10)
    offset = data.get("offset", 0)
    return send_json(
        result=db_get_users(limit, offset)
    )


@app.route("/search", methods=["POST", "GET"])
@only_with_apikey
def search(data):
    query = data.get("q")
    if not query:
        raise Exception("The \'q\' parameter is mandatory")
    return send_json(
        result=db_search_user(query)
    )


@app.route("/insert", methods=["POST", "GET"])
@only_with_apikey
def insert(data):
    nome = data.get("nome")
    cognome = data.get("cognome")
    email = data.get("email")
    telefono = data.get("telefono")
    utente = (nome, cognome, email, telefono)
    last_user_id = db_insert_user(utente)
    return send_json(
        result=last_user_id
    )


@app.route("/delete", methods=["POST", "GET"])
@only_with_apikey
def delete_user(data):
    utente_id = data.get("utente_id")
    return send_json(
        result=db_delete_user(utente_id)
    )


@app.route("/update", methods=["POST", "GET"])
@only_with_apikey
def update_user(data):
    nome = data.get("nome")
    cognome = data.get("cognome")
    email = data.get("email")
    telefono = data.get("telefono")
    utente_id = data.get("utente_id")
    utente = (nome, cognome, email, telefono, utente_id)
    return send_json(
        result=db_update_user(utente)
    )


# In a real use-case, this will not happen
# the API user is never defined within the API itself
@app.route("/")
def interface():
    return flask.render_template("interface.html")


if __name__ == '__main__':
    app.run()
