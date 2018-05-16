$(document).ready(function(){
	var $log = $('.log_toggle');
	// console.log($log);
	// var logArea = $('#log_area');
	var newProject = $('#create');
	var runningArea = $('#items');
	var todoArea = $('#todoArea');
	//bind log event
	get_info();
	$('#running-project').add('#recent-project').on('click','ul > li > span.log_toggle',function(event){
		var target = $(event.target);
		var logArea = target.parent().parent().parent().children('.log');
		if (logArea.css('display') == 'none'){
			logArea.css('display','block');
			// console.log('hi');
		}else{
			logArea.css('display','none');
			// console.log('kk');
		}
	})
	//bind delete event
	$('#recent-project').on('click','ul > li > span.del',function(event){
		var target = $(event.target);
		var oDiv = target.parent().parent().parent();
		var name = oDiv.find('.pro-name').eq(0).html();
		var data = del(name);
		// console.log(data);
		oDiv.remove();
		
	})
	//bind run event
	$('#running-project').add('#recent-project').on('click','ul > li > span.run',function(event){
		var target = $(event.target);
		var oDiv = target.parent().parent().parent();
		var name = oDiv.find('.pro-name').eq(0).html();
		console.log(name);
		run(name);
		get_info();
	})
	//bind stop event
	$('#running-project').add('#recent-project').on('click','ul > li > span.stop',function(event){
		var target = $(event.target);
		var oDiv = target.parent().parent().parent();
		var name = oDiv.find('.pro-name').eq(0).html();
		console.log(name);
		stop(name);
		get_info();
	})
	//bind results event
	$('#running-project').add('#recent-project').on('click','ul > li > span.results',function(event){
		var target = $(event.target);
		var oDiv = target.parent().parent().parent();
		var name = oDiv.find('.pro-name').eq(0).html();
		var type = window.localStorage.getItem(name);
		//for test
		if(!type){
			type = "news";
		}
		console.log(name);
		getResults(name,type);
	})
	
	function get_info(){
		// var item = [];
		$.ajax({
			url:'http://localhost:5000/get_info',
			type:'POST',
			success:function(item){
				// console.log(data);
				// item = data;
				var data = JSON.parse(item);
				console.log(data.length);
				if(data){
					runningArea.empty();
					todoArea.empty();
					for(var i = 0;i < data.length;i++){
						// console.log("2");
						// console.log(data.length);
						// console.log(data[i]['name']);
						var web="";
						if(data[i]['status'] == "RUNNING"){
							web = window.localStorage.getItem(data[i]['name']);
							addNodeRun(web,data[i]['name'],data[i]['status']);
						}else{
							web = window.localStorage.getItem(data[i]['name']);
							console.log("web:"+web);
							addNodeTodo(web,data[i]['name'],data[i]['status']);
						}
					}
				}
			}
		})
		// return item;
	}
	function addNodeRun(web,name,status){
		var appendPart = '<div class="item-box">'+
		'<ul class="ul_item">'+
		'<li class="item item_color" ><span>'+web+'</span></li>'+
		'<li class="item item_color" ><span class="pro-name">'+name+'</span></li>'+
		'<li class="item item_color" >'+
		'<span>'+status+'</span></li>'+
		'<li class="item item_color" ><span>progress</span></li>'+
	  	'<li class="item item_color" ><span class="log_toggle">log</span></li>'+
	  	'<li class="item item_color" ><span class="action run">run</span><span class="action stop">stop</span><span class="action del">del</span></li>'+
	  	'<li class="item item_color" ><span class="results " >results</span></li>'+
	  	'</ul>'+
	  	'<div class="log" ></div>'+
  		'</div>';
  		runningArea.append(appendPart);
	}
	function addNodeTodo(web,name,status){
		var appendPart = '<div class="item-box">'+
		'<ul class="ul_item">'+
		'<li class="item item_color" ><span>'+web+'</span></li>'+
		'<li class="item item_color" ><span class="pro-name">'+name+'</span></li>'+
		'<li class="item item_color" >'+
		'<span>'+status+'</span></li>'+
		'<li class="item item_color" ><span>progress</span></li>'+
	  	'<li class="item item_color" ><span class="log_toggle">log</span></li>'+
	  	'<li class="item item_color" ><span class="action run">run</span><span class="action stop">stop</span><span class="action del">del</span></li>'+
	  	'<li class="item item_color" ><span class="results " >results</span></li>'+
	  	'</ul>'+
	  	'<div class="log" ></div>'+
  		'</div>';
  		todoArea.append(appendPart);
	}
	function stop(name){
		var url1 = 'http://localhost:5000/'+name+'/run';
		$.ajax({
			url:'http://localhost:5000/update',
			type:'POST',
			data:{'pk':name,'name':'status','value':'TODO'},
			success:function(item){
				var data = JSON.parse(item);
				console.log(data);
				get_info();
			}
		})
	}
	function getResults(name,type){
		var url = "http://localhost:3000/results?project="+name+"&type="+type;
        window.localStorage.setItem("project_name",name);
        window.localStorage.setItem("project_type",type);
        setTimeout(function(){
            location.href = url;
        },500);
	}
	function del(name){
		var pUrl = "http://localhost:5000/spiderweb/delete";
		
		$.ajax({
			url:pUrl,
			type:"POST",
			data:{"project":name},
			success:function(e){
				data = JSON.parse(e);
				console.log(data.code);
				window.localStorage.removeItem(name);
				// return data;
				// console.log(temp);
				// console.log(e);
			},
			error:function(e){
				console.log(e);
			}
		})

	}
	function localStore(project,website){
		window.localStorage.setItem(project, website);
	}
})
