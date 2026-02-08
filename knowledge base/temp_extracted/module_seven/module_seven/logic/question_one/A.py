from logic.question_one.B import B


class A:
    """
    A depends on B, receives it through constructor
    """
    def __init__(self, b: B):  #
        self.b = b

    def run(self):  # Calls B's process method
        return self.b.process()

    def do_not_run(self, x: int) -> str:  # Calls B's process method
        return self.b.deny_access() + ": error " + str(x)