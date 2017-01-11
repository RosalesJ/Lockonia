import Event
import User
import Sheets

users = Sheets.User_Sheet('Lockonia_user_sheet', 0)
# logs = Sheets.Entry_Sheet('Lockonia_entry_sheet', 1)


#User_Sheet Interactions

def create_new_user():
    ''' Accept multiple inputs, create a User, and add it to the User_Sheet. '''

    print('Creating new user.')
    name = input('Enter user name: ')
    caseID = input('Enter case id: ')
    cardID = input('Tap card OR enter card number: ')
    email = caseID + '@case.edu'

    new_user = User.User(name, caseID, cardID, email)
    try:
        users.add_user(new_user)
        return True
    except:
        print('Creation of new user failed!')
        return False


def remove_user():
    ''' Remove a user from the user sheet. '''

    print('Removing user')
    userID = input('Enter Case ID (without trailing whitespace) OR tap card: ')

    if users.remove_user(userID):
        print('Deletion successful')
        return True
    else:
        print('Deletion failed. Please try again.')
        return False
