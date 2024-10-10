

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














-- the standard name to unify in the system. We still need to distingrish between IL-8 and IL-8(HA)
CREATE TABLE analyte
(
  id   INTEGER NOT NULL,
  name TEXT    NULL     UNIQUE,
  PRIMARY KEY (id)
);

-- To obtain the standard name using in the system
CREATE TABLE analyte_mapping
(
  id             INTEGER NOT NULL,
  name           TEXT    NULL     UNIQUE,
  std_analyte_id INTEGER NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (std_analyte_id) REFERENCES analyte (id)
);

