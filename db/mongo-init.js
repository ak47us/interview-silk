
// Access MongoDB:
var conn = new Mongo();
var db   = conn.getDB("host_scans");

// Set up service account for Python:
db.createUser({
    user: "python-sa",
    pwd:  "password",
    roles: [
        { role: "readWrite", db: "host_scans" }
    ]
});

// Set up service account for Grafana:
db.createUser({
    user: "grafana-sa",
    pwd:  "password",
    roles: [
        { role: "read", db: "host_scans" }
    ]
});

// Set up service account for Mongoku:
db.createUser({
    user: "mongoku-sa",
    pwd:  "password",
    roles: [
        { role: "read", db: "host_scans" }
    ]
});

// Set up the document collection:
var normalized = db.createCollection("normalized"); // Data that has been normalized into a unified format.

// Not working:
// await normalized.insertOne( { "hostname": "test" } );  // Does not seem to work, but if we do not put this, then the index does not work and the collection gets corrupted.
// normalized.createIndex({ "hostname": 1 });            // Speed up hostname searches.
// normalized.createIndex("hostname")

//const { MongoClient } = require('mongodb');
//
//async function run() {
//  const uri = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"; // Replace with your MongoDB connection string
//  const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true });
//
//  try {
//    await client.connect();
//
//    const db = client.db("myDatabase"); // Replace with your database name
//    const normalized = db.collection("normalized");
//
//    // Insert a document
//    await normalized.insertOne({ "hostname": "test" });
//
//    // Create an index on the hostname field
//    await normalized.createIndex({ "hostname": 1 });
//
//    console.log("Document inserted and index created successfully");
//
//  } finally {
//    await client.close();
//  }
//}
//
//run().catch(console.dir);


console.log("mongo-init.js has initializing up the database.");