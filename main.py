from flask import Flask as fl
from flask import request as req
import requests as res
from flask import render_template as temp
import os

# 创建flask对象
app = fl(__name__, static_folder='', static_url_path='')

# 初始化全局变量
url = "http://127.0.0.1:8080/reader3/"
br = '<div class="wb"></div>'
button = '<div id="cssbutton"><a id="btlogin" href="{link}">{str_}</a></div>'


@app.route("/")
def index():
    global url
    main_page = res.get(url + "getBookshelf").json()
    return temp("bookshelf.html", main_page=main_page)


@app.route('/book/')
def bookinfo():
    global url, br
    # 拼接url
    f_url = req.full_path
    b_url = f_url.replace("/book/?url=", "")
    del f_url  # 其实可以不用del,py有GC的,运行完会自动删

    # 获取book shelf
    shelf = res.get(url + "getBookshelf").json()

    book_info = {}
    for i in shelf['data']:
        if i["bookUrl"] == b_url:
            book_info = i

    return temp("bookinfo.html",
                br=br, cover=book_info["coverUrl"],
                name=book_info["name"],
                author=book_info["author"],
                intro=str(book_info["intro"]).replace("\n",br),
                lastread=book_info["durChapterTitle"],
                latestread=book_info["latestChapterTitle"])


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
