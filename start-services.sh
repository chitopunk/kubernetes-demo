#!/bin/bash

pushd /var/app

curl -s -L https://github.com/google/protobuf/releases/download/v3.1.0/protoc-3.1.0-linux-x86_64.zip -o protoc-3.1.0-linux-x86_64.zip 
unzip -qq protoc-3.1.0-linux-x86_64.zip -d protoc && protoc/bin/protoc --python_out=import_style=binary:. --proto_path=/var/app /var/app/addressbook.proto

python app.py
