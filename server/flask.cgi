#!/usr/bin/python
# encoding: utf-8

#
# import
#

import os
import sys

#
# dependencies
#

server_dir = os.getcwd()
app_dir = os.path.join( server_dir, 'app' )
lib_dir = os.path.join( server_dir, 'lib', 'flask_1.1.1' )

sys.path.append( "%s" % server_dir )
sys.path.append( "%s" % app_dir )
sys.path.append( "%s" % lib_dir )
sys.path.append( "%s/click" % lib_dir )
sys.path.append( "%s/flask" % lib_dir )
sys.path.append( "%s/flask_sqlalchemy" % lib_dir )
sys.path.append( "%s/itsdangerous" % lib_dir )
sys.path.append( "%s/jinja2" % lib_dir )
sys.path.append( "%s/markupsafe" % lib_dir ) 
sys.path.append( "%s/sqlalchemy" % lib_dir )
sys.path.append( "%s/werkzeug" % lib_dir )

#
# run
#

def run_with_cgi(application):
    environ                      = dict(os.environ.items())
    environ['wsgi.input']        = sys.stdin
    environ['wsgi.errors']       = sys.stderr
    environ['wsgi.version']      = (1,0)
    environ['wsgi.multithread']  = False
    environ['wsgi.multiprocess'] = True
    environ['wsgi.run_once']     = True

    if environ.get('HTTPS','off') in ('on','1'):
        environ['wsgi.url_scheme'] = 'https'
    else:
        environ['wsgi.url_scheme'] = 'http'

    headers_set  = []
    headers_sent = []

    def write(data):
        if not headers_set:
             raise AssertionError("write() before start_response()")

        elif not headers_sent:
             # Before the first output, send the stored headers
             status, response_headers = headers_sent[:] = headers_set
             sys.stdout.write('Status: %s\r\n' % status)
             for header in response_headers:
                 sys.stdout.write('%s: %s\r\n' % header)
             sys.stdout.write('\r\n')

        sys.stdout.write(data)
        sys.stdout.flush()

    def start_response(status,response_headers,exc_info=None):
        if exc_info:
            try:
                if headers_sent:
                    # Re-raise original exception if headers sent
                    raise exc_info[0], exc_info[1], exc_info[2]
            finally:
                exc_info = None     # avoid dangling circular ref
        elif headers_set:
            raise AssertionError("Headers already set!")

        headers_set[:] = [status,response_headers]
        return write

    result = application(environ, start_response)
    try:
        for data in result:
            if data:    # don't send headers until body appears
                write(data)
        if not headers_sent:
            write('')   # send headers now if body was empty
    finally:
        if hasattr(result,'close'):
            result.close()

#
# main
#

try:
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    sys.dont_write_bytecode = True
    # print "Content-type: text/html\n\n"

    uri = os.environ['REQUEST_URI']
    path = [ p for p in uri.split( '/' ) if p != '' ]
    if len( path ) == 0:
      raise AssertionError( 'missing flask application!' )
    app_name = path[0]
    app_file = os.path.join( os.getcwd(), 'app', '%s.py' % app_name )      
    if not os.path.isfile( app_file ):
      raise AssertionError( 'unknow %s application!' % app_name )

    if False:
      print "Content-type: text/html\n\n"
      print "<code style=\"display: block;margin: 10px 5%;width: 90%;text-align: left;border: 1px solid black;padding: 20px;background: rgba(0,0,0,0.2);\">"
      print "app_name: %s" % app_name
      print "<br>root: %s" % os.getcwd()
      print "<br>HTTP_HOST: %s" % os.environ['HTTP_HOST']
      print "<br>REQUEST_URI: %s" % os.environ['REQUEST_URI']
      print "<br>uri: %s" % uri
      print "<br>path: %s" % len( path )
      print "<br>path: %s" % ",".join( path )
      print "<br>app_name: %s" % app_name
      print "<br>app_file: %s" % app_file
      print "<br>is_file: %s" % os.path.isfile( app_file )
      print "<br>from app.%s import app as application" % app_name
      print "</code>"
    
    exec( 'from app.%s import app as application' % app_name )
    run_with_cgi( application )
    
except Exception, inst:
  print "Content-type: text/html\n\n"
  print "<code style=\"display: block;margin: 100px 20%;width: 60%;text-align: center;border: 1px solid red;padding: 20px;background: rgba(255,0,0,0.2);\">"
  print "error: %s" % inst
  print "</code>"
