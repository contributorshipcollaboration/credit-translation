# CRediT translations

The repository is for unofficial translations of [CRediT](https://credit.niso.org/). Each translation is entered as a json file, in a format created for this project to ensure machine-readability. The human-readable translations are generated automatically from the json files as markdown and can be viewed on the Contributorship Collaboration's website at [https://contributorshipcollaboration.github.io/](https://contributorshipcollaboration.github.io/).

Each translation was provided by volunteers whose names are listed in the licenses besides each translation file.

## New contributors welcome!

Everyone is welcome to contribute to the project by providing a new translation or proposing changes to the existing translations. If you would like to contribute please contact Marton Kovacs at marton.balazs.kovacs at gmail.com.

## Contributing 

### Creating a translation

For doing the actual translation, see the notes at the bottom of existing translation files, such as XXXX

### Creating a translation file

* To make your translation machine-readable, you must create a JSON file, following the format of `credit_translation_schema.json`
  * Start by duplicating the file for an existing language in the TRANSLATI?ONS directory
  * Rename the file according to the [two-letter language code](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) for your language.
  * Edit the file to insert the content of your translation
  * Validate that your edits have not messed up the formatting by entering it at [https://www.jsonschemavalidator.net/](https://www.jsonschemavalidator.net/) DOES THIS WORK?

### Entering a translation into this repository

* For Github experts: fork the repository, clone it, and create a branch for your translation
* For Non-experts
  * Click on the pencil
  
* Create a subdirectory for your translation in the `tranlsations/` directory using the [ISO 639-2 language code](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) of the translated language
* Add the JSON file containing your translation to the subdirectory you've just created
* Add an X license with your and your collaborators name to the subfolder containing the translation
* Create a pull request and add Marton Kovacs and Alex Holcombe as reviewers to the request
