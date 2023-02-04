import atexit
import platform
import os

from head.func import start, exit_do , ban_windows_window_close_button

if __name__ == "__main__":
    # 注册退出函数
    atexit.register(exit_do)

    # 禁用窗口关闭按钮
    if platform.system() == "Windows":
        try:
            ban_windows_window_close_button()
        except:
            try:
                os.system("pip install pywin32")
                ban_windows_window_close_button()
            except:
                ...
    start()
