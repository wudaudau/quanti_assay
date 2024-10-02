CREATE TABLE manufacture
(
  id   INTEGER NOT NULL,
  name TEXT    NULL    ,
  PRIMARY KEY (id)
);

CREATE TABLE storage
(
  id          INTEGER NOT NULL,
  name        TEXT    NOT NULL    ,
  description TEXT    NULL    ,
  PRIMARY KEY (id)
);

CREATE TABLE kit
(
  id             INTEGER NOT NULL,
  kit_cat_number TEXT    NOT NULL UNIQUE,
  name           TEXT    NULL    ,
  manufacture_id INTEGER NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (manufacture_id) REFERENCES manufacture (id)
);

CREATE TABLE kit_item
(
  id          INTEGER NOT NULL,
  cat_number  TEXT    NULL     UNIQUE,
  name        TEXT    NOT NULL,
  kit_id      INTEGER NOT NULL,
  storage_id  INTEGER NOT NULL,
  description TEXT    NULL    ,
  PRIMARY KEY (id),
  FOREIGN KEY (storage_id) REFERENCES storage (id),
  FOREIGN KEY (kit_id) REFERENCES kit (id)
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
















CREATE TABLE species
(
  id   INTEGER NOT NULL,
  name TEXT    NULL    ,
  PRIMARY KEY (id)
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
















-- This should be the base of analyte. We distingrish between IL-8 and IL-8(HA) here.
CREATE TABLE assays_analytes
(
  id               INTEGER NOT NULL,
  assay_id         INTEGER    NOT NULL,  -- UNIQUE(assay_id, analyte_id, spot)
  analyte_id       INTEGER NOT NULL,  -- UNIQUE(assay_id, analyte_id, spot)
  spot             INTEGER NOT NULL,  -- UNIQUE(assay_id, analyte_id, spot)
  opt_analyte_name TEXT    NOT NULL UNIQUE,
  PRIMARY KEY (id),
  FOREIGN KEY (assay_id) REFERENCES assay (name),
  FOREIGN KEY (analyte_id) REFERENCES analyte (id), 
  UNIQUE(assay_id, analyte_id, spot)
);
