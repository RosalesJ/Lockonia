import User
import Sheets

users = Sheets.UserSheet('Lockonia_User_Sheet', 0)
cameras = Sheets.CameraSheet('Lockonia_Cameras_Sheet', 0)

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


''' Main Program '''

print("#############################")
print("### LOCKONIA ADMIN CLIENT ###")
print("#############################\n")

print("Type 'User' for user management")
print("Type 'Camera' for camera case management")
action = input('User or Camera: ' )

command_not_entered = True

if action.lower() == 'user':
    print("Type 'create' to create a new user.")
    print("Type 'remove' to remove a user.")

    while command_not_entered:
        command = input("Only enter 'create' or 'remove': ")

        if command.lower() == 'create':
            command_not_entered = False
        elif command.lower() == 'remove':
            command_not_entered = False
        else:
            print("Only 'create' or 'remove' are valid commands!")

    if command == 'create':
        create_new_user()
    else:
        remove_user()

elif action.lower() == 'camera':
    print("Type 'disable' to disable a camera")
    print("Type 'enable' to enable a camera")

    while command_not_entered:
        command = input("Only enter 'enable' or 'disable': ")
        if command.lower() == 'enable':
            command_not_entered = False
            cameras.enable_camera()
        elif command.lower() == 'disable':
            command_not_entered = False
            cameras.disable_camera()
        else:
            print("Only 'enable' or 'disable' are valid commands!")

else:
    print("Error. Only enter 'Camera' or 'User'")
