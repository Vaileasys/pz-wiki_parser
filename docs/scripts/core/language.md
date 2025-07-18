[Previous Folder](../roomdefine.md) | [Previous File](file_loading.md) | [Next File](logger.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)

# language.py

## Functions

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L270)

## Classes

### `Language`
#### Static Methods
##### [`get_encoding(code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L109)
##### [`get_language_name(code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L113)
##### [`get_game_code(wiki_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L117)
#### Class Methods
##### [`get()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L49)
##### [`set(code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L55)
##### [`reset()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L60)
##### [`get_default()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L66)
##### [`get_subpage()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L72)
##### [`set_subpage(code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L78)
##### [`set_default(code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L83)
##### [`update_default()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L87)
##### [`init()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L92)
##### [`_prompt()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L100)

### `Translate`
#### Static Methods
##### [`_remove_comments(line: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L265)
#### Class Methods
##### [`get(property_value, property_key, lang_code, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L164)

Get a translation for a given value, using optional prefix logic.

##### [`get_wiki(value: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L180)

Translate all wiki-style placeholders (<< >>) inside a string.

##### [`load()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L189)

Force-load all translation data, bypassing lazy init.

##### [`_ensure_loaded()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L199)
##### [`_cache()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L204)
##### [`_parse(wiki_code, game_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L221)


[Previous Folder](../roomdefine.md) | [Previous File](file_loading.md) | [Next File](logger.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)
