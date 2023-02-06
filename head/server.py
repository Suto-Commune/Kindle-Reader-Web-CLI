from flask import Flask as fl
from flask import render_template as temp
from flask import request as req

from urllib.parse import unquote
from urllib.parse import quote

from head.config import *
from head.aes import aes_encode

import requests as res
import re


# 解析Book_url
def get_book_url(url_path: str):
    url_path = req.full_path.replace(url_path, "")

    if url_path[-1] == "?":
        url_path = url_path[0:len(url_path) - 1]

    regex = r"(http:/|https:/)([^/])"
    subst = "\\g<1>/\\g<2>"
    url_path = re.sub(regex, subst, url_path, 0, re.MULTILINE)

    url_path = unquote(url_path)
    return url_path


# 定义FlaskAPP

app = fl(__name__, static_folder='../storage', static_url_path='')


@app.route("/")
def index():
    global url
    main_page = res.get(url + "getBookGroups").json()
    main_page["data"].pop(1)
    main_page["data"].pop(1)
    return temp("groups.html", main_page=main_page)


@app.route("/bookshelf/")
def refresh_bookshelf():
    return '<meta http-equiv="refresh" content="0;url=./-1">'


@app.route("/bookshelf/<string:group>")
def bookshelf(group="-1"):
    global group_name
    main_page = res.get(url + "getBookshelf").json()

    group_sss = res.get(url + "getBookGroups").json()["data"]

    for i in group_sss:
        if int(group) == "0":
            group_name = "未分组"
            break
        elif int(i["groupId"]) == int(group):
            group_name = i["groupName"]
            break

    if group == "-1":
        for got_book_info in main_page['data']:
            got_book_info["groups"] = got_book_info[
                "coverUrl"] if "coverUrl" in got_book_info else '/assets/img/noCover.jpeg'
        return temp("bookshelf.html", main_page=main_page, group_name=group_name)
    if group == "-4":
        return '<meta http-equiv="refresh" content="0;url=/bookshelf/0">'
    else:
        in_list = {"data": []}
        for i in range(0, len(main_page["data"])):
            if int(main_page["data"][i]["group"]) == int(group):
                in_list["data"].append(main_page["data"][i])
        main_page = in_list
        for got_book_info in main_page['data']:
            got_book_info["groups"] = got_book_info[
                "coverUrl"] if "coverUrl" in got_book_info else '/assets/img/noCover.jpeg'
        return temp("bookshelf.html", main_page=main_page, group_name=group_name)


@app.route('/book/<path:p>')
def book_info(p):
    global url, br

    b_url = get_book_url("/book/")

    # 获取book shelf
    shelf = res.get(url + "getBookshelf").json()

    got_book_info = {}
    for i in shelf['data']:
        if i["bookUrl"] in b_url:
            got_book_info = i

    if "durChapterTitle" not in got_book_info.keys():
        last_read = "从未读过"
        continue_read_link = f'/read/0/0/{b_url}'
    else:
        last_read = got_book_info["durChapterTitle"]
        continue_read_link = f'/read/0/{got_book_info["durChapterIndex"]}/{b_url}'

    cover = got_book_info["coverUrl"] if "coverUrl" in got_book_info else '/assets/img/noCover.jpeg'
    intro = got_book_info["intro"] if 'intro' in got_book_info else '这本书没有介绍哦'
    return temp("bookinfo.html",
                br=br, cover=cover,
                name=got_book_info["name"],
                author=got_book_info["author"],
                intro=str(intro).replace("\n", br),
                lastread=last_read,
                latestread=got_book_info["latestChapterTitle"],
                continue_read_link=continue_read_link, book_url=b_url)


