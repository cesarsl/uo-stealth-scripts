import os
import json
import time
from datetime import datetime as dt

from stealth import GetStaticTilesArray, WorldNum, Weight, MaxWeight, \
                    ClientRequestObjectTarget, ClientTargetResponsePresent, \
                    ClientTargetResponse, Wait

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

def is_overweight():
    """"Return True if character is over MaxWeigth * 0.15, otherwise
    returns False.

    Returns
    -------
    Boolean
        True if overweight, False otherwise.
    """
    if Weight() > MaxWeight() - (MaxWeight() * 0.15):
        return True
    else:
        return False

def load_resources(path):
    with open(os.path.realpath(path), 'r') as resource:
        return json.load(resource)

def get_object_id():
    ClientRequestObjectTarget()
    while ClientTargetResponsePresent() is False:
        Wait(1)
    return ClientTargetResponse().get('ID')