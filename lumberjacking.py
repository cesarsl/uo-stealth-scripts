from stealth import *

from include.checksave import CheckSave

from datetime import datetime as dt

# TODO Transformar em listas as constantes
AXE_TYPE = 0x0F43
LOG_TYPE = 0x1BDD

NO_LOGS_MSG = 'There\'s not enough wood here to harvest.'
BAD_MSG = 'That is too far away.|Target cannot be seen.'

def check_tree_for_wood(before, after):
    if (
        InJournalBetweenTimes(NO_LOGS_MSG, before, after) > 0 or 
        InJournalBetweenTimes(BAD_MSG, before, after) > 0
        ):
        print('Não tem mais madeira nessa árvore.')
        return False
    return True

def check_axe():
    check_axe_in_hand = ObjAtLayer(LhandLayer())
    # Checking if there's an axe on left hand   
    if (check_axe_in_hand == 0 or ObjAtLayer(RhandLayer()) != 0):
        print('Machado não encontrado... Procurando na mochila.')
        UnEquip(LhandLayer())
        Wait(1000)
        UnEquip(RhandLayer())
        Wait(1000)
        if not (find_and_equipe_axe()):
            return False
    else:
        return True

def find_and_equipe_axe():
    # Look for axe in the bag
    if FindType(AXE_TYPE, Backpack()):
        print('Machado encontrado. Equipando...')
        Equip(LhandLayer(), FindItem())
        Wait(10)
        return True
    else:
        print('Nenhum machado encontrado. Parando o script.')
        return False

def cut_logs_to_boards():
    while FindType(LOG_TYPE, Backpack()):
        print('Transformando logs em boards...')
        if (check_axe()):
            UseObject(ObjAtLayer(LhandLayer()))
            WaitTargetObject(FindItem())
            Wait(1500)
        else:
            return False
    return False

def chop(tile_type, target_x, target_y, target_z):
    # Cancelling previous targets
    CancelWaitTarget()
    CancelTarget()
    check_axe()
    CheckLag()

    now = dt.now()
    counter = 0
    
    UseObject(ObjAtLayer(LhandLayer()))
    while not InJournalBetweenTimes('What do you want to use this item on?', now, dt.now()) >= 0 and counter <= 30:
        counter += 1
        Wait(1000)
    
    counter = 0
    WaitTargetTile(tile_type, target_x, target_y, target_z)
    
    return