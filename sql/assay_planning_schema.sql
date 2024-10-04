

CREATE TABLE project
(
  id          INTEGER NOT NULL,
  name        TEXT    NOT NULL UNIQUE,
  species_id  INTEGER NOT NULL,
  description TEXT    NULL    ,
  PRIMARY KEY (id),
  FOREIGN KEY (species_id) REFERENCES species (id)
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
