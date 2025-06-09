[Previous Folder](../consumables.md) | [Previous File](setup.md) | [Next File](version.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)

# translate.py

## Functions

### [`get_wiki_translation(value)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/translate.py#L88)

Gets the translations for a value within `<< >>` delimiters for defining the string to translate.

:param str value: The value to be translated. Can be a line with multiple strings wrapped in `<< >>`.
:return: Value with all strings translated.
:rtype: str

### [`change_language()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/translate.py#L109)
### [`detect_file_encoding(file_path)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/translate.py#L127)
### [`get_translation(property_value, property_key, lang_code, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/translate.py#L136)

Searches for the property value based on the property key and language code to return the translation.

:param property_value: Property value to be translated.
:param property_key (optional): Key for the property being translated.
:param lang_code (optional): Language code forced for translations. Leaving empty will use global 'language_code'.
:param default (optional): Default translation to use if no translation can be found. Uses 'property_value' if undefined.
:return: Translation for the property.

### [`parse_translation_file(wiki_language_code, game_language_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/translate.py#L177)
### [`remove_comments(line: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/translate.py#L251)
### [`cache_translations()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/translate.py#L261)
### [`get_language_code()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/translate.py#L288)
### [`set_language_code(new_language_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/translate.py#L296)
### [`update_default_language()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/translate.py#L301)

Updates the default language to the latest config entry.

Use 'get_default_langauge' instead for returning the default language.
:return: Updated default language.

### [`get_default_language()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/translate.py#L313)
### [`init_translations()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/translate.py#L320)
### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/translate.py#L330)


[Previous Folder](../consumables.md) | [Previous File](setup.md) | [Next File](version.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)
