import json
import re
from urllib.parse import quote
from urllib.parse import quote_plus
from urllib.parse import unquote

import requests as res
from flask import Flask
from flask import render_template as temp
from flask import request as req

from head import config
from head.aes import aes_encode


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

app = Flask(__name__, static_folder='../storage', static_url_path='')


@app.route("/")
def index():
    main_page = res.get(config.url + "getBookGroups").json()
    return temp("book_groups.html", main_page=main_page)


@app.route("/bookshelf/")
def refresh_bookshelf():
    return '<meta http-equiv="refresh" content="0;url=./-1">'


@app.route("/bookshelf/<string:group>")
def bookshelf(group="-1"):
    global group_name
    main_page = res.get(config.url + "getBookshelf").json()

    group_sss = res.get(config.url + "getBookGroups").json()["data"]

    for i in group_sss:
        if int(group) == 0:
            group_name = "未分组"
            break
        elif int(group) == (group_name := int(i["groupId"])):
            break

    match int(group):
        case -1:
            main_page = list(
                map(lambda x: {**x, "groups": x.get('coverUrl', '/assets/img/noCover.jpeg')}, main_page["data"]))
            return temp("bookshelf_category.html", main_page=main_page, group_name=group_name, quote=quote_plus)

        case -4:
            return '<meta http-equiv="refresh" content="0;url=/bookshelf/0">'

        case _:
            main_page_list = filter(lambda x: int(x["group"]) == int(group), main_page["data"])
            main_page = list(
                map(lambda x: {**x, "groups": x.get('coverUrl', '/assets/img/noCover.jpeg')}, main_page_list))
            return temp("bookshelf_category.html", main_page=main_page, group_name=group_name, quote=quote_plus)


@app.route('/book/<path:p>')
def book_info(p):
    b_url = get_book_url("/book/")

    # 获取book shelf
    shelf = res.get(config.url + "getBookshelf").json()

    for i in shelf['data']:
        if i["bookUrl"] in b_url:
            got_book_info = i
            break
    else:
        got_book_info = {}

    if "durChapterTitle" in got_book_info.keys():
        last_read = got_book_info["durChapterTitle"]
        continue_read_link = f'/read/0/{got_book_info["durChapterIndex"]}/{b_url}'
    else:
        last_read = "从未读过"
        continue_read_link = f'/read/0/0/{b_url}'

    cover = got_book_info.get("coverUrl", '/assets/img/noCover.jpeg')
    intro = got_book_info.get('intro', '这本书没有介绍哦')

    return temp("book_information.html",
                br=config.br, cover=cover,
                name=got_book_info["name"],
                author=got_book_info["author"],
                intro=str(intro).replace("\n", config.br),
                lastread=last_read,
                latestread=got_book_info["latestChapterTitle"],
                continue_read_link=continue_read_link, book_url=b_url)


@app.route("/read/<save>/<index_>/<path:p>")
def book_read(index_, save, p):
    # 拼接url
    # index和外部函数重名的,容易出bug,改成index_了
    b_url = get_book_url(f"/read/{save}/{index_}/")
    url_path = b_url.replace(f"/read/{save}/{index_}/", "")
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
    text = dict(res.post(config.url + "getBookContent", json=get_content_json).json())
    if "book-asset" in text["data"]:
        path1 = config.url.replace('reader3/', '') + text['data'][1:]
        path2 = path1.split('/')
        path1 = path1.replace(path2[-1], "")
        text233 = res.get(config.url.replace('reader3/', '') + text['data'][1:]).text
        text233 = text233.replace('src="', f'src="{path1}')
        text233 = text233.replace('href="', f'href="{path1}')
        text = text233
        text = text.replace(config.url.replace('reader3/', ''), "/reader/")
    else:
        text = "　　" + text["data"]
    chapter = res.post(config.url + "getChapterList", json=get_list_json).json()["data"]

    # 获取标题
    chapter_name = chapter[int(index_)]["title"]

    if int(save) == 1:
        save_book_json = {
            "url": config.url,
            "index": index_
        }
        res.post(config.url + "saveBookProgress", json=save_book_json)

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
        return temp("bookviewer_lr.html", chaptername=chapter_name,
                    br=config.br, text=text.replace("\n", "🎈"),
                    next_zhang=next_chapter, last_zhang=last_chapter, bookurl=b_url)
    else:
        return temp("bookviewer_roll.html", chaptername=chapter_name,
                    br=config.br, text=text.replace("\n", config.br),
                    next_zhang=next_chapter, last_zhang=last_chapter, bookurl=b_url)


