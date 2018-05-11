const express = require('express');
const app = express();
const multer = require('multer');
const bodyParser = require('body-parser');
const upload = multer();
const port = 8000;
const exec = require('child_process').exec

//initialize mongodb connect
const MongoClient = require('mongodb').MongoClient
const url ="mongodb://localhost:27017/"


app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:true}));
app.get('/', (req, res) => res.sendFile(__dirname + '/interfaceWeb/index.html'));
//app.get('/dispo',(req,res) => res.sendFile(__dirname+'/public/dispo.html'));
//app.use(express.static('public'));

app.post('/sp', upload.array(),(req,res,next) => {
  console.log(req.body.path);
  var arg1 = req.body.path.toString()
  exec('python H:/jupyterDirectory/Aviz/aviz_v_2_0/extractData/extractData.py '+arg1,function(error,stdout,stderr){
    if(stdout.length >1){
        console.log('you offer args:',stdout);
    } else {
        console.log(stdout);
        console.log('you don\'t offer args');
    }
    if(error) {
        console.info('stderr : '+stderr);
    }
  })
  res.json({response:req.body})
});

app.post('/query',upload.array(),(req,res,next)=>{
  console.log();
  var query = req.body
  MongoClient.connect(url, function(err,db){
    if (err) throw err;
    var dbo = db.db("canton")
    dbo.collection("metaData").find(query).toArray(function(err,result){
      if (err) throw err;
      console.log(result);
      res.json({response:result});
      db.close();
    })
  })
})


app.listen(port, () => {});

console.log(`Server started on port ${port}...`);
