#!/usr/bin/python
# encoding: utf-8

#
# import
#

import os
from flask import Flask, jsonify

#
# app
#

app = Flask( __name__ )

#
# mock
#

mock = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web', 
        'done': False
    }
]

#
# resources
#

@app.route( '/music', methods=[ 'GET' ] )
def retrieve_all():
    return jsonify( { 'musics': mock } )
    
@app.route( '/music/<int:music_id>', methods=[ 'GET' ] )
def retrieve( music_id ):
    music = [ music for music in mock if music['id'] == music_id ]
    if len( music ) == 0:
        abort( 404 )
    return jsonify( music[0] )        