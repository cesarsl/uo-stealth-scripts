from stealth import InJournalBetweenTimes, Wait
from datetime import datetime as dt
from datetime import timedelta

def CheckSave():
    Time = dt.now() - timedelta(0, 30)
    if InJournalBetweenTimes('Saving World State', Time, dt.now()) >= 0:
        Wait(30000)
    
if __name__ == "__main__":
        CheckSave()