[Previous Folder](../fluids/fluid_article.md) | [Next File](item_body_part.md) | [Next Folder](../lists/body_locations_list.md) | [Back to Index](../../index.md)

# item_article.py

## Functions

### [`load_item_id_dictionary(dictionary_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L193)

_Loads the item_id dictionary from a given CSV file._

<ins>**Args:**</ins>
  - **dictionary_dir (str)**:
      - _The path to the CSV file containing the item_id_
      - _dictionary._

<ins>**Returns:**</ins>
  - **dict:**
      - A dictionary with the item_id as the key and the article_name as
      - the value.

### [`generate_intro(lowercase_name, language_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L229)
### [`generate_header(category, skill_type, infobox_version, language_code, name)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L243)
### [`generate_consumable_properties(item_id, consumables_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L326)
### [`generate_condition(name, category, skill_type, infobox, fixing_dir, language_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L342)
### [`generate_crafting(item_id, crafting_dir, teachedrecipes_dir, language_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L376)
### [`generate_building(item_id, building_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L422)
### [`generate_learned_recipes(item_id, teached_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L433)
### [`generate_body_part(item_id, body_parts_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L444)
### [`generate_location(original_filename, infobox_name, item_id, distribution_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L461)
### [`generate_obtaining(item_id, crafting_dir, original_filename, infobox_name, distribution_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L475)
### [`generate_history(item_id, history_dir, language_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L493)
### [`generate_code(item_id, code_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L506)
### [`load_infoboxes(infobox_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L520)
### [`assemble_body(name, original_filename, infobox_name, item_id, category, skill_type, infobox, consumables_dir, fixing_dir, code_dir, distribution_dir, history_dir, crafting_dir, building_dir, teachedrecipes_dir, body_parts_dir, language_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L542)
### [`process_files(file_path, output_dir, consumables_dir, item_id_dict, generate_all, fixing_dir, code_dir, distribution_dir, history_dir, crafting_dir, building_dir, teached_dir, body_parts_dir, language_code, pbar)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L592)
### [`main(run_directly)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L671)


[Previous Folder](../fluids/fluid_article.md) | [Next File](item_body_part.md) | [Next Folder](../lists/body_locations_list.md) | [Back to Index](../../index.md)
