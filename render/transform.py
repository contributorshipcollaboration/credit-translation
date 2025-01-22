import json
import os
from datetime import datetime
import pycountry
import chardet

# Function to open json with guessed encoding style
def open_json_file(json_path):
    with open(json_path, 'rb') as f:  # Open the file in binary mode
        raw_data = f.read()
        encoding = chardet.detect(raw_data)['encoding']
        if encoding:
            print(f"The detected encoding is: {encoding}")
            return json.loads(raw_data.decode(encoding))
        else:
            raise ValueError("Encoding could not be determined.")
        
# Function to get full language name
def get_language_name(iso_code):
    try:
        return pycountry.languages.get(alpha_2=iso_code).name
    except AttributeError:
        return iso_code

# Get the absolute directory path where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct absolute paths for the translation and md_files directories
translation_dir = os.path.join(script_dir, "../translation/")
md_files_dir = os.path.join(script_dir, "../md_files/")

def json_to_md(json_data, en_data, filename):
    """
    Convert JSON data to Markdown text following the specified structure.
    """
    # YAML header with title and date
    # Check if "languageName" exists in metadata, otherwise use get_language_name
    language_name = json_data["metadata"].get("languageName") or get_language_name(json_data["metadata"]["languageCode"])
    md_content = f"""---
title: "{language_name} translation of CRediT"
date: {datetime.now().strftime('%Y-%m-%d')}
language: "{language_name}"
layout: "translation/single"
githublink: "https://github.com/contributorshipcollaboration/credit-translation/blob/main/translations/{filename}"
---

"""

    # Translations section as a table
    md_content += f"| {language_name} | English |\n"
    md_content += "| --- | --- |\n"

    for role_url, details in json_data["translations"].items():
        role_name_en = f"**{en_data['translations'][role_url]['name']}**"
        role_name_translated = f"**{details['name']}**"
        description_en = en_data["translations"][role_url]["description"]
        description_translated = details["description"]
        
        # Role name row
        md_content += f"| {role_name_translated} | {role_name_en} |\n"
        # Description row
        md_content += f"| {description_translated} | {description_en} |\n"

    # Translators section with ORCID hyperlink
    translators = json_data["metadata"]["translators"]
    translator_lines = []
    for t in translators:
        name = f'{t["firstName"]} {t.get("middleName", "")} {t["lastName"]}'.strip()
        if "ORCID" in t and t["ORCID"]:
            name = f'[{name}](https://orcid.org/{t["ORCID"]})'
        translator_lines.append(name)
    translator_names = ', '.join(translator_lines)
    md_content += f"\n## Translators\n\n{translator_names}\n\n"

    # Link to JSON
    md_content += f"## JSON Metadata\n\n[https://github.com/contributorshipcollaboration/credit-translation/blob/main/translations/{filename}](https://github.com/contributorshipcollaboration/credit-translation/blob/main/translations/{filename})\n\n"
    # License section 
    md_content += f"## License\n\n[CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)"
    # copyright is held by the translators together with the originators of CRediT
    md_content += f" {translator_names}, Brand, Allen, Altman, Hlava, & Scott\n\n"
    
    # Translation procedure section
    translation_procedure = json_data["metadata"]["translationProcedure"]
    md_content += f"## Translation Procedure\n\n{translation_procedure}"

    return md_content

def transform_json_to_md(directory, output_directory):
    """
    Transform JSON files in the given directory to Markdown files.
    """
    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Load the English translation for reference
    en_data = open_json_file(os.path.join(directory, "en.json"))

    for filename in os.listdir(directory):
        if filename.endswith(".json") and filename != "en.json":
            json_path = os.path.join(directory, filename)
            try:
                json_data = open_json_file(json_path)
            except ValueError as e:
                print(f"Error processing {filename}: {e}")
                continue
            
            # Convert JSON to Markdown
            md_content = json_to_md(json_data, en_data, filename)

            # Save Markdown content to a new file
            md_filename = filename.replace(".json", ".md")
            md_path = os.path.join(output_directory, md_filename)
            with open(md_path, 'w', encoding='utf-8') as md_file:
                md_file.write(md_content)

            print(f"Transformed {filename} to Markdown format.")

if __name__ == "__main__":
    # Compute absolute paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "..")) 
    translation_dir = os.path.join(project_root, "translations")
    md_files_dir = os.path.join(project_root, "md_files")

    # Ensure the directories exist
    if not os.path.exists(translation_dir):
        print(f"Directory not found: {translation_dir}")
        exit(1)
    if not os.path.exists(md_files_dir):
        os.makedirs(md_files_dir)

    transform_json_to_md(translation_dir, md_files_dir)
