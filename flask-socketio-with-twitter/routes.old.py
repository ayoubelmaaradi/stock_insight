#!/usr/bin/env python
# This code shows the real time streaming of tweets with Flask and StreamIO to your apps, after doing some processing on your backend. So it flows as follows in realtime. 
# Twitter -- (TwitterStreaming) --> YourBackend -- (Flask/StreamIO) --> YourFrontend

# YourBackend -- (Flask/StreamIO) --> YourFrontend part code is taken (after stripping off the listening part, so kept only one way communication codes from server to client) from very helpful tutorial by Miguel Grinberg on the topic:  http://blog.miguelgrinberg.com/post/easy-websockets-with-flask-and-gevent
# with accompanying github repo: https://github.com/miguelgrinberg/Flask-SocketIO

# I added Twitter -- (TwitterStreaming) --> YourBackend part to accompany rest of the codes. There could be a better way of doing it. Suggestions are very welcome. 

# Instead of making async_mode to use just one, leaving it as it is from Miguel's code. 

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on available packages.
async_mode = None
#
# if async_mode is None:
#     try:
#         import eventlet
#
#         async_mode = 'eventlet'
#     except ImportError:
#         pass
#
#     if async_mode is None:
#         try:
#             from gevent import monkey
#
#             async_mode = 'gevent'
#         except ImportError:
#             pass
#
#     if async_mode is None:
#         async_mode = 'threading'
#
#     print(('async_mode is ' + async_mode))
#
# # monkey patching is necessary because this application uses a background
# # thread
# if async_mode == 'eventlet':
#     import eventlet
#
#     eventlet.monkey_patch()
# elif async_mode == 'gevent':
#     from gevent import monkey
#
#     monkey.patch_all()

import json
import time
from threading import Thread
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

from tweepy.streaming import StreamListener
from tweepy import Stream
import tweepy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='eventlet')
thread = None

cred = {
    # "access_key": "",
    # "access_secret": "",
    # "consumer_key": "",
    # "consumer_secret": ""
    'consumer_key': 'p9smvhLm9SXh9z2EUNYyakFe7',
    'consumer_secret': 'Fu6f5YWPyEfrUwpGS02Ojm2eMSxanySYzvkhP7ypVLtlCvIvgy',
    'access_key': '809287937351249920-2S2imOpJVEy0oxDlGwVADh3wM2WPVpY',
    'access_secret': 'EkF2JQx9jcsBOyyMU4UsZYgFqLWJ1UH0W8NCDPL7Axnbs'
}
auth = tweepy.OAuthHandler(cred['consumer_key'], cred['consumer_secret'])
auth.set_access_token(cred['access_key'], cred['access_secret'])


def do_whatever_processing_you_want(text):
    return ('%s' % (text)).encode('utf-8')


class StdOutListener(StreamListener):
    def __init__(self):
        pass

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            text = do_whatever_processing_you_want(tweet['text'])
            socketio.emit('stream_channel',
                          {'data': text, 'time': tweet['timestamp_ms']},
                          namespace='/demo_streaming')
            print(text)
        except:
            pass

    def on_error(self, status):
        print('Error status code', status)
        exit()


def background_thread():
    """Example of how to send server generated events to clients."""
    stream = Stream(auth, l)
    _keywords = [':-)', ':-(']
    stream.filter(track=_keywords)


@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_thread)
        thread.daemon = True
        thread.start()
    return render_template('index.html')


l = StdOutListener()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)  # <host_ip_address> -- replace it with the IP address of your server where you are hosting
