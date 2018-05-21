$(document).ready(function(){
    
    
    var name = "";
    var url;
    var title_css;
    var nextpage_css;
    var href_css;
    var time_css;
    var src_css;
    var content_css;
    var move;
    var click;
    var nextpage_format;
    var deep_num;
    // var nextpage_format = $('input[name="format"]:checked').eq(0).val();
    var btn = $('#start');
    
    btn.on('click',function(){
        url = $('#crawler-url').val();
        title_css = $('#title-css').val();
        nextpage_css = $('#nextpage-css').val();
        href_css = $('#href-css').val();
        time_css = $('#time-css').val();
        src_css = $('#src-css').val();
        content_css = $('#content-css').val();
        move = $('#move').val();
        click = $('#click').val();
        deep_num = $('#deep_num').val();
        nextpage_format = $("#nextpage-format").val();
        if(nextpage_format == "下拉加载"){
            format = 'move';
        }else{
            format = 'click';
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
                'content_css':content_css,'deep_num':deep_num,'nextpage_format':format,'web-type':'news'
                },
                success:function(e){
                    console.log(e);
                    window.localStorage.setItem(name, "news");
                    // var tt = window.localStorage.getItem(name);
                    // console.log("123456");
                    // console.log("web:"+tt);
                    run(name);
                    setTimeout(function(){
                        window.location = 'http://localhost:3000/index';
                    },1000);
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
            console.log(name);
        console.log(url);
        console.log(title_css);
        console.log(nextpage_css);
        console.log(href_css);
        console.log(src_css);
        console.log(time_css);
        console.log(content_css);
        console.log(nextpage_format);
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
                                localStore(name,"news");
                                setTimeout(function(){
                                    window.location = 'http://localhost:3000/index';
                                },2000)
                                console.log(item);
                            },
                            error:function(e){
                                alert("crawler construction failed:\n"+e);
                            }
                        })
                    }
                },1000);
                

            }
        })
    }
    function localStore(project,type){
        window.localStorage.setItem(project, type);
    }
})