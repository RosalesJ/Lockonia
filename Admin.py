import Event
import User
import Sheets
import configparser

users = Sheets.User_Sheet('Lockonia_User_Sheet', 0)

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

def camera_init(disable):
''' Helper. Setups the access of the Cameras.ini to search for the correct options
    based on the command given. '''

    config = configparser.ConfigParser()
    config.read('.\\Cameras.ini')
    camera_count = config.getint('Cameras', 'cameras')

    # Disable branch: When the admin intends to disable a camera
    if disable:
        # Verifies that the limited slots on the camera shelf are not all vacant
        if camera_count > 0:
            cameras_list = config.items('Cameras')
            options_list = []
            tracker = 1
            for value in cameras_list:
                if value[1] == 2:
                    options_list.append('cam' + tracker)
                tracker = tracker + 1
            tracker = 1
            return True
        else:
            print("Disabling failed. No cameras to disable.")
            return False

    # Enable branch: When the admin intends to enable a camera
    else:
        # Verifies that the limited slots on the camera shelf are not all filled
        if camera_count < 4:
            cameras_list = config.items('Cameras')
            options_list = []
            tracker = 1
            for value in cameras_list:
                if value[1] == 0:
                    options_list.append('cam' + tracker)
                tracker = tracker + 1
            tracker = 1
            return True
        else:
            print('Enabling failed. No more camera slots available.')
            return False

def disable_camera():
''' Disables a camera slot, so that the case cannot be withdrawn '''

    if camera_init(True):    # 'Selects' the disable branch of camera_init
        cam_selection = input('Select which camera to remove')

        #TODO Verify that the options_list here will work. Expected: Will not work

        for camera in options_list:
            if cam_selection == camera:
                config.set('Cameras', cam_selection, '0')
                config.set('Camera_Count', 'cameras', str((config.getint('Cameras', 'cameras') - 1)))

def enable_camera():
''' Enables a camera slot, so that the case can be withdrawn. '''

    if camera_init(False):    # 'Selects' the enable branch of camera_init
        cam_selection = input('Select which camera to enable')

        #TODO Verify that the options_list here will work. Expected: Will not work

        for camera in options_list:
            if cam_selection == camera:
                config.set('Cameras', cam_selection, '2')
                config.set('Camera_Count', 'cameras', str((config.getint('Cameras', 'cameras') + 1)))


''' Main Program '''

print("#############################")
print("### LOCKONIA ADMIN CLIENT ###")
print("#############################\n")

print("Type 'User' for user management")
print("Type 'Camera' for camera case management")
action = input('User or Camera')

if action == 'User':
    print("Type 'create' to create a new user.")
    print("Type 'remove' to remove a user.")

    command_not_entered = True

    while command_not_entered:
        command = input("Only enter 'create' or 'remove'. ")

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

else:
    print("Error. Only enter 'Camera' or 'User'")
