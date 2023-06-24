import logging
import subprocess
import sys
import threading
import time

from gevent import pywsgi

from head import config
from head.backup import backup
from head.server import app


# 创建reader线程
def reader_thread():
    try:
        subprocess.check_output([f'{config.java_path}', '-jar', 'reader-pro.jar', '>nul'])
    except FileNotFoundError:
        ...
    try:
        subprocess.check_output([f'{config.java_path}', '-jar', 'reader-pro.jar', '>nul'])
        # os.system(f'"{java_path}" -jar reader-pro.jar')
    except FileNotFoundError as err:
        logging.getLogger(__name__).critical(err)
        logging.getLogger(__name__).critical('Unable to load thread:"reader",please check file or java integrity.')
        sys.exit()


# 创建flask线程
def flask_thread():
    app.run(host='0.0.0.0', debug=True, port=config.port)


def nginx_thread():
    try:
        subprocess.check_output(['nginx'], cwd='nginx')
    except FileNotFoundError as err:
        logging.getLogger(__name__).exception(err)
        logging.getLogger(__name__).critical('Unable to load thread:"nginx",please check file or nginx integrity.')
        sys.exit()
    except subprocess.CalledProcessError as err:
        logging.getLogger(__name__).exception(err)
        logging.getLogger(__name__).critical('Unable to load thread:"nginx",please check permission.')
        sys.exit()


def wsgi_thread():
    port = config.port if config.port is not None else 5000

    server = pywsgi.WSGIServer(('0.0.0.0', port), app)
    server.serve_forever()


def backup_thread():
    if config.AUTO_BACKUP:
        backup()
    elif not config.AUTO_BACKUP:
        logging.getLogger(__name__).info("Doesn't OPEN AUTO_BACKUP.")
        sys.exit()


# 线程创建
t_flask = threading.Thread(name='flask', target=flask_thread, daemon=True)
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
    if config.DEBUG:
        t_flask.start()
    elif not config.DEBUG:
        t_wsgi.start()
    t_nginx.start()
