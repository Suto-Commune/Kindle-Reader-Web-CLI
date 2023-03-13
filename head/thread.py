import logging
import os
import subprocess
import sys
import threading
import time

from gevent import pywsgi

from head.config import *
from head.server import app
from head.backup import backup


# 创建reader线程
def reader_thread():
    try:
        subprocess.check_output(['java', '-jar', 'reader-pro.jar', '>nul'])
    except:
        ...
    try:
        subprocess.check_output(['java', '-jar', 'reader-pro.jar'])
    except:
        logging.getLogger(__name__).critical('Unable to load thread:"reader",please check file or java integrity.')
        sys.exit()


# 创建flask线程
def flask_thread():
    app.run(host='0.0.0.0', debug=False, port=port)


def nginx_thread():
    try:
        os.system("cd nginx && nginx")
    except:
        logging.getLogger(__name__).critical('Unable to load thread:"nginx",please check file or nginx integrity.')
        sys.exit()


def wsgi_thread():
    if port is None:
        port1 = 5000
    else:
        port1 = port
    server = pywsgi.WSGIServer(('0.0.0.0', port1), app)
    server.serve_forever()


def backup_thread():
    if AUTO_BACKUP:
        backup()
    elif not AUTO_BACKUP:
        print("[INFO]Doesn't OPEN AUTO_BACKUP.")
        sys.exit()


# 线程创建
t_flask = threading.Thread(name='flask', target=flask_thread, daemon=True)
# t_print = threading.Thread(name='print', target=print_thread, daemon=True)
t_reader = threading.Thread(name='reader', target=reader_thread, daemon=True)
t_nginx = threading.Thread(name='nginx', target=nginx_thread, daemon=True)
t_wsgi = threading.Thread(name='wsgi', target=wsgi_thread, daemon=True)
t_backup = threading.Thread(name='backup', target=backup_thread, daemon=True)


# 线程启动
def thread_starter():
    # t_print.start()
    time.sleep(1)
    t_reader.start()
    t_backup.start()
    if DEBUG:
        t_flask.start()
    elif not DEBUG:
        t_wsgi.start()
    t_nginx.start()
