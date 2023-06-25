import atexit
import io
import logging
import os
import platform
import subprocess
import sys
import zipfile

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s][%(filename)s(%(lineno)d)][%(levelname)s] %(message)s',
                    datefmt='%b/%d/%Y-%H:%M:%S')

logger = logging.getLogger(__name__)


# 创建默认配置
def create_config():
    if not os.path.exists("head/config.py"):
        logger.info("Cannot Find the config.py,create the default config file.")
        zip_file = b'PK\x03\x04\x14\x00\x02\x00\x08\x00Dw\x95V\x81<\x83\xe4\xea\x00\x00\x00/\x01\x00\x00\t\x00\x00\x00config.py+\xc8/*Q\xb0U\xf0\xcb\xcfK\xe5\xe5rqu\nu\x07\xf2\xdc\x12s\x8a\x81\xdc\xd2\xa2\x1c G)\xa3\xa4\xa4\xc0J_\xdf\xd0\xc8\\\xcf\x00\x08\r\xad,\x0c,\x0c\xf4\x8bR\x13SR\x8b\x8c\xf5\x95x\xb9x\xb9\x1cCC\xfc\xe3\x9d\x1c\x9d\xbdC\x03\x10\xda\x91\x04\xe3C<}]\x812\xc6f\x06\x06\xbc\\\xce>\xfe~\xae\xf1\xbe\xfe.\xae\x08\xc5\xe9\x99%\x19\xa5I\xf1%\xf9\xd9\xa9y K\x95\xe0By\x89\xb9\xa9\xa8"E\xa9\x05\xf9P\x11G\xd7\xe0xo\xd7H\x10\xcf\xd0\xc8\xd8\xc4\xd4\xcc\xdc\xc2\xd2\x00(\x9e\x95X\x96\x18_\x90X\x92a\xab\x04b\x82\x1d\xa9\xac\xf0|\xf3\xee\xe7\xbb\xe7?\xef[\xfftQ\xf3\xd3\xfe\x19/\xdb\xfby\xb9\x92\x8a\x80\x9a\xd5mR2\xcb\x14\x92s\x12\x8b\x8bm\x95\xca\x93\x94\xecl\xf4\x81\x02v\xea\xbc\\ o\xc6\xe7\xe6\xa7\x80\x9c\x00t:\x00PK\x01\x02\x14\x00\x14\x00\x02\x00\x08\x00Dw\x95V\x81<\x83\xe4\xea\x00\x00\x00/\x01\x00\x00\t\x00$\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00config.py\n\x00 \x00\x00\x00\x00\x00\x01\x00\x18\x00\xb5\xf4\xac\x9f\x1et\xd9\x01\xb5\xf4\xac\x9f\x1et\xd9\x01\x7fZ*\x06\rJ\xd9\x01PK\x05\x06\x00\x00\x00\x00\x01\x00\x01\x00[\x00\x00\x00\x11\x01\x00\x00\x00\x00'
        zip_file = io.BytesIO(zip_file)
        with zipfile.ZipFile(zip_file, 'r') as f:
            for file in f.namelist():
                f.extract(file, "./head/")
            f.close()


def print_info():
    def multi_line_log(logger_: logging.Logger = logging.getLogger(), level: int = logging.INFO, msg: str = ""):
        for line in msg.splitlines():
            logger_.log(level, line)

    logger.info("--- PRINT ---")
    logger.info("\tKindle-Reader-Web-Client Start!")
    multi_line_log(logger_=logger, msg="""
          .-')                .-') _                
         ( OO ).             (  OO) )               
        (_)---\_) ,--. ,--.  /     '._  .-'),-----. 
        /    _ |  |  | |  |  |'--...__)( OO'  .-.  '
        \  :` `.  |  | | .-')'--.  .--'/   |  | |  |
         '..`''.) |  |_|( OO )  |  |   \_) |  |\|  |
        .-._)   \ |  | | `-' /  |  |     \ |  | |  |
        \       /('  '-'(_.-'   |  |      `'  '-'  '
         `-----'   `-----'      `--'        `-----' 
    """)
    logger.info("\tGithub: https://github.com/Suto-Commune/Kindle-Reader-Web-CLI/")
    multi_line_log(logger_=logger, msg="\tContributors LolingNatsumi,hsn8086,GooGuJiang\n\tThe Dockerfile By DDSRem")
    multi_line_log(logger_=logger, msg="\t * Kindle Web:http://127.0.0.1:5000 or http://127.0.0.1:1000\n"
                                       "\t * Reader Web: http://127.0.0.1:8080 or http://127.0.0.1:1000/reader")
    logger.info("\tPress Ctrl+C to exit.")
    logger.info("--- PRINT END---")


if __name__ == "__main__":
    print_info()
    # 引用
    create_config()
    from head.func import start, exit_do, ban_win_close_button

    # 注册退出函数
    atexit.register(exit_do)

    # 禁用窗口关闭按钮
    if platform.system() == "Windows":
        try:
            ban_win_close_button()
        except ImportError:
            try:
                subprocess.check_output([sys.executable, '-m', 'pip', 'install', 'pywin32'])
                ban_win_close_button()
            except ImportError:
                ...
    start()
