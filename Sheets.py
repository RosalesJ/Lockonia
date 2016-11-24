'''
A collection of Sheet models building off gspread Worksheet models
These models are very row-focused, meaning the actions built off of gspread
are focused on getting rows with certain falues, adding rows, removing rows etc.
'''

import gspread
from gspread.models import Worksheet
from oauth2client.service_account import ServiceAccountCredentials
from gspread.ns import _ns, ATOM_NS
from User import User

SCOPE = ['https://spreadsheets.google.com/feeds']
CLIENT_SECRET = "client_secret.json"

#gets the credentials for google sheets
def get_credentials():
    return ServiceAccountCredentials.from_json_keyfile_name(CLIENT_SECRET, SCOPE)

#returns a spreadsheet given the name of the sheet
def get_spreadsheet(sheetname):
    credentials = get_credentials()
    gc = gspread.authorize(credentials)
    return gc.open(sheetname)


                ##### SHEET CLASS #####


# represents a worksheet, extends gspread Worksheet
class Sheet(Worksheet):
    # initializes the sheet given the name of the spreadsheet and number of work
    def __init__(self, string, sheetnum):
        spreadsheet = get_spreadsheet(string)
        feed = spreadsheet.client.get_worksheets_feed(spreadsheet)
        lst = feed.findall(_ns('entry'))
        super(Sheet, self).__init__(spreadsheet, lst[sheetnum])

    #returns the row number of the sheet the value is located at
    #return None if the value cannot be found in the sheet
    def get_row_number(self, value):
        try:
            return self.find(value).row
        except:
            return None

    #returns whether or not a value is in the sheet
    def contains(self, value):
        if(self.get_row_number(value)):
            return True
        return False

    #returns a list of the entire row of values that contains the value provided
    #returns None if there is no such item in the sheet
    def get_row(self, value):
        user_row = self.get_row_number(value)
        if(user_row):
            return self.row_values(user_row)
        return None

    # removes the entire row that contains the value provided
    # returns True if the operation was successful
    # returns False if there is no shuch item in the sheet
    def remove_row(self, value):
        row_number = self.get_row_number(value)
        if(not row_number):
            return False

        if(row_number != self.row_count):
            ran = "A%d:%s"%(row_number, self.get_addr_int(self.row_count, self.col_count))
            cell_list = self.range(ran)

            for i in range(len(cell_list) - self.col_count):
                cell_list[i].value = cell_list[i + self.col_count].value

            self.update_cells(cell_list)

        self.resize(self.row_count - 1, self.col_count)
        return True

    # adds a row to a specified sheet given a list of values
    def add_row(self, values):
        self.append_row(values)
        return True


                #### USER SHEET CLASS #####


# Represents a user sheet, inherits everything from Sheet
class User_Sheet(Sheet):

    # Initializes a new User_Sheet given the name of the sheet
    # Calls the constructor of its supertype Sheet
    def __init__(self, string, sheetnum):
        super(User_Sheet, self).__init__(string, sheetnum)

    # adds a user to an instance of User_Sheet
    def add_user(self, user):
        return self.add_row(user.to_array())

    # removes a user from this User_Sheet
    def remove_user(self, userID):
        if(not self.contains(userID)):
            return False
        return self.remove_row(userID)

    # returns a User object given an identifyer
    # returns None if no row can be found that contains the identifier
    # or if the row is the very first row
    def get_user(self, userID):
        values = self.get_row(userID)
        if(self.get_row_number(userID) == 1 or not values):
            return None
        return User.from_array(values)

    # returns whether or not a user with a given identifier is in
    # this sheet. Returns false if no row with the given identifier
    # can be found or the row is the very first row of the sheet
    def contains(self, userID):
        if(self.get_user(userID)):
            return True
        return False
