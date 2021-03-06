var express = require('express');
var router = express.Router();
var mysql  = require('mysql'); 

/* GET detail page. */
router.get('/', function(req, res, next) {
	var type = req.query.type;
  	var project = req.query.project_name;
  	var connection = mysql.createConnection({     
	  host     : 'localhost',       
	  user     : 'repository',              
	  password : 'repository',       
	  port: '3306',                   
	  database: 'repository', 
	}); 
	connection.connect(function (err) {
	    if(err){
	        console.log('[query] - :'+err);
	    }
    	console.log('[connection connect]  succeed!');
	});
  	if(type == "news"){
  		var title = req.query.title;
  		var sql = "SELECT * FROM news where project_name='"+project+"' and news_title='"+title+"'";
  		console.log(sql);
  		connection.query(sql,function (err, result) {
	        if(err){
	          console.log('[SELECT ERROR] - ',err.message);
	          return;
	        }
	        console.log(result);
	 		res.render('detail_news', { title: title,data:result});
		});
  	}else if(type == "comment"){
  		var time = req.query.time;
  		var author = req.query.author;
  		var sql = "SELECT * FROM comments where project_name='"+project+"' and publish_time='"+time+"' and comment_author='"+author+"'";
  		connection.query(sql,function (err, result) {
	        if(err){
	          console.log('[SELECT ERROR] - ',err.message);
	          return;
	        }
        	if(result[0].response == ""){
					var sql2 = "select * from comment_reply where author='"+author+"' and content='"+result[0].content+"'";
					connection.query(sql2,function (err2, data) {
			        if(err2){
			          console.log('[SELECT ERROR] - ',err.message);
			          return;
			        }
			        // console.log(len(data));
			       if(data.length>0){
							res.render('detail_comment2', { title: author,data:data,result:result});
			       }else{
			      
			        	result[0].response = "null";
			        	
			       		res.render('detail_comment1', { title: author,data:result});
			       }
				});
	        	}
	        	else{
		 			res.render('detail_comment1', { title: author,data:result});
	        }
	        
		});
  	}else if(type == "forum"){
  		var title = req.query.title;
  		var sql = "SELECT * FROM forum where project_name='"+project+"' and title='"+title+"'";
  		connection.query(sql,function (err, result) {
	        if(err){
	          console.log('[SELECT ERROR] - ',err.message);
	          return;
	        }
	        if(result.length > 0){
	        	var sql2 = "SELECT * FROM sub_forum where project_name='"+project+"' and title='"+title+"'";
	        	connection.query(sql2,function (err2, data) {
			        if(err2){
			          console.log('[SELECT ERROR] - ',err.message);
			          return;
			        }
			        console.log(data);
			        console.log(result);
			        console.log(data.length);
			       if(data.length>0){
							res.render('detail_forum2', { title: result[0].tie_user,data:data,result:result});
			       }else{
			       		res.render('detail_forum1', { title: result[0].tie_user,result:result});
			       }
				});
	        }else{
	        	return;
	        }
		});
  	}
  	
});

module.exports = router;
