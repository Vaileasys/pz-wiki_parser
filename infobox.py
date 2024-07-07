import script_parser

def get_item(parsed_data):
    while True:
        item_id = input("Enter an item id\n>")
        for module, module_data in parsed_data.items():
            for item_type, item_data in module_data.items():
                if f"{module}.{item_type}" == item_id:
                    return item_data, item_id
        print(f"No item found for '{item_id}', please try again.")

def write_to_output(item_data, item_id, translate_names, language_code):
    #TODO add translating
    output_file = 'output.txt'
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("{{Infobox item")
        file.write(f"\n|name = {item_data.get('DisplayName', '')}")
        file.write(f"\n|model = {item_data.get('WeaponSprite', item_data.get('WorldStaticModel', ''))}_Model.png")
        file.write(f"\n|icon = {item_data.get('Icon', 'Question')}.png")
        file.write(f"\n|icon_name = {item_data.get('DisplayName', '')}")

        file.write(f"\n|category = {item_data.get('DisplayCategory', '')}")
        file.write(f"\n|weight = {item_data.get('Weight', 1)}")
        file.write(f"\n|equipped = {item_data.get(None, '')}")  # Replace None with actual key
        file.write(f"\n|attachment_type = {item_data.get('AttachmentType', '')}")
        file.write(f"\n|function = ")
        file.write(f"\n|skill_type = {item_data.get('Categories', item_data.get('SubCategory', ''))}")
        file.write(f"\n|ammo_type = {item_data.get('AmmoType', '')}")
        file.write(f"\n|clip_size = {item_data.get('MaxAmmo', '')}")
        
        file.write(f"\n|material = ")
        file.write(f"\n|material_value = ")
        file.write(f"\n|condition_max = {item_data.get('ConditionMax', '')}")
        file.write(f"\n|condition_lower_chance = {item_data.get('ConditionLowerChanceOneIn', '')}")
        
        file.write(f"\n|damage_type = ")
        file.write(f"\n|min_damage = {item_data.get('MinDamage', '')}")
        file.write(f"\n|max_damage = {item_data.get('MaxDamage', '')}")
        file.write(f"\n|door_damage = {item_data.get('DoorDamage', '')}")
        file.write(f"\n|tree_damage = {item_data.get('TreeDamage', '')}")
        file.write(f"\n|min_range = {item_data.get('MinRange', '')}")
        file.write(f"\n|max_range = {item_data.get('MaxRange', '')}")
        file.write(f"\n|sound_radius = {item_data.get('SoundRadius', '')}")
        file.write(f"\n|base_speed = {item_data.get('BaseSpeed', '')}")
        file.write(f"\n|push_back = {item_data.get('PushBackMod', '')}")
        file.write(f"\n|aiming_time = {item_data.get('AimingTime', '')}")
        file.write(f"\n|reload_time = {item_data.get('ReloadTime', '')}")
        file.write(f"\n|crit_chance = {item_data.get('CriticalChance', '')}")
        file.write(f"\n|crit_multiplier = {item_data.get('CritDmgMultiplier', '')}")
        file.write(f"\n|kill_move = {item_data.get('CloseKillMove', '').replace('_', ' ').lower().capitalize() if item_data.get('CloseKillMove') else ''}")
        
        file.write(f"\n|tag = ")
        file.write(f"\n|item_id = {item_id}")
        file.write("\n}}")
    print(f"Output saved to {output_file}")

def main():
    parsed_data = script_parser.main()
    item_data, item_id = get_item(parsed_data)
    translate_names, language_code = script_parser.get_language()
    write_to_output(item_data, item_id, translate_names, language_code)

if __name__ == "__main__":
    main()
