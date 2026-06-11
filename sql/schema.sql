CREATE TABLE IF NOT EXISTS emplois (
    job_id            VARCHAR PRIMARY KEY,
    titre_raw         VARCHAR,
    titre_normalise   VARCHAR,
    entreprise        VARCHAR,
    ville             VARCHAR,
    region            VARCHAR,
    date_publication  DATE,
    source            VARCHAR
);

CREATE TABLE IF NOT EXISTS competences (
    id          SERIAL PRIMARY KEY,
    job_id      VARCHAR REFERENCES emplois(job_id),
    competence  VARCHAR,
    categorie   VARCHAR
);
