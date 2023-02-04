import logging
import os
import subprocess
import sys
import threading
import time

from gevent import pywsgi

from head.config import *
from head.server import app


# 创建reader线程
def reader_thread():
    try:
        subprocess.check_output(['java', '-jar', 'reader-pro-2.7.3.jar', '>nul'])
    except:
        ...
    try:
        subprocess.check_output(['java', '-jar', 'reader-pro-2.7.3.jar'])
    except:
        logging.getLogger(__name__).critical('Unable to load thread:"reader",please check file or java integrity.')
        sys.exit()


# 创建flask线程
def flask_thread():
    app.run(host='0.0.0.0', debug=False, port=port)


def print_thread():
    print("[INFO] --- PRINT ---")
    print("\tKindle-Reader-Web-Client Start!")
    print("\tGithub: https://github.com/Suto-Commune/Kindle-Reader-Web-CLI/")
    print("\tAuthor LolingNatsumi,hsn8086,GooGuJiang")
    print(
        f"\t * Kindle Web: http://127.0.0.1:5000 or http://127.0.0.1:1000\n\t * Reader Web: http://127.0.0.1:8080 or http://127.0.0.1:1000/reader")
    print("\tPress Ctrl+C to exit.")
    print("[INFO] --- PRINT END---")


def nginx_thread():
    try:
        os.system("cd nginx && nginx")
    except:
        logging.getLogger(__name__).critical('Unable to load thread:"nginx",please check file or nginx integrity.')
        sys.exit()


def wsgi_thread():
    if port == None:
        port1 = 5000
    else:
        port1 = port
    server = pywsgi.WSGIServer(('0.0.0.0', port1), app)
    server.serve_forever()


# 线程创建
t_flask = threading.Thread(name='flask', target=flask_thread, daemon=True)
t_print = threading.Thread(name='print', target=print_thread, daemon=True)
t_reader = threading.Thread(name='reader', target=reader_thread, daemon=True)
t_nginx = threading.Thread(name='nginx', target=nginx_thread, daemon=True)
t_wsgi = threading.Thread(name='wsgi', target=wsgi_thread, daemon=True)


# 线程启动
def thread_starter():
    t_print.start()
    time.sleep(1)
    t_reader.start()
    if DEBUG == True:
        t_flask.start()
    elif DEBUG == False:
        t_wsgi.start()
    t_nginx.start()
