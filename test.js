// var PythonShell = require('python-shell');
// let options = {
//     args:[

//     ]
// }
// PythonShell.run('scraper.py', options, (err,data)=>{
//     if(err){
//         console.log("ERROR");
//     }
//     console.log(data);
// })
var spawn = require("child_process").spawn;
var processPYTHON = spawn('python3', ['-u', './scraper.py']);
processPYTHON.stdout.on('data', (data) => {
    console.log(data.toString());
});
processPYTHON.stderr.on('data', function (data) {
    console.log('stderr: ' + data);
});