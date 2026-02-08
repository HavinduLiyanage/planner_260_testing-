from Person import Person


class AllMyFriends:
    """
    A collection class that stores Person objects (e.g., friends or contacts).
    Automatically expands capacity when it's full.
    """
    DEFAULT_MAX_FRIENDS = 10  # Default starting capacity

    def __init__(self, max_friends: int = None):
        """
        Initialize the 'AllMyFriends' list with a specified capacity or use
        the default capacity if not provided.

        :param max_friends: Maximum size of the friend list (optional).
        """
        if max_friends is None:
            max_friends = self.DEFAULT_MAX_FRIENDS

        # Internally use a list pre-filled with None to mimic a fixed array
        self.friend_list = [None] * max_friends
        self.num_friends = 0  # How many slots are actually in use

    def add(self, first_name: str, last_name: str, email: str):
        """
        Create a new Person and add them to the friend list.
        If the list is full, automatically expand capacity.

        :param first_name: The new friend's first name
        :param last_name:  The new friend's last name
        :param email:      The new friend's email address
        """
        friend = Person(first_name, last_name, email)

        # If the array is full, expand its capacity
        if self.num_friends == len(self.friend_list):
            self.expand_capacity()

        # Insert the new friend into the first free slot
        self.friend_list[self.num_friends] = friend
        self.num_friends += 1

    def remove(self, first_name: str, last_name: str) -> bool:
        """
        Remove a friend from the list by matching first name and last name.

        :param first_name: The first name of the friend to remove
        :param last_name:  The last name of the friend to remove
        :return:           True if removal succeeded, False otherwise
        """
        if self.num_friends == 0:
            # No friends to remove
            return False

        # Use a temporary person object just to compare first+last name
        target = Person(first_name, last_name, "")

        # Search for the target friend
        found_index = -1
        for i in range(self.num_friends):
            if self.friend_list[i] == target:
                found_index = i
                break

        if found_index == -1:
            # Not found
            return False

        # Overwrite the removed friend with the last friend in the list,
        # then set the last slot to None.
        self.friend_list[found_index] = self.friend_list[self.num_friends - 1]
        self.friend_list[self.num_friends - 1] = None
        self.num_friends -= 1
        return True

    def __str__(self) -> str:
        """
        Provide a string representation of all friends in the list.
        """
        # Build up strings for each friend that actually exists
        friend_strings = [
            str(self.friend_list[i])
            for i in range(self.num_friends)
        ]
        return "\n".join(friend_strings)

    def expand_capacity(self):
        """
        Double the capacity of the internal list to accommodate more friends.
        """
        new_size = len(self.friend_list) * 2
        larger_list = [None] * new_size

        # Copy existing data to the new list
        for i in range(self.num_friends):
            larger_list[i] = self.friend_list[i]

        self.friend_list = larger_list
