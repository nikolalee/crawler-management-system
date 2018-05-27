$(document).ready(function(){
    var project_name = window.localStorage.getItem("project_name");
    var type = window.localStorage.getItem("project_type");
    var overview = $('#overview');
    var result = $('#result');
    var code = $('#code');
    var download = $('#download');
    $("#type").val(type);
    $('#project').val(project_name);
    var menuList = $('#menu');
    //menu animation
    $('#menu').add('#create').mouseout(function(){
        menuList.css('height','0');
    })
    $('#create').add('#menu').mouseover(function(){
        menuList.css('height','162px');
    })
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
    
    }
    
})
