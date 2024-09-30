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

CREATE TABLE kit_item
(
  id             INTEGER NOT NULL,
  kit_cat_number TEXT    NOT NULL UNIQUE,
  name           TEXT    NULL    ,
  manufacture_id INTEGER NOT NULL,
  storage_id     INTEGER NOT NULL,
  description    TEXT    NULL    ,
  PRIMARY KEY (id),
  FOREIGN KEY (manufacture_id) REFERENCES manufacture (id),
  FOREIGN KEY (storage_id) REFERENCES storage (id)
);


CREATE TABLE kits_kit_items
(
  id          INTEGER NOT NULL,
  kit_id      INTEGER NOT NULL,
  kit_item_id INTEGER NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (kit_id) REFERENCES kit (id),
  FOREIGN KEY (kit_item_id) REFERENCES kit_item (id)
);












-- It can see how many isoform we measure for the same analyte. It can also for selecting the assay.
CREATE TABLE analyte
(
  id   INTEGER NOT NULL,
  name TEXT    NULL     UNIQUE,
  PRIMARY KEY (id)
);

-- the standard name to unify in the system. We still need to distingrish between IL-8 and IL-8(HA)
CREATE TABLE std_analyte
(
  id   INTEGER NOT NULL,
  name TEXT    NULL     UNIQUE,
  PRIMARY KEY (id)
);

CREATE TABLE analyte_std_analyte
(
  id             INTEGER NOT NULL,
  analyte_id     INTEGER NOT NULL,
  std_analyte_id INTEGER NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (analyte_id) REFERENCES analyte (id),
  FOREIGN KEY (std_analyte_id) REFERENCES std_analyte (id)
  UNIQUE (analyte_id, std_analyte_id)
);