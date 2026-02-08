from logic.question_two.DummyDB import DummyDB



class DatabaseConnector:
    def __init__(self, db):  # Accepts a database instance
        self.db = db

    def connect(self):  # Delegates connection to the db object
        return self.db.connect()

    @classmethod
    def from_user_input(cls):  # Refactored class method: only gathers input
        host = input("Enter DB host: ")
        port = input("Enter DB port: ")
        return host, port  # Returns host and port for external DB construction

