var express = require('express');
var router = express.Router();
var mysql  = require('mysql'); 
/* GET result page. */
router.get('/', function(req, res, next) {
	project = req.query.project;
	res.render('result_code', { title: 'Result code'});
});

module.exports = router;
