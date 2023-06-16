from datetime import timedelta, date

class DateUtil:

    @staticmethod
    def cv2Year(dateList):
        year=[]
        for x in dateList:
            year.append(x.strftime("%Y"))
        return year
    
    @staticmethod
    def dateWeekStarting(d):
        dt = date.today()
        if dt < d:
           return (d,0)
        else:
            ndt=dt - timedelta(days=dt.weekday())
            weeks=(ndt - timedelta(date=d))/7
            return (ndt,weeks)


