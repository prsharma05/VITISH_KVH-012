var express = require('express');
var app = express();

app.use(express.static('public'));

app.get('/', function (req, res) {
   res.send('Hello World');
})

var server = app.listen(5050, function () {
   var host = server.address().address
   var port = server.address().port

   console.log("Example app listening at http://localhost:%s", port)
})