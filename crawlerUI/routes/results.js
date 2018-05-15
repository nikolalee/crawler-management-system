var express = require('express');
var router = express.Router();
var mysql  = require('mysql'); 
/* GET result page. */
router.get('/', function(req, res, next) {
	project = req.query.project;
	type = req.query.type;
	res.render('result_overview', { title: 'Result overview',name:project,type:type});
	// var connection = mysql.createConnection({     
	//   host     : 'localhost',       
	//   user     : 'repository',              
	//   password : 'repository',       
	//   port: '3306',                   
	//   database: 'repository', 
	// }); 
	// connection.connect(function (err) {
	//     if(err){
	//         console.log('[query] - :'+err);
	//     }
 //    	console.log('[connection connect]  succeed!');
	// });
	// if(type == "news"){
	// 	var sql = 'SELECT * FROM news';
	// }else if(type == "comment"){
	// 	var sql = 'SELECT * FROM comments2';
	// }else if(type == "forum"){
	// 	var sql = 'SELECT * FROM forum';
	// }else{
	// 	return;
	// }
	
	// connection.query(sql,function (err, result) {
 //        if(err){
 //          console.log('[SELECT ERROR] - ',err.message);
 //          return;
 //        }
 // 		res.render('result_overview', { title: 'Results',data:result});
	// });
  
});

module.exports = router;
