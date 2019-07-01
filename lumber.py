# -*- coding: utf-8 -*-

from datetime import datetime as dt
from stealth import *

#OTHER COLORS
logs = 0x19B9

#               iron,   copper, bd,     pagan,  silver
trash_colors = [0x0000, 0x08EB, 0x0425, 0x050C, 0x04EB]

bad_points = []
axe = 0x2398
failMsg = ''
emptyMsg = "You stop |You can't|There's no"
badMsg = 'see that| here.|Это слишком далеко.|too far'
tmpMsg = 'Это слишком далеко.'
	
def FindTiles(center_x, center_y, radius):
    min_x, min_y = center_x-radius, center_y-radius
    max_x, max_y = center_x+radius, center_y+radius
    tiles_coords = []
    tiles_coords += GetStaticTilesArray(min_x,min_y,max_x,max_y,WorldNum(),3283)
    return tiles_coords


def ChopTree(t,x,y):
    CancelWaitTarget()
    CancelTarget()
    now = dt.now()
    counter = 0
    global loop
    if not ObjAtLayer(RhandLayer()):
        if FindType(axe, Backpack()):
            Equip(RhandLayer(), FindItem())
            Wait(1000)
        else:
            AddToSystemJournal('no pickaxe found!')
            Wait(1000)
            return
    CheckLag()    
    UseObject(ObjAtLayer(RhandLayer()))
    while not InJournalBetweenTimes('Select', now, dt.now()) >=0 and counter <= 30:
        counter += 1
    counter = 0
    WaitTargetTile(t,x,y,0)
    now = dt.now()
    while not InJournalBetweenTimes(badMsg+'|'+emptyMsg, now, dt.now()) >=0 and counter <= 180:
        counter += 1
        Wait(1000)
        CheckLag()                        
    if InJournalBetweenTimes(badMsg, now, dt.now()) >=0:
        if [x,y] not in bad_points:
            bad_points.append([x,y])
    return

def StartLumber():
    while not newMoveXY(5790, 1120, True, 0, True):
        Wait(1000)
    while Weight() < 60000:
        loop = 0
        for t,x,y,z in FindTiles(GetX(Self()),GetY(Self()), 15):
            if ([x,y] not in bad_points) and newMoveXY(x,y,True,1,True):
                AddToSystemJournal('lubmer at {0} {1} - weight: {2}'.format(x, y, Weight()))
                ChopTree(t,x,y)
    return

StartLumber()