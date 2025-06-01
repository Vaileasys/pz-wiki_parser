[Previous Folder](../fluids/fluid_article.md) | [Next File](item_body_part.md) | [Next Folder](../lists/body_locations_list.md) | [Back to Index](../../index.md)

# item_article.py

## Functions

### [`load_item_id_dictionary(dictionary_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L194)

_Loads the item_id dictionary from a given CSV file._

<ins>**Args:**</ins>
  - **dictionary_dir (str)**:
      - _The path to the CSV file containing the item_id_
      - _dictionary._

<ins>**Returns:**</ins>
  - **dict:**
      - A dictionary with the item_id as the key and the article_name as
      - the value.
### [`generate_intro(lowercase_name, language_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L230)
### [`generate_header(category, skill_type, infobox_version, language_code, name)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L244)
### [`generate_consumable_properties(item_id, consumables_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L327)
### [`generate_condition(name, category, skill_type, infobox, fixing_dir, language_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L343)
### [`generate_crafting(item_id, crafting_dir, teachedrecipes_dir, language_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L377)
### [`generate_building(item_id, building_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L423)
### [`generate_learned_recipes(item_id, teached_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L434)
### [`generate_body_part(item_id, body_parts_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L445)
### [`generate_location(original_filename, infobox_name, item_id, distribution_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L462)
### [`generate_obtaining(item_id, crafting_dir, original_filename, infobox_name, distribution_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L476)
### [`generate_history(item_id, history_dir, language_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L494)
### [`generate_code(item_id, code_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L507)
### [`load_infoboxes(infobox_dir)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L521)
### [`assemble_body(name, original_filename, infobox_name, item_id, category, skill_type, infobox, consumables_dir, fixing_dir, code_dir, distribution_dir, history_dir, crafting_dir, building_dir, teachedrecipes_dir, body_parts_dir, language_code)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L543)
### [`process_files(file_path, output_dir, consumables_dir, item_id_dict, generate_all, fixing_dir, code_dir, distribution_dir, history_dir, crafting_dir, building_dir, teached_dir, body_parts_dir, language_code, pbar)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L593)
### [`main(run_directly)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/items/item_article.py#L672)


[Previous Folder](../fluids/fluid_article.md) | [Next File](item_body_part.md) | [Next Folder](../lists/body_locations_list.md) | [Back to Index](../../index.md)
