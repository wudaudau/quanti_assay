

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

