$(document).ready(function(){
    var project_name = window.localStorage.getItem("project_name");
    var type = window.localStorage.getItem("project_type");
    var overview = $('#overview');
    var result = $('#result');
    var code = $('#code');
    var download = $('#download');
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
                url = "http://localhost:3000/details?project_name="+project_name+"&type="+type+"&title="+title;           
            }else if(type == "comment"){
                var author =  oDiv.find('.author').eq(0).html(); 
                var time =  oDiv.find('.time').eq(0).html();  
                url = "http://localhost:3000/details?project_name="+project_name+"&type="+type+"&author="+author+"&time="+time;         
            }else if(type == "forum"){
                var title = oDiv.find('.title').eq(0).html(); 
                url = "http://localhost:3000/details?project_name="+project_name+"&type="+type+"&title="+title;
            }else{
                return;
            }
            
            location.href = url;
        })
    }
    
})