@app.route("/chapter/<page>/<path:p>")
def book_chapter(page, p):
    # 初始化参数
    global book_info_, next_page
    page_int = int(page)
    b_url = get_book_url(f"/chapter/{page}/")
    # 取书架
    shelf = res.get(config.url + "getBookshelf").json()["data"]
    for i in shelf:
        if i["bookUrl"] == b_url:
            book_info_ = i

    # 取章节列表
    get_list_json = {
        "url": b_url,
        "refresh": 1
    }
    chapter = res.post(config.url + "getChapterList", json=get_list_json).json()["data"]

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

    return temp("bookviewer_chapters.html", name=book_info_["name"], page=page, chapter=read_chapter, book_url=b_url,
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
    main_page = res.get(config.url + "getBookshelf").json()
    for i in main_page["data"]:
        a = res.get(config.url + f'cacheBookSSE?url={quote(i["bookUrl"])}&refresh=0')
        print(a.status_code)
    return "ok"


def get_book_sources_list():
    get_book_sources = res.get(config.url + "getBookSources").json()["data"]

    def tmp():
        for i in get_book_sources:
            if "," in (book_source_group := i["bookSourceGroup"]):
                yield from book_source_group.split(",")
            else:
                yield i["bookSourceGroup"]

    book_source_groups = filter(lambda i, v: v not in book_source_groups[:i], enumerate(tmp()))
    return list(map(lambda k, v: (v, f"./id/{str(k)}"), enumerate(book_source_groups)))


@app.route("/sources/")
def sources_index():
    return temp("getBookSources_group.html", bookSourceGroup=get_book_sources_list())


@app.route("/sources/id/<int:group_id>")
def sources_id(group_id):
    book_source_group = get_book_sources_list()[group_id][0]
    book_source = res.get(config.url + "getBookSources").json()["data"]
    s_list = [(i["bookSourceName"], i["bookSourceGroup"], f'/sources/get/{quote_plus(i["bookSourceUrl"])}') for i in
              filter(lambda x: str(book_source_group) in str(x["bookSourceGroup"]), book_source)]

    return temp("getBookSources_id.html", bookSourceGroup=book_source_group, s_list=s_list)


@app.route("/sources/get/<path:p>")
def sources_get(p):
    sources_get_url = get_book_url("/sources/get/")
    book_source = res.get(config.url + "getBookSources").json()["data"]

    for i in filter(lambda x: x["bookSourceUrl"] == sources_get_url, book_source):
        name = i["bookSourceName"]
        sources_explore_url = i["exploreUrl"]
        break
    else:
        name = str()
        sources_explore_url = str()

    matches = re.search(r'"(layout_flexGrow|layout_flexBasisPercent)"', sources_explore_url)
    if not matches:
        sources_explore_url = sources_explore_url\
            .replace("layout_flexBasisPercent", '"layout_flexBasisPercent"')\
            .replace("layout_flexGrow", '"layout_flexGrow"')

    if "::" in sources_explore_url:
        wait = sources_explore_url.split("\n")
        print(wait)
        wait2 = []
        for i in wait:
            j = i.split("::")
            wait1 = {"title": j[0], "url": j[1]}
            dict1 = {"layout_flexBasisPercent": "30"}
            wait1["style"] = dict1
            wait2.append(wait1)
        sources_explore_url = str(wait2)
        del wait
        del wait1

    try:
        sources_explore_url = eval(sources_explore_url)
    except:
        sources_explore_url = [
            {
                "url": 'errorsourceserror',
                "title": "此书源不可探索或探索错误，点击此按钮返回探索主页",
                "style": {
                    "layout_flexBasisPercent": "30"
                }
            }
        ]
    for i in sources_explore_url:
        i["url"] = f"{sources_get_url}%E6%88%91natsumi%E6%98%AF" + quote_plus(i["url"])

    return temp("getBookSources_get.html", sources_exploreUrl=sources_explore_url, name=name)


@app.route("/sources/login/<path:p>")
def sources_login(p):
    book_url = get_book_url("/sources/login/")
    ex_list = book_url.split("/")
    explore_book_url = f"{ex_list[0]}//{ex_list[2]}"
    json1 = {
        "bookSourceUrl": explore_book_url
    }
    login_url = res.post(config.url + "getBookSource", json=json1).json()["data"]["loginUrl"]
    return f"<a href='{login_url}'>点击此链接进行登录</a>；加载<a href='https://github.com/Suto-Commune/get-cookie'>插件</a" \
           f">后复制cookie转跳至<a href='/sources/cookie/{quote_plus(explore_book_url)}'>这</a> "


@app.route("/sources/cookie/<path:p>")
def sources_cookie(p):
    book_url = get_book_url("/sources/cookie/")
    ex_list = book_url.split("/")
    explore_book_url = f"{ex_list[0]}//{ex_list[2]}"
    return temp("cookie.html", url=quote_plus(explore_book_url))


@app.route("/sources/cookieadd/")
def add_cookie():
    s_url = req.args.get("url")
    s_cookie = req.args.get("cookie")
    ex_list = s_url.split("/")
    explore_book_url = f"{ex_list[0]}//{ex_list[2]}"
    json1 = {
        "bookSourceUrl": explore_book_url
    }
    login_url = res.post(config.url + "getBookSource", json=json1).json()["data"]
    header = str(login_url["header"])[0:len(login_url["header"]) - 1]
    print(header)
    header = header + ',\n' + f'"Cookie": "{s_cookie}"' + "}"
    login1 = login_url
    login1["header"] = header
    res.post(config.url + "saveBookSource", json=login1)
    return "ok"


@app.route("/sources/list/<path:p>")
def sources_list(p):
    rule_find_url = get_book_url("/sources/list/")
    print(rule_find_url)
    if "errorsourceserror" in rule_find_url:
        return '<meta http-equiv="refresh" content="0;url=/sources">'
    ex_list = rule_find_url.split("我natsumi是")
    print(ex_list)
    rule_find_url = ex_list[1]
    explore_book_url = ex_list[0]
    del ex_list
    json1 = {
        'bookSourceUrl': explore_book_url,
        "page": 1,
        "ruleFindUrl": rule_find_url
    }
    print(json1)
    explore = res.post(config.url + "exploreBook", json=json1).json()["data"]
    for i in explore:
        i["bookUrl"] = f"{i['origin']}%E6%88%91natsumi%E6%98%AF" + quote_plus(i["bookUrl"])
    return temp("getBookSources_list.html", explore=explore)


@app.route("/save/group/<path:p>")
def choose_book_groups(p):
    book_url = get_book_url("/save/group/")
    main_page = res.get(config.url + "getBookGroups").json()
    groups = main_page["data"]
    del main_page
    return temp("save_book_choose_book_groups.html", groups=groups, book_url=book_url)


@app.route("/save/group_id/<string:group_id>/<path:p>")
def save_book(p, group_id):
    group_id = int(group_id)
    book_url = get_book_url(f"/save/group_id/{group_id}/")
    origin_list = book_url.split("我natsumi是")
    print(origin_list)
    origin = origin_list[0]
    book_url = origin_list[1]
    if int(group_id) < 0:
        group_id = 0
    json1 = {
        "origin": origin,
        "bookUrl": book_url,
        "group": int(group_id)
    }
    save = res.post(config.url + "saveBook", json=json1)
    print(f'[INFO]\tSave book "{book_url}" to group {group_id}.Code: {save.status_code}')
    return f'<meta http-equiv="refresh" content="0;url=/book/{quote_plus(book_url)}">'


@app.route("/search/")
def search():
    return temp("multi_search.html")


@app.route("/multi_search/key/")
def multi_search_key():
    key = req.args.get("key")
    _file = res.get(config.url + f"searchBookMultiSSE?key={key}").content.decode("UTF-8").splitlines()
    _file = filter(lambda x: x, _file)
    data = []
    for i in filter(lambda x: "event" not in x and "bookUrl" in x, _file):
        t = json.loads(i.replace("data: ", ""))['data']
        t["bookUrl"] = f"{t['origin']}%E6%88%91natsumi%E6%98%AF" + quote_plus(t["bookUrl"])
        data.append(t)
    return temp("multi_search_book.html", data=data)


@app.route("/single_search/")
def single_sources_index():
    return temp("single_search_book.html", bookSourceGroup=get_book_sources_list())


@app.route("/single_search/id/<int:group_id>")
def single_sources_id(group_id):
    book_source_group = get_book_sources_list()[group_id][0]
    book_source = res.get(config.url + "getBookSources").json()["data"]
    s_list = [(i["bookSourceName"], i["bookSourceGroup"], f'/single_search/search/{quote_plus(i["bookSourceUrl"])}')
              for i in filter(lambda x: str(book_source_group) in str(x["bookSourceGroup"]), book_source)]
    return temp("getBookSources_id.html", bookSourceGroup=book_source_group, s_list=s_list)


@app.route("/single_search/search/<path:p>")
def search_sources_get(p):
    return temp("single_search.html", get_url=get_book_url("/single_search/search/"))


@app.route("/single_search/key/<path:p>")
def single_list(p):
    info = get_book_url("/single_search/key/").split("?key=")
    data = res.post(config.url + "searchBook", json={"key": info[1], "bookSourceUrl": info[0]}).json()["data"]
    data = map(lambda x: {**x, "bookUrl": f"{x['origin']}%E6%88%91natsumi%E6%98%AF" + quote_plus(x["bookUrl"])}, data)
    return temp("multi_search_book.html", data=list(data))
