
CREATE TABLE IF NOT EXISTS project (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cohort (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT, -- we can roufly add the disease, the number of samples, the sample type here.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS species (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS assay_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS assay (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    species_id INTEGER NOT NULL,
    assay_type_id INTEGER NOT NULL,
    unit_kit TEXT, -- ENUM('pg/mL', 'ng/mL', 'ug/mL', 'mg/mL', 'IU/mL', 'mIU/mL', 'ng/mL', 'ng/dL
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (species_id) REFERENCES species(id),
    FOREIGN KEY (assay_type_id) REFERENCES assay_type(id)
);
-- CREATE TABLE IF NOT EXISTS assay (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     name TEXT NOT NULL UNIQUE,
--     species TEXT NOT NULL, -- ENUM('Human', 'Mouse', 'Rat', 'Other')
--     assay_type TEXT NOT NULL, -- ENUM('ELISA', 'MSD')
--     unit TEXT, -- ENUM('pg/mL', 'ng/mL', 'ug/mL', 'mg/mL', 'IU/mL', 'mIU/mL', 'ng/mL', 'ng/dL
--     description TEXT,
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );


CREATE TABLE IF NOT EXISTS sample_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE, -- ENUM('Serum', 'EDTA Plasma', 'Citrate Plasma', 'Heparin Plasma', 'CSF', 'EVs', 'Other')
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS project_assay (
    project_id INTEGER NOT NULL,
    assay_id INTEGER NOT NULL,
    sample_type_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES project(id),
    FOREIGN KEY (assay_id) REFERENCES assay(id),
    FOREIGN KEY (sample_type_id) REFERENCES sample_type(id),
    PRIMARY KEY (project_id, assay_id)
);




CREATE TABLE IF NOT EXISTS analyte (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS assay_analyte (
    assay_id INTEGER NOT NULL,
    analyte_id INTEGER NOT NULL,
    spot_order INTEGER NOT NULL, -- INT between 1 and 10
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    FOREIGN KEY (assay_id) REFERENCES assay(id),
    FOREIGN KEY (analyte_id) REFERENCES analyte(id),
    PRIMARY KEY (assay_id, analyte_id)
);