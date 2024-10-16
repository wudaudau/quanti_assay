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
  manufacture_id INTEGER NOT NULL,  -- UNIQUE(manufacture_id, cat_number)
  cat_number TEXT    NOT NULL,  -- UNIQUE(manufacture_id, cat_number)
  name           TEXT    NULL    ,
  description            NULL    ,
  size                        NULL    ,
  storage_id          INTEGER NULL    ,
  quanti_item_type_id INTEGER NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (manufacture_id) REFERENCES manufacture (id),
  FOREIGN KEY (storage_id) REFERENCES storage (id),
  FOREIGN KEY (quanti_item_type_id) REFERENCES quanti_item_type (id),
  UNIQUE(manufacture_id, cat_number)
);




-- TODO: Reforactor kit_item table to become kits_items to associate kit items with kits
CREATE TABLE kits_items
(
  id                      NOT NULL    ,
  product_id_kit  INTEGER NOT NULL,  -- UNIQUE(product_id_kit, product_id_item)
  product_id_item INTEGER NOT NULL,  -- UNIQUE(product_id_kit, product_id_item)
  quantity        TEXT    NULL,
  PRIMARY KEY (id),    
  FOREIGN KEY (product_id_kit) REFERENCES product (id),
  FOREIGN KEY (product_id_item) REFERENCES product (id),
  UNIQUE(product_id_kit, product_id_item)
);


