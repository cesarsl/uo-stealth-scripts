import datetime
import logging
from typing import Type, Dict

import stealth


class Char:
    def __init__(self):
        self._name: str = None
        self._ability: Dict[str, int] = {}
        self._dead: bool = None
        self._position: Dict[str, int]
        self._resist: Dict[str, int] = {}
        self._skills: Dict[str, int] = {}
        self._stats: Dict[str, int] = {}

    @property
    def name(self) -> str:
        return self._name

    @property
    def ability(self) -> Dict[str, int]:
        return self._ability

    @property
    def dead(self) -> bool:
        return self._dead

    @property
    def position(self) -> Dict[str, int]:
        return self._position

    @property
    def resist(self) -> Dict[str, int]:
        return self._resist

    @property
    def skills(self) -> Dict[str, int]:
        return self._skills

    @property
    def stats(self) -> Dict[str, int]:
        return self._stats


class MyChar(Char):
    def __init__(self):
        self._armor: int = None
        self._backpack: int = None
        self._name: str = None
        self._title: str = None
        self._resist["cold"]: int = None
        self._resist["energy"]: int = None
        self._resist["fire"]: int = None
        self._resist["poison"]: int = None
        self._connected_time: str = stealth.ConnectedTime()
        self._dead: bool = stealth.Dead()
        self._ability["dex"]: int = stealth.Dex()
        self._disconnected_time: str = stealth.DisconnectedTime()
        self._resist["energy"]: str = stealth.EnergyResist()
        self._extended_info: Dict[str, str] = stealth.GetExtInfo()

    @property
    def armor(self):
        logging.info(f"Getting armor value")
        self._armor = stealth.Armor()
        return self._armor

    @property
    def backpack(self):
        logging.info(f"Getting backpack id")
        self._backpack = stealth.Backpack()
        return self._backpack

    @property
    def name(self):
        logging.info(f"Getting character name")
        self._name = stealth.CharName()
        return self._name

    @property
    def title(self):
        logging.info(f"Getting character title")
        self._title = stealth.CharTitle()

    @property
    def resist(self, prop=None):
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
