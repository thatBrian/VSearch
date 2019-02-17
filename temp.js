var spawn = require("child_process").spawn;
    var processPYTHON = spawn('python3', ['-u', './scraper.py']);
    processPYTHON.stdout.on('data', (data) => {
        // console.log(data.toString());
        // res.send(JSON.stringify(data));
        console.log(data);
        res.send(JSON.parse(data));
    });