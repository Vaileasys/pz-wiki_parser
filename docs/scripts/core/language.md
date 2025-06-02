[Previous Folder](../article_content/hotbar_slots_content.md) | [Previous File](file_loading.md) | [Next File](logger.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)

# language.py

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
##### [`prompt()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L100)

### `Translate`
#### Static Methods
##### [`_remove_comments(line: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L264)
#### Class Methods
##### [`get(property_value, property_key, lang_code, default)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L163)

Get a translation for a given value, using optional prefix logic.

##### [`get_wiki(value: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L179)

Translate all wiki-style placeholders (<< >>) inside a string.

##### [`load()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L188)

Force-load all translation data, bypassing lazy init.

##### [`_ensure_loaded()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L198)
##### [`_cache()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L203)
##### [`_parse(wiki_code, game_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/core/language.py#L220)


[Previous Folder](../article_content/hotbar_slots_content.md) | [Previous File](file_loading.md) | [Next File](logger.md) | [Next Folder](../fluids/fluid_article.md) | [Back to Index](../../index.md)
