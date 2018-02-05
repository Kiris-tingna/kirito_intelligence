'use strict';
var fs = require('fs');

function hello(req, res, next) {
    res.send('hello ' + req.params.name);
    return next();
}
function gethin(req, res, next) {
    // data loadded
    var nodes = JSON.parse(fs.readFileSync('./data/nodes.json'));
    var links = JSON.parse(fs.readFileSync('./data/links.json'));
    var filtered = []
    for (var link in links) {
        if (links[link].year == 2017){
            filtered.push(links[link])
        }
    }
    res.send({"nodes":nodes, "links": filtered});
    return next();
}
function posthin(req, res, next) {
    var nodes = JSON.parse(fs.readFileSync('./data/nodes.json'));
    var links = JSON.parse(fs.readFileSync('./data/links.json'));

    var s = new Date(req.body.filter.syear).getFullYear()
    var e = new Date(req.body.filter.eyear).getFullYear()

    if  (s <= e){
        var filtered = [];
        for (var link in links) {
            if (links[link].year <= e && links[link].year >= s){
                filtered.push(links[link])
            }
        }
        res.send({"nodes":nodes, "links": filtered});
        return next();
    }else{
        res.send({});
        return next();
    }  
}
function getheatmap(req, res, next){
    var animate = JSON.parse(fs.readFileSync('./data/animate_heatmap.json'));
    animate.height = 1000
    animate.value = animate.value.slice(0, 1000 * animate.width)
    res.send(animate);
    return next();
}
function postheatmap(req, res, next){
    var animate = JSON.parse(fs.readFileSync('./data/animate_heatmap.json'));
    var period = req.body.filter.period
    if (period == 1){
        animate.height = 1000
        animate.value = animate.value.slice(0, 1000 * animate.width)
    }else if (period == 2){
        animate.height = 1000
        animate.value = animate.value.slice(1000 * animate.width, 2000 * animate.width)
    }else if (period == 3){
        animate.height = 1000
        animate.value = animate.value.slice(2000 * animate.width, 3000 * animate.width)
    }else {
        var len = animate.value.length
        animate.height = animate.height - 3000
        animate.value = animate.value.slice(3000 * animate.width, len)
    }
    
    res.send(animate);
    return next();
}
function postcluster(req, res, next) {
    var clusters = JSON.parse(fs.readFileSync('./data/clusters.json'));
    var id = req.body.filter.cluster
    res.send(clusters[id]);
    return next();
}

function getdyn(req, res, next){
    var impacts = JSON.parse(fs.readFileSync('./data/dynamicimpact.json'));
    res.send(impacts[0].value);
    return next();
}

function postdyn(req, res, next){
    var impacts = JSON.parse(fs.readFileSync('./data/dynamicimpact.json'));
    var fname = req.body.filter.fname
    var result = []
    for (var film in impacts) {
        if (impacts[film].name == fname){
            result = impacts[film].value
            break;
        }
    }
    res.send(result);
    return next();
}

function getlist(req, res, next) {
    var animateList = JSON.parse(fs.readFileSync('./data/movielist.json'));
    res.send(animateList);
    return next();
}

function getsent(req, res, next){
    var sentiments = JSON.parse(fs.readFileSync('./data/sentiday.json'));
    res.send(sentiments[0].value);
    return next();
}

function postsent(req, res, next) {
    var sentiments = JSON.parse(fs.readFileSync('./data/sentiday.json'));
    var fname = req.body.filter.fname
    var result = []
    for (var film in sentiments) {
        if (sentiments[film].name == fname){
            result = sentiments[film].value
            break;
        }
    }
    res.send(result);
    return next();
}

function getprd(req, res, next){
    var prediction = JSON.parse(fs.readFileSync('./data/compare.json'));
    res.send(prediction);
    return next();
}

// functions
module.exports = {
    hello : hello,
    gethin: gethin,
    posthin: posthin,
    getani: getheatmap,
    postani: postheatmap,
    postcluster: postcluster,
    getdyn: getdyn,
    postdyn: postdyn,
    getlist: getlist,
    getsent: getsent,
    postsent: postsent,
    getprd: getprd,
}