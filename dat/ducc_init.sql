-- state of the ducc.
-- health points, stress level, etc
CREATE TABLE state (
	id           INTEGER NOT NULL,
	last_fed     INTEGER NOT NULL,
	health       INTEGER NOT NULL,
	stress       INTEGER NOT NULL,
	PRIMARY KEY (id)
);

-- events.
-- e.g. "watered by kiedtl on DATE"
CREATE TABLE events (
	id      INTEGER NOT NULL,
	ev_type TEXT    NOT NULL,
	date    INTEGER NOT NULL,
	ev_by   TEXT,
	PRIMARY KEY (id)
);

-- create the initial values
INSERT INTO state VALUES (
	0,     -- id
	0,     -- last_fed
	100,   -- health
	0      -- stress
);
