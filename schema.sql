DROP TABLE IF EXISTS votes;

CREATE TABLE votes (
    ip TEXT PRIMARY KEY,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    choice TEXT NOT NULL
);