import script_parser


def weapon_list(parsed_data):
    sorted_items = {}
    translate_names, language_code = script_parser.get_language()

    for module, module_data in parsed_data.items():
        for item_type, item_data in module_data.items():
            if item_data.get("Type") == "Weapon":
                skill = item_data.get("Categories")
                if skill is not None:
                    skill_list = [cat.strip() for cat in skill.split(";")]
                    # remove "Improvised" from list
                    if "Improvised" in skill_list and len(skill_list) > 1:
                        skill_list = [cat for cat in skill_list if cat != "Improvised"]
                    skill = ";".join(skill_list)

                    item_id = f"{module}.{item_type}"
                    item_name = item_data.get("DisplayName")
                    translated_item_name = translate_names.get(item_id, item_name)
                    icon = item_data.get("Icon", "Question")
                    weight = item_data.get("Weight", 1)

                    equipped = "1H"
                    if item_data.get("RequiresEquippedBothHands") == "TRUE":
                        equipped = "{{Tooltip|2H*|Limited impact when used one-handed.}}"
                    elif item_data.get("TwoHandWeapon", "FALSE") == "TRUE":
                        equipped = "2H"

                    damage_min = item_data.get("MinDamage", 0)
                    damage_max = item_data.get("MaxDamage", 0)
                    damage_door = item_data.get("DoorDamage", 0)
                    damage_tree = item_data.get("TreeDamage", 0)
                    min_range = item_data.get("MinRange", 0)
                    max_range = item_data.get("MaxRange", 0)
                    base_speed = item_data.get("BaseSpeed", 0)
                    crit_chance = item_data.get("CriticalChance", 0)
                    crit_multiplier = item_data.get("CritDmgMultiplier", 0)
                    knockback = item_data.get("PushBackMod", 0)
                    condition_max = item_data.get("ConditionMax", 0)
                    condition_chance = item_data.get("ConditionLowerChanceOneIn", 0)
                    condition_average = int(condition_max) * int(condition_chance)

                    # add item to the sorted dictionary
                    if skill not in sorted_items:
                        sorted_items[skill] = []
                    sorted_items[skill].append((item_id, item_name, translated_item_name, icon, weight, equipped, damage_min, damage_max, damage_door, damage_tree, min_range, max_range, base_speed, crit_chance, crit_multiplier, knockback, condition_max, condition_chance, condition_average))
    write_to_output(language_code, sorted_items)                    
                    

def write_to_output(language_code, sorted_items):
    output_file = 'output.txt'
    with open(output_file, 'w', encoding='utf-8') as file:

        lc_subpage = ""
        if language_code != "en":
            lc_subpage = f"/{language_code}"

        file.write("{{Note|content=The contents of this page are <b>auto-generated</b> using the <code>weapon_list</code> module from <code>pz-script_parser</code>. Any edits made to this page will be overridden automatically.}}\n\n")

        for skill in sorted(sorted_items.keys()):
            file.write(f"=={skill}==\n")
            file.write("{| class=\"wikitable theme-red sortable\" style=\"text-align: center;\"\n")
            file.write("! rowspan=2 | Icon\n")
            file.write("! rowspan=2 | Name\n")
            file.write("! rowspan=2 | [[File:Moodle_Icon_HeavyLoad.png|link=|Encumbrance]]\n")
            file.write("! rowspan=2 | [[File:UI_Hands.png|32px|link=|Equipped]]\n")
            file.write("! colspan=4 | Damage\n")
            file.write("! colspan=2 | Range\n")
            file.write("! rowspan=2 | [[File:UI_SwingTime.png|32px|link=|Attack speed]]\n")
            file.write("! rowspan=2 | [[File:UI_Percentage.png|32px|link=|Crit chance]]\n")
            file.write("! rowspan=2 | [[File:UI_PercentageX.png|32px|link=|Crit multiplier]]\n")
            file.write("! rowspan=2 | [[File:UI_Knockback.png|32px|link=|Knockback]]\n")
            file.write("! rowspan=2 | [[File:UI_Durability.png|32px|link=|Max condition]]\n")
            file.write("! rowspan=2 | {{Tooltip|[[File:UI_DurabilityPercent.png]]|Condition lower chance, 1 in (x + (maintenance × 2 + weapon level))}}\n")
            file.write("! rowspan=2 | Av. [[File:UI_Durability.png|32px|link=|Average condition at level 0]]\n")
            file.write("! rowspan=2 | Item ID\n")
            file.write("|-\n")
            file.write("! [[File:UI_Min.png|32px|link=|Minimum]]\n")
            file.write("! [[File:UI_Max.png|32px|link=|Maximum]]\n")
            file.write("! [[File:UI_Door.png|32px|link=|Door damage]]\n")
            file.write("! [[File:Container_Plant.png|32px|link=|Tree damage]]\n")
            file.write("! [[File:UI_Min.png|32px|link=|Minimum]]\n")
            file.write("! style=\"border-right: var(--border-mw);\" | [[File:UI_Max.png|32px|link=|Maximum]]\n")
            for item_id, item_name, translated_item_name, icon, weight, equipped, damage_min, damage_max, damage_door, damage_tree, min_range, max_range, base_speed, crit_chance, crit_multiplier, knockback, condition_max, condition_chance, condition_average in sorted_items[skill]:
                icons_image = f"[[File:{icon}.png]]"
                item_link = f"[[{item_name}]]"

                if language_code != "en":
                    item_link = f"[[{item_name}{lc_subpage}|{translated_item_name}]]"
                file.write(f"|-\n| {icons_image} \n| {item_link} \n| {weight} \n| {equipped} \n| {damage_min} \n| {damage_max} \n| {damage_door} \n| {damage_tree} \n| {min_range} \n| {max_range} \n| {base_speed} \n| {crit_chance} \n| {crit_multiplier} \n| {knockback} \n| {condition_max} \n| {condition_chance} \n| {condition_average} \n| {item_id}\n")
            file.write("|}\n\n")

    print(f"Output saved to {output_file}")


def main():
    weapon_list(script_parser.main())


if __name__ == "__main__":
    main()