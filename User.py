# Represents a user
class User:
    def __init__(self, name, caseID, cardID, email):
        self.name = name
        self.caseID = caseID
        self.cardID = cardID
        self.email = email

    # instantiates a User from an array of 4 items
    @classmethod
    def from_array(cls, arr):
        return cls(arr[0], arr[1], arr[2], arr[3])


    def to_array(self):
        arr = []

        arr.append(self.name)
        arr.append(self.caseID)
        arr.append(self.cardID)
        arr.append(self.email)

        return arr

    def __str__(self):
        return self.name + " " + self.caseID