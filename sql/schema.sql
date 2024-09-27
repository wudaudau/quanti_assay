CREATE TABLE kit
(
  id             INTEGER NOT NULL,
  kit_cat_number TEXT    NOT NULL DEFAULT Unique,
  name           TEXT    NULL    ,
  manufacture_id INTEGER NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (manufacture_id) REFERENCES manufacture (id)
);

CREATE TABLE kit_item
(
  id             INTEGER NOT NULL,
  cat_number     TEXT    NULL     DEFAULT Unique,
  name           TEXT    NOT NULL,
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

CREATE TABLE manufacture
(
  id   INTEGER NOT NULL,
  name TEXT    NULL    ,
  PRIMARY KEY (id)
);

CREATE TABLE storage
(
  id          INTEGER NOT NULL,
  name        TEXT    NULL    ,
  description TEXT    NULL    ,
  PRIMARY KEY (id)
);