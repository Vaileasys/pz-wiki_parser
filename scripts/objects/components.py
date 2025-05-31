from scripts.objects.fluid import Fluid
from scripts.core.language import Translate

class FluidContainer:
    def __init__(self, data: dict):
        self.data = data or {}

    def __bool__(self):
        return bool(self.data)

    @property
    def container_name(self):
        name = self.data.get("ContainerName")
        name = Translate.get("Fluid_Container_" + name, default=name)
        return name

    @property
    def rain_factor(self):
        return self.data.get("RainFactor", 0)

    @property
    def capacity(self):
        return self.data.get("capacity", 0)

    @property
    def custom_drink_sound(self):
        return self.data.get("CustomDrinkSound")

    @property
    def fluids(self):
        """Return a list of Fluid objects, capturing mix ratio and color if provided."""
        fluids_data = self.data.get("Fluids", {})

        if isinstance(fluids_data, dict):
            fluid_list = fluids_data.get("fluid", [])
        elif isinstance(fluids_data, list) and not fluids_data:
            fluid_list = []
        else:
            fluid_list = []

        final_fluids = []
        for fluid in fluid_list:
            fluid_id = fluid[0]
            mix_ratio = fluid[1] if len(fluid) > 1 else 1.0

            color = None
            if len(fluid) >= 5:
                possible_color = fluid[2:5]
                if all(isinstance(c, (float, int)) for c in possible_color):
                    color = possible_color

            final_fluids.append(Fluid(fluid_id, mix_ratio=mix_ratio, color=color))

        return final_fluids
    
    @property
    def fluid_proportions(self):
        """Return the raw list of fluid proportions."""
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
        Return a dict mapping Fluid objects to normalised proportions.
        If PickRandomFluid is True, just map each Fluid to 1.0 (equal chance).
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
        return self.data.get("PickRandomFluid", False)

    @property
    def initial_percent_min(self):
        return self.data.get("InitialPercentMin", 0.0)

    @property
    def initial_percent_max(self):
        return self.data.get("InitialPercentMax", 1.0)


class Durability:
    def __init__(self, data: dict):
        self.data = data or {}

    def __bool__(self):
        return bool(self.data)

    @property
    def material(self):
        return self.data.get("Material", "Default")

    @property
    def max_hit_points(self):
        return self.data.get("MaxHitPoints", 0)