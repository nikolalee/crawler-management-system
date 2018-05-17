var express = require('express');
var mysql = require('mysql');
var router = express.Router();
var csv = require('express-csv');
var jsonexport = require('jsonexport');

router.get('/',function(req,res,next){
	//解决跨域问题
	res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Content-Type,Content-Length, Authorization, Accept,X-Requested-With");
    res.header("Access-Control-Allow-Methods","PUT,POST,GET,DELETE,OPTIONS");
    res.header("X-Powered-By",' 3.2.1')
    if(req.method=="OPTIONS") res.send(200);/*让options请求快速返回*/

    var project = req.query.project_name;
  	var fileType= req.query.fileType;
  	var webType= req.query.webType;

	var connection = mysql.createConnection({
	  host     : '127.0.0.1',
	  user     : 'repository',
	  password : 'repository',
	  database : 'repository'
	});
	
	var filename = "";
	var sql = "";
	if(webType == "news"){
		sql = 'select * from news where project_name=' +'"'+project+'"';
	}else if(webType == "comment"){
		sql = 'select * from comments2 where project_name=' +'"'+project+'"';
	}else{
		sql = 'select * from forum where project_name=' +'"'+project+'"';
	}
	console.log(sql);
	connection.connect();
	connection.query(sql,function(err, rows, fields) {
    if (err) throw err;
    
	if(fileType === "json"){
		if(req.query.name !== ""){
			filename = filename + req.query.name + ".json";
		}else{
			filename = "download.json";
		}
		res.set({
		    "Content-type":"application/octet-stream",
		    "Content-Disposition":"attachment;filename="+filename
		});
		res.send(rows);
	}
	else if(fileType === "txt"){
		if(req.query.name !== ""){
			filename = filename + req.query.name + ".txt";
		}else{
			filename = "download.txt";
		}
		res.set({
		    "Content-type":"application/octet-stream",
		    "Content-Disposition":"attachment;filename="+filename
		});
		res.send(rows);
	}else if(fileType === "csv"){
		if(req.query.name !== ""){
			filename = filename + req.query.name + ".csv";
		}else{
			filename = "download.csv";
		}
		res.set({
		    "Content-type":"application/octet-stream",
		    "Content-Disposition":"attachment;filename="+filename
		});
		jsonexport(rows,function(err, csv){
		    if(err) return console.log(err);
		    res.send(csv);
		});
	}
    
    //res.send(rows);
  	
	});
	connection.end();
});
module.exports = router;