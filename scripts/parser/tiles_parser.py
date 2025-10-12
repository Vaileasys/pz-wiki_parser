"""
This script was originally written in JavaScript by User:Jab.
It has been converted to python for use in the wiki parser.
"""

import os
import struct
from scripts.core.constants import DATA_DIR
from scripts.core.cache import save_cache
from scripts.core.file_loading import get_media_dir

IsoFlagType = {
    'collideW': 0, 'collideN': 1, 'solidfloor': 2, 'noStart': 3, 'windowW': 4,
    'windowN': 5, 'hidewalls': 6, 'exterior': 7, 'NoWallLighting': 8, 'doorW': 9,
    'doorN': 10, 'transparentW': 11, 'transparentN': 12, 'WallOverlay': 13,
    'FloorOverlay': 14, 'vegitation': 15, 'burning': 16, 'burntOut': 17,
    'unflamable': 18, 'cutW': 19, 'cutN': 20, 'tableN': 21, 'tableNW': 22,
    'tableW': 23, 'tableSW': 24, 'tableS': 25, 'tableSE': 26, 'tableE': 27,
    'tableNE': 28, 'halfheight': 29, 'HasRainSplashes': 30, 'HasRaindrop': 31,
    'solid': 32, 'trans': 33, 'pushable': 34, 'solidtrans': 35, 'invisible': 36,
    'floorS': 37, 'floorE': 38, 'shelfS': 39, 'shelfE': 40, 'alwaysDraw': 41,
    'ontable': 42, 'transparentFloor': 43, 'climbSheetW': 44, 'climbSheetN': 45,
    'climbSheetTopN': 46, 'climbSheetTopW': 47, 'attachtostairs': 48,
    'sheetCurtains': 49, 'waterPiped': 50, 'HoppableN': 51, 'HoppableW': 52,
    'bed': 53, 'blueprint': 54, 'canPathW': 55, 'canPathN': 56, 'blocksight': 57,
    'climbSheetE': 58, 'climbSheetS': 59, 'climbSheetTopE': 60,
    'climbSheetTopS': 61, 'makeWindowInvincible': 62, 'water': 63,
    'canBeCut': 64, 'canBeRemoved': 65, 'taintedWater': 66, 'smoke': 67,
    'attachedN': 68, 'attachedS': 69, 'attachedE': 70, 'attachedW': 71,
    'attachedFloor': 72, 'attachedSurface': 73, 'attachedCeiling': 74,
    'attachedNW': 75, 'ForceAmbient': 76, 'WallSE': 77, 'WindowN': 78,
    'WindowW': 79, 'FloorHeightOneThird': 80, 'FloorHeightTwoThirds': 81,
    'CantClimb': 82, 'diamondFloor': 83, 'attachedSE': 84, 'TallHoppableW': 85,
    'WallWTrans': 86, 'TallHoppableN': 87, 'WallNTrans': 88, 'container': 89,
    'DoorWallW': 90, 'DoorWallN': 91, 'WallW': 92, 'WallN': 93, 'WallNW': 94,
    'SpearOnlyAttackThrough': 95, 'forceRender': 96, 'open': 97,
    'SpriteConfig': 98, 'BlockRain': 99, 'EntityScript': 100, 'isEave': 101,
    'openAir': 102, 'HasLightOnSprite': 103, 'unlit': 104, 'NeverCutaway': 105,
    'DoubleDoor1': 106, 'DoubleDoor2': 107, 'MAX': 108
}
IsoFlagTypeName = {v: k for k, v in IsoFlagType.items()}

