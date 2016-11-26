
from datetime import datetime
import User


class Event:
    '''
    Object class to contain Events, which are added to the Entry Log.
    '''

    def __init__(self, action, User):
        today = datetime.today()
        # Creation of date string for insertion for a cell
        self.date = str(today.year) + '-' + str(today.month) + '-' + str(today.day)
        # Creation of time string for insertion for a cell
        self.time = str(today.hour) + ':' + str(today.minute) + ':' + str(today.second)

        self.action = action
        self.caseID = User.caseID

    def to_array(self):
        ''' Create list representation of the Event. '''
        arr = []

        arr.append(self.date)
        arr.append(self.time)
        arr.append(self.action)
        arr.append(self.caseID)

        return arr

    def __str__(self):
        return self.date + ' ' + self.time + ' ' + self.action + ' ' + self.caseID


