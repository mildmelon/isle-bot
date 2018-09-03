from enum import Enum

from game.items.items import ItemLookup


class Recipe(Enum):
    """ A blueprint of sorts for what materials are needed to make a craftable item,
    value represents the harvested materials needed.
    """

    # tools
    STONE_AXE = {ItemLookup.WOOD: 2, ItemLookup.STONE: 1}

    def __str__(self):
        return self.name

    def needs_materials(self):
        return self.value

    def to_short_string(self):
        output = '['

        index = 0
        for material, amt in self.value.items():
            name = str(material)
            amt = str(amt)
            if index >= 1:
                output += ', '
            output += f'{name} : {amt}'
            index += 1

        output += ']'

        return output

    def to_extended_string(self):
        output = '```\n'

        header = self.name.replace('_', ' ') + ' RECIPE'
        output += header

        output += '\n' + '-' * len(header)

        for material, amt in self.value.items():
            name = str(material).ljust(10)
            amt = str(amt).zfill(3)
            output += f'\n{name} : {amt}'
        output += '\n```'

        return output