@app.route("/read/<save>/<index_>/<path:p>")
def book_read(index_, save, p):
    global url, br

    # 拼接url
    # index和外部函数重名的,容易出bug,改成index_了
    b_url = get_book_url(f"/read/{save}/{index_}/")

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
    text = dict(res.post(url + "getBookContent", json=get_content_json).json())
    if "epub" in text["data"]:
        text = str(text["data"]).replace("/book-assets/", "")
        path1 = text
        with open(f"storage/data/{text}", 'r', encoding="UTF-8") as f:
            text1 = f.read()
            f.close()
        # 去除累赘
        path2 = path1.split('/')
        # 替换绝对路径
        path1 = path1.replace(f"/{path2[-1]}", "").replace(f"/{path2[-2]}", "").replace(f"/{path2[-2]}", "")
        text = text1.replace("..", f"/data/{path1}")
    else:
        text = "　　" + text["data"].replace("\n", br)
    chapter = res.post(url + "getChapterList", json=get_list_json).json()["data"]

    # 获取标题
    chapter_name = chapter[int(index_)]["title"]

    if int(save) == 1:
        save_book_json = {
            "url": url,
            "index": index_
        }
        res.post(url + "saveBookProgress", json=save_book_json)

    # 按钮
    # 判断上一章是否存在
    if index_ != '0':
        last_chapter = f'/read/1/{int(index_) - 1}/{quote(b_url)}'
        last_chapter = f'href="{last_chapter}"'
    else:
        last_chapter = 'onclick="alert(\'没有上一章啦\');"'

    # 判断下一章是否存在
    if index_ != str(len(chapter) - 1):
        next_chapter = f'/read/1/{int(index_) + 1}/{quote(b_url)}'
        next_chapter = f'href="{next_chapter}"'
    else:
        next_chapter = 'onclick="alert(\'没有下一章啦\');"'

    if read_mode == 1:
        change_page = '<div name="change_page"><div style="z-index: 2;height: 100%;width: 20%;position: fixed;margin-right: 80%;"onclick="window.scroll(window.scrollY,window.scrollY-document.body.clientHeight);"></div><div style="z-index: 2;height: 100%;width: 20%;position: fixed;margin-left: 80%;"onclick="window.scroll(window.scrollY,window.scrollY+document.body.clientHeight);"></div></div>'
    else:
        change_page = ""

    return temp("readbook.html", chaptername=chapter_name,
                br=br, text=text,
                next_zhang=next_chapter, last_zhang=last_chapter, bookurl=b_url, change_page=change_page)


@app.route("/chapter/<page>/<path:p>")
def book_chapter(page, p):
    # 初始化参数
    global book_info_, next_page
    page_int = int(page)
    b_url = get_book_url(f"/chapter/{page}/")
    # 取书架
    shelf = res.get(url + "getBookshelf").json()["data"]
    for i in shelf:
        if i["bookUrl"] == b_url:
            book_info_ = i

    # 取章节列表
    get_list_json = {
        "url": b_url,
        "refresh": 1
    }
    chapter = res.post(url + "getChapterList", json=get_list_json).json()["data"]

    read_chapter = []
    for i in range((page_int - 1) * 20, (page_int - 1) * 20 + 20):
        if i >= len(chapter):
            break
        read_chapter.append(chapter[i])

    if page == '1':
        last_page = 'onclick="alert(\'没有上一页啦\');"'
    else:
        last_page = f'/chapter/{page_int - 1}/{b_url}'
        last_page = f'href="{last_page}"'

    if (page_int * 20) >= len(chapter):
        next_page = 'onclick="alert(\'没有下一页啦\');"'
    elif page_int < len(chapter):
        next_page = f'/chapter/{page_int + 1}/{b_url}'
        next_page = f'href="{next_page}"'

    link = f'/book/{b_url}'

    return temp("chapter.html", name=book_info_["name"], page=page, chapter=read_chapter, book_url=b_url,
                lastpage=last_page, nextpage=next_page, link=link)


@app.route("/mode/<int:modeid>")
def mode_change(modeid):
    global read_mode
    read_mode = modeid
    return '<h1>3秒后返回，刷新页面生效</h1><script>function sleep(time){var timeStamp=new Date().getTime();var endTime=timeStamp+time;while(true){if(new Date().getTime()>endTime){return}}};sleep(3000);window.history.back();</script>'


@app.route("/aes/<path:p>")
def encode(p):
    return str(aes_encode(p))

@app.route("/download/")
def download_all():
    main_page = res.get(url + "getBookshelf").json()
    for i in main_page["data"]:
        res.get(url+f'cacheBookSSE?url={quote(i["bookUrl"])}&refresh=0')
    return "ok"