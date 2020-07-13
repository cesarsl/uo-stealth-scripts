import os

from include.helpers import find_tiles, load_resources

from stealth import Self, GetX, GetY

LUMBER_RESOURCES = load_resources(
    os.path.realpath('./../scripts/assets/json/lumberjacking.json')
)
TREES_DATA = LUMBER_RESOURCES.get('trees')
TREES_NAMES = {int(tree.get('tile')): tree.get('name') for tree in TREES_DATA}
TREES_TILES = [int(tree.get('tile')) for tree in TREES_DATA]

class Trees:
    def __init__(self):
        self._trees = self.find_trees()
        self._current_tree = None
    
    def find_trees(self, radius=8):
        tiles = find_tiles(
            TREES_TILES,
            self._current_x(),
            self._current_y(),
            radius
        )
        return tiles

    def _current_x(self):
        return int(GetX(Self()))
    
    def _current_y(self):
        return int(GetY(Self()))
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if len(self._trees) == 0:
            return
        self._current_tree = self._trees[0]
        self._trees.pop(0)
        
        return {
                'name': TREES_NAMES.get(self._current_tree[0]),
                'tile': self._current_tree[0],
                'x': self._current_tree[1],
                'y': self._current_tree[2],
                'z': self._current_tree[3]
        }
