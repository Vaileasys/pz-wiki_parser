"""
Provides the FluidContainer and Durability classes for managing components 
related to fluid handling and durability.

- FluidContainer holds information about an item’s fluid types, capacities, 
  mixing ratios, and special behaviour (e.g., random fluid selection).
- Durability tracks an item’s material and maximum hit points, supporting 
  durability-based mechanics.

These classes serve as lightweight wrappers over raw component data, offering 
convenient property access and helper methods.
"""

from scripts.objects.fluid import Fluid
from scripts.core.language import Translate

class FluidContainer:
    """
    Represents the FluidContainer component of an item or entity, holding information 
    about contained fluids, capacities, and mixing proportions.
    """
    def __init__(self, data: dict):
        """
        Initialize a FluidContainer with raw component data.

        Args:
            data (dict): FluidContainer data dictionary.
        """
        self.data = data or {}

    def __bool__(self):
        """Allow FluidContainer to evaluate as False if empty, True if data exists."""
        return bool(self.data)

    def has_fluid(self, *fluids: Fluid | str | list[Fluid | str]) -> bool:
        """
        Check if the item contains any of the given fluids.

        Args:
            *fluids (Fluid | str | list[Fluid | str]): One or more Fluid objects or fluid ID strings.
                Accepts individual arguments or a list.

        Returns:
            bool: True if any of the fluids are present, False otherwise.
        """
        if not self.is_valid:
            return False

        # Ensure the fluid ID list is prepared
        if not hasattr(self, "_fluid_id_list"):
            self.fluids  # this presumably sets _fluid_id_list

        # Flatten input
        flat_fluids = []
        for f in fluids:
            if isinstance(f, list):
                flat_fluids.extend(f)
            else:
                flat_fluids.append(f)

        # Normalize to Fluid objects
        for f in flat_fluids:
            fluid = f if isinstance(f, Fluid) else Fluid(f)
            if fluid.id_type in self._fluid_id_list:
                return True

        return False

    @property
    def is_valid(self) -> bool:
        return bool(self.data)

    @property
    def container_name(self):
        """Return the translated container name."""
        name = self.data.get("ContainerName")
        name = Translate.get("Fluid_Container_" + name, default=name)
        return name

    @property
    def rain_factor(self):
        """Return the rain collection factor (float)."""
        return self.data.get("RainFactor", 0)

    @property
    def capacity(self):
        """Return the container’s fluid capacity (int)."""
        return self.data.get("Capacity", 0)

    @property
    def custom_drink_sound(self):
        """Return the custom drink sound, if defined (str or None)."""
        return self.data.get("CustomDrinkSound")

    @property
    def fluids(self):
        """Return a list of Fluid objects, including mix ratios and optional colors."""
        if not self.is_valid:
            return
        if not hasattr(self, "_fluids"):
            fluids_data = self.data.get("Fluids", {})

            if isinstance(fluids_data, dict):
                fluid_list = fluids_data.get("fluid", [])
            elif isinstance(fluids_data, list) and not fluids_data:
                fluid_list = []
            else:
                fluid_list = []

            self._fluids = []
            self._fluid_id_list = []
            for fluid in fluid_list:
                fluid_id = fluid[0]
                self._fluid_id_list.append(fluid_id)
                mix_ratio = fluid[1] if len(fluid) > 1 else 1.0

                color = None
                if len(fluid) >= 5:
                    possible_color = fluid[2:5]
                    if all(isinstance(c, (float, int)) for c in possible_color):
                        color = possible_color

                self._fluids.append(Fluid(fluid_id, mix_ratio=mix_ratio, color=color))

        return self._fluids
    
    @property
    def fluid_proportions(self):
        """Return the raw list of fluid proportions (list of floats)."""
        fluids_data = self.data.get("Fluids", {})

        if isinstance(fluids_data, dict):
            fluid_list = fluids_data.get("fluid", [])
        elif isinstance(fluids_data, list) and not fluids_data:
            fluid_list = []
        else:
            fluid_list = []

        return [entry[1] for entry in fluid_list]
    
    @property
    def fluid_map(self):
        """
        Return a dictionary mapping Fluid objects to normalised proportions.
        If PickRandomFluid is True, all fluids are given equal weighting (1.0).
        """
        fluids = self.fluids
        proportions = self.fluid_proportions

        if not fluids:
            return {}

        if self.pick_random_fluid:
            return {fluid: 1.0 for fluid in fluids}

        total = sum(proportions)
        if total == 0:
            normalized = [0 for _ in proportions]
        else:
            normalized = [p / total for p in proportions]

        return dict(zip(fluids, normalized))

    @property
    def pick_random_fluid(self):
        """Return whether the container picks a random fluid (bool)."""
        return self.data.get("PickRandomFluid", False)

    @property
    def initial_percent_min(self):
        """Return the minimum initial fill percentage (float)."""
        return self.data.get("InitialPercentMin", 0.0)

    @property
    def initial_percent_max(self):
        """Return the maximum initial fill percentage (float)."""
        return self.data.get("InitialPercentMax", 1.0)


class Durability:
    """
    Represents the Durability component of an item, including material type 
    and maximum hit points.
    """
    def __init__(self, data: dict):
        """
        Initialize a Durability object with raw component data.

        Args:
            data (dict): Durability data dictionary.
        """
        self.data = data or {}

    def __bool__(self):
        """Allow Durability to evaluate as False if empty, True if data exists."""
        return bool(self.data)

    @property
    def material(self):
        """Return the material type (str), defaults to 'Default'."""
        return self.data.get("Material", "Default")

    @property
    def max_hit_points(self):
        """Return the maximum hit points (int), defaults to 0."""
        return self.data.get("MaxHitPoints", 0)