var express = require('express');
var router = express.Router();
var mysql  = require('mysql'); 
/* GET result num. */
router.get('/', function(req, res, next) {
	project = req.query.project;
	type = req.query.type;
	console.log(112);
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
        
        res.json({len:result.length})
	});
});

module.exports = router;
