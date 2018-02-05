var restify = require('restify');
var CorsMiddleware = require('restify-cors-middleware');
var backendServEntity = 'filesystem'; // db
var serveStatic = require('serve-static');
var finalhandler = require('finalhandler')
var http = require('http')
// config
// var host = '192.168.1.186';
var host = '180.209.64.49';
var staticPort = 3000;
var apiPort = 4000;

// Create server
var server = restify.createServer({
    name: 'KDLIP',
    version: '1.0.0'
});
var static = http.createServer(function onRequest (req, res) {
    serveStatic('static', {'index': ['index_prod.html', 'index.html']})(req, res, finalhandler(req, res))
})

var cors = CorsMiddleware({
    preflightMaxAge: 5,
    origins: ['*'],
    allowedHeaders: ['X-Requested-With', 'Content-Type', 'Authorization'],
    exposedHeaders: ['Authorization']
})

server.pre(cors.preflight)
server.use(cors.actual)
server.use(restify.plugins.queryParser());
server.use(restify.plugins.bodyParser());

// migration datas
// node node_modules/db-migrate/bin/db-migrate up

// rest apis
var apis = backendServEntity == 'filesystem' ? require('./apis_local.js') : require('./apis_mongo.js');
server.get('/hello/:name', apis.hello)
server.get('/api/hin', apis.gethin)
server.post('/api/hin', apis.posthin)
server.get('/api/ani', apis.getani)
server.post('/api/ani', apis.postani)
server.post('/api/cluster', apis.postcluster)
server.get('/api/dyn', apis.getdyn)
server.post('/api/dyn', apis.postdyn)
server.get('/api/list', apis.getlist)
server.get('/api/sent', apis.getsent)
server.post('/api/sent', apis.postsent)
server.get('/api/prd', apis.getprd)


// Listen
server.listen(apiPort, host, function() {
  console.log('%s listening at %s', server.name, server.url);
});
static.listen(staticPort, host, function() {
  console.log('Static server listening at port %s', staticPort);
}) 
