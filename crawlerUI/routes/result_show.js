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
		var sql = 'SELECT * FROM comments2 where project_name="'+project+'"';
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
 			res.render('result_show', { title: 'Result show',data:result});
        }
        else if(type == "comment"){
        	res.render('result_show_comment', { title: 'Result show',data:result});
        }else{
        	res.render('result_show_forum', { title: 'Result show',data:result});
        }
	});
	// res.render('result_show', { title: 'Result show',name:project,type:type});
});

module.exports = router;
