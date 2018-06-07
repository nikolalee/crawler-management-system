var express = require('express');
var router = express.Router();
var mysql  = require('mysql'); 
/* delete data in mysql. */
router.get('/', function(req, res, next) {
	project = req.query.name;
	type = req.query.type;
	console.log('type');
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
	console.log(112);
	if(type == "news"){
		var sql = 'delete FROM news where project_name="'+project+'"';
	}else if(type == "comment"){
		var sql = 'SELECT * FROM comments where project_name="'+project+'"';
		var sql2 =  'delete FROM news where project_name="'+project+'"';
	}else if(type == "forum"){
		var sql = 'delete FROM forum where project_name="'+project+'"';
		var sql2 = 'delete FROM sub_forum where project_name="'+project+'"';
	}else{
		res.send('Type is not right.');
		return;
	}
	
	connection.query(sql,function (err, result) {
        if(err){
          console.log('[SELECT ERROR] - ',err.message);
          return;
        }
        if(type == "news"){
            res.json({status:'ok'});
        }
        else if(type == "comment"){
        	var sql3;
        	for(var i = 0;i < result.length;i++){
        		sql3 = 'delete form comment_reply where author ="'+result[i].comment_author+'"'
        		connection.query(sql3,function(err,result){
        			if(err){
			          console.log('[SELECT ERROR] - ',err.message);
			          return;
      				 }
        		});
        	}
        	connection.query(sql2,function(err,result){
    			if(err){
		          console.log('[SELECT ERROR] - ',err.message);
		          return;
  				 }
  				 res.json({status:'ok'});
        	});
        }else{
        	console.log(221);
        	connection.query(sql2,function (err, result) {
        		if(err){
		          console.log('[SELECT ERROR] - ',err.message);
		          return;
  				 }
  				 res.json({status:'ok'});
        	})
        }
	});
});

module.exports = router;
