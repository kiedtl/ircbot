-- state of the ducc.
-- health points, stress level, etc
CREATE TABLE state (
	id           INTEGER NOT NULL,
	date         INTEGER NOT NULL,
	last_fed     INTEGER NOT NULL,
	last_watered INTEGER NOT NULL,
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
