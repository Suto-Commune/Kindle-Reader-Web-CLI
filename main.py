from flask import Flask as fl
from flask import request as req
import requests as res
from flask import render_template as temp
import os

# 创建文件夹
try:
    os.makedirs(os.path.join(os.getcwd(), 'storage', 'kindle', 'cover'))
except:
    print(end='')

# 创建flask对象
app = fl(__name__, static_folder='', static_url_path='')

# 初始化全局变量
url = "http://127.0.0.1:8080/reader3/"
br = '<div class="wb"></div>'
button = '<div id="cssbutton"><a id="btlogin" href="{link}">{str_}</a></div>'
style = ''' <style>.jz{text-align:center}.d-div{height:200;width:auto;text-align:center;display:flex;flex-direction
:row;flex-wrap:wrap;justify-content:space-evenly;align-items:center}.wb{
display:block;color:antiquewhite;height:20;width:auto}.xu-light{border:0;border-top:2px dotted#a2a9b6}#cssbutton{
margin-top:32px;height:40px}#cssbutton a{text-decoration:none;background:#2f435e;color:#f2f2f2;padding:10px 30px 10px 
30px;font-size:16px;font-family:Arial,Helvetica,Verdana,
sans-serif;font-weight:bold;border-radius:3px;-webkit-transition:all linear 0.30s;-moz-transition:all linear 
0.30s;transition:all linear 0.30s}#cssbutton a:hover{background:#385f9e}.xu-line{border:0;border-top:2px 
dotted#a2a9b6}</style> '''


@app.route("/")
def index():
    global url
    main_page = res.get(url + "getBookshelf").json()
    return temp("bookshelf.html", main_page=main_page)


@app.route('/book/')
def book():
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
                intro=str(book_info["intro"]),
                lastread=book_info["durChapterTitle"],
                latestread=book_info["latestChapterTitle"])


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
