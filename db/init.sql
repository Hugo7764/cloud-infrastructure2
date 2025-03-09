CREATE TABLE utilisateurs (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
);

CREATE TABLE equipes (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE matchs (
    id SERIAL PRIMARY KEY,
    equipe1_id INTEGER REFERENCES equipes(id) ON DELETE CASCADE,
    equipe2_id INTEGER REFERENCES equipes(id) ON DELETE CASCADE,
    date TIMESTAMP NOT NULL,
    score_equipe1 INTEGER DEFAULT 0,
    score_equipe2 INTEGER DEFAULT 0
);
