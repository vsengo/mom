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
            print(d)
            return d
        else:
            return dt - timedelta(days=dt.weekday())