IsoObjectType = {
    'normal': 0, 'jukebox': 1, 'wall': 2, 'stairsTW': 3, 'stairsTN': 4,
    'stairsMW': 5, 'stairsMN': 6, 'stairsBW': 7, 'stairsBN': 8,
    'UNUSED9': 9, 'UNUSED10': 10, 'doorW': 11, 'doorN': 12,
    'lightswitch': 13, 'radio': 14, 'curtainN': 15, 'curtainS': 16,
    'curtainW': 17, 'curtainE': 18, 'doorFrW': 19, 'doorFrN': 20,
    'tree': 21, 'windowFN': 22, 'windowFW': 23, 'UNUSED24': 24,
    'WestRoofB': 25, 'WestRoofM': 26, 'WestRoofT': 27,
    'isMoveAbleObject': 28, 'MAX': 29
}
IsoObjectTypeName = {v: k for k, v in IsoObjectType.items()}

RenderLayer = {'Default': 0, 'Floor': 1}
RenderLayerName = {v: k for k, v in RenderLayer.items()}


# —————————————————————————————————————————————————————————————————————
# Binary reader
# —————————————————————————————————————————————————————————————————————

class BufferReader:
    def __init__(self, data: bytes):
        self.data = data
        self.offset = 0

    def read_int32(self) -> int:
        val = struct.unpack_from('<i', self.data, self.offset)[0]
        self.offset += 4
        return val

    def read_uint8(self) -> int:
        val = self.data[self.offset]
        self.offset += 1
        return val

    def read_string(self) -> str:
        chars = []
        while True:
            b = self.read_uint8()
            if b in (10, 255):
                break
            if b == 13:
                raise ValueError("\\r\\n unsupported")
            chars.append(chr(b))
            if len(chars) >= 1024:
                raise ValueError("String too long")
        return ''.join(chars)


# —————————————————————————————————————————————————————————————————————
# Tile property alias map
# —————————————————————————————————————————————————————————————————————

class TileProperty:
    def __init__(self):
        self.property_name = None
        self.possible_values = []
        self.id_map = {}

class TilePropertyAliasMap:
    PropertyToID = {}
    Properties = []

    @classmethod
    def generate(cls, prop_value_map: dict):
        cls.PropertyToID.clear()
        cls.Properties.clear()
        for prop, values in prop_value_map.items():
            cls.PropertyToID[prop] = len(cls.Properties)
            tp = TileProperty()
            tp.property_name = prop
            tp.possible_values = list(values)
            tp.id_map = {v: i for i, v in enumerate(tp.possible_values)}
            cls.Properties.append(tp)

    @classmethod
    def get_id_from_name(cls, name: str) -> int:
        return cls.PropertyToID.get(name, -1)

    @classmethod
    def get_name_from_id(cls, idx: int) -> str:
        for k, v in cls.PropertyToID.items():
            if v == idx:
                return k
        return None

    @classmethod
    def get_id_from_value(cls, prop_id: int, value: str) -> int:
        if prop_id < 0 or prop_id >= len(cls.Properties):
            return 0
        return cls.Properties[prop_id].id_map.get(value, 0)

    @classmethod
    def get_value_string(cls, prop_id: int, idx: int) -> str:
        if prop_id < 0 or prop_id >= len(cls.Properties):
            return ''
        pv = cls.Properties[prop_id].possible_values
        if idx < 0 or idx >= len(pv):
            return ''
        return pv[idx]


# —————————————————————————————————————————————————————————————————————
# Sprite property container
# —————————————————————————————————————————————————————————————————————

