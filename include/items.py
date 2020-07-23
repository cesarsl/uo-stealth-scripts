import re

from stealth import GetType, GetTooltipRec

from scripts.include.helpers import get_object_id
from scripts.assets.cliloc import CLILOCS
from scripts.include.constants import LOC_BOOLEANS, LOC_HANDLING, LOC_MATERIALS, \
                                    LOC_NAMES, LOC_SKILL_REQUIREMENT, LOC_SLAYERS

class Item:
    def __init__(self, item_id):
        self._item_id = item_id
        self._type_id = GetType(self._item_id)
        self._tooltip_dict = GetTooltipRec(self._item_id)
        self._properties = self._tooltips_parser(self._tooltip_dict)
    
    @property
    def properties(self):
        return self._properties
    
    def _is_integer(self, number):
        try:
            _res = int(number)
            return True
        except ValueError:
            return False

    def _get_cliloc_name(self, cliloc_id):
        return CLILOCS.get(cliloc_id).get('text')

    def _string_parser(self, string):
        if self._is_integer(string):
            return int(string)
        if re.match(r"[0-9]+[\.\,]?[0-9]+s|[0-9]+s", string):
            return float(string.replace("s", "").replace(",", "."))
        return str(string)

    def _tooltips_parser(self, tooltips):
        parsed = {}

        for tooltip in tooltips:
            cliloc_id = tooltip.get('Cliloc_ID')
            cliloc_name = self._get_cliloc_name(cliloc_id)
            cliloc_params = tooltip.get('Params')
            if not cliloc_params:
                if cliloc_id in LOC_NAMES:
                    parsed['name'] = cliloc_name.title()
                if cliloc_id in LOC_BOOLEANS:
                    parsed[cliloc_name.replace(' ', '_').casefold()] = True
                if cliloc_id in LOC_HANDLING:
                    parsed['handling'] = self._get_cliloc_name(cliloc_id)
                if cliloc_id in LOC_SKILL_REQUIREMENT:
                    parsed['skill_requirement'] = self._get_cliloc_name(cliloc_id).split(': ')[1]
                if cliloc_id in LOC_SLAYERS:
                    parsed['slayer'] = self._get_cliloc_name(cliloc_id)
            else:
                if len(cliloc_params) <= 1:
                    if cliloc_id == 1072225 or cliloc_id == 1072789:
                        parsed['weight'] = self._string_parser(cliloc_params[0])
                    else:
                        parsed[cliloc_name.replace(' ', '_').casefold()] = self._string_parser(cliloc_params[0])
                else:
                    if cliloc_id == 1053099:
                        parsed['material'] = self._get_cliloc_name(int(cliloc_params[0].replace('#', '')))
                        parsed['type'] = self._get_cliloc_name(int(cliloc_params[1].replace('#', '')))
                    if cliloc_id == 1061168:
                        parsed[cliloc_name.replace(' ', '_').casefold()] = {
                            'min': int(cliloc_params[0]),
                            'max': int(cliloc_params[1])
                        }
                    if cliloc_id == 1060639:
                        parsed[cliloc_name.replace(' ', '_').casefold()] = {
                            'cur': int(cliloc_params[0]),
                            'tot': int(cliloc_params[1])
                        }
        return parsed

item = Item(get_object_id())

print(item.properties)