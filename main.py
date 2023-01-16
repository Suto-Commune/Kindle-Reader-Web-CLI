from flask import Flask as fl
from flask import request as req
import requests as res
from flask import render_template as temp
import threading


def reader_luncher():
	os.system("java -jar reader-pro-2.7.3.jar>nul")


reader_start = threading.Thread(name='启动reader服务端', target=reader_luncher)

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


@app.route('/book/<path:p>')
def book__info(p):
	global url, br
	# 拼接url
	f_url = req.full_path
	b_url = f_url.replace("/book/", "")

	# 获取book shelf
	shelf = res.get(url + "getBookshelf").json()

	book_info = dict()
	for i in shelf['data']:
		if i["bookUrl"] == b_url:
			book_info = i
	continue_read_link = "/read/0/{index}/{b_url}".format(index=book_info["durChapterIndex"], b_url=b_url)

	if not "durChapterTitle" in book_info.keys():
		lastread = "从未读过"
	else:
		lastread = book_info["durChapterTitle"]
	return temp("bookinfo.html",
				br=br, cover=book_info["coverUrl"],
				name=book_info["name"],
				author=book_info["author"],
				intro=str(book_info["intro"]).replace("\n", br),
				lastread=lastread,
				latestread=book_info["latestChapterTitle"],
				continue_read_link=continue_read_link, book_url=b_url)


@app.route("/read/<save>/<index>/<path:p>")
def book__read(index, save, p):
	global url, br, next_zhang, last_zhang
	# 拼接url
	b_url = req.full_path.replace("/read/{save}/{index}/".format(index=index, save=save), "")
	# 请求数据
	json1 = {
		"url": b_url,
		"index": int(index),
		"cache": 0
	}
	json2 = {
		"url": b_url,
		"refresh": 0
	}
	# 请求
	text = res.post(url + "getBookContent", json=json1).json()["data"].replace("\n", br)
	chapter = res.post(url + "getChapterList", json=json2).json()["data"]
	chapter_name = chapter[int(index)]["title"]
	if int(save) == 1:
		json3 = {
			"url": url,
			"index": index
		}
		res.post(url + "saveBookProgress", json=json3)

	if not index == "0":
		last_zhang = "/read/1/{index}/{b_url}".format(index=str(int(index) - 1), b_url=b_url)
		last_zhang = 'href="{link}"'.format(link=last_zhang)
	elif index == "0":
		last_zhang = 'onclick="alert(\'没有上一章啦\');"'

	if not index == str(len(chapter) - 1):
		next_zhang = "/read/1/{index}/{b_url}".format(index=str(int(index) + 1), b_url=b_url)
		next_zhang = 'href="{link}"'.format(link=next_zhang)
	elif index == str(len(chapter) - 1):
		next_zhang = 'onclick="alert(\'没有下一章啦\');"'

	return temp("readbook.html", chaptername=chapter_name,
				br=br, text=text,
				next_zhang=next_zhang, last_zhang=last_zhang, bookurl=b_url)


@app.route("/chapter/<page>/<path:p>")
def book_chapter(page, p):
	global book_info
	book_url = req.full_path.replace("/chapter/{page}/".format(page=page), "")
	json = {
		"url": book_url,
		"refresh": 1
	}

	shelf = res.get(url + "getBookshelf").json()["data"]
	for i in shelf:
		if i["bookUrl"] == book_url:
			book_info = i

	chapter = res.post(url + "getChapterList", json=json).json()["data"]
	read_chapter = list()

	latest = int()
	for i in range((int(page) - 1) * 20, (int(page) - 1) * 20 + 20):
		if i >= len(chapter):
			latest = i
			break
		read_chapter.append(chapter[i])
		latest = i

	if page == str(1):
		lastpage = 'onclick="alert(\'没有上一章啦\');"'
	elif not page == str(1):
		lastpage = '/chapter/{page}/{url}'.format(page=str(int(page) - 1), url=book_url)
		lastpage = 'href="{link}"'.format(link=lastpage)

	if (int(page) * 20) >= len(chapter):
		nextpage = 'onclick="alert(\'没有下一章啦\');"'
	elif not (int(page)) >= len(chapter):
		nextpage = '/chapter/{page}/{url}'.format(page=str(int(page) + 1), url=book_url)
		nextpage = 'href="{link}"'.format(link=nextpage)

	link = '/book/{link}'.format(link=book_url)
	return temp("chapter.html", name=book_info["name"], page=page, chapter=read_chapter, book_url=book_url,
				lastpage=lastpage, nextpage=nextpage, link=link)


if __name__ == "__main__":
	reader_start.start()
	app.run(host='0.0.0.0', debug=True)
