$(document).ready(function(){
    var project_name = window.localStorage.getItem("project_name");
    var type = window.localStorage.getItem("project_type");
    var overview = $('#overview');
    var result = $('#result');
    var code = $('#code');
    var download = $('#download');
    var url = 'http://localhost:5000/spiderweb/counter';
    if($('#crawl-type').html() == ""){
        $('#crawl-type').html(type);
    }
    if($('#crawl-name').html() == ""){
        $('#crawl-name').html(project_name);
    }
    change_btn_color();
    bindEvent();
    get_counter();
    refresh_num();
    var timer = setInterval(function(){
        get_counter();
    },5000);
    function bindEvent(){
        overview.on('click',function(){
            location.href = "#";        
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
    function change_btn_color(){
        overview.css('background-color',"#e3e3e3");
        result.css('background-color',"#fff");
        code.css('background-color',"#fff");
        download.css('background-color',"#fff");
    }
    function refresh_num(){
        $.ajax({
            url:'/getNum',
            type:'GET',
            // dataType:'JSON',
            data:{'project':project_name,'type':type},
            success:function(data){
               
                $('#crawl-num').html(data.len);
            }
        })
    }
    function get_counter(){
        $.ajax({
            url:url,
            type:'GET',
            dataType:'JSON',
            data:{},
            success:function(res){
                // console.log(res);
                //console.log(res.test5.all);
                var name = project_name;
                var percent = [0,0,0,0];
                // console.log(name);
                if(res[name].hasOwnProperty("all")){
                    var data = res[name].all;
                }else{
                    data = {};
                }
                //console.log(data);
                var sum = 0;
                if("pending" in data){
                    percent[0] = data.pending;
                    sum += data.pending;
                }
                 if("success" in data){
                    percent[1] = data.success;
                    sum += data.success;
                }
                if("retry" in data){
                    percent[2] = data.retry;
                    sum += data.retry;
                }
                if("failed" in data){
                    percent[3] = data.failed;
                    sum += data.failed;
                }
                //console.log(percent);
                //console.log(sum);
                var percent2 = [];
                for(var i = 0;i < percent.length;i++){
                    if(percent[i]){
                        percent2[i] = (percent[i] / sum)*100;
                        percent2[i] = parseFloat(percent2[i].toFixed(2));
                    }else{
                        percent2[i] = 0;                            
                    }
                }
                
                // console.log(percent);
                $("#bars li .bar").each(function(index,item) {
                 
                    // console.log(res.data);
                    var percentage = percent2[index];
                    $(this).attr('data-percentage',percentage);
                    $(this).attr('data-num',percent[index]);
                    // console.log(percentage);
                    $(this).animate({
                        'height' : percentage + '%'
                    }, 1000);
                 });
                }
            })
    }


})

