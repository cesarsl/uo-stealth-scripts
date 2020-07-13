import datetime
import logging
from typing import Type, Dict

import stealth


class Char:
    def __init__(self):
        self._ability: Dict[str, int] = {}
        self._damage: Dict[str, int] = {}
        self._dead: bool = None
        self._name: str = None
        self._position: Dict[str, int] = {}
        self._race: str = None
        self._resist: Dict[str, int] = {}
        self._skills: Dict[str, int] = {}
        self._stats: Dict[str, int] = {}
        self._weight: Dict[str, int] = {}


class MyChar(Char):
    def __init__(self):
        super(MyChar, self).__init__()
        self._ability["dex"]: int = 0
        self._ability["int"]: int = 0
        self._ability["str"]: int = 0
        self._armor: int = None
        self._backpack: int = None
        self._connected_time: str = ""
        self._damage["max"]: int = None
        self._damage["min"]: int = None
        self._dead: bool = None
        self._disconnected_time: str = ""
        self._extended_info: Dict[str, str] = {}
        self._luck: int = None
        self._name: str = None
        self._title: str = None
        self._resist["cold"]: int = None
        self._resist["energy"]: int = None
        self._resist["fire"]: int = None
        self._resist["poison"]: int = None
        self._stats["hp_current"]: int = None
        self._stats["hp_max"]: int = None
        self._stats["mp_current"]: int = None
        self._stats["mp_max"]: int = None
        self._stats["st_current"]: int = None
        self._stats["st_max"]: int = None
        self._stats["hci"]: int = None
        self._stats["ssi"]: int = None
        self._stats["di"]: int = None
        self._stats["lrc"]: int = None
        self._stats["dci"]: int = None
        self._stats["sdi"]: int = None
        self._stats["fcr"]: int = None
        self._stats["fc"]: int = None
        self._stats["lmc"]: int = None
        self._stats["hp_regen"]: int = None
        self._stats["mp_regen"]: int = None
        self._stats["st_regen"]: int = None
        self._stats["reflect_damage"]: int = None
        self._tithing_points: int = None
        self._weight["current"]: int = None
        self._weight["max"]: int = None

    @property
    def ability(self, prop=None) -> int:
        logging.info(f"Getting character ability value for {prop}")
        if prop:
            if prop == "dex":
                self._ability[prop] = stealth.Dex()
            elif prop == "int":
                self._ability[prop] = stealth.Int()
            elif prop == "str":
                self._ability[prop] = stealth.Str()
            else:
                logging.info(f"Not a valid ability option")
            return self._ability[prop]
        logging.info(f"Try passing dex, int or str as a parameter")
        return None

    @property
    def armor(self) -> int:
        logging.info(f"Getting armor value")
        self._armor = stealth.Armor()
        return self._armor

    @property
    def backpack(self) -> int:
        logging.info(f"Getting backpack id")
        self._backpack = stealth.Backpack()
        return self._backpack

    @property
    def connected_time(self) -> str:
        logging.info(f"Getting connected time")
        self._connected_time = stealth.ConnectedTime()
        return self._connected_time

    @property
    def dead(self) -> bool:
        logging.info(f"Getting dead property")
        self._dead = stealth.Dead()
        return self._dead

    @property
    def extended_info(self) -> Dict[str, str]:
        logging.info(f"Getting character extended info")
        self._extended_info = stealth.GetExtInfo()
        return self._extended_info

    @property
    def name(self) -> str:
        logging.info(f"Getting character name")
        self._name = stealth.CharName()
        return self._name

    @property
    def title(self) -> str:
        logging.info(f"Getting character title")
        self._title = stealth.GetCharTitle()
        return self._title

    @property
    def resist(self, prop=None) -> int:
        logging.info(f"Getting character resistance for {prop}")
        if prop:
            if prop == "cold":
                self._resist[prop] = stealth.ColdResist()
            elif prop == "energy":
                self._resist[prop] = stealth.EnergyResist()
            elif prop == "fire":
                self._resist[prop] = stealth.FireResist()
            elif prop == "poison":
                self._resist[prop] = stealth.PoisonResist()
            else:
                logging.info(f"Not a valid resistance option")
            return self._resist[prop]
        logging.info(f"Try passing cold, energy, fire or poison as a parameter")
        return None
