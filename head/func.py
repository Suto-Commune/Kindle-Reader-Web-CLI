import logging
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from head import config
from head import thread
from head.aes import aes_decode


# 创建Nocover.png
def create_img():
    if not (img_path := Path('storage/assets/img/noCover.jpeg')).exists():
        shutil.copy(Path('noCover.jpeg'), img_path)


# 禁用Windows下的关闭按钮使得关闭程序只能使用Ctrl+C
def ban_win_close_button():
    import win32console, win32gui, win32con
    hwnd = win32console.GetConsoleWindow()
    if hwnd:
        h_menu = win32gui.GetSystemMenu(hwnd, 0)
        if h_menu:
            win32gui.EnableMenuItem(
                h_menu, win32con.SC_CLOSE, win32con.MF_DISABLED)


def storage_clone():
    logger = logging.getLogger(__name__)
    if config.CLONE_MODE and not Path("storage").exists():
        origin = f"https://{aes_decode(config.github_token)}@github.com/{config.github_name}/{config.github_repo}.git"
        logger.info("CLONE_MODE Enable.Start Clone...")
        os.system(f"git clone {origin} storage")
    elif not config.CLONE_MODE:
        logger.info("CLONE_MODE Disable.")


# 启动函数
def start():
    storage_clone()
    create_img()
    thread.thread_starter()
    while True:
        try:
            thread.t_reader.join(timeout=0.1)
        except KeyboardInterrupt:
            sys.exit()


# 结束时运行的函数
def exit_do():
    try:
        if platform.system() == "Windows":
            subprocess.check_output(["taskkill", "/f", "/im", "nginx.exe"])
        else:
            subprocess.check_output(["killall", "-9", "nginx"])
            subprocess.check_output(["killall", "-9", "nginx"])
    except FileNotFoundError:
        ...
