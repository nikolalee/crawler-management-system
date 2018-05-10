var express = require('express');
var router = express.Router();
var mysql  = require('mysql'); 
/* GET result page. */
router.get('/', function(req, res, next) {
	project = req.query.project;
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
	var sql = 'SELECT * FROM douban';
	connection.query(sql,function (err, result) {
        if(err){
          console.log('[SELECT ERROR] - ',err.message);
          return;
        }
 		res.render('results', { title: 'Results',data:result});
	});
  
});

module.exports = router;
