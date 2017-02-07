'''
A collection of Sheet models building off gspread Worksheet models
These models are very row-focused, meaning the actions built off of gspread
are focused on getting rows with certain falues, adding rows, removing rows etc.
'''

import os
import datetime
from User import User
import gspread
from gspread.ns import _ns, ATOM_NS
from gspread.models import Worksheet
from oauth2client.service_account import ServiceAccountCredentials


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
        ''' Initialize a new UserSheet given the name of the sheet.'''

        #Call the constructor of its supertype Sheet
        super(UserSheet, self).__init__(string, sheetnum)

    def add_user(self, user):
        ''' Add a user to an instance of UserSheet. '''
        return self.add_row(user.to_array())

    def remove_user(self, userID):
        ''' Remove a user from this UserSheet '''
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
        ''' Initialize a new EntrySheet with the given name of the sheet. '''

        #Call the constructor of its supertype Sheet.
        super(EntrySheet, self).__init__(string, sheetnum)

    def create_log(self, log_type, User, camera):
    	'''
    	Create and return a log in format:
    	DATETIME | log_type | User.name | User.caseID | camera
    	'''
    	log_row = []    # the list to store the
    	log_datetime = time.strftime('%Y-%m-%d %H:%M:%S')
    	log_row = [log_datetime, log_type, User.name, User.caseID, camera]

    	self.add_row(log_row)

    def download(self, path):
        ''' Export the current Entry Log as a .csv, and clears all entries '''
        self.write_csv(path)
        self.resize(1, 0)


class CameraSheet(Sheet):
    ''' Worksheet to track the status of cameras '''

    def __init__(self, string, sheetnum):
        ''' Initializes a new CameraSheet with the given name of sheet. '''

        # Call the constructor of its supertype Sheet
        super(CameraSheet, self).__init__(string, sheetnum)

    def to_list(self):
        '''
        Return the list of availabe cameras
        '''
        available_cameras = []

        for i in range(1, 5):
            if self.acell('B' + str(i)).value == 'IN':
                available_cameras.append(self.acell('A' + str(i)).value)

        return available_cameras

    def withdraw_camera(self, camera):
        ''' Changes the status of the camera from IN to OUT'''
        camera_num = camera[7:]
        if self.acell(B + camera_num).value == 'IN':
            self.update_acell('B' + camera_num, 'OUT')
            return True
        else:
            print("Selected camera is disabled or checked out! Invalid operation.")
            return False

    def deposit_camera(self, camera):
        ''' Changes the status of the camera from OUT to IN'''
        camera_num = camera[7:]
        if self.acell(B + camera_num).value != 'OUT':
            self.update_acell('B' + camera_num, 'IN')
            return True
        else:
            print("Selected camera is disabled or checked in! Invalid operation.")
            return False

    def disable_camera(self):
        '''
        Disable a camera slot, so that the case cannot be withdrawn
        '''
        print('Disabling a camera.')

        # Verifies that there are disabled cameras
        try:
            if int(self.acell('B5').value) > 0:
                camera_disable = input('Select a camera. eg: 3 : ')
            else:
                print('No availabe cameras to disable.')

        except ValueError:
            print('Enabling failed. Invalid values. Please enter only a number. ')

        except:
            print('Unknown error. Verify that your input is only a number.')

        # Validates the camera selection, ceases running with helpful error message if invalid input is entered
        try:
            if int(camera_disable) <= 4 and int(camera_disable) > 0: # Valid camera
                if self.acell('B' + camera_disable).value == 'IN':
                    self.update_acell('B' + camera_disable, 'DISABLED')
                    self.update_acell('B5', int(self.acell('B5').value) - 1)
                    print("Disable completed successfully. There are " + self.acell('B5').value + ' availabe cameras.\n')
                else:
                    print('Cannot disable that camera. It is either already disabled or currently checked out.')
            else:
                print('Disabling failed. Invalid values. Is your input between (inclusive) 1 and 4 ? \n')

        except ValueError:
            print('Disabling failed. Invalid values. Please enter only a number. ')

        except:
            print('Unknown error. Verify that your input is only a number.')

    def enable_camera(self):
        ''' Enables a camera slot, so that the case can be withdrawn. '''
        print('Enabling a camera.')

        # First verifies that there are disabled cameras
        try:
            if int(self.acell('B5').value) < 4:
                camera_enable = input('Select a camera. eg: 3 : ')
            else:
                print('No disabled cameras to enable.')
        except ValueError:
            print('Enabling failed. Invalid values. Please enter only a number. ')
        except:
            print('Unknown error. Verify that your input is only a number.')

        # Validates the camera selection, ceases running with helpful error message if invalid input is entered
        try:
            if int(camera_enable) <= 4 and int(camera_enable) > 0:   # Valid camera is selected
                if self.acell('B' + camera_enable).value == 'DISABLED':
                    self.update_acell('B' + camera_enable, 'IN')
                    self.update_acell('B5', int(self.acell('B5').value) + 1)
                    print("Enable completed successfully. There are " + self.acell('B5').value + ' availabe cameras.\n')
                else:
                    print('Cannot disable that camera. It is either already disabled or currently checked out.')
            else:
                print('Enabling failed. Invalid values. Is your input between (inclusive) 1 and 4 ? \n')
        except ValueError:
            print('Enabling failed. Invalid values. Please enter only a number. ')
        except:
            print('Unknown error. Verify that your input is only a number.')
