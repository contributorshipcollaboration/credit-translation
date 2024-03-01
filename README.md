# CRediT translations into other natural human languages

The repository is for translations of [CRediT](https://credit.niso.org/). The translations are unofficial - NISO policy is that they welcome translations but do not endorse any particular translation as official.

Translations here are stored as JSON files, in a format created for this project. The human-readable translations are generated automatically from the JSON files as markdown and can be viewed on the Contributorship Collaboration's website at [https://contributorshipcollaboration.github.io/](https://contributorshipcollaboration.github.io/).

Each translation was provided by volunteers whose names are listed in the license file that is in the same directory as the corresponding JSON file.

## New contributors welcome!

Everyone is welcome to contribute to the project by providing a new translation or proposing changes to the existing translations. If you would like to contribute please contact Marton Kovacs at marton.balazs.kovacs at gmail.com.

## Contributing 

### Creating a translation

*  We have created a Google Sheet for entering your translation work and seeing how others did it. Contact us for access to the Google Sheet.
* First, one speaker fluent in both languages translates the English into the target language and enters that on the Google Sheet.
* A second speaker, ideally one not familiar with CRediT, back-translates the translation into English.
* Discrepancies between the original English and the back-translated English can tip one off to parts of the translation that deserve attention, where one should consider alternative phrasings. So, the two speakers confer and resolve any discrepancies.
* To make your translation machine-readable, you must create a JSON file, following the format of the [schema](credit_translation_schema.json). See instructions below.

### When a .json file for your language does NOT already exist here:

Download one of the existing JSON files, such as [this Hungarian one](translations/hu/credit_translation_hu.json) and change all the Hungarian text to your target language. Then send it to us.

### When a .json for your language DOES already exist: 

* To see if a file already exists, look [here](translations/) for a file with the [two-letter language code](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) for your language. If it doesn't exist, contact us, unless you know how to use Github to create files, in which case follow the instructions [in the next section](#-Github-procedure-for-new-languages-if-you-are-very-comfortable-with-Github)
* To edit the file, click on the pencil icon. Insert the content for your translation. See [the file for Hungarian](translations/hu/credit_translation_hu.json) for an example.
* So that the Github repository gets updated, create a pull request by clicking on BLAH BLAH
* Don't forget to add information about how you did the translation in the "translationProcedure" string of the .json file, here is an example: "TL, CJ, and HH are all native speakers of German. A first version by TL existed for some time. CJ introduced an additional translation draft. TL and CJ merged the few differences between the two versions favoring broader (in the sense of suitability for as many disciplines and working environments as possible) translations. The final translation was then back-translated by HH, and finally approved by all parties." In this case, two forward translations were created, yielding discrepancies that surfaced parts to attend more to. As described in the above [Creating a translation](#-Creating-a-translation) section, however, another way to do that is to look at discrepancies highlighted by doing a back translation.
* Validate that your edits have not messed up the formatting by entering both the [schema](credit_translation_schema.json) and your file at [https://www.jsonschemavalidator.net/](https://www.jsonschemavalidator.net/). This checks for most formatting errors.
* Generate a pull request
 
### Github procedure for new languages if you are experienced with Github

* Fork the repository, clone it, and create a branch for your translation
* Create a subdirectory for your translation in the `translations/` directory using the [ISO 639-2 language code](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) of the translated language
* Following the example of the existing languages, create the JSON tranlation file, license file, and translation-process file.
* Validate that your edits have not messed up the JSON file formatting by entering both the [schema](credit_translation_schema.json) and your file at [https://www.jsonschemavalidator.net/](https://www.jsonschemavalidator.net/).
* Create a pull request and add DO WE NEED THIS? Marton Kovacs and Alex Holcombe as reviewers to the request
