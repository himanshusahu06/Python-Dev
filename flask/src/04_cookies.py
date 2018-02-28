from flask import Flask, json, request, Response
import jwt
import time
app = Flask(__name__)

secret = 'secret@123'
algorithm = 'HS256'

def create_login_token(username, password):
    data = {
        'username': username,
        'password': password,
        'created_timestamp': time.time()
    }
    jwt_encoded = jwt.encode(data, secret, algorithm) or None
    return jwt_encoded


def verify_login_token(token):
    try:
        jwt_decoded = jwt.decode(token, secret, algorithm)
        created_timestamp = jwt_decoded['created_timestamp']
        current_timestamp = time.time()
        return current_timestamp - created_timestamp <= 260
    except:
        return False


def get_error_response(error_message):
    data = {
        "errors": [
            {
                'error': error_message
            }
        ]
    }
    return json.dumps(data)


def get_success_response():
    data = {
        'status': 'OK'
    }
    return json.dumps(data)


@app.route("/login", methods=["POST"])
def login():
    login_data = json.loads(request.data)

    if 'username' in login_data and 'password' in login_data:
        login_token = create_login_token(login_data['username'], login_data['password'])
        if login_token:
            success_response_json = get_success_response()
            resp = Response(success_response_json, status=200, mimetype='application/json')
            resp.set_cookie('token', login_token)
            return resp
        else:
            error_response_json = get_error_response("somthing went wrong")
            resp = Response(error_response_json, status=401, mimetype='application/json')
            return resp
    else:
        error_response_json = get_error_response("Invalid username or password")
        resp = Response(error_response_json, status=401, mimetype='application/json')
        return resp

@app.route("/login-status")
def verify_login():
    token = request.cookies.get('token')
    if not token:
        error_response_json = get_error_response("Not LoggedIn")
        resp = Response(error_response_json, status=401, mimetype='application/json')
        return resp
    else:
        verify_token = verify_login_token(token)
        if verify_token:
            return Response(get_success_response(), status=200, mimetype='application/json')
        else:
            return Response(get_error_response("Token is invalid / expired"), status=401, mimetype='application/json')


if __name__ == "__main__":
    app.run()
