from decimal import Decimal


class Day(object):
    """docstring for Day"""

    def __init__(self, date, day, hours="0.00", time=Decimal(0.00)):
        super(Day, self).__init__()
        self.date = date
        self.day = day
        self.hours = hours
        self.notes = {}
        self.userhours = []
        self.totaltime = time
        self.allnotes = ""

    @property
    def two_date(self):
        return "%s" % self.date.strftime("%m/%d")

    def add_note(self, note):
        self.notes.append(note)
        return True

    def notes(self):
        return self.notes

    def __str__(self):
        return "%s - %s" % (self.day, self.date)

    def __repr__(self):
        return "<%s - %s>" % (self.day, self.date)


class Week(object):
    """
	Weeks run from sunday to saturday generally,
	however, a start date can be passed, in which
	case the week will start from that date.
	"""

    def __init__(self, start="Sun"):
        super(Week, self).__init__()
        self.days = []
        self.start = start
        self.users = []

    def days(self):
        return self.days

    def users(self):
        return self.users

    def usernotes(self):
        userlist = []
        noteslist = []
        for user in self.users:
            userlist.append(user)
            notes = []
            for day in self.days:
                notes.append(day.notes[user.username])
            noteslist.append(notes)
        final = zip(userlist, noteslist)
        return final

    def userhours(self):
        for user in self.users:
            for day in self.days:
                hours = day.hours[user.username]
                day.userhours.append((user, hours))

    @property
    def total(self):
        total = Decimal(0.00)
        for day in self.days:
            if type(day.totaltime) == Decimal:
                total += Decimal(day.totaltime)
        return total

    def add_day(self, day):
        self.days.append(day)
        return True

    def json(self):
        json = []

        for day in self.days:
            json.append(
                {
                    "date": day.date.strftime("%m/%d/%y"),
                    "two_day": day.date.strftime("%m/%d"),
                    "day": day.day,
                    "hours": day.hours,
                }
            )
        return json

    def __str__(self):
        return "Week starting %s" % self.start

    def __repr__(self):
        return "<Week starting %s>" % self.start
