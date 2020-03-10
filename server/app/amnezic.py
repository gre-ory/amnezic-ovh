#!/usr/bin/python
# encoding: utf-8

#
# import
#

from flask import Flask, jsonify

#
# app
#

app = Flask( __name__ )

#
# root
#

@app.route( '/' )
def hello_world():
    return 'Hello from Flask'
    
@app.route( '/test' )
def hello_test():
    return 'Hello test from Flask'    