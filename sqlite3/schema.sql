CREATE TABLE IF NOT EXISTS messages (
	id integer PRIMARY KEY,
	content text NOT NULL,
	noteDate date,
	course text
);