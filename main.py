import os
import subprocess
import sys
import threading

import requests as res
from flask import Flask as fl
from flask import render_template as temp
from flask import request as req
import logging


# 创建reader线程
def reader_thread():
    try:
        subprocess.check_output(['java', '-jar', 'reader-pro-2.7.3.jar', '>nul'])
    except:
        ...
    try:
        subprocess.check_output(['java', '-jar', 'reader-pro-2.7.3.jar'])
    except:
        logging.getLogger(__name__).critical('Unable to load threads:reader')
        sys.exit()


# 创建flask对象
app = fl(__name__, static_folder='storage', static_url_path='')

# 初始化全局变量
url = "http://127.0.0.1:8080/reader3/"
br = '<div class="wb"></div>'
button = '<div id="cssbutton"><a id="btlogin" href="{link}">{str_}</a></div>'


@app.route("/")
def index():
    global url
    main_page = res.get(url + "getBookshelf").json()
    return temp("bookshelf.html", main_page=main_page)


@app.route('/book/<path:p>')
def book_info(p):
    global url, br
    # 拼接url
    f_url = req.full_path
    b_url = f_url.replace("/book/", "")

    # 获取book shelf
    shelf = res.get(url + "getBookshelf").json()

    book_info_ = {}
    for i in shelf['data']:
        if i["bookUrl"] in b_url:
            book_info_ = i

    continue_read_link = f'/read/0/{book_info_["durChapterIndex"]}/{b_url}'

    if "durChapterTitle" not in book_info_.keys():
        last_read = "从未读过"
    else:
        last_read = book_info_["durChapterTitle"]

    cover = book_info_["coverUrl"] if "coverUrl" in book_info_ else '../../../../../assets/img/noCover.jpeg'
    intro = book_info_["intro"] if 'intro' in book_info_ else '这本书没有介绍哦'
    return temp("bookinfo.html",
                br=br, cover=cover,
                name=book_info_["name"],
                author=book_info_["author"],
                intro=str(intro).replace("\n", br),
                lastread=last_read,
                latestread=book_info_["latestChapterTitle"],
                continue_read_link=continue_read_link, book_url=b_url)


@app.route("/read/<save>/<index_>/<path:p>")
def book_read(index_, save, p):
    global url, br

    # 拼接url
    # index和外部函数重名的,容易出bug,改成index_了
    b_url = req.full_path.replace(f"/read/{save}/{index_}/", "").replace('?', '')
    # 创建请求数据
    get_content_json = {
        "url": b_url,
        "index": int(index_),
        "cache": 0
    }
    get_list_json = {
        "url": b_url,
        "refresh": 0
    }

    # 发送请求
    text = res.post(url + "getBookContent", json=get_content_json).json()["data"].replace("\n", br)
    chapter = res.post(url + "getChapterList", json=get_list_json).json()["data"]

    # 获取标题
    chapter_name = chapter[int(index_)]["title"]

    if int(save) == 1:
        save_book_json = {
            "url": url,
            "index": index_
        }
        res.post(url + "saveBookProgress", json=save_book_json)

    # 判断上一章是否存在
    if index_ != '0':
        last_chapter = f'/read/1/{int(index_) - 1}/{b_url}'
        last_chapter = f'href="{last_chapter}"'
    else:
        last_chapter = 'onclick="alert(\'没有上一章啦\');"'

    # 判断下一章是否存在
    if index_ != str(len(chapter) - 1):
        next_chapter = f'/read/1/{int(index_) + 1}/{b_url}'
        next_chapter = f'href="{next_chapter}"'
    else:
        next_chapter = 'onclick="alert(\'没有下一章啦\');"'

    return temp("readbook.html", chaptername=chapter_name,
                br=br, text=text,
                next_zhang=next_chapter, last_zhang=last_chapter, bookurl=b_url)


@app.route("/chapter/<page>/<path:p>")
def book_chapter(page, p):
    # 初始化参数
    page_int = int(page)
    book_url = req.full_path.replace(f"/chapter/{page}/", "").replace('?','')

    # 取书架
    shelf = res.get(url + "getBookshelf").json()["data"]
    for i in shelf:
        if i["bookUrl"] == book_url:
            book_info_ = i

    # 取章节列表
    get_list_json = {
        "url": book_url,
        "refresh": 1
    }
    chapter = res.post(url + "getChapterList", json=get_list_json).json()["data"]

    latest = int()
    read_chapter = []
    for i in range((page_int - 1) * 20, (page_int - 1) * 20 + 20):
        if i >= len(chapter):
            latest = i
            break
        read_chapter.append(chapter[i])
        latest = i

    if page == '1':
        last_page = 'onclick="alert(\'没有上一章啦\');"'
    else:
        last_page = f'/chapter/{page_int - 1}/{book_url}'
        last_page = f'href="{last_page}"'

    if (page_int * 20) >= len(chapter):
        next_page = 'onclick="alert(\'没有下一章啦\');"'
    elif page_int < len(chapter):
        next_page = f'/chapter/{page_int + 1}/{book_url}'
        next_page = f'href="{next_page}"'

    link = f'/book/{book_url}'
    return temp("chapter.html", name=book_info_["name"], page=page, chapter=read_chapter, book_url=book_url,
                lastpage=last_page, nextpage=next_page, link=link)


if __name__ == "__main__":
    t = threading.Thread(name='reader', target=reader_thread, daemon=True)
    t.start()
    app.run(host='0.0.0.0', debug=True)
