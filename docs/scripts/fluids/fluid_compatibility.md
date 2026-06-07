[Previous Folder](../core/cache.md) | [Previous File](fluid_article.md) | [Next File](fluid_infobox.md) | [Next Folder](../foraging/foraging_category_infobox.md) | [Back to Index](../../index.md)

# fluid_compatibility.py

## Functions

### [`are_fluids_compatible(fluid1: Fluid, fluid2: Fluid) -> bool`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/fluids/fluid_compatibility.py#L11)

Check if two fluids are compatible for mixing.

Rules:
1. All fluids are compatible with themselves
2. If neither fluid has a whitelist, they are compatible
3. If a fluid has a whitelist, it only allows fluids with categories in its whitelist
4. Both fluids must allow each other (if they have whitelists)

### [`sort_fluids(fluids)`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/fluids/fluid_compatibility.py#L61)

Sort fluids by first category, then alphabetically, with water fluids first

### [`generate_compatibility_table()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/fluids/fluid_compatibility.py#L110)

Generate the compatibility table content

### [`main()`](https://github.com/Vaileasys/pz-wiki_parser/blob/main/scripts/fluids/fluid_compatibility.py#L153)

Main function to generate the fluid compatibility table


[Previous Folder](../core/cache.md) | [Previous File](fluid_article.md) | [Next File](fluid_infobox.md) | [Next Folder](../foraging/foraging_category_infobox.md) | [Back to Index](../../index.md)
