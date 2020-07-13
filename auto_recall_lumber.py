import os
import json
import PySimpleGUI as sg

from stealth import *

from include.runebook import Runebook
from include.lumberjacking import Lumberjacking
from include.helpers import is_overweight

class AutoLumber:

    def __init__(self):
        self.LAG_FAILSAFE = 700
        self.start_pos = { 'x': GetX(Self()), 'y': GetY(Self()) }
        self.overweight = is_overweight()
        self.lumberjacking = Lumberjacking()
        self.deposit_box = None
        self.home_runebook = None
        self.home_rune = None
        self.tree_runebook = None
        self.current_rune = None
        self.last_rune = None
        self.current_tree = None
        self.resources_found = None
        self.status = False
        self.__setup()
    
    def start(self):
        self.status = True
        print('Starting Auto Lumber Recall.')
        while self.status is True:
            if self.overweight is True:
                if self.lumberjacking.can_convert_logs() is False:
                    can_remove = self.__check_backpack_items()

                    if can_remove is True:
                        self.__recall_home()
                    else:
                        raise Exception('You\'re overcrumbed. Remove some'
                                + ' weight and try again.')
                
            if not self.current_rune and not self.last_rune:
                self.last_rune = 0
                self.current_rune = 1

            if self.last_rune != self.current_rune:           
                print(f'Current rune number is {self.current_rune}')
                self.last_rune = self.current_rune
                self.tree_runebook.travel(self.current_rune)
            
            if not self.current_tree:
                self.lumberjacking.find_trees()
                self.current_tree = self.lumberjacking.next_tree()
            
            if self.current_tree:                
                print(f"Going to {self.lumberjacking.get_tree_name()} at {self.current_tree['x']}, {self.current_tree['y']}")
                newMoveXY(self.current_tree['x'], self.current_tree['y'], 
                        True, 1, True)
                
                chopping = True
                
                while chopping:
                    self.overweight = is_overweight()
                
                    if self.overweight is True:
                        if self.lumberjacking.can_convert_logs():
                            print(f'Excess weight. Trying to transform logs into boards.')
                            self.lumberjacking.convert_logs()
                            self.overweight = is_overweight()
                        
                        if self.overweight is True:
                            print(f'Can\'t transform any more logs in boards. Going to storage.')
                            self.__recall_home()
                            
                            print(f'Going back to the forest.')
                            self.tree_runebook.travel(self.current_rune)
                            
                            print(f"Going back to the tree at "
                                    + f"{self.current_tree['x']}, " 
                                    + f"{self.current_tree['y']}")
                            newMoveXY(self.current_tree['x'], 
                                    self.current_tree['y'], True, 1, True)

                    chopping = self.lumberjacking.chop()
                
                self.current_tree = self.lumberjacking.next_tree()
                
                if self.current_tree == False:
                    if self.current_rune < 16:
                            self.current_rune += 1
                    else:
                        self.last_rune = 1
                        self.current_rune = 1 
                else:
                    self.last_rune = self.current_rune

    
    def __get_obj_id(self):
        ClientRequestObjectTarget()
        while ClientTargetResponsePresent() is False:
            Wait(1)
        obj_id = ClientTargetResponse()
        return obj_id

    
    def __setup(self):
        json_path = os.path.realpath("./../cache/lumberjacking.json")

        try:
            with open(json_path, 'r') as json_config:
                config = json.load(json_config)
            
            self.deposit_box = config['deposit_box']
            self.home_runebook = Runebook(config['home_runebook'])
            self.home_rune = config['home_rune']
            self.tree_runebook = Runebook(config['tree_runebook'])
            pass
        except OSError as error:
            print(f'Setup file not found. Starting setup...')
            ClientPrint('Select your deposit box, where resources taken from trees'
                    + ' will be stored:')
            self.deposit_box = self.__get_obj_id()
            self.start_pos = { 'x': GetX(Self()), 'y': GetY(Self()) }
            
            UseObject(Backpack())

            ClientPrint('Select the runebook where is your house\'s rune:')
            self.home_runebook = Runebook(self.__get_obj_id().get('ID'))
            self.home_rune = int(sg.PopupGetText('Set your home\'s rune position (1-16):',
                    title='Runebook Setup', keep_on_top=True))

            ClientPrint('Select the runebook where are the trees\' runes:')
            self.tree_runebook = Runebook(self.__get_obj_id().get('ID'))

            save_config = {
                'deposit_box': self.deposit_box,
                'home_runebook': self.home_runebook.id,
                'home_rune': self.home_rune,
                'tree_runebook': self.tree_runebook.id
            }

            with open(json_path, 'w') as json_config:
                json.dump(save_config, json_config)

            pass
        return
    
    def __check_backpack_items(self):
        resources_types = [int(x['type'],16) for x in self.lumberjacking.resource_types]
        FindTypesArrayEx(resources_types, [0xffff], [Backpack()], False)
        self.resources_found = GetFindedList()

        if not self.resources_found:
            return False
        else:
            return True

    def __deposit_resources(self):
        for item in self.resources_found:
            MoveItem(item, 0, self.deposit_box.get('ID'), 0, 0, 0)
            Wait(self.LAG_FAILSAFE)
        return True
    
    def __recall_home(self):
        self.home_runebook.travel(self.home_rune)
        self.lumberjacking.convert_logs()
        self.__check_backpack_items()
        self.__deposit_resources()
        self.overweight = is_overweight()

if __name__ == "__main__":
    runner = AutoLumber()
    runner.start()