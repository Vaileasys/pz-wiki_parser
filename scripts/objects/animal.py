import os
from scripts.utils import lua_helper, util, echo
from scripts.core.cache import save_cache, load_cache
from scripts.core.language import Translate
from scripts.core.constants import CACHE_DIR
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from scripts.objects.item import Item
    from scripts.objects.fluid import Fluid
    from scripts.objects.animal_part import AnimalPart
#    from scripts.objects.zone import RanchZone


class Animal:
    """Represents a single animal entry."""
    _raw_data: dict = None
    _animals_data: dict = None
    _breeds_data: dict = None
    _stages_data: dict = None
    _genome_data: dict = None
    _animal_avatar_data: dict = None

    _stage_animals: dict[str, set[str]] = {}
    _instances = {}
    _data_file = "parsed_animal_data.json"
    _avatar_data_file = "parsed_animal_avatar_data.json"

    def __new__(cls, animal_id: str):
        """Ensures only one Animal instance exists per animal ID."""
        if not cls._animals_data:
            cls.load()
            cls.load_avatar()

        if animal_id in cls._instances:
            return cls._instances[animal_id]

        instance = super().__new__(cls)
        cls._instances[animal_id] = instance
        return instance

    def __init__(self, animal_id: str):
        """Initialise the Animal instance with its data if not already initialised."""
        if hasattr(self, 'animal_id'):
            return

        if Animal._animals_data is None:
           Animal.load()

        if Animal._animal_avatar_data is None:
            Animal.load_avatar()

        self.animal_id = animal_id
        self._data = Animal._animals_data.get(animal_id, {})
        self._avatar_data = Animal._animal_avatar_data.get(animal_id, {})

    @classmethod
    def _parse(cls):
        """
        Parses Animal data from the provided Lua file and caches it.
        """
        def _split_commas(obj):
            """Recursively split strings with commas into lists."""
            if isinstance(obj, dict):
                return {k: _split_commas(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [_split_commas(v) for v in obj]
            elif isinstance(obj, str) and "," in obj:
                return [s.strip() for s in obj.split(",")]
            return obj
        
        lua_copy_table = ("""
            function copyTable(tbl)
                local copy = {}
                for k, v in pairs(tbl) do
                    if type(v) == "table" then
                        copy[k] = copyTable(v)  -- Recursively copy nested tables
                    else
                        copy[k] = v
                    end
                end
                return copy
            end
        """)
        animal_files = [
            'ChickenDefinitions.lua',
            'CowDefinitions.lua',
            'DeerDefinitions.lua',
            'MouseDefinitions.lua',
            'PigDefinitions.lua',
            'RabbitDefinitions.lua',
            'RaccoonDefinitions.lua',
            'RatDefinitions.lua',
            'SheepDefinitions.lua',
            'TurkeyDefinitions.lua',
        ]
        lua_runtime = lua_helper.load_lua_file(animal_files, inject_lua=lua_copy_table)
        parsed_data = lua_helper.parse_lua_tables(lua_runtime, tables="AnimalDefinitions")
        
        # Split any values separated by a comma into a list
        parsed_data = _split_commas(parsed_data)

        cls._raw_data = parsed_data.get("AnimalDefinitions", {})

        save_cache(cls._raw_data, cls._data_file)

        return cls._raw_data
    
    @classmethod
    def _parse_avatar(cls):
        """
        Parse animal avatar data.
        """
        ISODIRECTIONS = """
        IsoDirections = {
            SE = "SE",
            SW = "SW"
        }
        """

        lua_runtime = lua_helper.load_lua_file("AnimalAvatarDefinition.lua", inject_lua=ISODIRECTIONS)
        parsed_data = lua_helper.parse_lua_tables(lua_runtime, tables="AnimalAvatarDefinition")

        cls._animal_avatar_data = parsed_data.get("AnimalAvatarDefinition", {})

        save_cache(cls._animal_avatar_data, cls._avatar_data_file)

        return cls._animal_avatar_data


    @classmethod
    def load(cls, attribute: str = None):
        """
        Loads Animal data from the cache, re-parsing the Lua file if the data is outdated.

        Returns:
            dict: Raw Animal data.
        """
        from scripts.core.version import Version
        if cls._raw_data is None:
            path = os.path.join(CACHE_DIR, cls._data_file)

            data, version = load_cache(path, cache_name="animal", get_version=True)

            # Re-parse if outdated
            if version != Version.get():
                data = cls._parse()

            cls._raw_data = data

            cls._animals_data = cls._raw_data.get("animals")
            cls._breeds_data = cls._raw_data.get("breeds")
            cls._genome_data = cls._raw_data.get("genome")
            cls._stages_data = cls._raw_data.get("stages")
        
        if attribute is not None and hasattr(cls, attribute):
            return getattr(cls, attribute)

        return cls._animals_data
    

    @classmethod
    def load_avatar(cls):
        from scripts.core.version import Version
        if cls._animal_avatar_data is None:
            path = os.path.join(CACHE_DIR, cls._avatar_data_file)

            data, version = load_cache(path, cache_name="animal avatar", get_version=True)

            # Re-parse if outdated
            if version != Version.get():
                data = cls._parse_avatar()

            cls._animal_avatar_data = data

        return cls._animal_avatar_data
    
    @classmethod
    def all(cls) -> dict[str, "Animal"]:
        """
        Returns all known Animal instances.

        Returns:
            dict[str, Animal]: Mapping of item ID to Animal instance.
        """
        if not cls._animals_data:
            cls.load()
        return {id: cls(id) for id in cls._animals_data}
    
    @classmethod
    def count(cls) -> int:
        """
        Returns the total number of Animal types parsed.

        Returns:
            int: Number of unique Animal types.
        """
        if not cls._animals_data:
            cls.load()
        return len(cls._animals_data)
    
    @classmethod
    def exists(cls, animal_id: str) -> bool:
        """
        Checks if a Animal with the given id exists in the parsed data.

        Returns:
            bool: True if found, False otherwise.
        """
        if not cls._animals_data:
            cls.load()
        return animal_id in cls._animals_data
    
    def get(self, key: str, default=None):
        """
        Returns a raw value from the animal data.

        Args:
            key (str): Key to look up.
            default: Value to return if key is missing.

        Returns:
            Any: Value from the raw data or default.
        """
        return self.data.get(key, default)
    
    def get_avatar(self, key: str, default=None):
        """
        Returns a raw value from the animal avatar data.

        Args:
            key (str): Key to look up.
            default: Value to return if key is missing.

        Returns:
            Any: Value from the raw data or default.
        """
        return self.avatar_data.get(key, default)

    def _translate_month(self, month: int):
        from scripts.core.language import Translate
        return Translate.get(f"Sandbox_StartMonth_option{month}")

    @property
    def is_valid(self) -> bool:
        return self.animal_id in Animal._animals_data
    
    @property
    def data(self) -> dict:
        return self._data
    
    @property
    def avatar_data(self) -> dict:
        return self._avatar_data
    
    @property
    def item(self) -> "Item":
        from scripts.objects.item import Item
        return Item(self.animal_id)
    
    @property
    def name(self) -> str:
        return Translate.get("IGUI_AnimalType_" + self.animal_id, default=self.animal_id)
    
    @property
    def name_en(self) -> str:
        return Translate.get("IGUI_AnimalType_" + self.animal_id, lang_code="en", default=self.animal_id)
    
    @property
    def corpse_name(self) -> str:
        return Translate.get("IGUI_Item_AnimalCorpse").replace("%1", self.name)
    
    @property
    def corpse_name_en(self) -> str:
        return Translate.get("IGUI_Item_AnimalCorpse", lang_code="en").replace("%1", self.name_en)
    
    @property
    def skeleton_name(self) -> str:
        return Translate.get("IGUI_Item_AnimalSkeleton").replace("%1", self.name)
    
    @property
    def skeleton_name_en(self) -> str:
        return Translate.get("IGUI_Item_AnimalSkeleton", lang_code="en").replace("%1", self.name_en)
    
    @property
    def page(self) -> str: # TODO: get from page dict
        return self.group_name_en
    
    @property
    def wiki_link(self) -> str:
        return util.link(self.page, self.name)
    
    # --- Base --- #
    @property
    def group(self) -> str: return self.get("group")
    @property
    def group_name(self) -> str:
        return Translate.get("IGUI_Animal_Group_" + self.group, default=self.group)
    @property
    def group_name_en(self) -> str: return Translate.get("IGUI_Animal_Group_" + self.group, lang_code="en", default=self.group)
    @property
    def group_link(self) -> str: return util.link(self.page, self.group_name)
    @property
    def base_encumbrance(self) -> float: return self.get("baseEncumbrance", 1.0)
    @property
    def trailer_base_size(self) -> float | None: return self.get("trailerBaseSize")
    @property
    def carcass_item(self) -> "Item | None":
        from scripts.objects.item import Item
        if not hasattr(self, "_carcass_item"):
            carcass_item = self.get("carcassItem")
            if Item.exists(carcass_item):
                self._carcass_item = Item(carcass_item)
            else:
                self._carcass_item = None
        return self._carcass_item
    @property
    def min_weight(self) -> float: return self.get("minWeight", 10.0)
    @property
    def max_weight(self) -> float: return self.get("maxWeight", 100.0)
    @property
    def min_size(self) -> float | None: return self.get("minSize")
    @property
    def max_size(self) -> float | None: return self.get("maxSize")
    @property
    def animal_size(self) -> float | None: return self.get("animalSize")
    @property
    def corpse_size(self) -> float: return self.get("corpseSize", 1.0)
    @property
    def collision_size(self) -> float: return self.get("collisionSize", 0.0)
    @property
    def texture_skeleton_bloody(self) -> str | None: return self.get("textureSkeletonBloody")
    @property
    def icon(self) -> str:
        if not hasattr(self, "_icon"):
            icons = [breed.icon for breed in self.breeds]
            if icons == 1:
                self._icon = "".join(icons)
            else:
                self._icon = f'<span class="cycle-img">{"".join(icons)}</span>'
        return self._icon
    @property
    def icon_all(self) -> str:
        if not hasattr(self, "_icon_all"):
            icons = [breed.icon for breed in self.breeds]
            self._icon = "".join(icons)
        return self._icon
    @property
    def icon_dead(self) -> str:
        if not hasattr(self, "_icon_dead"):
            icons = [breed.icon_dead for breed in self.breeds]
            if icons == 1:
                self._icon_dead = "".join(icons)
            else:
                self._icon_dead = f'<span class="cycle-img">{"".join(icons)}</span>'
        return self._icon_dead
    @property
    def icon_dead_all(self) -> str:
        if not hasattr(self, "_icon_dead_all"):
            icons = [breed.icon_dead for breed in self.breeds]
            self._icon_dead_all = "".join(icons)
        return self._icon_dead_all
    @property
    def icon_skeleton(self) -> str:
        if not hasattr(self, "_icon_skeleton"):
            icons = [breed.icon_skeleton for breed in self.breeds]
            if icons == 1:
                self._icon_skeleton = "".join(icons)
            else:
                self._icon_skeleton = f'<span class="cycle-img">{"".join(icons)}</span>'
        return self._icon_skeleton
    @property
    def icon_skeleton_all(self) -> str:
        if not hasattr(self, "_icon_skeleton_all"):
            icons = [breed.icon_skeleton for breed in self.breeds]
            self._icon_skeleton_all = "".join(icons)
        return self._icon_skeleton_all
    @property
    def model(self) -> str:
        if not hasattr(self, "_model"):
            models = []
            for breed in self.breeds:
                models.extend(breed.models)
            if models == 1:
                self._model = "".join(models)
            else:
                self._model = f'<span class="cycle-img">{"".join(models)}</span>'
        return self._model
    @property
    def model_all(self) -> str:
        if not hasattr(self, "_model_all"):
            models = []
            for breed in self.breeds:
                models.extend(breed.models)
            self._model_all = "".join(models)
        return self._model_all


    # --- Physiology and stats --- #
    @property
    def hunger_multiplier(self) -> float: return self.get("hungerMultiplier", 0.0) # Thirst rate per hour
    @property
    def thirst_multiplier(self) -> float: return self.get("thirstMultiplier", 0.0)
    @property
    def hunger_boost(self) -> float: return self.get("hungerBoost", 1.0)
    @property
    def thirst_boost(self) -> float: return self.get("thirstBoost", 1.0) # Thirst reduced (thirstBoost * 0.2), and fluid consumed (thirstBoost / 0.5L)
    @property
    def health_loss_multiplier(self) -> float: return self.get("healthLossMultiplier", 0.05)
    @property
    def max_blood(self) -> int | None: return self.get("maxBlood")
    @property
    def min_blood(self) -> int | None: return self.get("minBlood")
    @property
    def min_body_part(self) -> int: return self.get("minBodyPart", 0)
    @property
    def daily_water(self) -> str:
        thirst_increased = self.thirst_multiplier * 24 # Thirst increased per 24 hours
        thirst_reduction = 0.2 * self.thirst_boost # Thirst reduced per drink
        fluid_per_drink = 0.5 / self.thirst_boost # Fluid (L) reduced from source per drink

        drinks_needed = thirst_increased / thirst_reduction # Number of drinks needed per 24 hours
        fluid_needed = drinks_needed * fluid_per_drink
        
        # Return early and hardcode the value
        # Still displays as 0 mL for animals that don't consume any water
        if 0 < fluid_needed < 0.001:
            return "<1 mL"
        return util.convert_unit(round(fluid_needed, 3), unit="L") # Fluid needed in 24 hours (automatically sets the appropriate SI unit)
    @property
    def daily_hunger(self) -> float:
        hunger_increased = self.hunger_multiplier * 24 # Hunger increased per 24 hours
        hunger_per_unit = 1 * self.hunger_boost # Hunger reduced per unit of food (assumes -1 hungerChange)

        hunger_needed = hunger_increased / hunger_per_unit

        if 0 < hunger_needed < 0.001:
            return "<0.001"

        return round(hunger_needed, 3)

    # --- Behaviour and AI --- #
    @property
    def can_be_pet(self) -> bool: return self.get("canBePet", False)
    @property
    def can_thump(self) -> bool: return self.get("canThump", True)
    @property
    def can_be_picked(self) -> bool: return self.get("canBePicked", True)
    @property
    def always_flee_humans(self) -> bool: return self.get("alwaysFleeHumans", True)
    @property
    def flee_zombies(self) -> bool: return self.get("fleeZombies", True)
    @property
    def stress_under_rain(self) -> bool: return self.get("stressUnderRain", False)
    @property
    def stress_above_ground(self) -> bool: return self.get("stressAboveGround", False)
    @property
    def can_climb_fences(self) -> bool: return self.get("canClimbStairs", False)
    @property
    def sit_randomly(self) -> bool: return self.get("sitRandomly", False)
    @property
    def dont_attack_other_male(self) -> bool: return self.get("dontAttackOtherMale", False)
    @property
    def can_be_fed_by_hand(self) -> bool: return self.get("canBeFeedByHand", False)
    @property
    def feed_by_hand_type(self) -> list[str]:
        value = self.get("feedByHandType")
        if isinstance(value, str):
            value = [value]
        return value
    @property
    def knockdown_attack(self) -> bool: return self.get("knockdownAttack", False)
    @property
    def eat_grass(self) -> bool: return self.get("eatGrass", False)
    @property
    def can_do_laceration(self) -> bool: return self.get("canDoLaceration", False)
    @property
    def can_be_attached(self) -> bool: return self.get("canBeAttached", False)
    @property
    def can_be_transported(self) -> bool: return self.get("canBeTransported", False)
    @property
    def attack_dist(self) -> int: return self.get("attackDist", 1)
    @property
    def attack_timer(self) -> int: return self.get("attackTimer", 1000)
    @property
    def attack_if_stressed(self) -> bool: return self.get("attackIfStressed", False)
    @property
    def attack_back(self) -> bool: return self.get("attackBack", False)
    @property
    def base_dmg(self) -> float: return self.get("baseDmg", 0.5)
    @property
    def thirst_hunger_trigger(self) -> float: return self.get("thirstHungerTrigger", 0.1)
    @property
    def enter_hutch_time(self) -> int: return self.get("enterHutchTime", 0)
    @property
    def exit_hutch_time(self) -> int: return self.get("exitHutchTime", 0)
    @property
    def idle_type_nbr(self) -> int: return self.get("idleTypeNbr", 0)
    @property
    def eating_type_nbr(self) -> int: return self.get("eatingTypeNbr", 0)
    @property
    def sitting_type_nbr(self) -> int: return self.get("sittingTypeNbr", 0)
    @property
    def periodic_run(self) -> bool: return self.get("periodicRun", False)
    @property
    def male(self) -> bool: return self.get("male", False)
    @property
    def female(self) -> bool: return self.get("female", False)
    @property
    def baby(self) -> bool: return not self.male and not self.female # If it's not male or female, we assume it's a baby
    @property
    def gender(self) -> str:
        gender = "Female" if self.female else "Male" if self.male else "Baby" # If it's not male or female, we assume it's a baby
        translation = Translate.get("IGUI_Animal_" + gender, default=gender)
        return translation
    @property
    def udder(self) -> bool: return self.get("udder", False)
    @property
    def wild(self) -> bool: return self.get("wild", False)
    @property
    def eat_from_mother(self) -> bool: return self.get("eatFromMother", False)
    @property
    def need_mom(self) -> bool: return self.get("needMom", True)
    @property
    def can_climb_stairs(self) -> bool: return self.get("canClimbStairs", False)
    @property
    def add_tracking_xp(self) -> bool: return self.get("addTrackingXp", True)
    @property
    def wild_flee_time_until_dead_timer(self) -> int: return self.get("wildFleeTimeUntilDeadTimer", 0.0)
    @property
    def spotting_dist(self) -> int: return self.get("spottingDist", 10)
    @property
    def can_be_alerted(self) -> bool: return self.get("canBeAlerted", False)
    @property
    def can_be_domesticated(self) -> bool: return self.get("canBeDomesticated", True)
    @property
    def litter_eat_together(self) -> bool: return self.get("litterEatTogether", False)

    # --- Genetics and breeding --- #
    @property
    def genes(self) -> dict:
        return self.get("genes", {})
    @property
    def stages(self) -> dict:
        return self.get("stages", {})
    @property
    def stage(self) -> dict:
        return self.stages.get(self.animal_id, {})
    @property
    def breeds(self) -> "list[AnimalBreed]":
        if not hasattr(self, "_breeds"):
            breed_data: dict = self.get("breeds", {})
            self._breeds = [
                AnimalBreed(self.animal_id, breed_id)
                for breed_id in breed_data
            ]
        return self._breeds
    @property
    def mating_period_start(self) -> int: return self.get("matingPeriodStart", 0) # Zero means no period
    @property
    def mating_period_month_start(self) -> str | None: return self._translate_month(self.mating_period_start) if self.mating_period_start else None
    @property
    def mating_period_end(self) -> int: return self.get("matingPeriodEnd", 0) # Zero means no period
    @property
    def mating_period_month_end(self) -> str | None: return self._translate_month(self.mating_period_end) if self.mating_period_end else None
    @property
    def min_age(self) -> int | None:
        return 0 if self.baby else self.get("minAge")
    @property
    def max_age(self) -> int | None:
        return self.stage.get("ageToGrow") if self.baby else self.get("maxAgeGeriatric")
    @property
    def min_age_for_baby(self) -> int | None: return self.get("minAgeForBaby")
    @property
    def baby_type(self) -> str | None: return self.get("babyType")
    @property
    def mate(self) -> str | None: return self.get("mate")
    @property
    def baby_nbr(self) -> str | None: return self.get("babyNbr")
    @property
    def pregnant_period(self) -> int: return self.get("pregnantPeriod", 0)
    @property
    def time_before_next_pregnancy(self) -> int: return self.get("timeBeforeNextPregnancy", 0)
    @property
    def can_be_milked(self) -> bool: return self.get("canBeMilked", False)
    @property
    def min_milk(self) -> float: return self.get("minMilk", 0.0)
    @property
    def max_milk(self) -> float: return self.get("maxMilk", 0.0)
    @property
    def min_baby(self) -> int: return self.get("minBaby", 1)
    @property
    def max_baby(self) -> int: return self.get("maxBaby", 1)
    @property
    def eggs_per_day(self) -> int: return self.get("eggsPerDay", 0)
    @property
    def egg_type(self) -> "Item | None":
        from scripts.objects.item import Item
        return Item(self.get("eggType")) if self.get("eggType") else None
    @property
    def fertilized_time_max(self) -> int: return self.get("fertilizedTimeMax", 0) # Number of hours - divide by 24 for number of days
    @property
    #Note: Hatch time is dependent on sandbox settings. Apocalypse is 'Fast', which is floor(0.7 * timeToHatch) (see Food.setTimeToHatch())
    def time_to_hatch(self) -> int: return self.get("timeToHatch", 0) # Number of hours - divide by 24 for number of days

    # --- Animation and visuals --- #
    @property
    def model_script(self) -> str | None: return self.get("modelscript")
    @property
    def anim_set(self) -> str | None: return self.get("animset")
    @property
    def texture_skinned(self) -> str | None: return self.get("textureSkinned")
    @property
    def texture_skeleton(self) -> str | None: return self.get("textureSkeleton")
    @property
    def texture_skeleton_bloody(self) -> str | None: return self.get("textureSkeletonBloody")
    @property
    def body_model(self) -> str | None: return self.get("bodyModel")
    @property
    def body_model_skel(self) -> str | None: return self.get("bodyModelSkel")
    @property
    def body_model_skel_no_head(self) -> str | None: return self.get("bodyModelSkelNoHead")
    @property
    def body_model_headless(self) -> str | None: return self.get("bodyModelHeadless")
    @property
    def rope_bone(self) -> str: return self.get("ropeBone", "Bip01_Head")
    @property
    def shadow_w(self) -> float | None: return self.get("shadoww")
    @property
    def shadow_fm(self) -> float | None: return self.get("shadowfm")
    @property
    def shadow_bm(self) -> float | None: return self.get("shadowbm")
    @property
    def idle_emote_chance(self) -> int: return self.get("idleEmoteChance", 1000)

    # --- Sound --- #
    @property
    def sounds(self) -> dict: return self.get("sounds", {})
    @property
    def idle_sound_radius(self) -> float: return self.get("idleSoundRadius", 0.0)
    @property
    def idle_sound_volume(self) -> float: return self.get("idleSoundVolume", 0.0)

    # --- Misc --- #
    @property
    def dung(self) -> "Item | None":
        from scripts.objects.item import Item
        if not hasattr(self, "_dung"):
            dung = self.get("dung")
            if Item.exists(dung):
                self._dung = Item(dung)
            else:
                self._dung = None
        return self._dung
    @property
    def dung_chance_per_day(self) -> int: return self.get("dungChancePerDay", 50)
    @property
    def min_enclosure_size(self) -> float | None: return self.get("minEnclosureSize")
    @property
    def eat_type_trough(self) -> list[str] | None:
        value = self.get("eatTypeTrough", [])
        if isinstance(value, str):
            value = [value]
        return value
    @property
    def hutches(self) -> list[str]:
        value = self.get("hutches", [])
        if isinstance(value, str):
            value = [value]
        return value
    #TODO: Create a 'food' property that returns a list of all foods organised by the food type
    @property
    def food_types(self) -> dict[str, str]:
        #TODO: Refactor this to use a cache
        from scripts.objects.item import Item
        from scripts.objects.fluid import Fluid
        if not hasattr(self, "_food_types"):
            self._food_types = {}
            for value in self.eat_type_trough:

                value_type = None

                if value == "All":
                    value_type = "All"

                # Check if it's a Fluid/milk
#                elif "milk" in value.lower():
#                    if Fluid.exists(value):
#                        value_type = "Fluid"

                else:
                    # Check if it's an Item
                    if Item.exists(value):
                        value_type = "Item"
                    else:
                        # Loop through items checking for FoodType and AnimalFeedType
                        for item_id, item in Item.items():

                            if item.animal_feed_type == value:
                                value_type = "AnimalFeedType"
                                break

                            elif item.food_type == value:
                                value_type = "FoodType"
                                break
                        
                        if not value_type:
                            echo.warning(f"Animal '{self.animal_id}' has an unknown food type '{value}'.")
                            value_type = "Unknown"

                self._food_types[value] = value_type


        return self._food_types
    
    @property
    def lured_possible_items(self) -> list[str]:
        value = self.get("luredPossibleItems", [])
        if isinstance(value, str):
            value = [value]
        return value
    @property
    def wander_mul(self) -> float: return self.get("wanderMul", 400.0)
    @property
    def max_wool(self) -> float: return self.get("maxWool", 0.0)
    @property
    def min_clutch_size(self) -> int: return self.get("minClutchSize", 0) # Number of eggs laid in one season. E.g. Turkey produce 9-17 eggs per year, starting May
    @property
    def max_clutch_size(self) -> int: return self.get("maxClutchSize", 0)
    @property
    def lay_egg_period_start(self) -> int: return self.get("layEggPeriodStart", 0)
    @property
    def lay_egg_period_month_start(self) -> int: return self._translate_month(self.lay_egg_period_start) if self.lay_egg_period_start else None

#    @property
#    def ranch_zones(self) -> list["RanchZone"]:
#        from scripts.objects.zone import RanchZone
#        if self.animal_id in RanchZone.animal_index():
#            return [RanchZone(z) for z in RanchZone.animal_index().get(self.animal_id, [])]

    @property
    def can_be_hooked(self) -> bool:
        return bool(self.get_avatar("hook"))


    def __repr__(self):
        return f"<Animal {self.animal_id}>"


class AnimalBreed:
    _breeds_data: dict = Animal.load("_breeds_data")
    _instances: dict = {}
    _animal_keys: dict[str, dict[str, str]] = {}

    def __new__(cls, animal_id: str, breed_id: str):
        """Ensures only one instance exists per animal breed."""
        id = Animal(animal_id).group + breed_id

        if id in cls._instances:
            return cls._instances[id]

        instance = super().__new__(cls)
        cls._instances[breed_id] = instance
        return instance

    def __init__(self, animal_id: str, breed_id: str):
        """Initialise the breed instance with its data if not already initialised."""
        id = Animal(animal_id).group + breed_id

        if hasattr(self, 'id'):
            return

        self.id = id # A concatenation of the animal group and breed id. Used to lookup a specific breed in _breeds_data
        self.breed_id = breed_id # The raw key for a specific breed, inside an animal def
        self.animal_id = animal_id # The raw key for a specific animal stage
        self.animal_key = animal_id + breed_id # A concatenation of the animal id and breed id. Used as a bot flag on the wiki and to lookup animal part defs
        self._data = self._breeds_data.get(Animal(animal_id).group, {}).get("breeds", {}).get(breed_id, {})
    
    @classmethod
    def exists(cls, animal_id: str, breed_id: str) -> bool:
        """
        Checks if a animal breed with the given ids exists in the parsed data.

        Returns:
            bool: True if found, False otherwise.
        """
        group = Animal(animal_id).group
        
        if group not in cls._breeds_data:
            return False
        
        
        return breed_id in cls._breeds_data.get(group, {}).get("breeds")
    
    @classmethod
    def build_animal_keys(cls):
        for animal_id, animal in Animal.all().items():
            for breed in animal.breeds:
                animal_key = animal_id + breed.breed_id
                cls._animal_keys[animal_key] = {"animal_id": animal_id, "breed_id": breed.breed_id}
    
    @classmethod
    def get_animal_keys(cls) -> dict:
        if not cls._animal_keys:
            cls.build_animal_keys()
        return cls._animal_keys
    
    @classmethod
    def key_exists(cls, animal_key) -> bool:
        return animal_key in cls.get_animal_keys()
    
    @classmethod
    def from_key(cls, animal_key) -> "AnimalBreed":
        if not cls.key_exists(animal_key):
            echo.warning(f"Animal key '{animal_key}' could not be found. Was it misspelt?")
            return
        
        key_data:dict = cls.get_animal_keys().get(animal_key)
        
        animal_id = key_data.get("animal_id")
        breed_id = key_data.get("breed_id")

        return AnimalBreed(animal_id, breed_id)
    
    @classmethod
    def all(cls) -> "dict[str, AnimalBreed]":
        return {id: cls.from_key(id) for id in cls.get_animal_keys()}
    
    @classmethod
    def count(cls) -> int:
        return len(cls.all())
    
    def get(self, key: str, default=None):
        """
        Returns a raw value from the animal breed data.

        Args:
            key (str): Key to look up.
            default: Value to return if key is missing.

        Returns:
            Any: Value from the raw data or default.
        """
        return self.data.get(key, default)
    
    def format_icon(self, image: str, page: str, name: str, default: str = None) -> str:
        if not image:
            image = default
        return f"[[File:{image}|32x32px|link={page}|{name}]]"
    
    def format_models(self, image: list[str] | str, page: str, name: str, default: str = None) -> list[str]:
        if not image:
            image = default

        if isinstance(image, str):
            image = [image]
        
        images = []
        for img in image:
            images.append(f"[[File:{img}|64x64px|link={page}|{name}]]")

        return images
    
    def get_name(self, stage: str = None) -> str:
        text = self.name
        if stage == "dead":
            text = Translate.get("IGUI_Item_AnimalCorpse").replace("%1", text)
        elif stage == "skeleton":
            text = Translate.get("IGUI_Item_AnimalSkeleton").replace("%1", text)
        return text
    
    def get_link(self, stage: str = None) -> str:
        name = self.get_name(stage)
        return util.link(self.page, name)

    @property
    def is_valid(self) -> bool:
        return AnimalBreed.exists(self.animal_id, self.breed_id)

    @property
    def animal(self) -> Animal:
        return Animal(self.animal_id)
    
    @property
    def data(self) -> dict:
        return self._data
    
    @property
    def name(self) -> str:
        return self.breed_name + " " + self.animal.name
    
    @property
    def name_en(self) -> str:
        return self.breed_name_en + " " + self.animal.name_en
    
    @property
    def breed_name(self) -> str:
        return Translate.get("IGUI_Breed_" + self.breed_id, default=self.breed_id)
    
    @property
    def breed_name_en(self) -> str:
        return Translate.get("IGUI_Breed_" + self.breed_id, lang_code="en", default=self.breed_id)
    
    @property
    def page(self) -> str: #TODO: get from page dict?
        return self.name_en
    
    @property
    def wiki_link(self) -> str:
        return self.get_link()
    
    @property
    def icon(self) -> str:
        return self.format_icon(self.icon_file, self.page, self.name)
    
    @property
    def icons(self) -> list[str]:
        icons = set()
        icons.update([self.icon, self.icon_dead, self.icon_skeleton])
        return list(icons)
    
    @property
    def icon_file(self) -> str:
        if self.animal.baby:
            return self.inv_icon_baby.removeprefix("Item_").removesuffix(".png") + ".png"
        if self.animal.male:
            return self.inv_icon_male.removeprefix("Item_").removesuffix(".png") + ".png"
        # Fallback to female
        return self.inv_icon_female.removeprefix("Item_").removesuffix(".png") + ".png"
    
    @property
    def icon_files(self) -> list[str]:
        icons = []
        icons.extend([self.icon_file, self.icon_dead_file, self.icon_skeleton_file])
        return icons
    
    @property
    def icon_dead(self) -> str:
        return self.format_icon(self.icon_dead_file, self.page, self.get_name("dead"), default=self.icon_file)
    
    @property
    def icon_dead_file(self) -> str:
        if self.animal.baby:
            return self.inv_icon_baby_dead.removeprefix("Item_").removesuffix(".png") + ".png"
        if self.animal.male:
            return self.inv_icon_male_dead.removeprefix("Item_").removesuffix(".png") + ".png"
        # Fallback to female
        return self.inv_icon_female_dead.removeprefix("Item_").removesuffix(".png") + ".png"
    
    @property
    def icon_skeleton(self) -> str:
        return self.format_icon(self.icon_skeleton_file, self.page, self.get_name("skeleton"), default=self.icon_dead_file or self.icon_file)
    
    @property
    def icon_skeleton_file(self) -> str:
        if self.animal.baby:
            return self.inv_icon_baby_skel.removeprefix("Item_").removesuffix(".png") + ".png" if self.inv_icon_baby_skel else None
        if self.animal.male:
            return self.inv_icon_male_skel.removeprefix("Item_").removesuffix(".png") + ".png" if self.inv_icon_male_skel else None
        # Fallback to female
        return self.inv_icon_female_skel.removeprefix("Item_").removesuffix(".png") + ".png" if self.inv_icon_female_skel else None
    
    @property
    def inv_icon_male(self) -> str: return self.get("invIconMale")
    @property
    def inv_icon_female(self) -> str: return self.get("invIconFemale")
    @property
    def inv_icon_baby(self) -> str: return self.get("invIconBaby")
    @property
    def inv_icon_male_dead(self) -> str: return self.get("invIconMaleDead")
    @property
    def inv_icon_female_dead(self) -> str: return self.get("invIconFemaleDead")
    @property
    def inv_icon_baby_dead(self) -> str: return self.get("invIconBabyDead")
    @property
    def inv_icon_male_skel(self) -> str: return self.get("invIconMaleSkel")
    @property
    def inv_icon_female_skel(self) -> str: return self.get("invIconFemaleSkel")
    @property
    def inv_icon_baby_skel(self) -> str: return self.get("invIconBabySkel")

    @property
    def texture(self) -> list[str] | str: return self.get("texture")
    @property
    def texture_male(self) -> list[str] | str: return self.get("textureMale")
    @property
    def texture_baby(self) -> list[str] | str: return self.get("texturebaby")
    @property
    def rotten_texture(self) -> list[str] | str: return self.get("rottenTexture")

    @property
    def models(self) -> list[str]:
        return self.format_models(self.model_files, self.page, self.name)

    @property
    def model_files(self) -> list[str]:
        if self.animal.baby:
            textures = self.texture_baby
            if not textures:
                textures = self.texture if isinstance(self.texture, list) else [self.texture]
                textures = [tex + "_" + self.animal.animal_id for tex in textures]
        
        elif self.animal.male:
            textures = self.texture_male if isinstance(self.texture_male, list) else [self.texture_male]
        
        else:
            # Fallback to female
            textures = self.texture if isinstance(self.texture, list) else [self.texture]

        return [tex.removesuffix(".png").removesuffix("_Body").removesuffix("Body") + "_Body.png" for tex in textures]
    
    @property
    def parts_id(self) -> str:
        return self.animal.animal_id + self.breed_id
    @property
    def parts(self) -> "AnimalPart":
        from scripts.objects.animal_part import AnimalPart
        return AnimalPart(self.parts_id)
    @property
    def milk_type(self) -> "Fluid | None":
        from scripts.objects.fluid import Fluid
        return Fluid(self.get("milkType")) if self.get("milkType") else None
    @property
    def wool_type(self) -> "Item | None":
        from scripts.objects.item import Item
        return Item(self.get("woolType")) if self.get("woolType") else None
    @property
    def feather_item(self) -> "Item | None":
        from scripts.objects.item import Item
        return Item(self.get("featherItem")) if self.get("featherItem") else None
    @property
    def max_feather(self) -> int:
        return self.get("maxFeather", 0)
    
    ## ------------ Gene effects ------------ ##

    @property
    def forced_genes(self) -> dict | None: return self.get("forcedGenes", {})

    @property
    def min_milk(self) -> float:
        gene:dict = self.forced_genes.get("maxMilk")
        if not gene:
            return self.animal.min_milk
        return self.animal.min_milk * gene.get("maxValue", 1.0)
    @property
    def max_milk(self) -> float:
        gene:dict = self.forced_genes.get("maxMilk")
        if not gene:
            return self.animal.max_milk
        return self.animal.max_milk * gene.get("maxValue", 1.0)
    @property
    def milk_inc(self) -> list[float]:
        gene:dict = self.forced_genes.get("milkInc")
        if not gene:
            return 0.5 # default value
        return [gene.get("minValue"), gene.get("maxValue")]
    @property
    def meat_ratio(self) -> list[float]:
        gene:dict = self.forced_genes.get("meatRatio")
        if not gene:
            return [1.0, 1.0]
        return [gene.get("minValue"), gene.get("maxValue")]
    @property
    def min_weight(self) -> float:
        gene:dict = self.forced_genes.get("maxWeight")
        if not gene:
            return self.animal.min_weight
        return self.animal.min_weight * gene.get("minValue", 1.0)
    @property
    def max_weight(self) -> float:
        gene:dict = self.forced_genes.get("maxWeight")
        if not gene:
            return self.animal.max_weight
        return self.animal.max_weight * gene.get("maxValue", 1.0)
    @property
    def max_wool(self) -> float:
        gene:dict = self.forced_genes.get("maxWool")
        if not gene:
            return self.animal.max_wool
        return [self.animal.max_wool * gene.get("minValue"), self.animal.max_wool * gene.get("maxValue")]
    @property
    def wool_inc(self) -> list[float]:
        gene:dict = self.forced_genes.get("milkInc")
        if not gene:
            return 0.5 # default value
        return [gene.get("minValue"), gene.get("maxValue")]

    def __repr__(self):
        return f"<AnimalBreed {self.animal.animal_id}:{self.breed_id}>"


def animal_report(animal_id: str):
    import os
    from scripts.objects.item import Item
    from scripts.core.file_loading import write_file
    animal = Animal(animal_id)
    if not animal.is_valid:
        return
    
    content = []
    content.append(f"=={animal.animal_id}==")
    content.append("===General===")
    content.extend([
        f"*'''Name:''' {animal.wiki_link}",
        f"*'''Group:''' {animal.group_link}",
        f"*'''Stage:''' {animal.gender.capitalize()}",
        f"*'''Size:''' {animal.min_size}–{animal.max_size}",
        f"*'''Trailer size:''' {animal.trailer_base_size}",
        f"*'''Icons:''' {animal.icon_all} {animal.icon_dead_all} {animal.icon_skeleton_all}",
        f"*'''Models:''' {''.join([''.join(breed.models) for breed in animal.breeds])}"
    ])
    content.append("===Stats===")
    content.extend([
        f"*'''Weight:''' {animal.min_weight}–{animal.max_weight}",
        f"*'''Health:''' {util.convert_int(1 / (animal.health_loss_multiplier or 1))}",
        f"*'''Daily water:''' {animal.daily_water}",
        f"*'''Daily hunger:''' {animal.daily_hunger}",
        f"*'''Thirst rate:''' {util.convert_int(round(animal.thirst_multiplier * 24, 3))} per day",
        f"*'''Hunger rate:''' {util.convert_int(round(animal.hunger_multiplier * 24, 3))} per day",
        f"*'''Blood:''' {'–'.join([str(animal.min_blood), str(animal.max_blood)]) if animal.min_blood else 'N/A'}",
        f"*'''Damage:''' {animal.base_dmg or 'N/A'}",
        f"*'''Age:''' {animal.min_age}–{animal.max_age}",
        f"*'''Can be milked:''' {animal.can_be_milked}",
        f"*'''Milk:''' {'–'.join([str(animal.min_milk), str(animal.max_milk)]) if animal.min_milk else 'N/A'}",
        f"*'''Wool:''' {'–'.join(["0", str(util.convert_int(animal.max_wool))]) if animal.max_wool else 'N/A'}",
        f"*'''Dung chance per day:''' {f'{animal.dung_chance_per_day}%' if animal.dung_chance_per_day else 'N/A'}",
        f"*'''Dung:''' {animal.dung.icon if animal.dung else 'N/A'}"
    ])
    content.append("===Behaviour===")
    content.extend([
        f"*'''Lure:''' {''.join([Item(item.get("name")).icon for item in animal.lured_possible_items]) or 'N/A'}",
        f"*'''Eats grass:''' {animal.eat_grass}",
        f"*'''Trough food:''' {', '.join(animal.eat_type_trough) or 'N/A'}",
        f"*'''Food types:''' \n**{'\n**'.join([(f'{key} ({value})' if key != "All" else key) for key, value in animal.food_types.items()]) or 'N/A'}",
        f"*'''Pet:''' {animal.can_be_pet}",
        f"*'''Flees humans:''' {animal.always_flee_humans}",
        f"*'''Flees zombies:''' {animal.flee_zombies}",
        f"*'''Minimum enclosure size:''' {animal.min_enclosure_size or 'N/A'}",
        f"*'''Destroys furniture:''' {animal.can_thump}",
        f"*'''Stressed from rain:''' {animal.stress_under_rain}",
        f"*'''Stressed above ground:''' {animal.stress_above_ground}",
        f"*'''Attack if stressed:''' {animal.attack_if_stressed}",
        f"*'''Attacks back:''' {animal.attack_back}",
    ])
    content.append("===Breeding===")
    content.extend([
        f"*'''Mate:''' {Animal(animal.mate).wiki_link if animal.mate else 'N/A'}",
        f"*'''Baby:''' {Animal(animal.baby_type).wiki_link if animal.baby_type else 'N/A'}",
        f"*'''Baby amount:''' {'–'.join(animal.baby_nbr) if animal.baby_nbr else 'N/A'}",
        f"*'''Minimum age for baby:''' {animal.min_age_for_baby or 'N/A'}",
        f"*'''Mating period:''' {'–'.join([animal.mating_period_month_start, animal.mating_period_month_end]) if animal.mating_period_month_start else 'N/A'}",
        f"*'''Pregnant period:''' {animal.pregnant_period or 'N/A'}",
        f"*'''Time between pregnancies:''' {animal.time_before_next_pregnancy or 'N/A'}",
        f"*'''Egg:''' {animal.egg_type.icon if animal.egg_type else 'N/A'}",
        f"*'''Eggs per day:''' {animal.eggs_per_day or 'N/A'}",
        f"*'''Eggs per season:''' {'–'.join([str(animal.min_clutch_size), str(animal.max_clutch_size)]) if animal.min_clutch_size else 'N/A'}",
        f"*'''Laying season start:''' {animal.lay_egg_period_month_start or 'N/A'}",
    ])
    content.append("===Genes===")
    content.extend([
        '\n'.join("*" + util.split_camel_case(key).capitalize() for key in animal.genes.keys())
    ])
    content.append("===Breeds===")
    for breed in animal.breeds:
        content.append(f"===={breed.breed_name}====")
        if breed.forced_genes:
            content.append("*'''Forced genes:'''")
            for gene, gene_data in breed.forced_genes.items():
                content.append(f"**'''{util.split_camel_case(gene).capitalize()}:''' {gene_data.get("minValue", 0)}–{gene_data.get("maxValue", 0)}")
        if breed.parts:
            content.append("*'''Parts:'''")
            for part in breed.parts.all_parts:
                item = Item(part)
                content.append(f"**{item.icon} {item.wiki_link}")
    
    rel_path = os.path.join("animal_reports", f"animal_report_{animal.animal_id}.txt")
#    write_file(content, rel_path=rel_path)
    return content

if __name__ == "__main__":
#    from scripts.core.file_loading import write_file
#    content = []
#    for animal_id, animal in Animal.all().items():
#        content.extend(animal_report(animal_id))
#    write_file(content, rel_path="animal_reports.txt")

    print(Animal("chick").can_be_hooked)
