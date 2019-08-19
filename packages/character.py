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
        self._armor: int = stealth.Armor()
        self._backpack: int = stealth.Backpack()
        self._name: str = stealth.CharName()
        self._title: str = stealth.CharTitle()
        self._resist["cold"]: int = stealth.ColdResist()
        self._connected_time: str = stealth.ConnectedTime()
        self._dead: bool = stealth.Dead()
        self._ability["dex"]: int = stealth.Dex()
        self._disconnected_time: str = stealth.DisconnectedTime()
        self._resist["energy"]: str = stealth.EnergyResist()
        self._extended_info: Type["TExtendedInfo"] = stealth.ExtendedInfo()

    @property
    def armor(self):
        logging.info(f"Getting armor value")
        return self._armor

