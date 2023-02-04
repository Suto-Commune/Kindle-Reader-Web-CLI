import time
import datetime
import os
from head.config import *


def git():
    origin = f"https://{github_token}@github.com/{github_name}/{github_repo}.git"
    os.system("cd storage & git init")
    os.system("cd storage & git checkout -b main")
    os.system("cd storage & git add .")
    os.system(f'cd storage & git commit -m "Backup {datetime.datetime.now()}')
    os.system(f"cd storage & git push {origin} main:main")


def backup():
    print("[INFO]\tFirst backup will start after 20s.")
    while True:
        print("[INFO]\tStart backup.")
        git()
        print(f"[INFO]\tDone,the next backup will start after {AUTO_BACKUP_TIME}s")
        time.sleep(AUTO_BACKUP_TIME)