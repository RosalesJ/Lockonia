from datetime import datetime
import User

class Event:

    def __init__(self, action, User):
        d = datetime.today()
        # Creation of date string for insertion for a cell
        self.date = str(d.year) + '-' + str(d.month) + '-' + str(d.day)
        # Creation of time string for insertion for a cell
        self.time = str(d.hour) + ':' + str(d.minute) + ':' + str(d.second)
        
        self.action = action
        self.caseID = User.caseID

    def to_array(self):
        arr = []

        arr.append(self.date)
        arr.append(self.time)
        arr.append(self.action)
        arr.append(self.caseID)

        return arr

    def __str__(self):
        return self.date + ' ' + self.time + ' ' + self.action + ' ' + self.caseID


