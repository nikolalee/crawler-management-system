var express = require('express');
var router = express.Router();
var mysql  = require('mysql'); 

/* GET detail page. */
router.get('/', function(req, res, next) {
  var project = req.query.project;
  var name = req.query.title;
  console.log(project);
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
	var sql = 'SELECT * FROM douban where user_name = "'+name+'"';
	connection.query(sql,function (err, result) {
        if(err){
          console.log('[SELECT ERROR] - ',err.message);
          return;
        }
        console.log(result[0]);
 		res.render('details', { title: 'Details',data:result});
	});
});

module.exports = router;
