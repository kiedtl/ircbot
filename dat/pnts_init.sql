-- karma for each user
--
-- each karma point is stored by itself.
--
-- and yes, I know that storing each karma point
-- individually is not nearly as efficient as
-- storing it all together, but I think the speed
-- loss from doing it this way instead is
-- negotiable.
CREATE TABLE karma (
        id       INTEGER NOT NULL,
        username TEXT    NOT NULL,
        date     INTEGER NOT NULL,
        PRIMARY KEY (id)
);
