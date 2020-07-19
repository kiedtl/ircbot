CREATE TABLE beg (
        id INTEGER NOT NULL,
        word TEXT,
        PRIMARY KEY (id)
);

CREATE TABLE noun (
        id INTEGER NOT NULL,
        word TEXT,
        PRIMARY KEY (id)
);

CREATE TABLE prew (
        id INTEGER NOT NULL,
        pre TEXT,
        pro TEXT,
        PRIMARY KEY (id)
);

CREATE INDEX ix_prew_87ea5dfc8b8e384d ON prew (id);
CREATE TABLE IF NOT EXISTS "end" (
        id INTEGER NOT NULL,
        word TEXT,
        PRIMARY KEY (id)
);
