-- inventory of each user
CREATE TABLE inv (
        id   INTEGER NOT NULL,
        name TEXT    NOT NULL,
        item TEXT    NOT NULL,
        PRIMARY KEY (id)
);

-- list of users
CREATE TABLE qed (
        id   INTEGER NOT NULL,
        name TEXT    NOT NULL,
        PRIMARY KEY (id)
);
