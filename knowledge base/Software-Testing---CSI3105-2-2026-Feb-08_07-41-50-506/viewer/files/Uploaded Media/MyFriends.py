from AllMyFriends import AllMyFriends


def main():
    # Create an instance of AllMyFriends
    contacts = AllMyFriends()

    # Add a few friends
    contacts.add("John", "Smith", "johnsmith@ecu.edu.au")
    contacts.add("Felix", "Finley", "felixf@uwa.edu.au")
    contacts.add("Mike", "Spelling", "mikespe@uow.edu.au")
    contacts.add("Kathy", "Ellis", "kateellis@usydney.edu.au")
    contacts.add("Debbie", "Brown", "Dbrowny@umelb.edu.au")

    # Print them all
    print(contacts)


if __name__ == "__main__":
    main()
