var request = require('request');
var cheerio = require('cheerio');

var url = 'https://en.wikipedia.org/wiki/Train';

var array = [];

request(url, function (err, resp, body) {
    $ = cheerio.load(body);
    links = $('a');
    $(links).each(function (i, link) {
        var href = $(link).attr('href');
        array.push(href);

    });
    array = array.filter(el => el !== undefined && el.indexOf("/wiki/") !== -1);
    console.log(array);
})
