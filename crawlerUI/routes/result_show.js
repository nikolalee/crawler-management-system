var express = require('express');
var router = express.Router();
var mysql  = require('mysql'); 
/* GET result page. */
router.get('/', function(req, res, next) {
	project = req.query.project_name;
	type = req.query.type;
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
		var sql = 'SELECT * FROM news where project_name="'+project+'"';
	}else if(type == "comment"){
		var sql = 'SELECT * FROM comments where project_name="'+project+'"';
	}else if(type == "forum"){
		var sql = 'SELECT * FROM forum where project_name="'+project+'"';
	}else{
		return;
	}
	
	connection.query(sql,function (err, result) {
        if(err){
          console.log('[SELECT ERROR] - ',err.message);
          return;
        }
        if(type == "news"){
            var head = ['新闻标题','新闻地址','发布时间'];
 			res.render('result_show', { title: 'Result show',data:result,head:head});
        }
        else if(type == "comment"){
            var head = ['评论作者','评论内容','评论时间'];
        	res.render('result_show_comment', { title: 'Result show',data:result,head:head});
        }else{
            var head = ['帖子标题','帖子地址','发布时间'];
        	res.render('result_show_forum', { title: 'Result show',data:result,head:head});
            
        }
	});
	// res.render('result_show', { title: 'Result show',name:project,type:type});
});

module.exports = router;
