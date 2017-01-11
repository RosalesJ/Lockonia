import unittest
import Sheets
from Sheets import User_Sheet
from User import User

'''

A collection of unit tests for Lockonia

'''

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

firstMiddleLast = [users[0], users[4], users[len(users) - 1]]
usersLite = [users[0], users[1], users[2]]

class SheetEmpty(unittest.TestCase):

    sheet = Sheets.Sheet("Lockonia_User_Sheet", 0)

    def setUp(self):
        self.sheet.resize(1,0)

    def tearDown(self):
        self.sheet.resize(1,0)

    def testContains(self):
        self.assertFalse(self.sheet.contains(""))
        self.assertFalse(self.sheet.contains("a"))
        self.assertFalse(self.sheet.contains("Many"))

    def testGetRow(self):
        self.assertIsNone(self.sheet.get_row(""))
        self.assertIsNone(self.sheet.get_row("a"))
        self.assertIsNone(self.sheet.get_row("Many"))

    def testAddRow(self):
        self.sheet.add_row(usersLite[0])
        self.assertTrue(self.sheet.contains("Harry"))
        self.assertTrue(self.sheet.contains("hxp1"))
        self.assertTrue(self.sheet.contains("urawizard"))
        self.assertTrue(self.sheet.contains("h.potter@hogwarts.edu"))
        self.assertFalse(self.sheet.contains(""))
        self.assertFalse(self.sheet.contains("harry"))

class SheetPopulated(unittest.TestCase):
    sheet = Sheets.Sheet("Lockonia_User_Sheet", 0)

    def setUp(self):
        for user in usersLite:
            self.sheet.add_row(user)

    def tearDown(self):
        self.sheet.resize(1,0)

    def testContains(self):
        self.assertTrue(self.sheet.contains("Harry"))
        self.assertTrue(self.sheet.contains("hxp1"))
        self.assertTrue(self.sheet.contains("h.potter@hogwarts.edu"))
        self.assertTrue(self.sheet.contains("Barry"))
        self.assertTrue(self.sheet.contains("no"))
        self.assertTrue(self.sheet.contains("barry@jetpackfarm.edu"))
        self.assertTrue(self.sheet.contains("Bork"))
        self.assertTrue(self.sheet.contains("bor6"))
        self.assertTrue(self.sheet.contains("bork@doge.net"))

        self.assertFalse(self.sheet.contains(""))
        self.assertFalse(self.sheet.contains("notInList"))
        self.assertFalse(self.sheet.contains("harry"))

    def testGetRow(self):
        self.assertEqual(2, self.sheet.get_row_number("Harry"))
        self.assertEqual(2, self.sheet.get_row_number("hxp1"))
        self.assertEqual(2, self.sheet.get_row_number("h.potter@hogwarts.edu"))
        self.assertEqual(3, self.sheet.get_row_number("Barry"))
        self.assertEqual(3, self.sheet.get_row_number("no"))
        self.assertEqual(3, self.sheet.get_row_number("barry@jetpackfarm.edu"))
        self.assertEqual(4, self.sheet.get_row_number("Bork"))
        self.assertEqual(4, self.sheet.get_row_number("bor6"))
        self.assertEqual(4, self.sheet.get_row_number("bork@doge.net"))

        self.assertEqual(usersLite[0], self.sheet.get_row("Harry"))
        self.assertEqual(usersLite[0], self.sheet.get_row("hxp1"))
        self.assertEqual(usersLite[0], self.sheet.get_row("h.potter@hogwarts.edu"))
        self.assertEqual(usersLite[1], self.sheet.get_row("Barry"))
        self.assertEqual(usersLite[1], self.sheet.get_row("no"))
        self.assertEqual(usersLite[1], self.sheet.get_row("barry@jetpackfarm.edu"))
        self.assertEqual(usersLite[2], self.sheet.get_row("Bork"))
        self.assertEqual(usersLite[2], self.sheet.get_row("bor6"))
        self.assertEqual(usersLite[2], self.sheet.get_row("bork@doge.net"))

    def testAddRow(self):
        self.sheet.add_row(users[3])
        self.assertTrue(self.sheet.contains("Mr. Bantuski"))
        self.assertTrue(self.sheet.contains("axb34"))
        self.assertTrue(self.sheet.contains("none"))

    def testRemoveRow(self):
        self.assertFalse(self.sheet.remove_row("notInList"))

        self.sheet.remove_row("Barry")

        self.assertFalse(self.sheet.contains("Barry"))
        self.assertFalse(self.sheet.contains("no"))
        self.assertFalse(self.sheet.contains("barry@jetpackfarm.edu"))
        self.assertTrue(self.sheet.contains("Harry"))
        self.assertTrue(self.sheet.contains("Bork"))
        self.assertEqual(3, self.sheet.get_row_number("Bork"))

        self.sheet.remove_row("Bork")

        self.assertFalse(self.sheet.contains("Bork"))
        self.assertFalse(self.sheet.contains("bor6"))
        self.assertFalse(self.sheet.contains("bork@doge.net"))
        self.assertFalse(self.sheet.contains("Barry"))
        self.assertTrue(self.sheet.contains("Harry"))
        self.assertEqual(2, self.sheet.get_row_number("Harry"))

        self.sheet.remove_row("Harry")

        self.assertFalse(self.sheet.contains("Harry"))
        self.assertFalse(self.sheet.contains("hxp1"))
        self.assertFalse(self.sheet.contains("h.potter@hogwarts.edu"))
        self.assertFalse(self.sheet.contains("Barry"))
        self.assertFalse(self.sheet.contains("Bork"))

if __name__ == '__main__':
    unittest.main()
