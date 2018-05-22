$(document).ready(function(){
    var project_name = window.localStorage.getItem("project_name");
    var type = window.localStorage.getItem("project_type");
    var overview = $('#overview');
    var result = $('#result');
    var code = $('#code');
    var download = $('#download');
    change_btn_color();
    bindEvent();
    function bindEvent(){
        overview.on('click',function(){
            location.href = "/results?project_name="+project_name+"&type="+type;       
        });
        result.on('click',function(){
            var href = "/result_show?project_name="+project_name+"&type="+type;
            location.href = href;        
        });
        code.on('click',function(){
            var href = "/result_code?project_name="+project_name+"&type="+type;
            location.href = href;        
        });
        download.on('click',function(){
            var href = "/result_download?project_name="+project_name+"&type="+type;
            location.href = href;        
        });
        $('#container').on('click','ul > li > span.details',function(event){
            var target = $(event.target);
            var oDiv = target.parent().parent();
            var url = "";
            if(type == "news"){
                var title = oDiv.find('.title').eq(0).html(); 
                url = "http://localhost:3000/details?project_name="+project_name+"&type="+type+"&title="+encodeURIComponent(title);           
            }else if(type == "comment"){
                var author =  oDiv.find('.author').eq(0).html(); 
                var time =  oDiv.find('.time').eq(0).html();  
                url = "http://localhost:3000/details?project_name="+project_name+"&type="+type+"&author="+author+"&time="+time;         
            }else if(type == "forum"){
                var title = oDiv.find('.title').eq(0).html(); 
                url = "http://localhost:3000/details?project_name="+project_name+"&type="+type+"&title="+encodeURIComponent(title);
            }else{
                return;
            }
            
            location.href = url;
        })
    }
    function change_btn_color(){
        result.css('background-color',"#e3e3e3");
        overview.css('background-color',"#fff");
        code.css('background-color',"#fff");
        download.css('background-color',"#fff");
    }
    
})

