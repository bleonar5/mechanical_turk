var fs = require('fs');
var file = "test.db";
var exists = fs.existsSync(file);

if(!exists) {
	fs.openSync(file,"w");
}

var sqlite3 = require('sqlite3').verbose();
var db = new sqlite3.Database(file);

db.serialize(function() {
	var circleData = [{"adj":"miniscule"},{"adj":"small","value":3},{"adj":"big","value":6},{"adj":"huge","value":8},{"adj":"gargantuan","value":10}];

	db.run("Create table Adjectives (adj primary key, val integer, attr text)");

	var stmt = db.prepare("INSERT INTO Adjectives VALUES (?,?,?)");

	for(i = 0;i<circleData.length;i++){
		try{
			stmt.run(circleData[i].adj,circleData[i].value,"smaller-bigger");
		}
		catch(err){
			console.log('whoops');
		}
	}

	stmt.finalize();

	db.each("SELECT * FROM Adjectives", function(err,row) {
		console.log(row);
	});
});

db.close();