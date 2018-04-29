var express = require('express');
var router = express.Router();

/* GET detail page. */
router.get('/', function(req, res, next) {
  res.render('forum', { title: 'Forum'});
});

module.exports = router;
