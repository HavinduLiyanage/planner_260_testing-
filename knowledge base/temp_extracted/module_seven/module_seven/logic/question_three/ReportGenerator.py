class ReportGenerator:
    def __init__(self, fetcher, formatter):  # Depends on two components
        self.fetcher = fetcher
        self.formatter = formatter

    def generate(self):  # Retrieves data and formats it
        raw_data = self.fetcher.fetch()
        return self.formatter.format(raw_data)