import json
import struct
import argparse


FILE_TYPE = {
    15: "SAVE",
    16: "MOD"
}

RECORD_DATATYPE = {
    2147483647: "DELETED",
    -2147483646: "NEW",
    -2147483647: "CHANGED",
    -2147483645: "CHANGED_RENAMED"
}

RECORD_TYPE = {
    0: "BUILDING",
    1: "CHARACTER",
    2: "WEAPON",
    3: "ARMOUR",
    4: "ITEM",
    5: "ANIMAL_ANIMATION",
    6: "ATTACHMENT",
    7: "RACE",
    9: "NATURE",
    10: "FACTION",
    13: "TOWN",
    16: "LOCATIONAL_DAMAGE",
    17: "COMBAT_TECHNIQUE",
    18: "DIALOGUE",
    19: "DIALOGUE_LINE",
    21: "RESEARCH",
    22: "AI_TASK",
    24: "ANIMATION",
    25: "STATS",
    26: "PERSONALITY",
    27: "CONSTANTS",
    28: "BIOMES",
    29: "BUILDING_PART",
    30: "INSTANCE_COLLECTION",
    31: "DIALOG_ACTION",
    34: "PLATOON",
    36: "GAMESTATE_CHARACTER",
    37: "GAMESTATE_FACTION",
    38: "GAMESTATE_TOWN_INSTANCE_LIST",
    41: "INVENTORY_STATE",
    42: "INVENTORY_ITEM_STATE",
    43: "REPEATABLE_BUILDING_PART_SLOT",
    44: "MATERIAL_SPEC",
    45: "MATERIAL_SPECS_COLLECTION",
    46: "CONTAINER",
    47: "MATERIAL_SPECS_CLOTHING",
    49: "VENDOR_LIST",
    50: "MATERIAL_SPECS_WEAPON",
    51: "WEAPON_MANUFACTURER",
    52: "SQUAD_TEMPLATE",
    53: "ROAD",  # *1
    55: "COLOR_DATA",
    56: "CAMERA",
    57: "MEDICAL_STATE",
    59: "FOLIAGE_LAYER",
    60: "FOLIAGE_MESH",
    61: "GRASS",
    62: "BUILDING_FUNCTIONALITY",
    63: "DAY_SCHEDULE",
    64: "NEW_GAME_STARTOFF",
    66: "CHARACTER_APPEARANCE",
    67: "GAMESTATE_AI",
    68: "WILDLIFE_BIRDS",
    69: "MAP_FEATURES",
    70: "DIPLOMATIC_ASSAULTS",
    71: "SINGLE_DIPLOMATIC_ASSAULT",
    72: "AI_PACKAGE",
    73: "DIALOGUE_PACKAGE",
    74: "GUN_DATA",
    76: "ANIMAL_CHARACTER",
    77: "UNIQUE_SQUAD_TEMPLATE",
    78: "FACTION_TEMPLATE",
    80: "WEATHER",
    81: "SEASON",
    82: "EFFECT",
    83: "ITEM_PLACEMENT_GROUP",
    84: "WORD_SWAPS",
    86: "NEST_ITEM",
    87: "CHARACTER_PHYSICS_ATTACHMENT",
    88: "LIGHT",
    89: "HEAD",
    92: "FOLIAGE_BUILDING",
    93: "FACTION_CAMPAIGN",
    94: "GAMESTATE_TOWN",
    95: "BIOME_GROUP",
    96: "EFFECT_FOG_VOLUME",
    97: "FARM_DATA",
    98: "FARM_PART",
    99: "ENVIRONMENT_RESOURCES",
    100: "RACE_GROUP",
    101: "ARTIFACTS",
    102: "MAP_ITEM",
    103: "BUILDINGS_SWAP",
    104: "ITEMS_CULTURE",
    105: "ANIMATION_EVENT",
    107: "CROSSBOW"
}


def get_file_type(type_id):
    try:
        return FILE_TYPE[type_id],
    except KeyError:
        return "UNKNOWN[%d]" % type_id


def get_record_type(type_id):
    try:
        return RECORD_TYPE[type_id],
    except KeyError:
        return "UNKNOWN[%d]" % type_id


def get_record_datatype(datatype_id):
    try:
        return RECORD_DATATYPE[datatype_id],
    except KeyError:
        return "UNKNOWN[%d]" % type_id


