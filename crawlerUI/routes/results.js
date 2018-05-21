var express = require('express');
var router = express.Router();
var mysql  = require('mysql'); 
/* GET result page. */
router.get('/', function(req, res, next) {
	project = req.query.project;
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
        var head = [];
        if(type == "news"){
            head[0] = '爬取新闻条数 :';
        }
        else if(type == "comment"){
        	head[0] = '爬取评论条数 :';
        }else{
        	head[0] = '爬取帖子数 :';
        }
        head[1] = result.length;
		res.render('result_overview', { title: 'Result overview',name:project,type:type,head:head});

	});
});

module.exports = router;
