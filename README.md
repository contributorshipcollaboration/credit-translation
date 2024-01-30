# CRediT translations

The repository contains the unofficial translations of [CRediT](https://credit.niso.org/). The translations are primarely stored formatted according to a json-schema created specifically for this project to ensure machine-readability. The human-readable markdown formatted translations are generated automatically from the json files and can be viewed on the Contributorship Collaboration's website at [https://contributorshipcollaboration.github.io/](https://contributorshipcollaboration.github.io/).

Each translation was provided by volunteers whose names are listed in the licenses besides each translation file.

## Contribute

Everyone is welcomed to contribute to the project by providing a new translation or proposing changes to the existing translations. If you would like to contribute please contact Marton Kovacs at marton.balazs.kovacs at gmail.com. When uploading a new translation please:

* Ensure that you follow our translation schema that can be found in `credit_translation_schema.json`
* You can validate your json file with the new translation against our schema at [https://www.jsonschemavalidator.net/](https://www.jsonschemavalidator.net/)
* Fork the repository, clone it, and create a branch for your translation
* Create a subdirectory for your translation in the `tranlsations/` directory using the [ISO 639-2 language code](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) of the translated language
* Add the json file containing your translation to the subdirectory you've just created
* Add an X license with your and your collaborators name to the subfolder containing the translation
* Create a pull request and add Marton Kovacs and Alex Holcombe as reviewers to the request
