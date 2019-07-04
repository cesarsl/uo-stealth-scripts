import time

from stealth import *

class Gumps:
    def __init__(self):
        return

    def close_gump(self, gump_index=-1, simple_gump=True, wait=True, timeout=5000, delay=1):
        _gump_index = self.get_last_gump_index() if gump_index < 0 else gump_index
        gump_serial = self.get_gump_serial_from_index(_gump_index)

        if simple_gump:
            CloseSimpleGump(_gump_index)
        else:
            # TODO: implementar
            pass
        
        if wait:
            timeout /= 1000
            timeout += time.time()
            while time.time() <= timeout:
                if self.get_gump_serial_from_index() != gump_serial:
                    return True
                else:
                    Wait(delay)
            return False

    def get_gump_serial_from_index(self, gump_index=-1):
        return GetGumpSerial(self.get_last_gump_index() if gump_index < 0 else gump_index)
    
    def get_gump_id_from_index(self, gump_index=-1):
        return GetGumpID(self.get_last_gump_index() if gump_index < 0 else gump_index)

    def get_last_gump_index(self):
        return (GetGumpsCount() - 1) if GetGumpsCount() > 0 else -1
    
    def get_gump_dict(self, gump_index=0):
        return GetGumpInfo(gump_index)
    
    def get_gump_from_object(self, object_id, gump_id=0, wait=True,
            timeout=5000, delay=1, use_delay=700):
        gump_serial = self.get_gump_serial_from_index()
        UseObject(object_id)
        Wait(use_delay)

        if wait:
            if not gump_id or gump_id == 0:
                raise TypeError('No gump ID passed.')
            
            timeout /= 1000
            timeout += time.time()

            while time.time() <= timeout:
                if self.get_gump_serial_from_index() != gump_serial and self.get_gump_id_from_index() == gump_id:
                    return True
                else:
                    Wait(delay) 
            
            return False
        return None
            
