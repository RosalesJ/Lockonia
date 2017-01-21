'''
A collection of Sheet models building off gspread Worksheet models
These models are very row-focused, meaning the actions built off of gspread
are focused on getting rows with certain falues, adding rows, removing rows etc.
'''

from datetime import date
import os
import gspread
from gspread.ns import _ns, ATOM_NS
from gspread.models import Worksheet
from oauth2client.service_account import ServiceAccountCredentials
from User import User

SCOPE = ['https://spreadsheets.google.com/feeds']
CLIENT_SECRET = "client_secret.json"

def get_credentials():
    ''' Get the credentials for Google Sheets. '''
    return ServiceAccountCredentials.from_json_keyfile_name(CLIENT_SECRET, SCOPE)

def get_spreadsheet(sheetname):
    ''' Return a spreadsheet given the name of the sheet. '''
    credentials = get_credentials()
    gc = gspread.authorize(credentials)
    return gc.open(sheetname)


                ##### SHEET CLASS #####


class Sheet(Worksheet):
    ''' Represents a worksheet, extends gspread Worksheet. '''

    def __init__(self, string, sheetnum):
        ''' Initialize the sheet given the name of the spreadsheet and number of work. '''
        spreadsheet = get_spreadsheet(string)
        feed = spreadsheet.client.get_worksheets_feed(spreadsheet)
        lst = feed.findall(_ns('entry'))
        super(Sheet, self).__init__(spreadsheet, lst[sheetnum])

    def get_row_number(self, value):
        '''
        Return the row number of the sheet the value is located at.
        Return None if the value cannot be found in the sheet.
        '''

        try:
            return self.find(value).row
        except:
            return None

    def contains(self, value):
        ''' Return whether or not a value is in the sheet. '''
        if self.get_row_number(value):
            return True
        return False

    def get_row(self, value):
        '''
        Return a list of the entire row of values that contains the value provided.
        Return None if there is no such item in the sheet.
        '''
        user_row = self.get_row_number(value)
        if user_row:
            return self.row_values(user_row)
        return None

    def remove_row(self, value):
        '''
        Remove the entire row that contains the value provided.
        Return True if the operation was successful.
        Return False if there is no shuch item in the sheet.
        '''

        row_number = self.get_row_number(value)

        if not row_number:
            return False

        if row_number != self.row_count:
            ran = "A%d:%s"%(row_number, self.get_addr_int(self.row_count, self.col_count))
            cell_list = self.range(ran)

            for i in range(len(cell_list) - self.col_count):
                cell_list[i].value = cell_list[i + self.col_count].value

            self.update_cells(cell_list)

        self.resize(self.row_count - 1, self.col_count)
        return True

    def add_row(self, values):
        ''' Add a row to a specified sheet given a list of values. '''
        self.append_row(values)
        return True

    def write_csv(self, path):
        ''' Export the Sheet as a .csv to a specified path location. '''
        today = date.today()
        cur_date = str(today.year) + '-' + str(today.month) + '-' + str(today.day)
        write_path = os.path.join(path, (cur_date + ' Entry Log.csv'))

        with open(write_path, 'wb') as elog:
            elog.write(self.export(format='csv'))


                #### USER SHEET CLASS #####

class UserSheet(Sheet):
    ''' Represents a user sheet, inherits everything from Sheet. '''

    def __init__(self, string, sheetnum):
        ''' Initialize a new User_Sheet given the name of the sheet.'''

        #Call the constructor of its supertype Sheet
        super(User_Sheet, self).__init__(string, sheetnum)

    def add_user(self, user):
        ''' Add a user to an instance of User_Sheet. '''
        return self.add_row(user.to_array())

    def remove_user(self, userID):
        ''' Remove a user from this User_Sheet '''
        if not self.contains(userID):
            return False
        return self.remove_row(userID)

    def get_user(self, userID):
        '''
        Return a User object given an identifier.
        Return None if no row can be found that contains the identifier
        or if the row is the very first row.
        '''
        values = self.get_row(userID)
        if self.get_row_number(userID) == 1 or not values:
            return None
        return User.from_array(values)

    def contains(self, userID):
        '''
        Returns whether or not a user with a given identifier is in
        this sheet. Return false if no row with the given identifier
        can be found or the row is the very first row of the sheet
        '''
        if self.get_user(userID):
            return True
        return False


                #### ENTRY SHEET CLASS #####


class EntrySheet(Sheet):
    ''' Worksheet to log activity with Lockonia. '''

    def __init__(self, string, sheetnum):
        ''' Initialize a new Entry_Sheet with the given name of the sheet. '''

        #Call the constructor of its supertype Sheet.
        super(Entry_Sheet, self).__init__(string, sheetnum)

    def add_event(self, Event):
        ''' Add an event to the Entry Sheet. '''
        return self.add_row(Event.to_array)

    def download(self, path):
        ''' Export the current Entry Log as a .csv, and clears all entries '''
        self.write_csv(path)
        self.resize(1, 0)
