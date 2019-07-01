# _*_ coding: utf-8 _*_
# ! python3

# =============================================================================
# Author: César Liedke
# Description: Auto Recall Lumberjacking
# 
# Setup:
#
# 1. Change the `CHEST_TYPE` constant to a secure chest type near the stairs
#    of your house. If you have more than one chest, it may put into a random
#    chest.
#
# 2. You can increase or decrease the search area radius in the `LUMBER_RADIUS`
#    constant
#
# =============================================================================

from stealth import *
from datetime import datetime as dt

from include.helpers import check_overload, runebook_recall, find_tiles

from lumberjacking import cut_logs_to_boards, check_tree_for_wood, chop

# =============
# Setup Section
# =============

LAG_FAILSAFE = 500

CHEST_TYPE = 0x0E43
LUMBER_RADIUS = 8

HOME_RUNE_BOOK = 0x4128FE00
TREE_BOOKS = [
    0x45295BB4,
    0x45294F2C,
    0x4523E2FA 
]

# =====================
# No changes after here
# =====================

TREE_TYPES = [
    3277,
    3283,
    3286,
    3293,
    3299   
]

# =======================
# Lumberjacking materials
# =======================
#
# 0x1BD7 : Boards
# 0x2F5F : Switch
# 0x318F : Bark Fragment
# 0x3190 : Parasitic Plant
# 0x3191 : Luminescent Fungi
# 0x3199 : Brilliant Amber

KEEP_TYPES = [
    0x1BD7,
    0x2F5F,
    0x318F,
    0x3190,
    0x3191,
    0x3199
]

KEEP_NAMES = {
    7127: 'boards',
    12127: 'switchs',
    12687: 'bark fragments',
    12688: 'parasitic plants',
    12689: 'luminescent fungi',
    12697: 'brilliant ambers'
}

can_keep_chopping = True
already_recalled_back = False
current_rune = 0
current_book = 0

# Helper functions

def store_items(current_book, current_rune):
    # Recall home
    print(f'Casa xirrin.')
    recall_status = runebook_recall(HOME_RUNE_BOOK, 0)

    if recall_status:
        # Store items
        if FindType(CHEST_TYPE, Ground()):
            print('Abrindo o baú...')
            chest = FindItem()
            for item_type in KEEP_TYPES:
                while FindType(item_type, Backpack()):
                    item_pile = FindItem()
                    print(f'Guardando {KEEP_NAMES[GetType(item_pile)]} no baú...')
                    DragItem(item_pile, 0)
                    Wait(LAG_FAILSAFE)
                    DropItem(chest, 0, 0 , 0)
                    Wait(LAG_FAILSAFE)

        # Go back to the current rune
        print('Este idiota xirrion.')
        recall_status = runebook_recall(TREE_BOOKS[current_book], current_rune)

        if not recall_status:
            print('Não foi possível retornar para a floresta. Parando script.')
            exit(0)
        
        return True
    else:
        print('Não foi possível retornar para casa. Parando script.')
        exit(0)

# Start
print(f'Iniciando o corte de lenha.')

while can_keep_chopping:
    if not check_overload():
        if not already_recalled_back:
            print(f'Indo para a runa {current_rune + 1} do livro {current_book + 1}.')
            recall_status = runebook_recall(TREE_BOOKS[current_book], current_rune)
            
            if not recall_status:
                print('Não foi possível retornar para a floresta. Parando script.')
                exit(0)

        char_x = GetX(Self())
        char_y = GetY(Self())

        tree_map = find_tiles(TREE_TYPES, char_x, char_y, LUMBER_RADIUS)
        print(f'Foram encontradas {len(tree_map)} árvores.')
        
        counter = 0

        for tile, tile_x, tile_y, tile_z in tree_map:
            AddToSystemJournal(f'Indo para a árvore {counter + 1} de {len(tree_map)} em {tile_x}, {tile_y} | Peso atual: {Weight()}')
            
            before = dt.now()
            Wait(1000)
            after = dt.now()

            while check_tree_for_wood(before, after) and not check_overload() and counter <= len(tree_map):
                newMoveXY(tile_x, tile_y, True, 1, True)

                before = dt.now()
                chop(tile, tile_x, tile_y, tile_z)
                Wait(1000)
                after = dt.now()
                
                if check_overload():
                    can_reduce_weigth = cut_logs_to_boards()
                    if not can_reduce_weigth:
                        already_recalled_back = store_items(current_book, current_rune)

            counter += 1
        
        already_recalled_back = False

        if current_rune >= 15 and current_book < len(TREE_BOOKS):
            current_book += 1

        if current_book == len(TREE_BOOKS):
            current_book = 0

        if current_rune < 15:
            current_rune += 1
        else:
            current_rune = 0  
    else:
        can_reduce_weigth = cut_logs_to_boards()
        if not can_reduce_weigth:
            already_recalled_back = store_items(current_book, current_rune)
        else:
            already_recalled_back = False
            

            
        


