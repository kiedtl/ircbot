-- karma for each user
CREATE TABLE karma (
        id       INTEGER NOT NULL,
        username TEXT    NOT NULL,
        amount   INTEGER NOT NULL,
        PRIMARY KEY (id)
);
