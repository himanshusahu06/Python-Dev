import json
import jwt

datastore = '{"username": "hsahu", "password": "password@123"}'
json_data = json.loads(datastore)

secret = 'secret@123'
algorithm = 'HS256'

print(json_data)

encoded_string = jwt.encode(json_data, secret, algorithm)

print(encoded_string)

decoded_string = jwt.decode(encoded_string, secret, algorithm)

print(decoded_string)
