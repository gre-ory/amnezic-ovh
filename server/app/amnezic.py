#!/usr/bin/python
# encoding: utf-8

#
# import
#

import os
import random
from flask import Flask, jsonify, request
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
  artist = db.Column( db.String( 120 ), unique=False, nullable=True )
  media = db.Column( db.String( 240 ), unique=True, nullable=False )
  cover = db.Column( db.String( 240 ), unique=False, nullable=True )
  
  tags = db.relationship( "Tag", secondary="music_tags", lazy=True )

  def __repr__( self ):
    return '<Music #%s - %s>' % ( self.id, self.title )

class Tag( db.Model ): 
  __tablename__ = 'tags'    
  id = db.Column( db.Integer, primary_key=True )
  name = db.Column( db.String( 120 ), unique=False, nullable=False )
  
  musics = db.relationship( "Music", secondary="music_tags" )

  def __repr__( self ):
    return '<Tag #%s - %s>' % ( self.id, self.name )

class MusicTag( db.Model ): 
  __tablename__ = 'music_tags'
  id = db.Column( db.Integer, primary_key=True )
  music_id = db.Column( db.Integer, db.ForeignKey( 'musics.id' ) )
  tag_id = db.Column( db.Integer, db.ForeignKey( 'tags.id' ) )

  music = db.relationship( Music, backref=db.backref( "music_tags", cascade="all, delete, delete-orphan" ) )
  tag = db.relationship( Tag, backref=db.backref( "music_tags", cascade="all, delete, delete-orphan" ) )

  def __repr__( self ):
    return '<MusicTag %s - %s - %s>' % ( self.id, self.music_id, self.tag_id )

#
# models
#

class Answer:
  
  def __init__( self, title, hint, correct ):
    self.title = title or 'Answer'
    self.hint = hint or 'Hint'
    self.correct = correct or False
    
class Question:
  
  def __init__( self, title, music ):
    self.title = title or 'Question'
    self.music = music
    self.answers = []
  
  def add_answer( self, answer ):
    if answer:
      self.answers.append( answer )

class Game:
  
  def __init__( self, nb_question, nb_answer ):
    self.nb_question = nb_question
    self.nb_answer = nb_answer
    self.questions = []
  
  def add_question( self, question ):
    if question:
      self.questions.append( question )

#
# services
#

def delete_tables():
  Tag.query.delete()
  Music.query.delete()
  MusicTag.query.delete()
  db.session.commit()  

def retrieve_musics():
  return Music.query.all()

def retrieve_music( music_id ):
  music = Music.query.filter_by( id=music_id ).first()
  if music is None:
    raise ItemNotFound( 'music' )
  return music   
  
def create_music( request ):
  if request is None:
    raise MissingItem( 'request' )
  db.session.add( Music( title=request.get( 'title' ), artist=request.get( 'artist' ), media=request.get( 'media' ), cover=request.get( 'cover' ) ) )
  music = Music.query.filter_by( media=request.get( 'media' ) ).first()
  for tag_name in request.get( 'tags', [] ):
    tag = retrieve_tag_by_name( tag_name )
    if tag is None:
      db.session.add( Tag( name=tag_name ) )
      tag = retrieve_tag_by_name( tag_name )
    music.tags.append( tag )
  db.session.commit()  
  return music   
  
def update_music( music_id, request ):
  if request is None:
    raise MissingItem( 'request' ) 
  music = Music.query.filter_by( id=music_id ).first()
  if music is None:
    raise ItemNotFound( 'music' )
  music.title = request.get( 'title', music.title )
  music.artist = request.get( 'artist', music.artist )
  music.media = request.get( 'media', music.media )
  music.cover = request.get( 'cover', music.cover )
  
  # tags
  
  old_tag_names = [ tag.name for tag in music.tags ]
  new_tag_names = [ tag_name for tag_name in request.get( 'tags', [] ) ]
  deleted_tag_names = [ old_tag_name for old_tag_name in old_tag_names if not old_tag_name in new_tag_names ]
  added_tag_names = [ new_tag_name for new_tag_name in new_tag_names if not new_tag_name in old_tag_names ]
  
  # remove deleted tags
  
  for tag in music.tags:
    if tag.name in deleted_tag_names:
      music.tags.remove( tag )
  
  # add new tags
  
  for added_tag_name in added_tag_names:
    tag = retrieve_tag_by_name( added_tag_name )
    if tag is None:
      db.session.add( Tag( name=added_tag_name ) )
      tag = retrieve_tag_by_name( added_tag_name )
    music.tags.append( tag )
  
  # remove unused tags
        
  for tag in Tag.query.all():
    if len( tag.musics ) == 0:
      db.session.delete( tag )     
         
  db.session.commit()  
  return music     

def retrieve_tags():
  return Tag.query.all()
  
def retrieve_tag( tag_id ):
  return Tag.query.filter_by( id=tag_id ).first()

def retrieve_tag_by_name( tag_name ):
  return Tag.query.filter_by( name=tag_name ).first()
  
def create_tag( tag_name ): 
  if not tag_name:
    raise MissingItem( 'tag name' )
  db.session.add( Tag( name=tag_name ) )
  db.session.commit()  
  return Tag.query.filter_by( name=tag_name ).first()    
  
def update_tag( tag_id, request ):
  if request is None:
    raise MissingItem( 'request' ) 
  tag = Tag.query.filter_by( id=tag_id ).first()
  if tag is None:
    raise ItemNotFound( 'tag' )
  tag.name = request.get( 'name', tag.name )
  db.session.commit()
  return Tag.query.filter_by( id=tag_id ).first()

