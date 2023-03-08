var page=new Hpage();
var booklist = function () {
    var view=$('#list').html();

    var tip = "<div  style='font-size: 1.6em;margin-top: 140px;text-align: center' >\n" +
        "        您尚未收藏任何小说<br >点击左下角在线搜书哦\n" +
        "</div>";

    var a = $("#booklist");
    var book = new Book();
    
    if (book.book.length !== 0) {
        a.text("");
        a.attr("style", "text-align:initial;margin-top:0px");
        var value;
        for (var i = 0; i < book.book.length; i++) {
            value = book.book[i];
            var bookid=value.id;

            var result=bookid.split(':');
            if(result.length>=2){
                bookid=encode(bookid,'base16');
            }
            var res = view.replace(/{{title}}/g, value.title);
            res = res.replace(/{{author}}/g, value.author);
            res = res.replace(/{{id}}/g, bookid);
            res = res.replace(/{{bid}}/g, bookid);
            if(value.totalCount < value.readCount) value.readCount = value.totalCount;
            res = res.replace(/{{num}}/g, value.totalCount - value.readCount);
            var pecent =  value.readCount /  value.totalCount * 100;
            res = res.replace(/{{width}}/g, pecent + "%");
            var lastChapter=$("#lastChapter"+bookid);
            res = res.replace(/{{readChapter}}/g, value.readChapter?value.readChapter:'暂无数据');
            res = res.replace(/{{totalChapter}}/g, value.totalChapter?value.totalChapter:'暂无数据');
            res = res.replace(/{{total}}/g, value.totalCount );
            res = res.replace(/{{read}}/g, value.readCount  );
            a.append(res);
        }
        
        page.init(".w3-ul",0);

    } else {
        a.text("");
        a.append(tip);

    }

};//书籍页面调用

var read = function (id) {
    var bookid=id;
    var lastChapter=$("#lastChapter"+bookid);
    var title=$("#title"+bookid);
    var view=$('#info').html();

    var t=title.text();


    t=t.replace(/\[[0-9]+]/g,'').replace(/\n/,'');



    var html=view.replace(/{{title}}/g,t);
    html=html.replace(/{{lastChapter}}/g,lastChapter.text());
    html=html.replace(/{{readLast}}/g,lastChapter.attr('data-id'));
    html=html.replace(/{{id}}/g,id);

    var book = new Book();

    html = html.replace(/{{favoriteStatus}}/g, book.isFavourite(t));

    var bookData=book.getData(t);

    html = html.replace(/{{read}}/g, bookData.readCount);
    html = html.replace(/{{page}}/g, bookData.page|0);
    html = html.replace(/{{type}}/g, bookData.index);


    $.ajax.post(bookToc, "index="+bookData.index+"&url=" + bookid, function (data) {
        data=JSON.parse(data);
        if(data.state){
            $("#update").text('更新成功，用时'+data.efficiency+'。');
            bookData.totalCount=data.total-1;
            bookData.readCount=bookData.readCount>bookData.totalCount?data.total-1:bookData.readCount;
            var percent =  bookData.readCount /  bookData.totalCount *100;

            $("#progressWidth"+bookid).css('width',percent + "%");
            $("#num"+bookid).text("["+(bookData.totalCount - bookData.readCount).toString()+"]");

            var lastChapter=$("#lastChapter"+bookid);

            bookData.readChapter=data.data[bookData.readCount].name.replace(/<\/?.+?>/g,"");
            bookData.totalChapter=data.data[bookData.totalCount].name.replace(/<\/?.+?>/g,"");

            lastChapter.text("最新章节："+bookData.totalChapter);
            lastChapter.attr("data-id",bookData.totalCount);
            var read=$("#read"+bookid);
            read.text("已阅章节："+bookData.readChapter);
            read.attr("data-id",bookData.readCount);
            book.tmp=bookData;
            book.saveTmp();
            var last=$('#lastbutton');
            var url=last.attr('data-url').replace(/{{readLast0}}/g, bookData.totalCount);
            last.attr('href',url);
            last.text("最新章节："+bookData.totalChapter);
             book.update(bookData.title);
            
            localStorage.setItem(bookid,JSON.stringify(data.data));
        }else{
            $("#update").text('更新失败，请尝试换源或稍后再试。')
        }
    }, true);
    ShowTip(t,'关闭',html);

};
var favourite=function (id,iid) {
    var book = new Book();
    var bookid=iid;
    if(!book.favourite(id)){

        $("#book"+bookid).css('display','none');
    }else{
        $("#book"+bookid).css('display','block');
    }
    $('#favoriteStatus').text(book.isFavourite(id));
};
var changeSource=function(name){
    var book = new Book();
    var bookData=book.getData(name);

    ShowTip(name+'('+bookData.siteName+')','关闭',"    <div style=\"text-align: center;\">\n" +
        "        <b>书源加载中...请稍后...(时间较长)</b>\n" +
        "    </div>");
    var error =
        "    <div style=\"text-align: center;\">\n" +
        "        <b>抱歉，找不到该书籍,请稍后再试！</b>\n" +
        "    </div>";
    var view=$('#list_li').html();
    var success=function(data){
      var json= JSON.parse(data);
      if(json.state){
            var h='';
            for(var m=0;m<json.total;m++){
                var html=view;
                html=html.replace(/{{lastChapter}}/g,json.data[m].lastChapter);
                html=html.replace(/{{site}}/g,json.data[m].siteName+" - "+getRoot(json.data[m].siteUrl));
                html=html.replace(/{{site2}}/g,json.data[m].siteName);
                html=html.replace(/{{name}}/g,encodeURI(json.data[m].name));
                html=html.replace(/{{type}}/g,json.data[m].siteIndex);
                html=html.replace(/{{id}}/g,encode(json.data[m].nameUrl,'base16'));
                h+=html;
            }
          ShowTip(name+'('+bookData.siteName+')','关闭','<ul class=\'w3-ul\' style="text-align:left;">'+h+'</ul>');
      }else{
          ShowTip(name+'('+bookData.siteName+')','关闭',error);
      }
    };
    $.ajax.post("/index/Book/SearchName", "name="+name, success, false);
};

var getRoot=function(url){
    var urls =url.split('.');
    var count=urls.length;
    if(count>=2){
        return urls[count-2]+"."+urls[count-1];
    }
};

var changeBook=function(name,site,index,id){
    name=decodeURI(name);
    site=decodeURI(site);
    index=decodeURI(index);
    id=decodeURI(id);
    var book = new Book();
    var bookData=book.getData(name);
    bookData.id=id;
    bookData.index=index;
    bookData.siteName=site;
    book.tmp=bookData;
    book.saveTmp();

    $('#tipName').html(name+'('+site+')');
};