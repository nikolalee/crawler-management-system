$(document).ready(function(){
	var data = {};
	var btn = $('#start');
	var menuList = $('#menu');
	$('#response-type').change(function(){
		console.log(123);
		if($('#response-type').val() == 'after'){
			$('#response-box').css('display','block');
		}else{
			$('#response-box').css('display','none');
		}
	})
	//menu animation
	$('#menu').add('#create').mouseout(function(){
		menuList.css('height','0');
	})
	$('#create').add('#menu').mouseover(function(){
		menuList.css('height','162px');
		
	})
	// btn animation
	$('.btn-box').mouseover(function(){
		$('#start').css('top',0);
	})
	$('.btn-box').mouseout(function(){
		$('#start').css('top','-50px');
	})
	
	btn.on('click',function(){
		get_data(data);
		var flag;
		flag = isEmpty();
		if(flag){
			alert('there is empty box.');
			return;
		}
		// data['content_css'] = $('#content-css').val();
		data['crawler_name'] = $('#crawler-name').val();
		var url1 = 'http://localhost:5000/debug/'+data['crawler_name']+'/get_script_save';
		console.log(data);
		$.ajax({
			url:url1,
			type:"POST",
			data:{'web-type':'comment','start_url':data['crawler_url'],'nextpage_tag':data['nextpage_css'],'nextpage_name':data['nextpage_name'],
				'comment_box_css':data['comment_box_css'],'comment_author_css':data['comment_author_css'],
				'time_css':data['time_css'],'content_css':data['content_css'],'has_re_content_css':data['has_re_content_css'],
				'vote_css':data['vote_css'],'response_type':data['response_type'],'response_css':data['response_css'],
				'response_box_css':data['response_box_css'],'res_user_css':data['res_user_css'],'res_time_css':data['res_time_css'],
				'res_content_css':data['res_content_css'],'isIframe':data['isIframe'],'iframe_id':data['iframe_id'],'more_type':data['more_type'],
				'deep_num':data['crawler_depth'],'step':data['step']
			},
			success:function(e){
				console.log(e);
				run(data['crawler_name']);
			},
			error:function(e){
				console.log(e);
			}
		})
	})

	function get_data(data){
		 data['crawler_name'] = $('#crawler-name').val();
		 console.log(data['crawler_name']);
		 data['crawler_url'] = $('#crawler-url').val();
		 data['nextpage_css'] = $('#nextpage-css').val();
		 data['nextpage_name'] = $('#nextpage-name').val();
		 data['crawler_depth'] = $('#crawler-depth').val();
		 data['more_type'] = $('#more-type').val();
		 data['isIframe'] = $('#isIframe').val();
		 data['step'] = $('#step').val();
		 
		 data['comment_box_css'] = $('#comment-box-css').val();
		 data['comment_author_css'] = $('#comment-author-css').val();
		 data['time_css'] = $('#time-css').val();
		 data['content_css'] = $('#content-css').val();
		 console.log(data['content_css']);
		 data['has_re_content_css'] = $('#has-re-content-css').val();
		 data['vote_css'] = $('#vote-css').val();
		 data['response_type'] = $('#response-type').val();
		 
		if(data['isIframe'] == "no"){
			data['iframe_id'] = "#";
		}else{
			data['iframe_id'] = $('#iframe-id').val();
		}
		if(data['response_type'] == 'before'){
			data['response_css'] = $('#response-css').val();
			data['response_box_css'] = $('#response-box-css').val();
		 	data['res_user_css'] = "#";
		 	data['res_time_css'] = "#";
		 	data['res_content_css'] = "#";
		}else{
			data['response_css'] = "#";
			data['response_box_css'] = $('#response-box-css').val();
		 	data['res_user_css'] = $('#res-user-css').val();
		 	data['res_time_css'] = $('#res-time-css').val();
		 	data['res_content_css'] = $('#res-content-css').val();
		}
	}

	function isEmpty(){
		if(data['crawler_name']=""||data['crawler_url']==""||data['nextpage_css']==""||data['nextpage_name']==""||data['crawler_depth']==""||
			data['comment_box_css']==""||data['comment_author_css']==""||data['time_css']==""||data['content_css']==""||data['has_re_content_css']==""||
			data['vote_css']==""||data['iframe_id']==""||data['response_css']==""||data['response_box_css']==""||data['res_user_css']==""||data['res_time_css']==""||
			data['res_content_css']==""){
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
								localStore(name,"comment");
								setTimeout(function(){
									window.location = 'http://localhost:3000/index';
								},2000)
							},
							error:function(e){
								alert("crawler construction failed:\n"+e);
							}
						})
					}
				},500);
			}
		})
	}
	function localStore(project,type){
		window.localStorage.setItem(project, type);
	}

})