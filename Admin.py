import Event
import User
import Sheets

users = Sheets.User_Sheet('Lockonia_User_Sheet', 0)
cameras = Sheets.Sheet('Lockonia_Cameras_Sheet', 0)

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


# Cameras Interactions

def disable_camera():
    ''' Disables a camera slot, so that the case cannot be withdrawn '''
    print('Disabling a camera.')

    # Verifies that there are disabled cameras
    try:
        if int(cameras.acell('B5').value) > 0:
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
            if cameras.acell('B' + camera_disable).value == 'IN':
                cameras.update_acell('B' + camera_disable, 'DISABLED')
                cameras.update_acell('B5', int(cameras.acell('B5').value) - 1)
                print("Disable completed successfully. There are " + cameras.acell('B5').value + ' availabe cameras.\n')
            else:
                print('Cannot disable that camera. It is either already disabled or currently checked out.')
        else:
            print('Disabling failed. Invalid values. Is your input between (inclusive) 1 and 4 ? \n')

    except ValueError:
        print('Disabling failed. Invalid values. Please enter only a number. ')

    except:
        print('Unknown error. Verify that your input is only a number.')

def enable_camera():
    ''' Enables a camera slot, so that the case can be withdrawn. '''
    print('Enabling a camera.')

    # First verifies that there are disabled cameras
    try:
        if int(cameras.acell('B5').value) < 4:
            camera_enable = input('Select a camera. eg: 3 : ')
        else:
            print('No disabled cameras to enable.')
    except ValueError:
        print('Enabling failed. Invalid values. Please enter only a number. ')
    except:
        print('Unknown error. Verify that your input is only a number.')

    # Validates the camera selection, ceases running with helpful error message if invalid input is entered
    try:
        if int(camera_enable) < 4 and int(camera_enable) > 0:   # Valid camera is selected
            if cameras.acell('B' + camera_enable).value == 'DISABLED':
                cameras.update_acell('B' + camera_enable, 'IN')
                cameras.update_acell('B5', int(cameras.acell('B5').value) + 1)
                print("Enable completed successfully. There are " + cameras.acell('B5').value + ' availabe cameras.\n')
            else:
                print('Cannot disable that camera. It is either already disabled or currently checked out.')
        else:
            print('Enabling failed. Invalid values. Is your input between (inclusive) 1 and 4 ? \n')
    except ValueError:
        print('Enabling failed. Invalid values. Please enter only a number. ')
    except:
        print('Unknown error. Verify that your input is only a number.')

''' Main Program '''

print("#############################")
print("### LOCKONIA ADMIN CLIENT ###")
print("#############################\n")

print("Type 'User' for user management")
print("Type 'Camera' for camera case management")
action = input('User or Camera: ' )

command_not_entered = True

if action == 'User':
    print("Type 'create' to create a new user.")
    print("Type 'remove' to remove a user.")

    while command_not_entered:
        command = input("Only enter 'create' or 'remove': ")

        if command == 'create':
            command_not_entered = False
        elif command == 'remove':
            command_not_entered = False
        else:
            print("Only 'create' or 'remove' are valid commands!")

    if command == 'create':
        create_new_user()
    else:
        remove_user()

elif action == 'Camera':
    print("Type 'disable' to disable a camera")
    print("Type 'enable' to enable a camera")

    while command_not_entered:
        command = input("Only enter 'enable' or 'disable': ")
        if command == 'enable':
            command_not_entered = False
        elif command == 'disable':
            command_not_entered = False
        else:
            print("Only 'enable' or 'disable' are valid commands!")

    if command == 'enable':
        enable_camera()
    else:
        disable_camera()

else:
    print("Error. Only enter 'Camera' or 'User'")
