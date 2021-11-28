import warnings
from datetime import date, timedelta
from typing import List, Tuple


class VisaError(Exception):
    pass


class OverstayWarning(UserWarning):
    pass


class Visa:
    """This class represents a schengen type C visa."""

    def __init__(self, valid_from: date, valid_until: date):
        self.valid_from = valid_from
        self.valid_until = valid_until
        self._duration_of_stay = timedelta(days=90)
        self._trips: List[Tuple[date, date]] = []

    def __str__(self) -> str:
        result = ""
        for entry, exit in self._trips:
            result += f"{entry} {exit} {exit-entry+timedelta(days=1)}\n"
        return result

    def add_trip(self, entry: date, exit: date, strict: bool = True) -> None:
        assert exit < self.valid_until, "Stay exeeds validity of visa"
        self._trips.append((entry, exit))
        result = self._duration_of_stay
        for days in range((exit - entry).days + 1):
            day = entry + timedelta(days=days)
            result = min(result, self.evaluate(day))
        if result < timedelta(0):
            if strict:
                del self._trips[-1]
                raise VisaError(f"Trip could not be added because of overstay by {-result}")
            else:
                warnings.warn(f"Overstay in the period from {entry} to {exit} by {-result}", OverstayWarning)

    def evaluate(self, day: date) -> timedelta:
        result = self._duration_of_stay
        for entry, exit in self._trips:
            if exit < (start := day - timedelta(days=179)):  # 180 days in the closed intervall start...day
                pass
            else:
                result -= min(exit, day) - max(entry, start) + timedelta(days=1)
        return result

    @property
    def valid(self) -> bool:
        for entry, exit in self._trips:
            overstay = timedelta(days=1)
            for days in range((exit - entry).days + 1):
                day = entry + timedelta(days=days)
                overstay = min(overstay, self.evaluate(day))
            if overstay < timedelta(0):
                warnings.warn(f"Overstay in the period from {entry} to {exit} by {-overstay}", OverstayWarning)
                return False
        return True
