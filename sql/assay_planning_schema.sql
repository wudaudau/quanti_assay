

CREATE TABLE project
(
  id          INTEGER NOT NULL,
  name        TEXT    NOT NULL UNIQUE,
  species_id  INTEGER NOT NULL,
  description TEXT    NULL    ,
  PRIMARY KEY (id),
  FOREIGN KEY (species_id) REFERENCES species (id)
);

