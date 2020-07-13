import os
import json
import datetime as dt

from stealth import *

from include.helpers import find_tiles

class Lumberjacking:

    def __init__(self):
        self.LAG_FAILSAFE = 700
        self.NO_LOGS_MSG = 'There\'s not enough wood here to harvest.'
        self.axe_types = []
        self.tree_tiles = []
        self.resource_types = []
        self.trees = []
        self.tree_map = []
        self.current_axe = None
        self.current_tree = None
        self.secure_chest = None
        self._backpack_logs = []
        self.__load_resources()
        self.__find_axe()


    def __load_resources(self):
        json_path = os.path.realpath("./../scripts/assets/json/lumberjacking.json")
        with open(json_path, 'r') as file:
            data = json.load(file)

        self.axes = data['axes']
        self.axe_types = [int(x['type'],16) for x in self.axes]
        self.trees = data['trees']
        self.tree_tiles = [int(x['tile']) for x in self.trees]
        self.resource_types = data['resources']


    def __find_axe(self):
        left_hand = ObjAtLayer(LhandLayer())
        right_hand = ObjAtLayer(RhandLayer())
        
        if left_hand == 0 and right_hand == 0:
            self.__equip_axe()
            return True
        elif left_hand != 0 and GetType(left_hand) in self.axe_types:
            self.current_axe = left_hand
            return True
        elif right_hand != 0 and GetType(right_hand) not in self.axe_types:
            UnEquip(RhandLayer())
            Wait(self.LAG_FAILSAFE)
            self.__equip_axe()
            return True
        else:
            raise Exception('No axe found in the backpack or hands')


    def __equip_axe(self):
        if FindTypesArrayEx(self.axe_types, [0], [Backpack()], False) > 0:
            if FindCount() < 2:
                self.current_axe = FindItem()
                Equip(LhandLayer(), self.current_axe)
            else:
                ClientPrint('Two or more axes found in bag, choose one:')
                CancelWaitTarget()
                CancelTarget()
                ClientRequestObjectTarget()
                while ClientTargetResponsePresent() is False:
                    Wait(1)
                target_response = ClientTargetResponse()
                self.current_axe = target_response['ID']
                Equip(LhandLayer(), self.current_axe)
        else:
            raise Exception('No axes in the backpack')
    
    def get_tree_name(self):
        tree_name = [x['name'] for x in self.trees if x['tile'] == str(self.current_tree['tile'])][0]
        return tree_name
    
    @property
    def name(self, tile):
        return [tree['name'] for tree in self.trees if tree['tile'] == tile].pop(0)

    def find_trees(self, radius=8):
        char_x = GetX(Self())
        char_y = GetY(Self())

        self.tree_map = find_tiles(self.tree_tiles, char_x, char_y, radius)
        self.tree_map = [{"tile": tile, "x": x, "y": y, "z": z} for tile, x, y, z in self.tree_map]
        self.tree = iter(self.tree_map)
        return self.tree_map
    
    def next_tree(self):
        try:
            self.current_tree = next(self.tree)
            return self.current_tree
        except StopIteration:
            return False

    def chop(self):
        CancelWaitTarget()
        CancelTarget()

        time_before = dt.datetime.now()
        UseObject(self.current_axe)
        while InJournalBetweenTimes('What do you want to use this item on?', time_before, dt.datetime.now()) <= 0:
            Wait(1)
        
        WaitTargetTile(
            self.current_tree['tile'],
            self.current_tree['x'],
            self.current_tree['y'],
            self.current_tree['z'], 
        )
        Wait(self.LAG_FAILSAFE)
        if WaitJournalLine(time_before, self.NO_LOGS_MSG, 4000):
            print(f'No more logs available on this tree.')
            return False
        else:
            return True
    
    def harvest(self, tile, x, y, z):
        CancelWaitTarget()
        CancelTarget()
        
        timestamp_before = dt.datetime.now()
        UseObject(self.current_axe)
        while InJournalBetweenTimes('What do you want to use this item on?', timestamp_before, dt.datetime.now()) <= 0:
            Wait(1)
        
        WaitTargetTile(tile, x, y, z)
        Wait(self.LAG_FAILSAFE)

        if WaitJournalLine(timestamp_before, self.NO_LOGS_MSG, 4000):
            print('No more logs available on this tree.')
            return False
        return True

    def can_convert_logs(self):
        board_type = int([x['type'] for x in self.resource_types if x['name'] == 'logs'][0],16)
        FindType(board_type, Backpack())
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
                    UseObject(self.current_axe)
                    while InJournalBetweenTimes('What do you want to use this item on?', time_before, dt.datetime.now()) <= 0:
                        Wait(1)
                    
                    WaitTargetObject(log)
                    Wait(self.LAG_FAILSAFE)
            return
        




