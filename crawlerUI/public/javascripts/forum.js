$(document).ready(function(){
	var data = {};
	var btn = $('#start');
	btn.on('click',function(){
		get_data(data);
		var flag;
		flag = isEmpty();
		if(flag){
			alert('there is empty box.');
			return;
		}
		console.log(data)
		data['crawler_name'] = $('#crawler-name').val();
		var url1 = 'http://localhost:5000/debug/'+data['crawler_name']+'/get_script_save';
		console.log(data['crawler_name']);
		$.ajax({
			url:url1,
			type:"POST",
			data:{'web-type':'forum','start_url':data['crawler_url'],'main_nextpage_tag':data['main_nextpage_css'],'nextpage_keyword':data['nextpage_keyword'],
				'main_page_num':data['main_page_num'],'nextpage_type':data['nextpage_type'],
				'href_css':data['href_css'],'title_css':data['title_css'],'author_css':data['author_css'],'publish_time_css':data['publish_time_css'],
				'content_css':data['content_css'],'main_step':data['main_step'],'sub_page_num':data['sub_page_num'],
				'sub_nextpage_tag':data['sub_nextpage_tag'],'tie_box_css':data['tie_box_css'],
				'tie_user_css':data['tie_user_css'],'tie_time_css':data['tie_time_css'],'tie_content_css':data['tie_content_css'],'more_type':data['more_type'],
				'sub_step':data['sub_step']
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
		 console.log(data['crawler_url'])
		 data['main_nextpage_css'] = $('#main-nextpage-css').val();
		 data['nextpage_keyword'] = $('#nextpage_keyword').val();
		 data['main_page_num'] = $('#main_page_num').val();
		 if($('#nextpage-type').val()=="单按钮加载"){
		 	data['nextpage_type'] = 'single_btn';
		 }else{
		 	data['nextpage_type'] = 'btn_list';
		 }
		 

		 data['href_css'] = $('#href_css').val();
		 data['title_css'] = $('#title_css').val();
		 data['author_css'] = $('#author_css').val();
		 data['publish_time_css'] = $('#publish_time_css').val();
		 data['content_css'] = $('#content_css').val();
		 data['main_step'] = $('#main_step').val();
		 data['sub_page_num'] = $('#sub_page_num').val();
		 console.log(data['sub_page_num'])

		 data['sub_nextpage_tag'] = $('#sub_nextpage_tag').val();
		 data['tie_box_css'] = $('#tie_box_css').val();
		 data['tie_user_css'] = $('#tie_user_css').val();
	 	 data['tie_time_css'] = $('#tie_time_css').val();
	 	 data['tie_content_css'] = $('#tie_content_css').val();
	 	 data['sub_step'] = $('#sub_step').val();
	}

	function isEmpty(){
		 data['sub_nextpage_name'] = $('#sub_nextpage_name').val();
		if(data['crawler_name']=""||data['crawler_url']==""||data['main_nextpage_css']==""||data['main_nextpage_name']==""||data['main_page_num']==""||
			data['href_css']==""||data['title_css']==""||data['author_css']==""||data['publish_time_css']==""||data['content_css']==""||
			data['main_step']==""||data['sub_page_num']==""||data['sub_nextpage_tag']==""||data['tie_box_css']==""||data['tie_user_css']==""||
			data['tie_time_css']==""||data['tie_content_css']==""||data['sub_step']==""){
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
								localStore(name,"forum");
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