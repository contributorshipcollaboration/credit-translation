import json
import os
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import fastjsonschema

# Function to convert spreadsheet data to JSON following the schema
def convert_to_json(lang, pathtoschema, credpath):
    #open json schema file
    schema = json.load(open(pathtoschema))
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credpath, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open("CRediT_Translation")
    sheet = spreadsheet.worksheet(lang)
    data = sheet.get_all_records()
    metadata = {
             "languageCode" : lang,
             "languageName" : data[60]["translation"],
             "translators" : [
                {
                    "firstName": data[61]["translation"],
                    "lastName": data[61]["translation"]
                }
                 ],
             "translationProcedure" : data[62]["translation"]   
             }

    translations = {
        "https://credit.niso.org/contributor-roles/conceptualization/": {
            "name": data[1]["translation"],
            "description": data[3]["translation"]
        },
        "https://credit.niso.org/contributor-roles/data-curation/": {
            "name": data[5]["translation"],
            "description": data[7]["translation"]
        },
        "https://credit.niso.org/contributor-roles/formal-analysis/": {
            "name": data[9]["translation"],
            "description": data[11]["translation"]
        },
        "https://credit.niso.org/contributor-roles/funding-acquisition/": {
            "name": data[13]["translation"],
            "description": data[15]["translation"]
        },
        "https://credit.niso.org/contributor-roles/investigation/": {
            "name": data[17]["translation"],
            "description": data[19]["translation"]
        },
        "https://credit.niso.org/contributor-roles/methodology/": {
            "name": data[21]["translation"],
            "description": data[23]["translation"]
        },
        "https://credit.niso.org/contributor-roles/project-administration/": {
            "name": data[25]["translation"],
            "description": data[27]["translation"]
        },
        "https://credit.niso.org/contributor-roles/resources/": {
            "name": data[29]["translation"],
            "description": data[31]["translation"]
        },
        "https://credit.niso.org/contributor-roles/software/": {
            "name": data[33]["translation"],
            "description": data[35]["translation"]
        },
        "https://credit.niso.org/contributor-roles/supervision/": {
            "name": data[37]["translation"],
            "description": data[39]["translation"]
        },
        "https://credit.niso.org/contributor-roles/validation/": {
            "name": data[41]["translation"],
            "description": data[43]["translation"]
        },
        "https://credit.niso.org/contributor-roles/visualization/": {
            "name": data[45]["translation"],
            "description": data[47]["translation"]
        },
        "https://credit.niso.org/contributor-roles/writing-original-draft/": {
            "name": data[49]["translation"],
            "description": data[51]["translation"]
        },
        "https://credit.niso.org/contributor-roles/writing-review-editing/": {
            "name": data[53]["translation"],
            "description": data[55]["translation"]
        }
    }

    json_data = {
        "metadata": metadata,
        "translations": translations
    }

    return json_data, schema, lang
    # Convert the data according to your schema
# input function parameters from cli, usage: python3 convert.py <lang> <pathtoschema> <credpath>

json_data, schema, lang = convert_to_json(sys.argv[1], sys.argv[2], sys.argv[3])
 
try:
    fastjsonschema.validate(schema, json_data)
except fastjsonschema.JsonSchemaException as e:
    print("JSON data does not conform to the schema")
    print(e)

file_path = f"./automatic_translations/{lang}.json"
os.makedirs(os.path.dirname(file_path), exist_ok=True)
# Write the JSON data to a file in translations folder
with open(file_path, 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

print("JSON conversion complete!")
