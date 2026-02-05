class Date_Mock:
    @classmethod
    def day_month_year(self, day, month, year):
        return self(day, month, year)

    def __init__(self, day, month, year):

        self.day = day
        self.month = month
        self.year = year

    def strftime(self, string):
        if string == "%d/%m/%Y":
            return "" + str(self.day) + '/' + str(self.month) + '/' + str(self.year)

    def __gt__(self, otra_fecha):
        return self.year > otra_fecha.year or self.month > otra_fecha.month or self.day > otra_fecha.day


    def __lt__(self, otra_fecha):
        return self.year < otra_fecha.year or self.month < otra_fecha.month or self.day < otra_fecha.day
