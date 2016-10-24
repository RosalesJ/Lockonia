import Sheets
from Sheets import User_Sheet
from User import User

usrsheet = Sheets.User_Sheet("Lockonia_user_sheet")

sheet = Sheets.get_sheet("Lockonia_user_sheet")

def populate():
    user1 = User("Harry", 'hxp1', 'urawizard', 'h.potter@hogwarts.edu')
    user2 = User("Barry", 'blt3', 'no', 'barry@jetpackfarm.edu')
    user3 = User("Bork", 'bor6', 'literallybork', 'bork@doge.net')
    user4 = User("Mr. Bantuski", 'axb34', 'tusssshy', 'none')
    user5 = User("Marvin", 'mad838', 'ladDiggity', 'fish@glub.sea')
    user6 = User("Nobody", 'nbd000', '0', 'nobody@somewhere.japan')
    user7 = User("Alan", 'axb34', 'menslenissimo', 'terrible@case.edu')
    user8 = User("Terry", 'ter9', 'mansuplicatoriness', 'cruz@aiders.org')

    usrsheet.add_user(user1)
    usrsheet.add_user(user2)
    usrsheet.add_user(user3)
    usrsheet.add_user(user4)
    usrsheet.add_user(user5)
    usrsheet.add_user(user6)
    usrsheet.add_user(user7)
    usrsheet.add_user(user8)

print(usrsheet.remove_user("Harry"))
print(usrsheet.remove_user("Marvin"))
print(usrsheet.remove_user("Terry"))