def create_game():
  game = Game( nb_question=4, nb_answer=3 )
  
  musics = [ music for music in Music.query.all() if len( music.tags ) > 0 ]
  musics = random.sample( musics, min( len( musics ), game.nb_question ) )
  
  for music in musics:
    tags = [ tag for tag in music.tags if len( tag.musics ) > 1 ]
    if len( tags ) > 0:
      tag = random.choice( tags )
      question = Question( title=tag.name, music=music )
      
      answers = [ answer for answer in tag.musics if answer.id != music.id ]
      answers = random.sample( answers, min( len( answers ), game.nb_answer - 1 ) )
      answers.append( music )    
      random.shuffle( answers )
      for answer in answers:
        question.add_answer( Answer( title=answer.title, hint=answer.artist, correct=( answer.id == music.id ) ) )
        
      game.add_question( question )
  
  return game        

#
# resources
#

@app.route( '/amnezic/game', methods=[ 'GET' ] )
def api_game_create():
  return json_success( game=game_to_json( create_game() ) )

@app.route( '/amnezic/music', methods=[ 'GET' ] )
def api_music_retrieve_all():
  return json_success( musics=[ music_to_simple_json( music ) for music in retrieve_musics() ] )

@app.route( '/amnezic/music', methods=[ 'POST' ] )
def api_music_create():
  return json_success( music=music_to_json( create_music( request.get_json() ) ) )
    
@app.route( '/amnezic/music/<int:music_id>', methods=[ 'GET' ] )
def api_music_retrieve( music_id ):
  return json_success( music=music_to_json( retrieve_music( music_id ) ) )

@app.route( '/amnezic/music/<int:music_id>', methods=[ 'POST' ] )
def api_music_update( music_id ):
  return json_success( music=music_to_json( update_music( music_id, request.get_json() ) ) )

@app.route( '/amnezic/tag', methods=[ 'GET' ] )
def api_tag_retrieve_all():
  return json_success( tags=[ tag_to_simple_json( music ) for music in retrieve_tags() ] )
    
@app.route( '/amnezic/tag/<int:tag_id>', methods=[ 'GET' ] )
def api_tag_retrieve( tag_id ):
  return json_success( tag=tag_to_json( retrieve_tag( tag_id ) ) ) 

@app.route( '/amnezic/tag/<int:tag_id>', methods=[ 'POST' ] )
def api_tag_update( tag_id ):
  return json_success( tag=tag_to_json( update_tag( tag_id, request.get_json() ) ) ) 

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
  
@app.after_request
def after_request_func( response ):
  headers = response.headers
  headers['Access-Control-Allow-Origin'] = '*'
  return response

#
# adapters
#

def to_json( **kwargs ):
  return dict( ( key, value ) for key, value in kwargs.items() if value is not None )

def music_to_json( music ):
  return to_json( id=music.id, title=music.title, artist=music.artist, media=music.media, cover=music.cover, tags=[ tag.name for tag in music.tags if tag is not None ] ) if music is not None else None  

def music_to_simple_json( music ):
  return to_json( id=music.id, title=music.title, artist=music.artist ) if music is not None else None  

def music_tag_to_json( music_tag ):
  return to_json( id=music_tag.id, music=music_tag.music, tag=music_tag.tag ) if music_tag is not None else None  

def tag_to_json( tag ):
  return to_json( id=tag.id, name=tag.name, musics=[ music_to_simple_json( music ) for music in tag.musics ] ) if tag is not None else None

def tag_to_simple_json( tag ):
  return to_json( id=tag.id, name=tag.name ) if tag is not None else None
  
def answer_to_json( answer ):  
  return to_json( title=answer.title, hint=answer.hint, correct=True if answer.correct else None ) if answer is not None else None

def question_to_json( question ):  
  return to_json( title=question.title, music=music_to_json( question.music ), answers=[ answer_to_json( answer ) for answer in question.answers ] ) if question is not None else None

def game_to_json( game ):  
  return to_json( nb_question=game.nb_question, nb_answer=game.nb_answer, questions=[ question_to_json( question ) for question in game.questions ] ) if game is not None else None
  
def json_success( **kwargs ):
  if len( kwargs ) > 0:
    data = to_json( **kwargs )
    if len( data ) > 0:
      return jsonify( { 'success': 'true', 'data': data } )
    else:
      return jsonify( { 'error': 'missing object [%s] for json encoding!' % ','.join( kwargs.keys() ) } ), 404
  return jsonify( { 'success': 'true' } )  
    
#
# error handling
#    

class AppException(Exception):
  def __init__( self, httpStatus, msg ):
    self.httpStatus = httpStatus
    self.msg = msg

class MissingItem(Exception):
  def __init__(self, name):
    super( MissingItem, self ).__init__( 400, 'missing item [%s]!' % name )

class InvalidItem(Exception):
  def __init__(self, name):
    super( InvalidItem, self ).__init__( 400, 'invalid item [%s]!' % name )

class ItemNotFound(Exception):
  def __init__(self, name):
    super( ItemNotFound, self ).__init__( 404, 'item [%s] not found!' % name )

@app.errorhandler(Exception)
def all_exception_handler(error):
  if isinstance( error, AppException ):
    return jsonify( { 'error': error.msg } ), error.httpStatus
  return jsonify( { 'error': str(error) } ), 500

#
# main
#
    
if __name__ == "__main__":
    app.run( debug=True )    
            