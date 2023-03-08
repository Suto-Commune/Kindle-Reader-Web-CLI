var Hpage = function () {
    var t=this;
    this.top=0;
    this.one=1;
    this.heighView=0;
    this.list=[];
    this.realHeigh=0;
    this.now=0;
    this.count=0;
    this.next=$("#next");
    this.before=$("#before");
    this.total=0;
    this.init=function (select,top,height) {
        this.top=top;

        t.list=$(select);
        if(this.list.length!==0){
            var max=t.list[0].offsetHeight;
            for(var m=0;m<t.list.length;m++)
                if(t.list[m].offsetHeight>max)
                    max=t.list[m].offsetHeight;

                t.one=max;
        }
        height=height||'.right_t.flexone';
        this.heighView = $(height)[0].offsetHeight;

        this.realHeigh=this.heighView-this.top;
        console.log("heighView："+this.heighView+" realHeigh:"+this.realHeigh+" one:"+this.one);
        this.count=parseInt(this.realHeigh/this.one);
        //一个页面显示多少标签

        this.total=this.list.length;
        console.log("total："+this.total+" count/page:"+this.count);
        t.set('next','nextY');
        if(this.total<=this.count){
            this.now=this.total;
            t.set('before','beforeN');
            t.set('next','nextN');
            return;
        }
        for(var i=this.count;i<this.total;i++){
            $(t.list[i]).css('display','none');
        }
        this.now=this.count;
        /*$('#before').click(function(){

        });
        $('#next').click(function(){

        });
*/
    };
    this.set = function (poc, name) {
        //
        var img = {
            "nextY": "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBzdGFuZGFsb25lPSJubyI/PjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+PHN2ZyB0PSIxNDk4MTk1NTQ5MzUxIiBjbGFzcz0iaWNvbiIgc3R5bGU9IiIgdmlld0JveD0iMCAwIDEwMjQgMTAyNCIgdmVyc2lvbj0iMS4xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHAtaWQ9IjE4NDQiIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iMzIiIGhlaWdodD0iMzIiPjxkZWZzPjxzdHlsZSB0eXBlPSJ0ZXh0L2NzcyI+PC9zdHlsZT48L2RlZnM+PHBhdGggZD0iTTc4My40NTE5MzcgMzIyLjE3MzQ1NCA1MTIuMDAxNTgzIDU5My4xNTA0NyAyNDAuNTUyODEyIDMyMi4xNzM0NTRjLTIwLjAzNjg5OS0yMC4wMjEwNjgtNTIuNDg1MDU2LTIwLjAyMTA2OC03Mi41MjE5NTUgMC0xMC4wMTEzMjYgMTAuMDExMzI2LTE1LjAyNjQ4NyAyMy4xMTQzODQtMTUuMDI2NDg3IDM2LjIyNjk0MiAwIDEzLjExNDE0IDUuMDE1MTYxIDI2LjIyNjY5NyAxNS4wMjY0ODcgMzYuMjMzMjc0bDMwNy43MDczNzMgMzA3LjE5OTIwOGMxMC4wMTYwNzUgMTAuMDExMzI2IDIzLjEzNDk2NCAxNS4wMTA2NTYgMzYuMjYzMzUyIDE1LjAxMDY1NiAxMy4xMTg4ODkgMCAyNi4yNDI1MjgtNS4wMDA5MTQgMzYuMjU4NjAzLTE1LjAxMDY1NmwzMDcuNzEzNzA2LTMwNy4yMDA3OTJjMTAuMDA0OTkzLTEwLjAwNDk5MyAxNS4wMjE3MzgtMjMuMTE5MTM0IDE1LjAyMTczOC0zNi4yMzMyNzRzLTUuMDE1MTYxLTI2LjIxNzE5OS0xNS4wMjE3MzgtMzYuMjI2OTQyQzgzNS45MzA2NiAzMDIuMTUwODAzIDgwMy40ODQwODcgMzAyLjE1MDgwMyA3ODMuNDUxOTM3IDMyMi4xNzM0NTR6IiBwLWlkPSIxODQ1IiBmaWxsPSIjMDAwMDAwIj48L3BhdGg+PC9zdmc+",
            "beforeN": "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBzdGFuZGFsb25lPSJubyI/PjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+PHN2ZyB0PSIxNDk4MTk1NTk2NTg2IiBjbGFzcz0iaWNvbiIgc3R5bGU9IiIgdmlld0JveD0iMCAwIDEwMjQgMTAyNCIgdmVyc2lvbj0iMS4xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHAtaWQ9IjI2ODQiIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iMzIiIGhlaWdodD0iMzIiPjxkZWZzPjxzdHlsZSB0eXBlPSJ0ZXh0L2NzcyI+PC9zdHlsZT48L2RlZnM+PHBhdGggZD0iTTI0MC41NDgwNjMgNzAxLjgyNjU0NmwyNzEuNDUwMzU0LTI3MC45NzcwMTYgMjcxLjQ0ODc3MSAyNzAuOTc3MDE2YzIwLjAzNjg5OSAyMC4wMjEwNjggNTIuNDg1MDU2IDIwLjAyMTA2OCA3Mi41MjE5NTUgMCAxMC4wMTEzMjYtMTAuMDExMzI2IDE1LjAyNjQ4Ny0yMy4xMTQzODQgMTUuMDI2NDg3LTM2LjIyNjk0MiAwLTEzLjExNDE0LTUuMDE1MTYxLTI2LjIyNjY5Ny0xNS4wMjY0ODctMzYuMjMzMjc0TDU0OC4yNjE3NjkgMzIyLjE2NzEyMmMtMTAuMDE2MDc1LTEwLjAxMTMyNi0yMy4xMzQ5NjQtMTUuMDEwNjU2LTM2LjI2MzM1Mi0xNS4wMTA2NTYtMTMuMTE4ODg5IDAtMjYuMjQyNTI4IDUuMDAwOTE0LTM2LjI1ODYwMyAxNS4wMTA2NTZMMTY4LjAyNjEwOCA2MjkuMzY3OTEzYy0xMC4wMDQ5OTMgMTAuMDA0OTkzLTE1LjAyMTczOCAyMy4xMTkxMzQtMTUuMDIxNzM4IDM2LjIzMzI3NHM1LjAxNTE2MSAyNi4yMTcxOTkgMTUuMDIxNzM4IDM2LjIyNjk0MkMxODguMDY5MzQgNzIxLjg0OTE5NyAyMjAuNTE1OTEzIDcyMS44NDkxOTcgMjQwLjU0ODA2MyA3MDEuODI2NTQ2eiIgcC1pZD0iMjY4NSIgZmlsbD0iI2JiYmJiYiI+PC9wYXRoPjwvc3ZnPg==",
            "nextN": "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBzdGFuZGFsb25lPSJubyI/PjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+PHN2ZyB0PSIxNDk4MTk1NTQ5MzUxIiBjbGFzcz0iaWNvbiIgc3R5bGU9IiIgdmlld0JveD0iMCAwIDEwMjQgMTAyNCIgdmVyc2lvbj0iMS4xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHAtaWQ9IjE4NDQiIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iMzIiIGhlaWdodD0iMzIiPjxkZWZzPjxzdHlsZSB0eXBlPSJ0ZXh0L2NzcyI+PC9zdHlsZT48L2RlZnM+PHBhdGggZD0iTTc4My40NTE5MzcgMzIyLjE3MzQ1NCA1MTIuMDAxNTgzIDU5My4xNTA0NyAyNDAuNTUyODEyIDMyMi4xNzM0NTRjLTIwLjAzNjg5OS0yMC4wMjEwNjgtNTIuNDg1MDU2LTIwLjAyMTA2OC03Mi41MjE5NTUgMC0xMC4wMTEzMjYgMTAuMDExMzI2LTE1LjAyNjQ4NyAyMy4xMTQzODQtMTUuMDI2NDg3IDM2LjIyNjk0MiAwIDEzLjExNDE0IDUuMDE1MTYxIDI2LjIyNjY5NyAxNS4wMjY0ODcgMzYuMjMzMjc0bDMwNy43MDczNzMgMzA3LjE5OTIwOGMxMC4wMTYwNzUgMTAuMDExMzI2IDIzLjEzNDk2NCAxNS4wMTA2NTYgMzYuMjYzMzUyIDE1LjAxMDY1NiAxMy4xMTg4ODkgMCAyNi4yNDI1MjgtNS4wMDA5MTQgMzYuMjU4NjAzLTE1LjAxMDY1NmwzMDcuNzEzNzA2LTMwNy4yMDA3OTJjMTAuMDA0OTkzLTEwLjAwNDk5MyAxNS4wMjE3MzgtMjMuMTE5MTM0IDE1LjAyMTczOC0zNi4yMzMyNzRzLTUuMDE1MTYxLTI2LjIxNzE5OS0xNS4wMjE3MzgtMzYuMjI2OTQyQzgzNS45MzA2NiAzMDIuMTUwODAzIDgwMy40ODQwODcgMzAyLjE1MDgwMyA3ODMuNDUxOTM3IDMyMi4xNzM0NTR6IiBwLWlkPSIxODQ1IiBmaWxsPSIjYmJiYmJiIj48L3BhdGg+PC9zdmc+",
            "beforeY": "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBzdGFuZGFsb25lPSJubyI/PjwhRE9DVFlQRSBzdmcgUFVCTElDICItLy9XM0MvL0RURCBTVkcgMS4xLy9FTiIgImh0dHA6Ly93d3cudzMub3JnL0dyYXBoaWNzL1NWRy8xLjEvRFREL3N2ZzExLmR0ZCI+PHN2ZyB0PSIxNDk4MTk1NTk2NTg2IiBjbGFzcz0iaWNvbiIgc3R5bGU9IiIgdmlld0JveD0iMCAwIDEwMjQgMTAyNCIgdmVyc2lvbj0iMS4xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHAtaWQ9IjI2ODQiIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB3aWR0aD0iMzIiIGhlaWdodD0iMzIiPjxkZWZzPjxzdHlsZSB0eXBlPSJ0ZXh0L2NzcyI+PC9zdHlsZT48L2RlZnM+PHBhdGggZD0iTTI0MC41NDgwNjMgNzAxLjgyNjU0NmwyNzEuNDUwMzU0LTI3MC45NzcwMTYgMjcxLjQ0ODc3MSAyNzAuOTc3MDE2YzIwLjAzNjg5OSAyMC4wMjEwNjggNTIuNDg1MDU2IDIwLjAyMTA2OCA3Mi41MjE5NTUgMCAxMC4wMTEzMjYtMTAuMDExMzI2IDE1LjAyNjQ4Ny0yMy4xMTQzODQgMTUuMDI2NDg3LTM2LjIyNjk0MiAwLTEzLjExNDE0LTUuMDE1MTYxLTI2LjIyNjY5Ny0xNS4wMjY0ODctMzYuMjMzMjc0TDU0OC4yNjE3NjkgMzIyLjE2NzEyMmMtMTAuMDE2MDc1LTEwLjAxMTMyNi0yMy4xMzQ5NjQtMTUuMDEwNjU2LTM2LjI2MzM1Mi0xNS4wMTA2NTYtMTMuMTE4ODg5IDAtMjYuMjQyNTI4IDUuMDAwOTE0LTM2LjI1ODYwMyAxNS4wMTA2NTZMMTY4LjAyNjEwOCA2MjkuMzY3OTEzYy0xMC4wMDQ5OTMgMTAuMDA0OTkzLTE1LjAyMTczOCAyMy4xMTkxMzQtMTUuMDIxNzM4IDM2LjIzMzI3NHM1LjAxNTE2MSAyNi4yMTcxOTkgMTUuMDIxNzM4IDM2LjIyNjk0MkMxODguMDY5MzQgNzIxLjg0OTE5NyAyMjAuNTE1OTEzIDcyMS44NDkxOTcgMjQwLjU0ODA2MyA3MDEuODI2NTQ2eiIgcC1pZD0iMjY4NSIgZmlsbD0iIzAwMDAwMCI+PC9wYXRoPjwvc3ZnPg=="
        };


        $('#'+poc+"_img").attr('src', img[name]);
    };
    this.beforeClick=function () {
        var t=this;
        if(t.now<=t.count)return;
        console.log("before 当前页面页数：",t.now);
        if(t.now-t.count<=t.count){
            t.set('before','beforeN');
        }
        for(var i=0;i<this.total;i++){
            $(t.list[i]).css('display','none');
        }
        for(i=t.now-t.count*2;i<t.now-t.count;i++){
            $(t.list[i]).css('display','block');
        }
        t.now=t.now-t.count;
        t.set('next','nextY');
        console.log("before完成，当前页面页数：",t.now);
    };
    this.nextClick=function () {
        var t=this;
        console.log("next当前页面页数：",t.now);
        if(t.now>=t.list.length)return;
        if(t.now+t.count>=t.list.length){
            t.set('next','nextN')

        }
        for(var i=0;i<this.total;i++){
            $(t.list[i]).css('display','none');
        }
        for(i=t.now;i<t.now+t.count;i++){
            $(t.list[i]).css('display','block');
        }
        t.now=t.now+t.count;

        t.set('before','beforeY');
        console.log("next执行完成，当前页面页数：",t.now);
    }
};//页面翻页控制器