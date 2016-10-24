'''
 Jacob Rosales Chase
 A collection of methods to get and modify Google Sheets using gspread
 All methods will take a single value and modify a single row of a sheet
'''

import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
        return = sheet.row_values(user_row)
    return None

# removes the entire row that contains the value provided
# returns True if the operation was successful
# returns False if there is no shuch item in the sheet
def remove_row(value, sheet):
    row_number = get_row_number(value, sheet)
    if(row_number):
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
