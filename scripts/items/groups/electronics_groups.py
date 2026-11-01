"""Electronics grouping shared by item lists and navboxes."""

from __future__ import annotations

import typing

from scripts.items.item_groups import GroupInfo, ItemGroups

if typing.TYPE_CHECKING:
    from scripts.objects.item import Item


def is_electronics_item(item: "Item") -> bool:
    return bool(item.valid and item.has_category("electronics"))


class ElectronicsGroups(ItemGroups):
    GROUPS: dict[str, GroupInfo] = {
        "generator": GroupInfo("generator", "Generators", "electronics", 1),
        "battery": GroupInfo("battery", "Batteries", "electronics", 2),
        "light_bulb": GroupInfo("light_bulb", "Light bulbs", "electronics", 3),
        "appliance": GroupInfo("appliance", "Appliances", "electronics", 4),
        "component": GroupInfo("component", "Components", "electronics", 5),
        "upgrade": GroupInfo("upgrade", "Upgrades", "electronics", 6),
        "other": GroupInfo("other", "Other", "electronics", 7),
    }

    _context_loaded = False
    _dismantle_inputs: frozenset[str] = frozenset()
    _dismantle_outputs: frozenset[str] = frozenset()
    _upgrade_outputs: frozenset[str] = frozenset()

    @classmethod
    def _ensure_context_loaded(cls) -> None:
        if cls._context_loaded:
            return

        from scripts.objects.craft_recipe import CraftRecipe

        dismantle_inputs: set[str] = set()
        dismantle_outputs: set[str] = set()
        for recipe_id in (
            "DismantleMiscElectronics",
            "DismantleElectronics",
            "DismantlePowerBar",
        ):
            recipe = CraftRecipe(recipe_id)
            dismantle_inputs.update(recipe.input_items)
            dismantle_outputs.update(recipe.output_items)

        upgrade_outputs: set[str] = set()
        for recipe_id in (
            "MakeRemoteTrigger",
            "MakeRemoteControllerV1",
            "MakeRemoteControllerV2",
            "MakeRemoteControllerV3",
            "MakeTimer",
        ):
            upgrade_outputs.update(CraftRecipe(recipe_id).output_items)

        cls._dismantle_inputs = frozenset(dismantle_inputs)
        cls._dismantle_outputs = frozenset(dismantle_outputs)
        cls._upgrade_outputs = frozenset(upgrade_outputs)
        cls._context_loaded = True

    @classmethod
    def classify(cls, item: "Item", **kwargs) -> str:
        cls._ensure_context_loaded()
        if item.has_tag("Generator"):
            return "generator"
        if "Battery" in item.id_type:
            return "battery"
        if "LightBulb" in item.id_type:
            return "light_bulb"
        if (
            item.has_tag("MiscElectronic", "TVRemote")
            or item.item_type == "radio"
            or item.item_id in cls._dismantle_inputs
        ):
            return "appliance"
        if item.item_id in cls._dismantle_outputs or item.item_id in {
            "Base.RadioReceiver",
            "Base.RadioTransmitter",
            "Base.ScannerModule",
        }:
            return "component"
        if item.item_id in cls._upgrade_outputs:
            return "upgrade"
        return "other"

