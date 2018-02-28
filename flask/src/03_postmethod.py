from flask import Flask, request, json, Response
import time

app = Flask(__name__)


@app.route('/post', methods=['POST'])
def post():
    if request.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + str(request.data)

    elif request.headers['Content-Type'] == 'application/json':
        # loads would take a file-like object, read the data from that object, and use that string to create an object
        request_data = json.loads(request.data)
        data = {
            'timestamp': time.time(),
            'request-data': request_data
        }
        # dumps takes an json object and produces a string
        js = json.dumps(data)

        resp = Response(js, status=200, mimetype='application/json')
        resp.headers['referer'] = 'http://localhost:5000'
        return resp


if __name__ == "__main__":
    app.run(debug=True)
