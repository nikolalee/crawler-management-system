$(document).ready(function(){
    var project_name = window.localStorage.getItem("project_name");
    var type = window.localStorage.getItem("project_type");
    var overview = $('#overview');
    var result = $('#result');
    var code = $('#code');
    var download = $('#download');
    
    if($('#crawl-type').html() == ""){
        $('#crawl-type').html(type);
    }
    if($('#crawl-name').html() == ""){
        $('#crawl-name').html(project_name);
    }
    bindEvent();
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
var url = 'http://localhost:5000/spiderweb/counter';
$.ajax({
    url:url,
    type:'GET',
    dataType:'JSON',
    data:{},
    success:function(res){
            console.log(res);
            //console.log(res.test5.all);
            var name = project_name;
            var percent = [0,0,0,0];
            console.log(name);
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
            for(var i = 0;i < percent.length;i++){
                if(percent[i]){
                    percent[i] = (percent[i] / sum)*100;
                    _this.percent[i] = parseFloat(percent[i].toFixed(2));
                }else{
                    _this.percent[i] = 0;                            
                }
            }
            
            console.log(_this.percent);
            $("#bars li .bar").each(function(index,item) {
             
                // console.log(res.data);
                var percentage = _this.percent[index];
                // console.log(percentage);
                $(this).animate({
                    'height' : percentage + '%'
                }, 1000);
             });
    }
})

})

