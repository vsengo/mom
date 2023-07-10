from datetime import timedelta, date
import math
class DateUtil:

    @staticmethod
    def cv2Year(dateList):
        year=[]
        for x in dateList:
            year.append(x.strftime("%Y"))
        return year
    
    @staticmethod
    def dateWeekStarting(raceDay):
        dt = date.today()
        monday=dt - timedelta(days=dt.weekday())
        ndays=(raceDay - monday)
        weeks=math.ceil(ndays.days/7)

        return (monday,weeks)




