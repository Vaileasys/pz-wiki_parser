[Previous Folder](../tiles/entity_article.md) | [Next File](diff.md) | [Next Folder](../utils/categories.md) | [Back to Index](../../index.md)

# batch_processor.py

## Functions

### [`_mark_once(key)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/batch_processor.py#L24)

Return True the first time a key is seen in this batch, else False.

### [`reset_mark_once()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/batch_processor.py#L32)

Reset the once_run_scripts set for a new batch.

### [`select_languages()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/batch_processor.py#L37)

Prompt user for language selection.

<ins>**Returns:**</ins>
  - **list**:
      - _List of language codes to process._

### [`setup_language(lang_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/batch_processor.py#L85)

Set up the language system for the specified language code.

<ins>**Args:**</ins>
  - **lang_code (str)**:
      - _Language code to set up_

### [`batch_items(lang_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/batch_processor.py#L104)

Run items batch processing for a single language.

<ins>**Args:**</ins>
  - **lang_code (str)**:
      - _Language code to process_

### [`batch_recipes(lang_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/batch_processor.py#L215)

Run recipes batch processing.

<ins>**Args:**</ins>
  - **lang_code (str)**:
      - _Language code to process (only used for setup, recipes run once per batch)_

### [`batch_tiles(lang_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/batch_processor.py#L236)

Run tiles batch processing.

<ins>**Args:**</ins>
  - **lang_code (str)**:
      - _Language code to process_

### [`batch_fluids(lang_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/batch_processor.py#L248)

Run fluids batch processing.

<ins>**Args:**</ins>
  - **lang_code (str)**:
      - _Language code to process_

### [`batch_lists(lang_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/batch_processor.py#L264)

Run lists batch processing.

<ins>**Args:**</ins>
  - **lang_code (str)**:
      - _Language code to process_

### [`batch_animals(lang_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/batch_processor.py#L310)

Run animals batch processing.

<ins>**Args:**</ins>
  - **lang_code (str)**:
      - _Language code to process_

### [`batch_vehicles(lang_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/batch_processor.py#L332)

Run vehicles batch processing.

<ins>**Args:**</ins>
  - **lang_code (str)**:
      - _Language code to process_

### [`batch_misc(lang_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/batch_processor.py#L356)

Run misc batch processing.

<ins>**Args:**</ins>
  - **lang_code (str)**:
      - _Language code to process_

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/tools/batch_processor.py#L374)

Main function for the items batch processor.


[Previous Folder](../tiles/entity_article.md) | [Next File](diff.md) | [Next Folder](../utils/categories.md) | [Back to Index](../../index.md)
