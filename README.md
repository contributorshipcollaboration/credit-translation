# CRediT translations from English into other languages

The repository is for translations of [CRediT](https://credit.niso.org/). The translations are unofficial (NISO policy is that although they welcome translations, they do not endorse any particular translation as official).

Translations here are stored as JSON files. The human-readable translations are generated automatically from the JSON files as markdown and can be viewed on the Contributorship Collaboration's website at [https://contributorshipcollaboration.github.io/](https://contributorshipcollaboration.github.io/).

Each translation was provided by volunteers, and  attribution and license is listed.

## New contributors welcome!

See our [Instructions for Contributors](https://contributorshipcollaboration.github.io/projects/translation/instructions/)

All contributors are bound by the [code of conduct](https://github.com/marton-balazs-kovacs/tenzing/blob/master/CODE_OF_CONDUCT.md).

## Tools that use these translations

If you build a tool that uses these translations, please let us know by [opening an issue](https://github.com/contributorshipcollaboration/credit-translation/issues) or a pull request, and we will add it to this list.

| Tool | Description | Languages used |
| --- | --- | --- |
| [CRediT Matrix](https://credit.duinlab.nl) ([source](https://github.com/simonvanlierde/credit-matrix)) | Free, open-source web app for writing CRediT statements. Co-authors can check their own roles in the app. The translations are also available in the `credit-matrix` npm package, so scripts, Quarto and MyST documents and a command line tool can write the statement in every supported language. The project [credits every translator](https://github.com/simonvanlierde/credit-matrix/blob/main/src/core/credit-i18n/translations/CREDITS.md). | de, es, fr, it, ja, nl, pt-PT, zh-Hans (plus English) |


## Notes for programmers and project coordinators

How the translation file is created:
JSON->new file table of finished languages .md->HTML

How the polished landing page is created, including the [human-readable translations](https://contributorshipcollaboration.github.io/projects/translation/completed/):

Hugo partial, then the top of the page can be edited without affecting the rendering of the list of languages. 
The rendering is done by Github Action which can be triggered by editing the [webpage repo](https://github.com/contributorshipcollaboration/contributorshipcollaboration.github.io/blob/master/README.md
)

### Validating translation files

Every translation in `translations/` is checked against the JSON schema (`credit_translation_schema-X.Y.Z.json`) by a GitHub Action on every pull request and push. To run the same checks on your computer before opening a pull request:

```
pip install -r scripts/requirements.txt
python scripts/validate.py
```

The script reports errors (which must be fixed) and warnings (which should be fixed but do not fail the check). Besides the schema it checks, for example, that:

- the file is named `<languageCode>_<scriptCode>.json`, e.g. `nn_Latn.json`;
- `languageCode` is an [ISO 639](https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes) code, the two-letter ISO 639-1 code wherever one exists (`it`, not `ita`), and `scriptCode` is an [ISO 15924](https://en.wikipedia.org/wiki/ISO_15924) code, e.g. `Latn`;
- each translator's `ORCID` is given as the bare iD (`0000-0000-0000-0000`, not a URL) with a valid checksum, and is left out if the translator has none (do not use `""` or `NA`).

Files you change must use the newest schema: set `"$schema"` to the latest `credit_translation_schema-X.Y.Z.json` in this repository. Files you do not touch may stay on an older schema. Bumping a translation's `version` when its content changes is done by hand.
