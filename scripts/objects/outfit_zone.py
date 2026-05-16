"""
Provides access to outfit zombie zone spawn data.

OutfitZone loads parsed ZombiesZoneDefinition data and provides helpers for
finding which zombie zones reference a given outfit ID.
"""

from scripts.parser import outfit_zone_parser


class OutfitZone:
    """Provides cached lookup for outfit zombie zone spawn data."""
    _data: dict | None = None

    @classmethod
    def load(cls, force: bool = False) -> dict:
        """
        Load outfit zone data.

        Args:
            force: Reload data even if already loaded.
        """
        if cls._data is not None and not force:
            return cls._data

        cls._data = outfit_zone_parser.parse_outfit_zones(
            force_regenerate=force,
        )

        return cls._data

    @classmethod
    def all(cls) -> dict:
        """Return all outfit zone data."""
        return cls.load()

    @classmethod
    def get(cls, outfit_id: str) -> list[dict]:
        """
        Return zones that reference an outfit ID.

        Args:
            outfit_id: Outfit ID to search for.
        """
        data = cls.load()

        found_zones = []

        for table_name, table_data in data.items():
            if not isinstance(table_data, dict):
                continue

            for zone_name, zone_info in table_data.items():
                if not isinstance(zone_info, dict):
                    continue

                for outfit_key, outfit_data in zone_info.items():
                    if not isinstance(outfit_data, dict):
                        continue

                    if outfit_data.get("name", "") == outfit_id:
                        found_zones.append(
                            {
                                "zone_name": zone_name,
                                "outfit_key": outfit_key,
                                "outfit_info": outfit_data,
                                "table_name": table_name,
                            }
                        )

        return cls._dedupe_zones(found_zones)

    @classmethod
    def has(cls, outfit_id: str) -> bool:
        """
        Check whether an outfit appears in any zone.

        Args:
            outfit_id: Outfit ID to check.
        """
        return bool(cls.get(outfit_id))

    @staticmethod
    def _dedupe_zones(zones: list[dict]) -> list[dict]:
        """
        Remove duplicate zone names.

        Args:
            zones: Zone match dictionaries.
        """
        seen_zones = set()
        unique_zones = []

        for zone in zones:
            zone_name = zone["zone_name"]

            if zone_name in seen_zones:
                continue

            seen_zones.add(zone_name)
            unique_zones.append(zone)

        return unique_zones