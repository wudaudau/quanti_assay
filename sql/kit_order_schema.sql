CREATE TABLE manufacture
(
  id   INTEGER NOT NULL,
  name TEXT    NOT NULL UNIQUE,
  PRIMARY KEY (id)
);

CREATE TABLE storage
(
  id          INTEGER NOT NULL,
  name        TEXT    NOT NULL UNIQUE,
  description TEXT    NULL    ,
  PRIMARY KEY (id)
);

-- e.g. kit, item-SD, item-QC, item-plate, item-Ab, item-buffer
CREATE TABLE quanti_item_type
(
  id          INTEGER NOT NULL,
  name        TEXT    NOT NULL UNIQUE,
  description TEXT    NULL    ,
  PRIMARY KEY (id)
);

-- TODO: Merge kit and kit_item tables into one product table
CREATE TABLE product
(
  id             INTEGER NOT NULL,
  manufacture_id INTEGER NOT NULL,  -- UNIQUE(manufacture_id, kit_cat_number)
  kit_cat_number TEXT    NOT NULL,  -- UNIQUE(manufacture_id, kit_cat_number)
  name           TEXT    NULL    ,
  description            NULL    ,
  storage_id     INTEGER NOT NULL,
  quanti_item_type_id INTEGER NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (manufacture_id) REFERENCES manufacture (id),
  FOREIGN KEY (storage_id) REFERENCES storage (id),
  FOREIGN KEY (quanti_item_type_id) REFERENCES quanti_item_type (id),
  UNIQUE(manufacture_id, kit_cat_number)
);


-- TODO: Reforactor kit_item table to become kits_items to associate kit items with kits
CREATE TABLE kits_items
(
  id             INTEGER NOT NULL,
  kit_cat_number TEXT    NOT NULL UNIQUE,
  name           TEXT    NULL    ,
  manufacture_id INTEGER NOT NULL,
  description    TEXT    NULL    ,
  PRIMARY KEY (id),
  FOREIGN KEY (manufacture_id) REFERENCES manufacture (id),
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

