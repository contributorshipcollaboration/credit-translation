# CRediT translations into other natural human languages

The repository is for translations of [CRediT](https://credit.niso.org/). The translations are unofficial - NISO policy is that they welcome translations but do not endorse any particular translation as official.

Translations here are stored as JSON files, in a format created for this project. The human-readable translations are generated automatically from the JSON files as markdown and can be viewed on the Contributorship Collaboration's website at [https://contributorshipcollaboration.github.io/](https://contributorshipcollaboration.github.io/).

Each translation was provided by volunteers whose names are listed in the license file that is in the same directory as the corresponding JSON file.

## New contributors welcome!

Everyone is welcome to contribute to the project by providing a new translation or proposing changes to the existing translations. If you would like to contribute please contact Marton Kovacs at marton.balazs.kovacs at gmail.com.

## Contributing 

### Creating a translation

* Actually do the translation work.
 * For examples of the procedure to do the translation work, see the `translation-process.md` files for different languages that you can find in the subdirectories of the [translations directory](translations/).
* To make your translation machine-readable, you must create a JSON file, following the format of the [schema](credit_translation_schema.json). See instructions below.

### Editing the translation files, when a directory for your language already exists

* Check whether a directory exists yet for your translation. Look [here](translations/) for a directory with the [two-letter language code](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) for your language. If it doesn't exist, contact us, unless you know how to use Github to create directories, in which case follow the instructions [in the next section](#-Github-procedure-for-new-languages-if-you-are-very-comfortable-with-Github)
*  Go to the Github page for the JSON file for your language, in your language's subdirectory of the [translations directory](translations/).
  * To edit the file, click on the pencil icon. Insert the content for your translation. See [the file for Hungarian](translations/hu/credit_translation_hu.json) for an example.
  * So that the Github repository gets updated, create a pull request by clicking on BLAH BLAH
  * Validate that your edits have not messed up the formatting by entering both the [schema](credit_translation_schema.json) and your file at [https://www.jsonschemavalidator.net/](https://www.jsonschemavalidator.net/).
* Edit the license file by inserting the names of the translators. See [the license file for Hungarian](translations/hu/license.html) FIX for an example.
  * Generate a pull request
* Edit the translation-process.md file to describe how you did the translation and validated it, for example by doing back-translation and comparing the back-translation to the original English.
  * Generate a pull request
 
### Github procedure for new languages if you are very comfortable with Github

* Fork the repository, clone it, and create a branch for your translation
* Create a subdirectory for your translation in the `translations/` directory using the [ISO 639-2 language code](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) of the translated language
* Following the example of the existing languages, create the JSON tranlation file, license file, and translation-process file.
* Validate that your edits have not messed up the JSON file formatting by entering both the [schema](credit_translation_schema.json) and your file at [https://www.jsonschemavalidator.net/](https://www.jsonschemavalidator.net/).
* Create a pull request and add DO WE NEED THIS? Marton Kovacs and Alex Holcombe as reviewers to the request
