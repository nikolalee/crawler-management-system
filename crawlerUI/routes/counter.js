var express = require('express');
var router = express.Router();
var mysql  = require('mysql'); 
var news_counter = {};
var comment_counter = {};
var forum_counter = {};
/* GET detail page. */
router.get('/', function(req, res, next) {
	
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
	var sql1 = "SELECT crawl_time FROM news";
	connection.query(sql1,function (err, result) {
    if(err){
      console.log('[SELECT ERROR] - ',err.message);
      return;
    }
    	news_counter = {hour:0,day:0,month:0,all:0};
		for(var i = 0;i < result.length;i++){
			var date = result[i]['crawl_time'].replace(/\-/g, "/");
			var startTime = new Date(date).getTime();
			var endTime = new Date().getTime();
			var minus = parseInt(endTime - startTime);
			if(minus <= 60*60*1000){
				news_counter.hour = news_counter.hour + 1;
				news_counter.day = news_counter.day + 1;
				news_counter.month = news_counter.month + 1;
				news_counter.all = news_counter.all + 1;
			}else if(minus <= 60*60*24*1000){
				news_counter.day = news_counter.day + 1;
				news_counter.month = news_counter.month + 1;
				news_counter.all = news_counter.all + 1;
			}else if(minus <= 60*60*24*30*1000){
				news_counter.month = news_counter.month + 1;
				news_counter.all = news_counter.all + 1;
			}else{
				news_counter.all = news_counter.all + 1;
				// console.log(news_counter);
			}
		}
	});
	var sql2 = "SELECT crawl_time FROM comments";
	connection.query(sql2,function (err, result) {
    if(err){
      console.log('[SELECT ERROR] - ',err.message);
      return;
    }
    comment_counter = {hour:0,day:0,month:0,all:0};
		for(var i = 0;i < result.length;i++){
			var date = result[i]['crawl_time'].replace(/\-/g, "/");
			var startTime = new Date(date).getTime();
			var endTime = new Date().getTime();
			var minus = parseInt(endTime - startTime);
			// console.log(minus);
			if(minus <= 60*60*1000){
				comment_counter.hour = comment_counter.hour + 1;
				comment_counter.day = comment_counter.day + 1;
				comment_counter.month = comment_counter.month + 1;
				comment_counter.all = comment_counter.all + 1;
			}else if(minus <= 60*60*24*1000){
				comment_counter.day = comment_counter.day + 1;
				comment_counter.month = comment_counter.month + 1;
				comment_counter.all = comment_counter.all + 1;
			}else if(minus <= 60*60*24*30*1000){
				comment_counter.month = comment_counter.month + 1;
				comment_counter.all = comment_counter.all + 1;
			}else{
				comment_counter.all++;
			}
		}
	});
	var sql3 = "SELECT crawl_time FROM forum";
	connection.query(sql3,function (err, result) {
    if(err){
      console.log('[SELECT ERROR] - ',err.message);
      return;
    }
    forum_counter = {hour:0,day:0,month:0,all:0};
		for(var i = 0;i < result.length;i++){
			var date = result[i]['crawl_time'].replace(/\-/g, "/");
			var startTime = new Date(date).getTime();
			var endTime = new Date().getTime();
			var minus = parseInt(endTime - startTime);
			if(minus <= 60*60*1000){
				// console.log("hour");
				forum_counter.hour = forum_counter.hour + 1;
				forum_counter.day = forum_counter.day + 1;
				forum_counter.month = forum_counter.month + 1;
				forum_counter.all = forum_counter.all + 1;
			}else if(minus <= 60*60*24*1000){
				// console.log("day");
				forum_counter.day = forum_counter.day + 1;
				forum_counter.month = forum_counter.month + 1;
				forum_counter.all = forum_counter.all + 1;
			}else if(minus <= 60*60*24*30*1000){
				// console.log("month");
				forum_counter.month = forum_counter.month + 1;
				forum_counter.all = forum_counter.all + 1;
			}else{
				// console.log("all");
				// console.log(forum_counter);
				forum_counter.all = forum_counter.all + 1;
			}
		}
	});
	var data = {};
	data.news = news_counter;
	data.comment = comment_counter;
	data.forum = forum_counter;
	res.json(data);
});

module.exports = router;
