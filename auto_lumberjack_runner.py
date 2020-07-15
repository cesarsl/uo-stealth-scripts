import os
import json
import PySimpleGUI as psg

from stealth import Self, GetX, GetY, CharName, ClientPrint, UseObject, Backpack, \
                    FindTypesArrayEx, GetFindedList, MoveItem, Wait, newMoveXY, \
                    FindTypeEx, FindFullQuantity

from include.constants import TREES, WEAPONS, MATERIALS, LAG_THRESHOLD
from include.helpers import get_object_id, is_overweight
from include.lumberjacking import Lumberjacking
from include.runebook import Runebook
from include.trees import Trees

WAITING = 700 # Lag prevention

class Runner:
    def __init__(self):
        self._char_name = CharName()
        self._running = False
        self._start_xy = (GetX(Self()), GetY(Self()))
        self._lumberjacking = Lumberjacking()
        self._deposit_box = None
        self._home_runebook = None
        self._home_rune_pos = None
        self._trees = None
        self._trees_runebooks = []
        self._current_book = None
        self._current_rune = None
        self._last_rune = None
        self._current_tree = None
        self._resources_found_list = []
        self._is_at_home = None
        self._setup()
    
    def _setup(self):
        setup_cache_file = os.path.realpath('./../cache/autolumber.json')
        
        try:
            with open(setup_cache_file, 'r') as setup_file:
                setup_json = json.load(setup_file)
                char_config = setup_json.get(self._char_name)
                self._deposit_box = char_config.get('deposit_box')
                self._home_runebook = Runebook(char_config.get('home_runebook'))
                self._home_rune_pos = char_config.get('home_rune_pos')
                for book in char_config.get('trees_books'):
                    self._trees_runebooks.append(Runebook(book))
            pass
        except OSError as err:
            print(f'File not found. Error {err}.')
            print('Setup file not found. Starting new configuration...')
            ClientPrint('Select your deposit box:')
            self._deposit_box = get_object_id()
            
            UseObject(Backpack())
            ClientPrint('Select the runebook where is your house\'s rune:')
            self._home_runebook = Runebook(get_object_id())
            self._home_rune_pos = int(psg.PopupGetText(
                'Which position is your rune in the book (1-16)?',
                title='Home Runebook Setup',
                keep_on_top=True
            ))

            trees_books_count = int(psg.PopupGetText(
                'How many trees books you will use?',
                title='Trees Runebooks Setup',
                keep_on_top=True
            ))
            for i in range(trees_books_count):
                ClientPrint(f'Select your book {i+1}:')
                self._trees_runebooks.append(Runebook(get_object_id()))
            
            setup_data = {
                self._char_name: {
                    'deposit_box': self._deposit_box,
                    'home_runebook': self._home_runebook.id,
                    'home_rune_pos': self._home_rune_pos,
                    'trees_books': [book.id for book in self._trees_runebooks]
                }
            }

            with open(setup_cache_file, 'w+') as setup_file:
                json.dump(setup_data, setup_file)
            pass
        return

    def _can_store_items(self):
        storage_types = [material for material in MATERIALS.get('lumberjacking')]
        FindTypesArrayEx(storage_types, [0xffff], [Backpack()], False)
        self._resources_found_list = GetFindedList()

        if len(self._resources_found_list) == 0:
            return False
        return True
    
    def _deposit_items(self):
        for item in self._resources_found_list:
            MoveItem(item, 0, self._deposit_box, 0, 0, 0)
            Wait(WAITING)
        return

    def _store_resources(self):
        self._home_runebook.travel(self._home_rune_pos)
        if self._lumberjacking.can_convert_logs():
            self._lumberjacking.convert_logs()
        
        if self._can_store_items():
            self._deposit_items()

    def _get_material_type(self, name):
        return [uid for uid, props in MATERIALS.get('lumberjacking').items() if props.get('name') == name][0]
    
    def _get_material_colors(self, material_type):
        colors = []
        for material, props in MATERIALS.get('lumberjacking').items():
            if material == material_type:
                [colors.append(color) for color in props.get('colors')]
        return colors
    
    def _get_color_name(self, material_type, color_id):
        colors = []
        for material, props in MATERIALS.get('lumberjacking').items():
            if material == material_type:
                for color, name  in props.get('colors').items():
                    if color == color_id:
                        return name

    def _count_resources(self):
        board_type = self._get_material_type('boards')
        UseObject(self._deposit_box)
        Wait(LAG_THRESHOLD)
        print('Deposit Box Inventory')
        print('---------------------')
        for color in self._get_material_colors(board_type):
            FindTypeEx(board_type, color, self._deposit_box, False)
            print(f'{self._get_color_name(board_type, color)}: {FindFullQuantity()}')
        return

    def start(self):
        self._running = True
        print('Starting the Auto Lumberjacking Recall.')
        while self._running is True:
            if is_overweight() is True:
                if self._lumberjacking.can_convert_logs() is False:
                    if self._can_store_items() is True:
                        self._store_resources()
                    else:
                        raise Exception('Overcrumbed. Can\'t proceed.')
            
            if not self._current_rune and not self._last_rune and not self._current_book:
                self._current_book = 0
                self._last_rune = 0
                self._current_rune = 1
            
            if self._last_rune != self._current_rune:
                print(f'Current book is {self._current_book + 1} and rune is {self._current_rune}')
                self._last_rune = self._current_rune
                self._trees_runebooks[self._current_book].travel(self._current_rune)
                self._trees = Trees()
            
            for tree in self._trees:
                if tree is not None:
                    print(f'Going to {tree.get("name")} at {tree.get("x")}, {tree.get("y")}')
                    newMoveXY(tree.get('x'), tree.get('y'), True, 1, True)
                    still_have_logs = True
                    while still_have_logs:
                        if is_overweight():
                            if self._lumberjacking.can_convert_logs():
                                print('Excess weight. Transforming logs into boards.')
                                self._lumberjacking.convert_logs()

                            if is_overweight():
                                print('No more logs to convert into boards. Going to deposit box.')
                                self._store_resources()
                                self._count_resources()
                                print('Going back to the forest.')
                                self._trees_runebooks[self._current_book].travel(self._current_rune)
                                print(f'Going back to {tree.get("name")} at {tree.get("x")}, {tree.get("y")}')
                                newMoveXY(tree.get('x'), tree.get('y'), True, 1, True)
                        
                        still_have_logs = self._lumberjacking.harvest(
                            tree.get('tile'),
                            tree.get('x'),
                            tree.get('y'),
                            tree.get('z')
                        )
                else:
                    break

            if self._current_rune:
                if self._current_rune < 16:
                    self._current_rune += 1
                else:
                    if self._current_book < len(self._trees_runebooks):
                        self._current_book += 1
                    else:
                        self._current_book = 0
                    self._last_rune = 0
                    self._current_rune = 1

if __name__ == '__main__':
    runner = Runner()
    runner.start()