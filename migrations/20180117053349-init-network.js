'use strict';

var dbm;
var type;
var seed;
var fs = require('fs')

/**
  * We receive the dbmigrate dependency from dbmigrate initially.
  * This enables us to not have to rely on NODE_PATH.
  */
exports.setup = function(options, seedLink) {
  dbm = options.dbmigrate;
  type = dbm.dataType;
  seed = seedLink;
};

exports.up = function(db) {
    return db.createCollection('mhinodes',{
            name: 'string',
            group: 'int',
            order: 'int'
        }).then(() => db.createCollection('mhinlinks', {
            source: 'int',
            target: 'int',
            year: 'int'
        })).then(() => db.insert('mhinodes', JSON.parse(fs.readFileSync('./data/nodes.json')))
        ).then(() => db.insert('mhinlinks', JSON.parse(fs.readFileSync('./data/links.json'))));
};

exports.down = function(db) {
    return db.dropCollection('mhinodes').then(() => db.dropCollection('mhinlinks'));
};

exports._meta = {
  "version": 1
};
