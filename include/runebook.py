import datetime as dt

from stealth import ClientRequestObjectTarget, ClientTargetResponsePresent, \
                    ClientTargetResponse, Wait, GetTooltip, GetGumpTextLines, \
                    GetX, GetY, Self, WaitGump, WaitJournalLine, FoundedParamID

from include.gumps import Gumps

class Runebook:
    """Runebook Manipulation Class"""
    LAG_FAILSAFE = 750
    RUNEBOOK_GUMP_ID = 0x554B87F3
    type = 0x22C5
    
    def __init__(self, runebook_id=None):
        if runebook_id != None:
            self.id = runebook_id
        else:
            self.id = self.__choose_book()
        
        self.name = self.__get_book_name()
        self.gump = Gumps()
        self.gump_dict = self.__get_gump_dict()
        self.rune_names = self.__get_rune_names()
        self.rune_count = len(self.rune_names)

        self.gump.close_gump()
    
    def __choose_book(self):
        ClientRequestObjectTarget()
        while ClientTargetResponsePresent() is False:
            Wait(1)
        runebook = ClientTargetResponse()
        if runebook['ID'] != 0:
            return runebook['ID']
        else:
            return None
    
    def __get_book_name(self):
        text = GetTooltip(self.id)
        text = text.split('|')
        return text[len(text)-1]
    
    def __get_gump_dict(self):
        while self.gump.get_gump_from_object(self.id, self.RUNEBOOK_GUMP_ID) is False:
            Wait(1)
        gump_dict = self.gump.get_gump_dict(self.gump.get_last_gump_index())
        return gump_dict

    def __get_rune_names(self):
        rune_names = []
        text_lines = []
        while not text_lines:
            text_lines = GetGumpTextLines(self.gump.get_last_gump_index())
            Wait(1000)
        rune_names = [text_lines[x['TextID']] for x in self.gump_dict['CroppedText'] if
                        x['Page'] == 1 and text_lines[x['TextID']] != 'Empty']
        return rune_names
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        return self.name

    def travel(self, rune_position, method='r', 
            retry=['fizzles', 'recover', 'reagents', 'tithing', 'mana']):
        
        BAD_MSGS = [
            'fizzles', 'location is blocked', 'not yet recovered',
            'no charges left', 'more reagents', 'tithing points',
            'insufficient mana', 'not marked', 'cannot teleport from here',
        ]

        if rune_position not in list(range(1,17)):
            raise Exception(f'Rune number must be between 1 and 16, got {rune_position}')
        
        if rune_position > self.rune_count:
            raise Exception(f'This book only contains {self.rune_count} runes, got position {rune_position}')

        if method not in ['r', 'g', 's', 'c']:
            raise Exception(f'Unknown travel method: {method}')

        if not isinstance(retry, list):
            raise TypeError(f'Retry phrases require a list, got {type(retry)}')
        
        while True:
            char_pos = (GetX(Self()), GetY(Self()))

            while not self.gump.get_gump_from_object(self.id, self.RUNEBOOK_GUMP_ID):
                Wait(1)
            
            if method == 'r':
                gump_button = 5 + ((rune_position - 1) * 6)
            elif method == 'g':
                gump_button = 6 + ((rune_position - 1) * 6)
            elif method == 'c':
                gump_button = 7 + ((rune_position - 1) * 6)
            elif method == 's':
                raise Exception('Scroll traveling not implemented yet')
            
            before = dt.datetime.now()
            timeout = before + dt.timedelta(seconds=7)
            WaitGump(gump_button)

            if WaitJournalLine(before, ('|').join(BAD_MSGS), 4000):
                if BAD_MSGS[FoundedParamID()] not in retry:
                    return BAD_MSGS[FoundedParamID()]
            else:
                if method == 'g':
                    pass
                while dt.datetime.now() < timeout:
                    if (GetX(Self()), GetY(Self())) != char_pos:
                        return 'success'
                    else:
                        Wait(1)
        
        return 'unknown'

    def drop_rune(self, position):
        return
    
    def add_rune(self, rune_id):
        return