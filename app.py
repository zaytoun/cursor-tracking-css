import time
import urllib.parse
from flask import Flask, session, render_template, Response, request, send_from_directory

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'SECRET_KEY'

@app.route('/')
def root():
	return Response(get_file_and_format('html/index.html','<link rel="stylesheet" href="/static/css/tracker.css">'),
			        mimetype='text/html')
    #return render_template('index.html', import_line='<link rel="stylesheet" href="/static/css/tracker.css">')

@app.route('/tracker/<selector>/<duration>/')
def tracker(selector, duration):
	selector = urllib.parse.unquote(selector)
	session[selector] = float(duration)

	if session[selector] == 0:
		return 'OK'

	if 'events' not in session:
		session['events'] = []

	timestamp = int(round(time.time() * 1000))
	session['events'].append({'timestamp': timestamp, 'selector': selector})
	print('[%s] Hovered on element matching selector %s\nTotal Duration: %s' % (timestamp, selector, duration)) 

	return 'OK'

@app.route('/results/')
def results():
	events = session.get('events', [])
	return Response(get_file_and_format('html/index.html', '<script> var events = {}; </script> <script src="/static/js/playback.js"></script>'.format(str(events))),
		            mimetype='text/html')
	#return render_template('index.html', 
	#	   import_line='<script> var events = {}; </script> <script src="/static/js/playback.js"></script>'.format(str(events)))

@app.route('/clear/')
def clear():
	session.clear()
	return 'OK'

def get_file_and_format(path, content):
	with open(path) as f:
		return f.read().replace('{css_tracker_import_line}', content)