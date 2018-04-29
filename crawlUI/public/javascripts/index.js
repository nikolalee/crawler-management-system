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
		console.log(name);
		getResults(name);
	})
	//bind create event
	newProject.click(function(){
		var web = $('#web').val();
		var name = $('#name').val();
		var oriUrl = $('#url').val();
		// console.log(name);
		// console.log(oriUrl);
		if(name ===""||oriUrl===""){
			alert('empty not allowed.');
			return;
		}
		var url1 = "http://localhost:5000/debug/"+name+"/get_script_save";
		$.ajax({
			url:url1,
			type:"GET",
			// async:false, 
			// dataType:"jsonp",
			// jsonp:"callback",
			// jsonpCallback:"successCallback",
			data:{'start-url':oriUrl,'web-type':web},
			success:function(e){
				console.log(e);
				localStore(name,web);
				run(name);
				get_info();
			},
			error:function(e){
				console.log("fail:"+e);
			}
		})
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
						var web;
						if(data[i]['status'] == "RUNNING"){
							web = window.localStorage.getItem(data[i]['name']);
							addNodeRun(web,data[i]['name'],data[i]['status']);
						}else{
							web = window.localStorage.getItem(data[i]['name']);
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
								get_info();
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
	function getResults(name){
		var url = "http://localhost:3000/results?project="+name;
		location.href = url;
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