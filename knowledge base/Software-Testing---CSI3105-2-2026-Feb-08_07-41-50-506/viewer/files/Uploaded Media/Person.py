class Person:
    """
    Represents a person with a first name, last name, and email address.
    """

    def __init__(self, first_name: str, last_name: str, email: str):
        """
        Initialize the person with a given name and email address.

        :param first_name: The person's first name
        :param last_name:  The person's last name
        :param email:      The person's email address
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def get_name(self) -> str:
        """
        Return the person's full name: first name followed by last name.
        """
        return f"{self.first_name} {self.last_name}"

    def get_email(self) -> str:
        """
        Return the person's email address.
        """
        return self.email

    def set_email(self, email: str):
        """
        Set (or update) the person's email address.

        :param email: The new email address
        """
        self.email = email

    def __eq__(self, other) -> bool:
        """
        Determine whether two Person objects have the same name.

        :param other: Another Person object to compare
        :return:      True if both first and last names match, otherwise False
        """
        if not isinstance(other, Person):
            return False
        return (
                self.first_name == other.first_name
                and self.last_name == other.last_name
        )

    def __str__(self) -> str:
        """
        Return a string representation of the Person, including
        first name, last name, and email address.
        """
        return f"{self.first_name} {self.last_name}\t{self.email}"
