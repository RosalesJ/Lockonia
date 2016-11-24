# Lockonia

Comprised of the following modules:
  User
    A representation of a user

  Sheets:
    A collection of Sheet models building off gspread Worksheet models
    These models are very row-focused are focused on getting rows with 
    certain falues and adding/removing rows.

      UserSheet:
        An extension of the Sheet class defined as storing User objects.
	Each user is one row and as many columns as the number of User's fields.

