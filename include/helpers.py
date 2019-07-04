import time
from datetime import datetime as dt

from stealth import *

def find_tiles(tile_types, center_x, center_y, radius):
    """Find every tile(s) around the player in a determined
    radius.

    Parameters
    ----------
    tile_types : array 
        an array of integers
    center_x : integer
        character X position
    center_y : integer 
        character Y position
    radius : integer
        search radius
    
    Returns
    -------
    Array
        Return an array of tuples
    """
    min_x, min_y = center_x-radius, center_y-radius
    max_x, max_y = center_x+radius, center_y+radius
    tiles_coords = []

    for tile in tile_types:
        tiles_coords += GetStaticTilesArray(
            min_x,
            min_y,
            max_x,
            max_y,
            WorldNum(),
            tile
        )

    return tiles_coords

def check_overweight():
    """"Return True if character is over MaxWeigth - 75, otherwise
    returns False.

    Returns
    -------
    Boolean
        True if overweight, False otherwise.
    """
    if Weight() > MaxWeight() - 75:
        return True
    else:
        return False

def runebook_recall(runebook, rune_position):
    """Recall using a runebook.

    Params
    ------
    runebook : Serial
    rune_position : Integer
    """
    RUNE_RECALL_POSITIONS = [5+(x*6) for x in range(0,16)]
    MAX_ATTEMPTS = 3
    BAD_MSG = 'That location is blocked.'
    
    def recall(runebook, rune_position):
        UseObject(runebook)
        Wait(500)
        WaitGump(RUNE_RECALL_POSITIONS[rune_position]) 
        Wait(500)
    
    char_x = GetX(Self())
    char_y = GetY(Self())
    
    diff_x = False
    diff_y = False
    
    attempts = 0

    if (GetMana(Self()) < 30):
        print('Sem mana para magias. Tentando meditar...')
        UseSkill('Meditation')
        Wait(15000)
    
    while not (diff_x or diff_y) and (attempts < MAX_ATTEMPTS):
        attempts += 1
        before_time = dt.now()

        recall(runebook, rune_position)
        Wait(3500)
        
        after_time = dt.now()

        after_x = GetX(Self())
        after_y = GetY(Self())

        diff_x = char_x != after_x
        diff_y = char_y != after_y

        check_recall_msg = InJournalBetweenTimes(
            BAD_MSG, 
            before_time,
            after_time
        )

        if check_recall_msg > 0 and attempts >= MAX_ATTEMPTS:
            status = False
        else:
            status = True
    
    return status
        