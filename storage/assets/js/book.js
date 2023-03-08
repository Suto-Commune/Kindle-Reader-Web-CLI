function convertObj(data) {
    var _result = [];
    for (var key in data) {
        var value = data[key];
        if (value.constructor&&value.constructor === Array) {
            value.forEach(function(_value) {
                _result.push(key + "=" + _value);
            });
        } else {
            _result.push(key + '=' + value);
        }
    }
    return _result.join('&');
}
var Book=function(){
    this.setStorage=function (local) {
        $.cookie.set('storage',local,3650,"/");
    };
    this.getStorage=function () {
        var res=$.cookie.get('storage');
        if(res==='')return 'cookie';
        else return res;
    };
    this.isVip=function () {
        var vip=$.cookie.get('vip');
        if(vip==='')return false;
        var tmp = Date.parse( new Date() ).toString();
        tmp = tmp.substr(0,10);
        return (parseInt(tmp)-parseInt(vip)<0);
    };
    this.getBook=function () {

        if(this.isVip()){
            var th=this;
            $.ajax.get('/index/user/getbook',function (data) {

                data=JSON.parse(data);
                th.book = [];
                if(data.state){
                    th.book=data.data;
                }

            },false);

            
        }else if(this.getStorage()==='cookie'){
            this.book=$.cookie.get("book");
            if (this.book ===  '')
                this.book = [];
            else {
                this.book = JSON.parse(decodeURI(this.book));
            }
        }else{
            this.book=localStorage.getItem('book');
            if (this.book ===  null)
                this.book = [];
            else {
                this.book = JSON.parse(decodeURI(this.book));
            }
        }
    };
    this.save=function () {
        if(this.getStorage()==='cookie'){
            $.cookie.set("book", encodeURI(JSON.stringify(this.book)), 3650,"/");
        }else{
            localStorage.setItem('book',encodeURI(JSON.stringify(this.book)));
        }
    };

    this.sync=function (data,opt) {
        data.opt=opt;
        console.log(data);
        data=convertObj(data);
        if(this.isVip()){
            var th=this;
            $.ajax.post('/index/user/setbook',data,function (data) {
                data=JSON.parse(data);
                th.book = [];
                if(data.state){
                    th.book=data.data;
                }
            });
        }else{
            this.save();
        }
    };


    this.insert = function () {//添加书籍,所加的书籍必须是不存在，并且在tmp中，就是查看信息必须要写的
        if(this.find(this.tmp.title) === -1){
            this.book.push(this.tmp);//每次查看书籍都保留在tmp中
            this.sync(this.tmp,'insert');
        }
    };
    this.find = function (title) {//找书的位置
        //title=decodeURI(title);
        for (var i = 0; i < this.book.length; i++) {

            if (this.book[i].title=== title) return i;
            if (this.book[i].id === title) return i;
        }
        return -1;//找不到这个书
    };
    this.delete = function (title) {//删除书籍
        var index = this.find(title);
        if (index === -1) {
            return false;
        } else {
            this.book.splice(index, 1);
            this.sync({title:title},'del');
            return true;
        }
    };
    this.update = function (title) {//更新缓存中的书籍信息
        var index = this.find(title);
        if (index !== -1) {
            this.book[index] = this.tmp;//存储了才更新
            this.sync(this.tmp,'update');

        }
        //没找到就不管了
    };
    this.saveTmp = function () {//保存临时书籍信息
        localStorage.setItem("tmp", encodeURI(JSON.stringify(this.tmp)));
        this.update(this.tmp.title,'update');
    };
    this.isFavourite = function (title) {
        if (this.find(title) === -1) {
            return "收藏本书";
        } else {
            return "取消收藏";
        }
    };//是否收藏
    this.favourite = function (title) {
        var index = this.find(title);
        if (index === -1) {//没有收藏
            this.insert();
            return true;
        } else {
            this.delete(title);
            return false;
        }
    };//收藏或者取消收藏
    this.getData = function (title) {
        var index = this.find(title);
        if (index === -1) {//没有收藏
            return {"title":"","id":"","readCount":0,"totalCount":1,"index":0,'readChapter':'','totalChapter':'','siteName':'',"author":"","page":0};
        } else {
            return this.book[index];
        }
    };//取得收藏的节点信息

    this.book=null;//书籍列表
    this.getBook();
    this.tmp = localStorage.getItem("tmp");//临时存储当前阅读书籍
    if (this.tmp ===  null) this.tmp = []; else this.tmp = JSON.parse(decodeURI(this.tmp));
    this.length=function () {
        return Object.keys(this.book).length;
    };
};