import json

import jsonschema
from jsonschema import validate

from flask import Flask
from flask_compress import Compress
from flask import request
from flask import Response
from flask import render_template
import addressbook_pb2
import data

app = Flask(__name__)
Compress(app)

schema = {
    "type": "object",
    "properties": {
        "first_name": { "type": "string"},
        "last_name": { "type": "string"},
        "address": {
            "type": "object",
            "properties": {
                "postcode": {"type": "string"},
                 "address_lines": {
                      "type": "array",
                      "items": {"type": "string"}
                 }
            }
        },
        "phone_numbers": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type":"string"},
                    "number": {"type": "string"}
                },
                "required": ["type", "number"]
            }
        },
    },
    "required": ["first_name", "last_name", "address", "phone_numbers"]
}

def validate_post(post_data):
    try:
        validate(post_data, schema)
    except:
        return False
    return True

@app.route('/', methods=['GET'])
def home():
    return json.dumps('{}')

@app.route('/api/contacts', methods=['GET', 'POST'])
def contacts():

    if request.is_json:
        if request.method == 'GET':
            return Response(json.dumps(data.contacts), mimetype = "application/json")
        elif request.method == 'POST':
            post_data = request.get_json()
            if not validate_post(post_data):
                response = Response(json.dumps({"status":"error"}), mimetype='application/json')
                response.status_code = 400
                return response
            data.contacts.append(request.get_json())
            return json.dumps(data.contacts)

    else:
        if request.method == 'GET':
            return data.get_protobuf_data().SerializeToString()

    # Won't persist protobuf ones, just to see how that works
    contact = addressbook_pb2.Contact()
    contact.ParseFromString(request.data)
    address_book = data.get_protobuf_data()
    address_book.contacts.extend([contact])
    return address_book.SerializeToString()

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
