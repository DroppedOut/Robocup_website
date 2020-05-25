"""
This script runs the Robocup application using a development server.
"""
from em import Sender
from os import environ
from Robocup import application
from threading import Thread
import threading
import time
Sender.send_activator()

def mail_activator():
    timing = time.time()
    print("started thread")
    while 1:
        if time.time() - timing > 86400:
            Sender.send_activator()
            timing = time.time()
sender_thread = threading.Thread(target = mail_activator)  
sender_thread.start()
if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    application.run(HOST, PORT)
    