USE manhdx;

CREATE TABLE chartdata (
	    id INT AUTO_INCREMENT PRIMARY KEY,
	    timestamp VARCHAR(20),
	    light_level FLOAT,
	    humidity FLOAT,
	    temperature FLOAT
);

CREATE TABLE realtimedata (
	    id INT AUTO_INCREMENT PRIMARY KEY,
	    timestamp VARCHAR(22),
	    light_level FLOAT,
	    humidity FLOAT,
	    temperature FLOAT
);

CREATE TABLE actionhistory (
	    id INT AUTO_INCREMENT PRIMARY KEY,
		timestamp VARCHAR(30),
	    topic VARCHAR(20),
	    command VARCHAR(20),
	    status VARCHAR(20),
);