class PropertyContainer:
    SURFACE_VALID      = 1
    SURFACE_ISOFFSET   = 2
    SURFACE_ISTABLE    = 4
    SURFACE_ISTABLETOP = 8
    numeric_property_names = ['PickUpWeight']

    def __init__(self):
        self.SpriteFlags1 = 0
        self.SpriteFlags2 = 0
        self.Properties   = {}
        self.SurfaceFlags = 0
        self.flags_set    = []

    def set_flag(self, flag: int):
        # 32-bit shift space
        if flag == 0:
            self.SpriteFlags1 |= (1 << (flag % 32))
        else:
            self.SpriteFlags2 |= (1 << (flag % 32))
        if flag not in self.flags_set:
            self.flags_set.append(flag)

    def set_property(self, name: str, value: str, is_flag: bool = True):
        if not name:
            return
        if name == 'container':
            is_flag = False
        if is_flag and name in IsoFlagType:
            f = IsoFlagType[name]
            if f != IsoFlagType['MAX']:
                self.set_flag(f)
                return
        pid = TilePropertyAliasMap.get_id_from_name(name)
        if pid == -1:
            return
        vid = TilePropertyAliasMap.get_id_from_value(pid, value)
        self.SurfaceFlags &= ~self.SURFACE_VALID
        self.Properties[pid] = vid

    def val(self, name: str):
        pid = TilePropertyAliasMap.get_id_from_name(name)
        if pid not in self.Properties:
            return None
        idx = self.Properties[pid]
        val = TilePropertyAliasMap.get_value_string(pid, idx)
        if name in self.numeric_property_names:
            try:
                val = float(val)
            except:
                pass
        return val

    def to_json(self) -> dict:
        j = {}
        if self.SpriteFlags1:
            j['spriteFlags1'] = self.SpriteFlags1
        if self.SpriteFlags2:
            j['spriteFlags2'] = self.SpriteFlags2
        if self.flags_set:
            j['flags'] = [IsoFlagTypeName[f] for f in self.flags_set]
        if self.Properties:
            generic = {}
            for pid, vid in self.Properties.items():
                name = TilePropertyAliasMap.get_name_from_id(pid)
                if name is None:
                    continue
                vstr = TilePropertyAliasMap.get_value_string(pid, vid)
                if name in self.numeric_property_names:
                    try:
                        vstr = float(vstr)
                    except:
                        pass
                generic[name] = vstr
            j['generic'] = generic
        return j


# —————————————————————————————————————————————————————————————————————
# Sprite and manager
# —————————————————————————————————————————————————————————————————————

class IsoSprite:
    def __init__(self):
        self.properties = PropertyContainer()
        self.TintMod    = [1.0, 1.0, 1.0, 1.0]
        self.name       = ''
        self.id         = 20000000
        self.tileSheetIndex = 0
        self.type       = IsoObjectType['MAX']
        self.isBush     = False
        self.firerequirement = 0
        self.burntTile  = None
        self.forceAmbient= False
        self.solidFloor = False
        self.canBeRemoved = False
        self.attachedFloor= False
        self.cutN       = False
        self.cutW       = False
        self.solid      = False
        self.solidTrans = False
        self.invisible  = False
        self.alwaysDraw = False
        self.forceRender= False
        self.moveWithWind= False
        self.windType   = 1
        self.Animate    = True
        self.treatAsWallOrder = False
        self.hideForWaterRender= False
        self.renderLayer = RenderLayer['Default']

    def to_json(self) -> dict:
        j = {'id': self.id, 'type': IsoObjectTypeName[self.type], 'tileSheetIndex': self.tileSheetIndex}
        if self.renderLayer != RenderLayer['Default']:
            j['renderLayer'] = RenderLayerName[self.renderLayer]
        if any(v != 1.0 for v in self.TintMod):
            j['tintMod'] = {'r': self.TintMod[0], 'g': self.TintMod[1], 'b': self.TintMod[2], 'a': self.TintMod[3]}
        props = self.properties.to_json()
        if props:
            j['properties'] = props
        if self.isBush:           j['isBush']=True
        if self.firerequirement:  j['fireRequirement']=self.firerequirement
        if self.burntTile:        j['burntTile']=self.burntTile
        if self.forceAmbient:     j['forceAmbient']=True
        if self.solidFloor:       j['solidFloor']=True
        if self.canBeRemoved:     j['canBeRemoved']=True
        if self.attachedFloor:    j['attachedFloor']=True
        if self.cutN:             j['cutN']=True
        if self.cutW:             j['cutW']=True
        if self.solid:            j['solid']=True
        if self.solidTrans:       j['solidTrans']=True
        if self.invisible:        j['invisible']=True
        if self.alwaysDraw:       j['alwaysDraw']=True
        if self.forceRender:      j['forceRender']=True
        if self.moveWithWind:     j['moveWithWind']=True
        if self.windType!=1:      j['windType']=self.windType
        if not self.Animate:      j['animate']=False
        if self.treatAsWallOrder: j['treatAsWallOrder']=True
        if self.hideForWaterRender: j['hideForWaterRender']=True
        return j

