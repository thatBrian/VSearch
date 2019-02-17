var express = require('express');
var path = require('path');
var favicon = require('static-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');


var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'hbs');

app.use(favicon());
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded());
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.get("/",(req,res)=>{
    res.render('index');        
})
app.get('/search/:url', function (req, res) {
    console.log(req.params.url);
    if (req.params.url == "") {
        res.send("NO URL");
    } else {
        var spawn = require("child_process").spawn;
        var processPYTHON = spawn('python3', ['-u', './scrapy2.py', "https://en.wikipedia.org/wiki/" + req.params.url]);
        processPYTHON.stdout.on('data', (data) => {

            callThis(data, res);
        });
    }

});
function callThis(data, res) {
    var bob = require('./data.json');
    res.setHeader('Content-Type', 'application/json');
    res.send(bob);
    console.log(data.toString());
}



/// catch 404 and forwarding to error handler
app.use(function (req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

/// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function (err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}

// production error handler
// no stacktraces leaked to user
app.use(function (err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});


module.exports = app;
