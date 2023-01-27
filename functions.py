import cache
import datetime

def getShipInfo(hex:str, day:datetime.date, repeat:int=1):
    ships = cache.getFromCache("ships", date=day)
    for ship in ships:
        if ship["hex_code"] == hex:
            return ship
    if repeat > 0:
        return getShipInfo(hex, day+datetime.timedelta(1), repeat-1)
    raise NameError("Couldn't find ship {} on day {}, nor the next {} days".format(hex, day, repeat-1))

def dateRange(startDate:datetime.date=cache.startDate, endDate:datetime.date=datetime.date.today()):
    for dayCount in range((endDate-startDate).days):
        day = startDate+datetime.timedelta(dayCount)
        daysLeft = (endDate-startDate).days-dayCount
        yield (day, daysLeft)