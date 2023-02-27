/**
 * 主页管理类
 * @constructor
 */
var Home = function () {//主页类
    this.MenuChoose = function (modle) {
        var menus = [
            {"key": "小说书架", "url": "Books"},
            {"key": "RSS阅读", "url": "Rss"},
            {"key": "小说搜索", "url": "Search"},
            {"key": "其他功能", "url": "Other"},
            {"key": "会员中心", "url": "User"},
            {"key": "进入后台", "url": "WeChat"},
            {"key": "退出登录", "url": "Logout"},
            {"key": "使用帮助", "url": "Help"},
            {"key": "加书友群", "url": "Group"},
            {"key": "免责声明", "url": "About"},
        ];
        //主菜单
        var choose = '<img alt="" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAB9ElEQVR4nO2a4ZGCMBBGXwmUQAmUQAmWQAfawVmCHZgOvA7uOtAOzg60A+4Hw8jcAWYlycaQN7N/M98LYROikMlkMplM6nwApXYIDSrgDLSA0Y0Sni2d+LBKzUChKIAT/+VXsQoq4Idx+Ra460XzT8O0eC9faYXzzZGVyhfAFyuVH25xq5S/MS/f0vWF5Gh4Lr56+Z1SPq886/RJH3Zs5T+1AvrEVv5Cty0mha38ncTkbQ44Se/1tk++BTZKGb0hkd/rRPSHRN7oRPSHRD65ji+Rv5PY1ZZEvgVqlZSe2CGT32uELPCz1TTI5FWOuQWPS4fG4bgbZPJXFJreUL6vo4NxbS8zhhX8pDcm39eJ159GiVw++Lf9nHxfZ+Rbkc24Ubz3tiFvyJbm1K81Ub33IOvON+ya40Ewptp7P6QZCTRXW4djtUTykWOQhR7bIV7p+N9+dF7DIAt/5vHeFsz/UDlWUZ7zDfJJqLC/0RlWlJcbBd3np1RGWlHf6PqehLe41PQ5CXU4jWWUdE/LpfwhpIALKtxNwpU3WPpjuJqEOnBup9QskzehA/ugIeGub0uDfAKiPPAsQXK5GfWBZwkGu6Vf6sQLg2F+AvZawUJiGJe/KGYKytSRuVbMFJy/k2BU0yjRT0LyjW+OkkT/s5fJZDKZFPgF2+acfXQipdoAAAAASUVORK5CYII=" width="64">';
        //选择的图标
        var menu = $("#Real_Menu");
        //清空选项
        menu.text("");

        var html = '';
        //整理好加入选项
        for (var i = 0; i < menus.length; i++) {
            if (modle === menus[i].url) {
                html = '<li><div class="display_inline" data-v-46207b3c  data-url="' + menus[i].url + '">' + choose + '</div>' + menus[i].key + '</li>';
            } else
                html = '<li><div class="display_inline"  data-v-46207b3c data-url="' + menus[i].url + '"></div>' + menus[i].key + '</li>';

            menu.append(html);
        }



        //其他各种选项进行初始化操作
        switch (modle) {
            case "Books": booklist();break;
            case "Detail":detail();break;
            case "Search":break;
            case "Rss":break;
            case "WeChat":break;
            case "Logout":break;
            case "User":User();break;
            case "Help":help();break;
            case "Group":break;
            case "About":about();break;
            case "Other":other();break;
            default :booklist();
        }
        //监听按钮
        window.onload = function () {

            var menu = $("#Menu");
            $("#Menu_button").click(function (e) {
                var item = $("#dropup2");
                var values = menu.attr("data-menu");
                if (values === "false") {
                    item.addClass("open");
                    menu.attr("data-menu", "true");
                } else {
                    item.removeClass("open");
                    menu.attr("data-menu", "false");
                }
                $("#dropdown-backdrop").attr("class", "dropdown-backdrop");


            });//弹出菜单按钮
            $("#dropdown-backdrop").click(function (e) {
                $("#dropup2").removeClass("open");
                $('#tipBox').css('display','none');
                menu.attr("data-menu", "false");
                $("#dropdown-backdrop").attr("class", "");

            });//遮罩关闭
            $("ul#Real_Menu>li").click(function (e) {
                window.open("/index/main/" + $(this).find("div").attr("data-url"), '_self');
            });//对应选项选择事件

            $('#white').click(function () {


                var isBlack=$.cookie.get('black');
                if(isBlack===undefined)isBlack=false;
                else isBlack = isBlack.toString() === 'true';
                if(isBlack){
                    $.cookie.set('black','false');
                    $('html').attr('class','white-theme');
                    alert('已取消暗黑模式');
                } else{
                    $.cookie.set('black','true');
                    $('html').attr('class','dark-theme');
                    alert('已切换暗黑模式');

                }



            });
            $('#storage').click(function () {
                var html="<ul class='w3-ul' style=\"text-align:left;\"><li>\n" +
                    "         <div id='{{id}}' class='w3-hover-black' onclick=window.location.href=\"https://github.com/Suto-Commune/Kindle-Reader-Web-CLI\">\n" +
                    "                 <div style='font-size: 0.8em'><b>声明</b></div>\n" +
                    "                 <div style='font-size: 0.8em'>本站使用Reader及Kindle-Reader-Web-Cli搭建，网页文件来源于https://iread.ankio.net/</div>\n" +
                    "             </div>" +
                    "       </li>" +
                    "<li>"
                    "</ul>";
                //弹框
                ShowTip('公告','关闭',html);
            });
            //检查设置
            if($.cookie.get('stroage')===''){
                $('#storage').click();

            }

        };


    };//生成菜单
    this.init = function () {


        $.ajax.get("/index/main/log",function (d) {
            d=JSON.parse(d);
            var ver=$.cookie.get("ver");
            if(ver===''||ver===null||parseFloat(ver)<parseFloat(d.ver)){
                alert(d.log);
                $.cookie.set("ver",d.ver,60);
            }
        });


        $("#before").click(function () {
            if(typeof page!=="undefined")
                page.beforeClick();
        });
        $("#next").click(function () {
            if(typeof page!=="undefined")
            page.nextClick();
        });


    };
};
