import os
import json
import datetime as dt

from stealth import Backpack, CancelTarget, CancelWaitTarget, ClientPrint, \
                    ClientRequestObjectTarget, ClientTargetResponse, \
                    ClientTargetResponsePresent, Equip, FindCount, FindItem, \
                    FindType, FindTypesArrayEx, GetFindedList, GetType, GetX, \
                    GetY, InJournalBetweenTimes, LhandLayer, ObjAtLayer, RhandLayer, \
                    Self, UnEquip, UseObject, Wait, WaitJournalLine, WaitTargetObject, \
                    WaitTargetTile 

from include.constants import WEAPONS, TREES, MATERIALS, LAG_THRESHOLD
from include.helpers import find_tiles

class Lumberjacking:
    NO_LOGS_MSG = 'There\'s not enough wood here to harvest.'
    def __init__(self):
        self._axe_types = [axe for axe in WEAPONS.get('axes')]
        self._log_type = [material for material, props in MATERIALS.get('lumberjacking').items() if props.get('name') == 'logs'][0]
        self._material_types = [material for material in MATERIALS.get('lumberjacking')]
        self._equipped_axe = None
        self._backpack_logs = []
        self.__find_axe()

    def __find_axe(self):
        left_hand = ObjAtLayer(LhandLayer())
        right_hand = ObjAtLayer(RhandLayer())
        
        if left_hand == 0 and right_hand == 0:
            self.__equip_axe()
            return True
        elif left_hand != 0 and GetType(left_hand) in self._axe_types:
            self._equipped_axe = left_hand
            return True
        elif right_hand != 0 and GetType(right_hand) not in self._axe_types:
            UnEquip(RhandLayer())
            Wait(LAG_THRESHOLD)
            self.__equip_axe()
            return True
        else:
            raise Exception('No axe found in the backpack or hands')


    def __equip_axe(self):
        if FindTypesArrayEx(self._axe_types, [0], [Backpack()], False) > 0:
            if FindCount() < 2:
                self._equipped_axe = FindItem()
                Equip(LhandLayer(), self._equipped_axe)
            else:
                ClientPrint('Two or more axes found in bag, choose one:')
                CancelWaitTarget()
                CancelTarget()
                ClientRequestObjectTarget()
                while ClientTargetResponsePresent() is False:
                    Wait(1)
                target_response = ClientTargetResponse()
                self._equipped_axe = target_response['ID']
                Equip(LhandLayer(), self._equipped_axe)
        else:
            raise Exception('No axes in the backpack')
    
    def harvest(self, tile, x, y, z):
        CancelWaitTarget()
        CancelTarget()
        
        timestamp_before = dt.datetime.now()
        UseObject(self._equipped_axe)
        while InJournalBetweenTimes('What do you want to use this item on?', timestamp_before, dt.datetime.now()) <= 0:
            Wait(1)
        
        WaitTargetTile(tile, x, y, z)
        Wait(LAG_THRESHOLD)

        if WaitJournalLine(timestamp_before, self.NO_LOGS_MSG, 3000):
            print('No more logs available on this tree.')
            return False
        return True

    def can_convert_logs(self):
        FindType(self._log_type, Backpack())
        logs_found = GetFindedList()
        if len(logs_found) == 0:
            self._backpack_logs = []
            return False
        self._backpack_logs = logs_found
        return True

    def convert_logs(self):
        if self.can_convert_logs():
            if len(self._backpack_logs) != 0:
                for log in self._backpack_logs:
                    time_before = dt.datetime.now()
                    UseObject(self._equipped_axe)
                    while InJournalBetweenTimes('What do you want to use this item on?', time_before, dt.datetime.now()) <= 0:
                        Wait(1)
                    
                    WaitTargetObject(log)
                    Wait(LAG_THRESHOLD)
            return
        




