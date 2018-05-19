$(document).ready(function(){
    var project_name = window.localStorage.getItem("project_name");
    var container = $('#container');
    var type = window.localStorage.getItem("project_type");
    var overview = $('#overview');
    var result = $('#result');
    var code = $('#code');
    var download = $('#download');
    bindEvent();
    var url = 'http://localhost:5000/debug/'+project_name+'/get';
    $.ajax({
        url:url,
        type:'GET',
        dataType:'JSON',
        data:{},
        success:function(res){
            console.log("success");
            
            console.log(res['script']);
            if(res == null){
                container.html("no code now.");
            }else{
                container.html("<pre>"+res.script+"</pre>");
            }
            
        }
    })
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
