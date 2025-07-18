[Previous Folder](../lists/attachment_list.md) | [Previous File](evolved_recipe.md) | [Next File](fixing.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)

# farming.py

## Classes

### `Farming`
#### Class Methods
##### [`_parse_farming_definitions()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L13)
##### [`_load_farming_definitions()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L40)
##### [`from_item(item: Item | str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L64)
##### [`from_recipe(recipe: str | list[str])`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L79)
#### Object Methods
##### [`__init__(crop: str)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L89)
##### [`get_sprite(sprite, dim)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L93)
#### Properties
##### [`crop`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L114)
##### [`data`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L118)
##### [`icon`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L122)
##### [`texture`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L126)
##### [`season_recipe`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L130)
##### [`seed_name`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L134)
##### [`seed_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L141)
##### [`vegetable_item`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L147)
##### [`special_seed`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L151)
##### [`seed_types`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L155)
##### [`sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L161)
##### [`dying_sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L165)
##### [`unhealthy_sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L169)
##### [`dead_sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L173)
##### [`trampled_sprite`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L177)
##### [`time_to_grow`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L183)
##### [`grow_time_days`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L187)
##### [`full_grown_stage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L191)
##### [`mature_stage`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L195)
##### [`harvest_level`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L199)
##### [`water_needed_raw`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L203)
##### [`water_needed`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L207)
##### [`water_level`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L211)
##### [`rot_time`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L215)
##### [`grow_back`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L219)
##### [`harvest_position`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L223)
##### [`sow_month_num`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L229)
##### [`sow_months`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L233)
##### [`best_month_num`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L237)
##### [`best_months`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L241)
##### [`risk_month_num`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L245)
##### [`risk_months`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L249)
##### [`bad_month_num`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L253)
##### [`bad_months`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L257)
##### [`min_veg`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L263)
##### [`max_veg`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L267)
##### [`min_veg_authorized`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L271)
##### [`max_veg_authorized`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L275)
##### [`is_flower`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L281)
##### [`moth_food`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L285)
##### [`moth_bane`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L289)
##### [`aphids_bane`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L293)
##### [`rabbit_bane`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L297)
##### [`cold_hardy`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L301)
##### [`slugs_proof`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L305)
##### [`scythe_harvest`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/objects/farming.py#L309)


[Previous Folder](../lists/attachment_list.md) | [Previous File](evolved_recipe.md) | [Next File](fixing.md) | [Next Folder](../parser/distribution_container_parser.md) | [Back to Index](../../index.md)
