from datetime import date, timedelta


class OverstayError(Exception):
    pass


class Visa:
    def __init__(self, valid_from, valid_until, duration_of_stay, type_of_visa):
        assert type_of_visa == "C", "Only type C visas are supported"
        self.valid_from = valid_from
        self.valid_until = valid_until
        self.duration_of_stay = duration_of_stay
        self.trips = []

    def add_trip(self, entry, exit):
        assert exit < self.valid_until, "Stay exeeds validity of visa"
        self.trips.append((entry, exit))

    def __str__(self):
        result = ""
        for entry, exit in self.trips:
            result += f"{entry} {exit} {exit-entry+timedelta(days=1)}\n"
        return result

    def evaluate(self, day):
        result = self.duration_of_stay
        for entry, exit in self.trips:
            if exit < (start := day - timedelta(days=180)):
                pass
            else:
                result -= min(exit, day) - max(entry, start) + timedelta(days=1)
        return result

    def validate(self):
        for entry, exit in self.trips:
            overstay = timedelta(days=1)
            for days in range((exit - entry).days + 1):
                day = entry + timedelta(days=days)
                if (tmp := self.evaluate(day)) <= timedelta(0):
                    overstay = min(overstay, tmp)
            if overstay <= timedelta(0):
                raise OverstayError(f"Overstay in the period from {entry} to {exit} by {overstay}")
        return True

    def plan(self, entry, exit):
        self.trips.append((entry, exit))
        print(self)
        for days in range((exit - entry).days + 1):
            day = entry + timedelta(days=days)
        result = self.evaluate(exit)
        del self.trips[-1]
        if result <= timedelta(0):
            raise OverstayError(f"Overstay in the period from {entry} to {exit} by {result}")
        return result
