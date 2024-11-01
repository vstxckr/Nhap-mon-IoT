USE manhdx;

CREATE TABLE actionhistory (
	    id INT AUTO_INCREMENT PRIMARY KEY,
	    timestamp VARCHAR(30),
	    topic VARCHAR(20),
	    command VARCHAR(20),
	    status VARCHAR(20)
);
