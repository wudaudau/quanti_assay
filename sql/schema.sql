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












-- Mostly are 
CREATE TABLE item_lot
(
  id         INTEGER NOT NULL,
  item_id    INTEGER NOT NULL,  -- UNIQUE(item_id, lot_number)
  lot_number TEXT    NOT NULL,  -- UNIQUE(item_id, lot_number)
  expiration_date TEXT    NULL    ,
  PRIMARY KEY (id),
  FOREIGN KEY (item_id) REFERENCES kit_item (id),
  UNIQUE(item_id, lot_number)
);

CREATE TABLE sd_initial_conc
(
  id              INTEGER NOT NULL,
  item_lot_id     INTEGER NOT NULL,  -- UNIQUE(item_lot_id, analyte_id)
  analyte_id      INTEGER NOT NULL,  -- UNIQUE(item_lot_id, analyte_id)
  conc            NUMERIC NULL    ,
  unit            TEXT    NULL    ,
  PRIMARY KEY (id),
  FOREIGN KEY (analyte_id) REFERENCES analyte (id),
  FOREIGN KEY (item_lot_id) REFERENCES item_lot (id),
  UNIQUE(item_lot_id, analyte_id)
);

