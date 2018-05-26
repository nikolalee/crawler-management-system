$(document).ready(function(){
	var $log = $('.log_toggle');
	// console.log($log);
	// var logArea = $('#log_area');
	var newProject = $('#create');
	var runningArea = $('#items table');
	var todoArea = $('#todoArea table');
	var menuList = $('#menu');
	//bind log event
	get_info();
	//menu animation
	$('#menu').add('#create').mouseout(function(){
		menuList.css('height','0');
	})
	$('#create').add('#menu').mouseover(function(){
		menuList.css('height','162px');
		
	})
	// $('#running-project').add('#recent-project').on('click','table > tr > td > span.log_toggle',function(event){
	// 	var target = $(event.target);
	// 	var logArea = target.parent().parent().parent().children('.log');
	// 	if (logArea.css('display') == 'none'){
	// 		logArea.css('display','block');
	// 		// console.log('hi');
	// 	}else{
	// 		logArea.css('display','none');
	// 		// console.log('kk');
	// 	}
	// })
	//bind delete event
	$('#recent-project').on('click','table > tr > td > span.del',function(event){
		var target = $(event.target);
		var oDiv = target.parent().parent();
		var name = oDiv.find('.pro-name').eq(0).html();
		sure_to_delete(name);
	})
	//bind delete event
	$('#running-project').on('click','table > tr > td > span.del',function(event){
		alert("请先暂停该爬虫.");
	})
	//bind run event
	$('#running-project').add('#recent-project').on('click','table > tr > td > span.run',function(event){
		var target = $(event.target);
		var oDiv = target.parent().parent();
		var name = oDiv.find('.pro-name').eq(0).html();
		console.log(name);
		run(name);
		get_info();
	})
	//bind stop event
	$('#running-project').add('#recent-project').on('click','table > tr > td > span.stop',function(event){
		var target = $(event.target);
		var oDiv = target.parent().parent();
		var name = oDiv.find('.pro-name').eq(0).html();
		console.log(name);
		stop(name);
		get_info();
	})
	//bind results event
	$('#running-project').add('#recent-project').on('click','table > tr > td > span.results',function(event){
		var target = $(event.target);
		var oDiv = target.parent().parent();
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
				// console.log(data.length);
				if(data){
					runningArea.empty();
					todoArea.empty();
					for(var i = 0;i < data.length;i++){
						// console.log("2");
						// console.log(data.length);
						// console.log(data[i]['status']);
						var web="";
						if(data[i]['status'] == "RUNNING"){
							web = window.localStorage.getItem(data[i]['name']);
							addNodeRun(web,data[i]['name'],data[i]['status']);
						}else{
							web = window.localStorage.getItem(data[i]['name']);
							// console.log("web:"+web);
							addNodeTodo(web,data[i]['name'],data[i]['status']);
						}
					}
				}
			}
		})
		// return item;
	}
	function addNodeRun(web,name,status){
		var appendPart =
		'<tr class="tr-item">'+
            '<td >'+web+'</td>'+
            '<td ><span class="pro-name">'+name+'</span></td>'+
            '<td ><span class="run-color">'+status+'</span></td>'+
            '<td class="btn"><span class="action run">启动</span><span class="action stop">暂停</span><span class="action del">删除</span></td>'+
            '<td class="btn"><span class="results " >结果</span></td>'+
          '</tr>';
		// var appendPart = '<div class="item-box">'+
		// '<ul class="ul_item">'+
		// '<li class="item item_color" ><span>'+web+'</span></li>'+
		// '<li class="item item_color" ><span class="pro-name">'+name+'</span></li>'+
		// '<li class="item item_color" >'+
		// '<span class="run-color">'+status+'</span></li>'+
	 //  	'<li class="item item_color btn" ><span class="action run">启动</span><span class="action stop">暂停</span><span class="action del">删除</span></li>'+
	 //  	'<li class="item item_color btn" ><span class="results " >结果</span></li>'+
	 //  	'</ul>'+
  // 		'</div>';
  		runningArea.append(appendPart);
	}
	function addNodeTodo(web,name,status){
		var appendPart =
		'<tr class="tr-item">'+
            '<td >'+web+'</td>'+
            '<td ><span class="pro-name">'+name+'</span></td>'+
            '<td ><span class="todo-color">'+status+'</span></td>'+
            '<td class="btn"><span class="action run">启动</span><span class="action stop">暂停</span><span class="action del">删除</span></td>'+
            '<td class="btn"><span class="results " >结果</span></td>'+
          '</tr>';
		// var appendPart = '<div class="item-box">'+
		// '<ul class="ul_item">'+
		// '<li class="item item_color" ><span>'+web+'</span></li>'+
		// '<li class="item item_color" ><span class="pro-name">'+name+'</span></li>'+
		// '<li class="item item_color" >'+
		// '<span class="todo-color">'+status+'</span></li>'+
	 //  	'<li class="item item_color btn" ><span class="action run">启动</span><span class="action stop">暂停</span><span class="action del">删除</span></li>'+
	 //  	'<li class="item item_color btn" ><span class="results " >结果</span></li>'+
	 //  	'</ul>'+
  // 		'</div>';
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
				// console.log(data);
				get_info();
			}
		})
	}
	//  delete data in mysql
	function delSql(name,type){
		$.ajax({
			url:'/delete',
			type:'GET',
			data:{'name':name,'type':type},
			success:function(e){
				console.log(e);
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
								get_info();
							},
							error:function(e){
								alert("crawler start failed:\n"+e);
							}
						})
					}
				},500);
			}
		})
	}
	function sure_to_delete(name){
		$('#shadow').removeClass('hide');
		$('#yes').on('click',function(){
			$('#shadow').addClass('hide');
			del(name);
			get_info();
		})
		$('#no').on('click',function(){
			$('#shadow').addClass('hide');
		})
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
				var type = window.localStorage.getItem(name);
				delSql(name,type);
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
