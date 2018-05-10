var express = require('express');
var router = express.Router();

/* GET detail page. */
router.get('/', function(req, res, next) {
  res.render('comment', { title: 'Comment'});
});

module.exports = router;
