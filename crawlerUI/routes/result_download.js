var express = require('express');
var router = express.Router();
var mysql  = require('mysql'); 
/* GET result page. */
router.get('/', function(req, res, next) {
	res.render('result_download', { title: 'Result download'});
});

module.exports = router;