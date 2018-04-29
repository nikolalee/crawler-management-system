$(document).ready(function(){
    
    var url = $('#crawler-url').val();
    var title_css = $('#title-css').val();
    var nextpage_css = $('#nextpage-css').val();
    var href_css = $('#href-css').val();
    var time_css = $('#time-css').val();
    var src_css = $('#src-css').val();
    var content_css = $('#content-css').val();
    var move = $('#move').val();
    var click = $('#click').val();
    var nextpage_format = "";
    var name = "";
    
    // var nextpage_format = $('input[name="format"]:checked').eq(0).val();
    var btn = $('#start');
    
    btn.on('click',function(){
        if($('#click').is(':checked')){
            nextpage_format = click;
        }else if($('#move').is(':checked')){
            nextpage_format = move;
        }
        name = $('#crawler-name').val();
        console.log(name);
        var flag = isEmpty();
        console.log(flag);
        if(!flag){
            var url1 = "http://localhost:5000/debug/"+name+"/get_script_save";
            $.ajax({
                url:url1,
                type:"POST",
                data:{'name':name,'url':url,'title_css':title_css,'nextpage_css':nextpage_css,
                'href_css':href_css,'time_css':time_css,'src_css':src_css,
                'content_css':content_css,'nextpage_format':nextpage_format,'web-type':'news'
                },
                success:function(e){
                    console.log(e);
                    run(name);
                    window.location = 'http://localhost:3000/index';
                },
                error:function(e){
                    console.log(e);
                }
            })
        }else{
            alert('There is empty item.');
        }
    })
    function isEmpty(){
        if(name ==""||url==""||title_css==""||nextpage_css==""||href_css==""||time_css==""||
            src_css==""||content_css==""||nextpage_format==""){
            return 1;
        }else{
            return 0;
        }
    } 
    function run(name){
        var url1 = 'http://localhost:5000/spiderweb/run';
        console.log(url1);
        $.ajax({
            url:'http://localhost:5000/update',
            type:'POST',
            data:{'pk':name,'name':'status','value':'RUNNING'},
            success:function(item){
                var data = JSON.parse(item);
                console.log(data);
                console.log(1);
                setTimeout(function(){
                    if(data.code === 200){
                        $.ajax({
                            url:url1,
                            type:"POST",
                            data:{'project':name},
                            success:function(item){
                                console.log(item);
                            },
                            error:function(e){
                                console.log(e);
                            }
                        })
                    }
                },500);
                

            }
        })
    }
})