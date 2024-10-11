# TODO

## About the modules hierachy
- Core
  - assay_planning
  - kit_order
  - assay_log


## Project progress
- [ ] feature/shema-and-function-transformation
  - [ ] `core`
    - [ ] `db_utils.py`
      - [ ] 
    - [ ] `core_tables.py`
      - [ ] add manufacture and kit tables
  - [ ] `assay_planning`
    - [ ] Look up assays 
      - [ ] by project
      - [ ] by assay_type
    - [ ] 
  - [ ] `kit_order`
  - [ ] `assay_log`
- [ ] 

## Unstructured TODO
- [/] Create `test_app.py`
- [ ] check unit. e.g. assay, kit, and SD_analyte may have a column of unit. to process the Quanti exp, we need to ensure no inconsistence for the unit.
- [ ] complete projct-assay (Be aware of the data sensitivity.)
  - [ ] Ensure all the assays are listed for "CE-PSY" project
  - [ ] Find our all Julies assay
    - [ ] From my notes in OneNote
    - [ ] From our files in OneDrive
    - [ ] From data process reports (assay log)
    - [ ] From her cahier
- [ ] Add functions for handling the database in `db_utils.py`
  - [ ] is_existing(), need_update(), update_entry()
- [ ] Move the batch data part from the project of batch analysis. (Be aware of the data sensitivity.) (make it works, at least.)
- [ ] Add sample dilution instruction tables. e.g. to prepare certain assay, how to we need to prepare the sample aliquot to prevent increasing freeze-thaw cycles.

Functionality-related
- [ ] Recap the assays and analytes count by project.
- [ ] sample type related functions...
- [ ] Refactor the schema to show analytes by assay and list avalible assays by topic. 
  - [ ] e.g.1: What assays are gut permilisation related?
  - [ ] e.g.2: What analytes are gut permilisation related?
  - [ ] e.g.3: What project has certain analyte or certain assay? 



Repository to find data:
- `OneDrive-UPEC/Documents partages - Team Ryad/05_Manip - ELISA et MSD/data process`
- `OneDrive-UPEC/01_Protocols and Docs/Protocol_Quanti`
- Kit info files:
  - `OneDrive-UPEC/WorkingPlace_CLW/00_to arrange into channels or libraries/06_Project_BIOFACE-PSY`
  - ...