class IsoSpriteManager:
    instance = None

    def __init__(self):
        if IsoSpriteManager.instance is not None:
            raise Exception("IsoSpriteManager already initialized")
        IsoSpriteManager.instance = self
        self.int_map = {}
        self.named_map = {}
        # empty sprite
        empty = IsoSprite()
        empty.name = ''
        empty.id   = -1
        empty.properties.set_property('invisible','true',False)
        self.named_map[''] = empty

    def add_sprite(self, name: str, id_: int) -> IsoSprite:
        if name in self.named_map:
            existing = self.named_map[name]
            print(f"[Duplicate] name='{name}' existing(id={existing.id}, type={IsoObjectTypeName[existing.type]}, "
                  f"tileSheetIndex={existing.tileSheetIndex}) new(id={id_}) → reusing")
            return existing
        spr = IsoSprite()
        spr.name = name
        spr.id   = id_
        self.named_map[name] = spr
        self.int_map[id_] = spr
        return spr


# —————————————————————————————————————————————————————————————————————
# World parser
# —————————————————————————————————————————————————————————————————————

class IsoWorld:
    def __init__(self):
        self.property_value_map = {}
        self.tiles = {}

    def load_tile_definitions_property_strings(self, path: str):
        data = open(path,'rb').read()
        r = BufferReader(data)
        r.read_int32(); r.read_int32()
        sheet_count = r.read_int32()
        for _ in range(sheet_count):
            r.read_string(); r.read_string()
            r.read_int32(); r.read_int32(); r.read_int32()
            def_count = r.read_int32()
            for _ in range(def_count):
                prop_ct = r.read_int32()
                for _ in range(prop_ct):
                    name = r.read_string()
                    val  = r.read_string()
                    lst = self.property_value_map.setdefault(name,[])
                    if val not in lst:
                        lst.append(val)

    def set_custom_property_values(self):
        for k in ('WindowN','WindowW','DoorWallN','DoorWallW','WallSE'):
            self.property_value_map.setdefault(k,[]).append(k)
        offsets = [str(i) for i in range(-96,97)]
        for off in ('Noffset','Soffset','Woffset','Eoffset'):
            self.property_value_map[off] = offsets[:]
        for v in ('5','6'): self.property_value_map.setdefault('tree',[]).append(v)
        for c in ('lightR','lightG','lightB'): self.property_value_map.setdefault(c,[]).append('0')

    def generate_tile_property_lookup_tables(self):
        TilePropertyAliasMap.generate(self.property_value_map)
        self.property_value_map.clear()

    def transform_tile_definition(self, spr, base, name, val):
        # Object-type
        if name in IsoObjectType and IsoObjectType[name]!=IsoObjectType['MAX']:
            t = IsoObjectType[name]
            if not ((spr.type in (IsoObjectType['doorW'],IsoObjectType['doorN'])) and t==IsoObjectType['wall']):
                spr.type = t
            if t==IsoObjectType['doorW']:
                spr.properties.set_flag(IsoFlagType['doorW'])
            elif t==IsoObjectType['doorN']:
                spr.properties.set_flag(IsoFlagType['doorN'])
            return

        # Other
        if name in ('firerequirement','fireRequirement'):
            spr.firerequirement = int(val)
        elif name=='BurntTile':
            spr.burntTile = val
        elif name in ('ForceAmbient','solidFloor','canBeRemoved','attachedFloor',
                      'cutW','cutN','solid','solidTrans','invisible','alwaysDraw','forceRender'):
            setattr(spr,{
                'ForceAmbient':'forceAmbient','solidFloor':'solidFloor','canBeRemoved':'canBeRemoved',
                'attachedFloor':'attachedFloor','cutW':'cutW','cutN':'cutN','solid':'solid',
                'solidTrans':'solidTrans','invisible':'invisible','alwaysDraw':'alwaysDraw',
                'forceRender':'forceRender'
            }[name],True)
            spr.properties.set_property(name,val,False)
        elif name=='MoveWithWind':
            spr.moveWithWind=True
            spr.properties.set_property(name,val,False)
        elif name=='WindType':
            spr.windType=int(val)
            spr.properties.set_property(name,val,False)
        elif name=='RenderLayer':
            spr.properties.set_property(name,val,False)
            spr.renderLayer = RenderLayer.get(val,RenderLayer['Default'])
        elif name=='TreatAsWallOrder':
            spr.treatAsWallOrder=True
            spr.properties.set_property(name,val,False)
        else:
            spr.properties.set_property(name,val,False)

    def set_open_door_properties(self, base, defs):
        for spr in defs:
            if spr.type in (IsoObjectType['doorN'],IsoObjectType['doorW']) and IsoFlagType['open'] not in spr.properties.flags_set:
                dd=spr.properties.val('DoubleDoor')
                if dd is not None and int(dd)>=5:
                    spr.properties.set_flag(IsoFlagType['open'])
                else:
                    gd=spr.properties.val('GarageDoor')
                    if gd is not None and int(gd)>=4:
                        spr.properties.set_flag(IsoFlagType['open'])
                    else:
                        sib=IsoSpriteManager.instance.named_map.get(f"{base}_{spr.tileSheetIndex+2}")
                        if sib:
                            sib.type=spr.type
                            # set sibling flag correctly
                            if spr.type==IsoObjectType['doorN']:
                                sib.properties.set_flag(IsoFlagType['doorN'])
                            else:
                                sib.properties.set_flag(IsoFlagType['doorW'])
                            spr.properties.set_flag(IsoFlagType['open'])

    def read_tile_definitions(self, path: str, file_num: int):
        data=open(path,'rb').read()
        r=BufferReader(data)
        r.read_int32(); r.read_int32()
        sheet_count=r.read_int32()
        for _ in range(sheet_count):
            base=r.read_string()
            r.read_string()
            r.read_int32(); r.read_int32()
            magic=r.read_int32()
            variants=r.read_int32()
            defs=[]
            for i in range(variants):
                name=f"{base}_{i}"
                tid = file_num*100000 + 10000 + magic*1000 + i
                spr=IsoSpriteManager.instance.add_sprite(name, tid)
                spr.name=name
                spr.tileSheetIndex=i
                defs.append(spr)
                if 'damaged' in name or 'trash_' in name:
                    spr.attachedFloor=True
                    spr.properties.set_property('attachedFloor','true',False)
                prop_ct=r.read_int32()
                for _ in range(prop_ct):
                    pname=r.read_string(); pval=r.read_string()
                    self.transform_tile_definition(spr, base, pname, pval)
                self.tiles[name]=spr
            self.set_open_door_properties(base, defs)

def main():
    media_dir = get_media_dir()
    os.makedirs(DATA_DIR, exist_ok=True)

    IsoSpriteManager()
    world = IsoWorld()

    # Find all .tiles files in media directory
    tiles_files = []
    for root, dirs, files in os.walk(media_dir):
        for fname in files:
            if fname.endswith('.tiles'):
                tiles_files.append(os.path.join(root, fname))

    # Load tile definition property strings from all .tiles files
    for tiles_file in sorted(tiles_files):
        world.load_tile_definitions_property_strings(tiles_file)
    world.set_custom_property_values()
    world.generate_tile_property_lookup_tables()

    # Read tile definitions from all .tiles files
    for tiles_file in sorted(tiles_files):
        world.read_tile_definitions(tiles_file, 1)

    combined = {k: spr.to_json() for k, spr in world.tiles.items()}
    save_cache(combined, 'tiles_data.json', DATA_DIR)

if __name__=='__main__':
    main()
