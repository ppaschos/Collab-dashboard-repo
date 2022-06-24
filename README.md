This is to collect scripts, parsers or even data for the collab dashboard

## Notice

The /data folder is generated automatically from the contents of /indata. All data changes should be made to the csvs there. 

## Formatting

to_json.py parsing file expects the following to be true:

Columns contain at least:
    - For APs
        - Institute Site
        - Access Point
        - Show
    - For CEs
        - 'COMPUTE ENTRY POINT (CE)'
        - Institute Site 
        - Latitude 
        - Longitude 
        - Hosted CE - ( Yes or No )
        - CE location -  ( local if not hosted, hosted location otherwise )
    - For Institutions
        - Lab
        - Institute
        - Latitude 
        - Longitude
        - Country

Filenames:

The file reading is simplistic and will break if extraneous/non-conforming files are added to the /indata folder.

- APs: <collaboration>-ap-sites.csv
- CEs: <collaboration>-ce-sites.csv
- Institutions: <collaboration>-institutions.csv


