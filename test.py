import Sheets
from Sheets import User_Sheet
from User import User

usrsheet = User_Sheet("Lockonia_user_sheet", 0)

users = [
    ["Harry", 'hxp1', 'urawizard', 'h.potter@hogwarts.edu'],
    ["Barry", 'blt3', 'no', 'barry@jetpackfarm.edu'],
    ["Bork", 'bor6', 'literallybork', 'bork@doge.net'],
    ["Mr. Bantuski", 'axb34', 'tusssshy', 'none'],
    ["Marvin", 'mad838', 'ladDiggity', 'fish@glub.sea'],
    ["Nobody", 'nbd000', '0', 'nobody@somewhere.japan'],
    ["Alan", 'axb34', 'menslenissimo', 'terrible@case.edu'],
    ["Terry", 'ter9', 'mansuplicatoriness', 'cruz@aiders.org']
    ]

fml = [users[0], users[4], users[len(users) - 1]]  #first middle last

def populate():
    testadd(users)

def testadd(to_add):
    for user in to_add:
        print("add %s"%str(user))
        print(usrsheet.add_user(User.from_array(user)))

def testdelete(to_delete):
    for item in to_delete:
        print("delete %s"%str(item))
        print(usrsheet.remove_user(item[0]))
