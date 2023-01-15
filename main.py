from flask import Flask as fl
from flask import request as req
import requests as res
from flask import render_template as temp
import os

app = fl(__name__, static_folder='', static_url_path='')

url = "http://127.0.0.1:8080/reader3/"
br = '<div class="wb"></div>'
button = '<div id="cssbutton"><a id="btlogin" href="{link}">{str_}</a></div>'
try:
    os.system('mkdir storage\kindle\cover')
except:
    print(end='')

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
    zhuye = res.get(url + "getBookshelf")
    zhuye = zhuye.json()
    return temp("bookshelf.html",zhuye=zhuye)


@app.route('/book/')
def book():
    furl = req.full_path
    burl = furl.replace("/book/?url=", "")
    del furl
    # 获取bookurl成功

    shelf = res.get(url + "getBookshelf")
    shelf = shelf.json()
    book_info = dict()
    for i in shelf['data']:
        if i["bookUrl"] == burl:
            book_info = i

    return temp("bookinfo.html",br=br,cover=book_info["coverUrl"], name=book_info["name"], author=book_info["author"],
               intro=str(book_info["intro"]),
               lastread=book_info["durChapterTitle"], latestread=book_info["latestChapterTitle"])


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