def get_arguments():
    parser = argparse.ArgumentParser(
        description="Extracts Kenshi game data and dump"
                    + " it in processable format."
    )
    parser.add_argument('input',
                        metavar='FILE',
                        type=str,
                        nargs='+',
                        help='list of files to be processed'
                             + ' and merged (order matters)'
                        )
    parser.add_argument('--output',
                        type=str,
                        help='output file name (default:'
                             + ' output.json)',
                        default='output.json'
                        )
    return parser.parse_args()


class BinaryFileReader:
    def __init__(self, path):
        self.path = path
        self.handle = open(path, "rb")

    def int(self):
        binary = self.handle.read(4)
        return struct.unpack("i", binary)[0]

    def string(self):
        binary = self.handle.read(self.int())
        return binary.decode("utf-8")

    def char(self):
        binary = self.handle.read(1)
        return struct.unpack("c", binary)[0].decode("utf-8")

    def bool(self):
        binary = self.handle.read(1)
        return struct.unpack("?", binary)[0]

    def float(self):
        binary = self.handle.read(4)
        return struct.unpack("f", binary)[0]

    def vec3i(self):
        return self.int(), self.int(), self.int()

    def vec3f(self):
        return self.float(), self.float(), self.float()

    def vec4f(self):
        return self.float(), self.float(), self.float(), self.float()


class ModFileReader(BinaryFileReader):
    def bool_value(self):
        name = self.string()
        return {
            name: self.bool()
        }

    def int_value(self):
        name = self.string()
        return {
            name: self.int()
        }

    def float_value(self):
        name = self.string()
        return {
            name: self.float()
        }

    def vec3f_value(self):
        name = self.string()
        return {
            name: self.vec3f()
        }

    def vec4f_value(self):
        name = self.string()
        return {
            name: self.vec4f()
        }

    def vec3i_value(self):
        name = self.string()
        return {
            name: self.vec3i()
        }

    def string_value(self):
        name = self.string()
        return {
            name: self.string()
        }

    def filename_value(self):
        return self.string_value()

    def fields(self, value_type):
        fields = []
        for _ in range(0, self.int()):
            fields.append(value_type())
        return fields

    def extras(self):
        extras = {}
        length = self.int()
        for _ in range(0, length):
            name = self.string()
            extras[name] = self.extra_items()
        return extras

    def extra_items(self):
        items = []
        length = self.int()
        for _ in range(0, length):
            items.append(self.vec3i_value())
        return items

    def instances(self):
        instances = []
        length = self.int()
        for _ in range(0, length):
            instances.append({
                "id": self.string(),
                "target": self.string(),
                "position": self.vec3f(),
                "rotation": self.vec4f(),
                "states": self.instance_states()
            })
        return instances

    def instance_states(self):
        return [self.string() for _ in range(0, self.int())]


def get_mod_data(path):
    mod = ModFileReader(path)
    file_type = get_file_type(mod.int())

    if file_type != "MOD":
        raise Exception("%s is not a mod file, %s found." % (path, file_type))

    metadata = {
        "version": mod.int(),
        "author": mod.string(),
        "description": mod.string(),
        "dependencies": mod.string().split(","),
        "references": mod.string().split(","),
        "flags": mod.int(),
        "record_count": mod.int(),
    }

    records = []

    for _ in range(0, metadata["record_count"]):
        record = {
            "instance_count": mod.int(),
            "type": get_record_type(mod.int()),
            "id": mod.int(),
            "name": mod.string(),
            "string_id": mod.string(),
            "datatype": get_record_datatype(mod.int()),
            "fields": {
                "bool": mod.fields(mod.bool_value),
                "float": mod.fields(mod.float_value),
                "int": mod.fields(mod.int_value),
                "vec3f": mod.fields(mod.vec3f_value),
                "vec4f": mod.fields(mod.vec4f_value),
                "string": mod.fields(mod.string_value),
                "filename": mod.fields(mod.filename_value)
            },
            "extra": mod.extras(),
            "instances": mod.instances()
        }
        records.append(record)
    metadata["records"] = records

    return metadata


if __name__ == '__main__':
    args = get_arguments()

    print(args)
    exit()


    with open('mod.json', 'w') as outfile:
        json.dump(data, outfile)
