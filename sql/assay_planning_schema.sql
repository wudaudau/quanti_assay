

CREATE TABLE project
(
  id          INTEGER NOT NULL,
  name        TEXT    NOT NULL UNIQUE,
  species_id  INTEGER NOT NULL,
  description TEXT    NULL    ,
  PRIMARY KEY (id),
  FOREIGN KEY (species_id) REFERENCES species (id)
);


















CREATE TABLE assay_type
(
  id   INTEGER NOT NULL,
  name TEXT    NULL    ,
  PRIMARY KEY (id)
);

CREATE TABLE assay
(
  id            INTEGER NOT NULL,
  name          TEXT    NOT NULL UNIQUE,
  species_id   INTEGER NOT NULL,
  assay_type_id INTEGER NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (species_id) REFERENCES species (id),
  FOREIGN KEY (assay_type_id) REFERENCES assay_type (id)
);












-- Junction table to assign assays to projects
CREATE TABLE project_assay
(
  id         INTEGER NOT NULL,
  project_id INTEGER NOT NULL,  -- UNIQUE (project_id, assay_id)
  assay_id   INTEGER NOT NULL,  -- UNIQUE (project_id, assay_id)
  PRIMARY KEY (id),
  FOREIGN KEY (project_id) REFERENCES project (id),
  FOREIGN KEY (assay_id) REFERENCES assay (id),
  UNIQUE (project_id, assay_id)
);
