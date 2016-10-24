'''
 Jacob Rosales Chase
 A collection of methods to get and modify Google Sheets using gspread
 All methods will take a single value and modify a single row of a sheet
'''

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from User import User

SCOPE = ['https://spreadsheets.google.com/feeds']
CLIENT_SECRET = "client_secret.json"

#gets the credentials for google sheets
def get_credentials():
    return ServiceAccountCredentials.from_json_keyfile_name(CLIENT_SECRET, SCOPE)

#returns a worksheet given the name of the sheet
def get_sheet(sheetname):
    credentials = get_credentials()
    gc = gspread.authorize(credentials)
    worksheet = gc.open(sheetname).sheet1
    return worksheet

#returns the row number of the sheet the value is located at
#return None if the value cannot be found in the sheet
def get_row_number(value, sheet):
    try:
        return sheet.find(value).row
    except:
        return None

#returns whether or not a value is in the sheet
def contains(value, sheet):
    if(get_row_number(value, sheet)):
        return True
    return False

#returns a list of the entire row of values that contains the value provided
#returns None if there is no such item in the sheet
def get_row(value, sheet):
    user_row = get_row_number(value, sheet)
    if(user_row):
        return sheet.row_values(user_row)
    return None

# removes the entire row that contains the value provided
# returns True if the operation was successful
# returns False if there is no shuch item in the sheet
def remove_row(value, sheet):
    row_number = get_row_number(value, sheet)
    if(not row_number):
        return False

    if(row_number != sheet.row_count):
        ran = str("A" + str(row_number) + ":" + "D" + str(sheet.row_count))
        cell_list = sheet.range(ran)

        for i in range(len(cell_list) - sheet.col_count):
            cell_list[i].value = cell_list[i + sheet.col_count].value

        sheet.update_cells(cell_list)

    sheet.resize(sheet.row_count - 1, sheet.col_count)
    return True

# adds a row to a specified sheet given a list of values
def add_row(values, sheet):
    sheet.append_row(values)
    return True

# represents a spreadsheet
class Sheet:
    # initializes the sheet given the name of the sheet
    def __init__(self, string):
        self.name = string
        self.sheet = get_sheet(string)

    #returns the row number of the sheet the value is located at
    #return None if the value cannot be found in the sheet
    def get_row_number(self, value):
        return get_row_number(value, self.sheet)

    #returns whether or not a value is in the sheet
    def contains(self, value):
        return contains(value)

    #returns a list of the entire row of values that contains the value provided
    #returns None if there is no such item in the sheet
    def get_row(self, value):
        return get_row(value, self.sheet)

    # removes the entire row that contains the value provided
    # returns True if the operation was successful
    # returns False if there is no shuch item in the sheet
    def remove_row(self, value):
        return remove_row(value, self.sheet)

    # adds a row to a specified sheet given a list of values
    def add_row(self, values):
        return add_row(values, self.sheet)

# Represents a user sheet, inherits everything from Sheet
class User_Sheet(Sheet):

    # Initializes a new User_Sheet given the name of the sheet
    # Calls the constructor of its supertype Sheet
    def __init__(self, string):
        super(User_Sheet, self).__init__(string)

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
        if(get_row_number(userID, self.sheet) == 1 or not values):
            return None
        return User.from_array(values)

    # returns whether or not a user with a given identifier is in
    # this sheet. Returns false if no row with the given identifier
    # can be found or the row is the very first row of the sheet
    def contains(self, userID):
        if(self.get_user(userID)):
            return True
        return False
