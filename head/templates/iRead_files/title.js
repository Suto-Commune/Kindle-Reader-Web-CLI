var Title=function(){
    this.title=document.title;
    this.set=function(title){
        document.title=title;
    };
    this.reset=function(){
        document.title=this.title;
    };
    this.update=function(title){
        document.title=this.title+" - "+title;
    }
};//标题修改