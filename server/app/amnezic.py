#!/usr/bin/python
# encoding: utf-8

#
# import
#

import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

#
# app
#

app = Flask( __name__ )
server_dir = os.getcwd() # run from flask.cgi

db_file = os.path.join( server_dir, 'db', 'amnezic.db' )
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///%s' % db_file
db = SQLAlchemy( app )

#
# database
#

class Music( db.Model ):
  __tablename__ = 'musics'
  id = db.Column( db.Integer, primary_key=True )
  title = db.Column( db.String( 120 ), unique=False, nullable=False )
  artist = db.Column( db.String( 120 ), unique=False, nullable=False )
  media = db.Column( db.String( 240 ), unique=False, nullable=False )
  cover = db.Column( db.String( 240 ), unique=False, nullable=True )
  
  #tags = db.relationship( "Tag", secondary="music_tags" )

  def __repr__( self ):
    return '<Music #%s - %s>' % ( self.id, self.title )

class Tag( db.Model ): 
  __tablename__ = 'tags'    
  id = db.Column( db.Integer, primary_key=True )
  name = db.Column( db.String( 120 ), unique=False, nullable=False )
  
  # musics = db.relationship( "Music", secondary="music_tags" )

  def __repr__( self ):
    return '<Tag #%s - %s>' % ( self.id, self.name )

#class MusicTag( db.Model ): 
#  __tablename__ = 'music_tags'
#  id = db.Column( db.Integer, primary_key=True )
#  music_id = db.Column( db.Integer, db.ForeignKey( 'musics.id' ) )
#  tag_id = db.Column( db.Integer, db.ForeignKey( 'tags.id' ) )
#
#  music = db.relationship( Music, backref=db.backref( "music_tags", cascade="all, delete-orphan" ) )
#  tag = db.relationship( Tag, backref=db.backref( "music_tags", cascade="all, delete-orphan" ) )
#
#  def __repr__( self ):
#    return '<MusicTag %s - %s - %s>' % ( self.id, self.music_id, self.tag_id )

#
# services
#

def delete_tables():
  Tag.query.delete()
  Music.query.delete()

def retrieve_musics():
  return Music.query.all()
  
def retrieve_music( music_id ):
  return Music.query.filter_by( id=music_id ).first()    

def retrieve_tags():
  return Tag.query.all()
  
def retrieve_tag( tag_id ):
  return Tag.query.filter_by( id=tag_id ).first()    

#
# adapters
#

def to_json( **kwargs ):
  return dict( ( key, value ) for key, value in kwargs.items() if value is not None )

def music_to_json( music ):
  return to_json( id=music.id, title=music.title, artist=music.artist, media=music.media, cover=music.cover ) if music is not None else None  

def music_tag_to_json( music_tag ):
  return to_json( id=music_tag.id, music=music_tag.music, tag=music_tag.tag ) if music_tag is not None else None  

def tag_to_json( tag ):
  return to_json( id=tag.id, name=tag.name ) if tag is not None else None
  
def json_success( **kwargs ):
  if len( kwargs ) > 0:
    data = to_json( **kwargs )
    if len( data ) > 0:
      return jsonify( { 'success': 'true', 'data': data } )
    else:
      return jsonify( { 'error': 'missing %s!' % ','.join( kwargs.keys() ) } ), 404
  return jsonify( { 'success': 'true' } )

#
# resources
#

@app.route( '/amnezic/music', methods=[ 'GET' ] )
def api_music_retrieve_all():
  return json_success( musics=[ music_to_json( music ) for music in retrieve_musics() ] )
    
@app.route( '/amnezic/music/<int:music_id>', methods=[ 'GET' ] )
def api_music_retrieve( music_id ):
  return json_success( music=music_to_json( retrieve_music( music_id ) ) )

@app.route( '/amnezic/tag', methods=[ 'GET' ] )
def api_tag_retrieve_all():
  return json_success( tags=[ tag_to_json( music ) for music in retrieve_tags() ] )
    
@app.route( '/amnezic/tag/<int:tag_id>', methods=[ 'GET' ] )
def api_tag_retrieve( tag_id ):
  return json_success( tag=tag_to_json( retrieve_tag( tag_id ) ) ) 

@app.route( '/amnezic/db/drop', methods=[ 'GET' ] )
def api_db_drop_all():
  db.drop_all()
  return json_success()
 
@app.route( '/amnezic/db/create', methods=[ 'GET' ] )
def api_db_create_all():
  db.create_all()
  return json_success()

@app.route( '/amnezic/db/delete', methods=[ 'GET' ] )
def api_db_delete():
  delete_tables()
  return json_success()
  
@app.route( '/amnezic/db/insert', methods=[ 'GET' ] )
def api_db_insert():
  delete_tables()
  
  db.session.add( Tag( name='Rock' ) )
  db.session.add( Tag( name='1990' ) )
  
  db.session.add( Music( title='Bitter sweet symphony', artist='The Verve', media='http://cache.amnezic.com/8150_TheVerve_Bittersweetsymphony_1997.mp3' ) )
  db.session.add( Music( title='Avalon', artist='Roxy Music', media='http://cache.amnezic.com/6976_RoxyMusic_Avalon_1982.mp3' ) )
  db.session.add( Music( title='Woman', artist='John Lennon', media='http://cache.amnezic.com/49957_JohnLennon_Woman_1980.mp3' ) )
  db.session.add( Music( title='Only you', artist='The Platters', media='http://cache.amnezic.com/6367_ThePlatters_Onlyyou_1956.mp3' ) )
  
  db.session.commit()
  
  return json_success()
    
#
# error handling
#    

@app.errorhandler(Exception)
def all_exception_handler(error):
  return jsonify( { 'error': str(error) } ), 500

#
# main
#
    
if __name__ == "__main__":
    app.run(debug=True)    
            