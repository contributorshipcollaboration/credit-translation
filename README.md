# CRediT translations from English into other languages

The repository is for translations of [CRediT](https://credit.niso.org/). The translations are unofficial (NISO policy is that although they welcome translations, they do not endorse any particular translation as official).

Translations here are stored as JSON files. The human-readable translations are generated automatically from the JSON files as markdown and can be viewed on the Contributorship Collaboration's website at [https://contributorshipcollaboration.github.io/](https://contributorshipcollaboration.github.io/) (NOT DONE YET).

Each translation was provided by volunteers whose names are listed. When using the translations, please provide attribution, e.g. for Hungarian "CC-BY Marton Kovacs and Marton Varga".

## New contributors welcome!

All contributors are bound by the [code of conduct](https://github.com/marton-balazs-kovacs/tenzing/blob/master/CODE_OF_CONDUCT.md).

### Contributing to translations 

Anyone fluent in a language not already translated can help provide a new translation, or propose a change to an existing translation.

Before starting on a new translation:

* [Check the current status](language_status.md) of translation for your language.
* Fill out [our Google Form](https://docs.google.com/forms/d/e/1FAIpQLSfdhqlnk4sw61MkkDuufZyqO1SKmnp--QE6vEG1_7qnP9MzJg/viewform?usp=sf_link) so we have a record of your interest and potentially to help match you with another translator or project contributor.
* Follow the instructions in the below [translation section](#-Creating-a-translation).

Contributors will be recognized in that their names will appear in the attribution for the translation they helped create. For example, see the [draft human-readable page for German](https://github.com/contributorshipcollaboration/credit-translation/blob/main/md_files/credit_translation_de.md).



## Contributing to other facets of the project

* Code: check the Github issues or email us)
* Outreach and implementation 
 * Contact scientific societies and scientific publishers who publish in these languages
* Help us organise a hackathon ad hoc or at a scientific conference

### Creating a translation

*  We have created a Google Sheet for entering your translation work and seeing how others did it. Contact us for access to the Google Sheet.
* First, one speaker fluent in both languages translates the English into the target language and enters that on the Google Sheet. 
* A second speaker, ideally one not familiar with CRediT, back-translates the translation into English.
* Feel free to use Google Translate to assist, just don't rely on it, for example don't use it for both the forward and back-translation.
* Discrepancies between the original English and the back-translated English can tip one off to parts of the translation that deserve attention, where one should consider alternative phrasings. So, the two speakers confer and resolve any discrepancies.
* To make your translation machine-readable, you must create a JSON file, following the format of the [schema](credit_translation_schema.json). See instructions below.

### When a .json file for your language does NOT already exist here:

Download one of the existing JSON files, such as [the German one](translations/credit_translation_de.json) and change all the German text to your target language. Then send it to us.

### When a .json for your language DOES already exist: 

* To see if a file already exists, look [here](translations/) for a file with the [two-letter language code](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) for your language. If it doesn't exist, contact us, unless you know how to use Github to create files, in which case follow the instructions [in the next section](#-Github-procedure-for-new-languages-if-you-are-very-comfortable-with-Github)
* To edit the file, click on the pencil icon. Insert the content for your translation. See [the German one](translations/credit_translation_de.json) for an example.
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
