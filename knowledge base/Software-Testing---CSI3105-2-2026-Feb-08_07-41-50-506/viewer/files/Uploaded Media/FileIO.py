from AllMyFriends import AllMyFriends


class FileIO:
    """
    Class that does file I/O (read and write) for an AllMyFriends instance.
    """

    def write_file(self, path_name: str, file_name: str, contacts: AllMyFriends) -> None:
        """
        Write the current list of contacts to a file.

        :param path_name: The directory path where the file will be written.
        :param file_name: The name of the output file.
        :param contacts:  An AllMyFriends instance containing Person objects.
        """
        file_path = f"{path_name}/{file_name}"
        try:
            with open(file_path, "w", encoding="utf-8") as out_file:
                out_file.write(str(contacts))
        except Exception as e:
            print(f"File write error: {e}")

    def read_file(self, path_name: str, file_name: str, contacts: AllMyFriends) -> None:
        """
        Read contacts from a file and add them to the given AllMyFriends instance.
        Each line in the file is assumed to have three space-separated parts:
        first_name, last_name, and email.

        :param path_name: The directory path where the file is located.
        :param file_name: The name of the file to read.
        :param contacts:  An AllMyFriends instance where new Persons will be added.
        """
        file_path = f"{path_name}/{file_name}"
        try:
            with open(file_path, "r", encoding="utf-8") as in_file:
                for line in in_file:
                    line = line.strip()
                    if not line:
                        # Skip blank lines
                        continue

                    # Here we assume each line has exactly three parts
                    parts = line.split()
                    if len(parts) == 3:
                        first_name, last_name, email = parts
                        contacts.add(first_name, last_name, email)
                    else:
                        print(f"Skipping malformed line: {line}")
        except Exception as e:
            print(f"File read error: {e}")
