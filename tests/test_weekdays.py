
import pytest

from models.weekday import Weekday

class TestString:
    def test(self):
        assert str(Weekday.MON) == 'Monday'
        assert str(Weekday.TUE) == 'Tuesday'
        assert str(Weekday.WED) == 'Wednesday'
        assert str(Weekday.THU) == 'Thursday'
        assert str(Weekday.FRI) == 'Friday'
        assert str(Weekday.SAT) == 'Saturday'
        assert str(Weekday.SUN) == 'Sunday'

class TestName:
    def test(self):
        assert Weekday.MON.name == 'Monday'
        assert Weekday.TUE.name == 'Tuesday'
        assert Weekday.WED.name == 'Wednesday'
        assert Weekday.THU.name == 'Thursday'
        assert Weekday.FRI.name == 'Friday'
        assert Weekday.SAT.name == 'Saturday'
        assert Weekday.SUN.name == 'Sunday'

class TestShortName:
    def test(self):
        assert Weekday.MON.short_name == 'Mon'
        assert Weekday.TUE.short_name == 'Tue'
        assert Weekday.WED.short_name == 'Wed'
        assert Weekday.THU.short_name == 'Thu'
        assert Weekday.FRI.short_name == 'Fri'
        assert Weekday.SAT.short_name == 'Sat'
        assert Weekday.SUN.short_name == 'Sun'

class TestAbbreviation:
    def test(self):
        assert Weekday.MON.abbreviation == 'M'
        assert Weekday.TUE.abbreviation == 'T'
        assert Weekday.WED.abbreviation == 'W'
        assert Weekday.THU.abbreviation == 'T'
        assert Weekday.FRI.abbreviation == 'F'
        assert Weekday.SAT.abbreviation == 'S'
        assert Weekday.SUN.abbreviation == 'S'

class TestIsWorkday:
    def test_workdays(self):
        assert Weekday.MON.is_workday
        assert Weekday.TUE.is_workday
        assert Weekday.WED.is_workday
        assert Weekday.THU.is_workday
        assert Weekday.FRI.is_workday
    
    def test_weekends(self):
        assert not Weekday.SAT.is_workday
        assert not Weekday.SUN.is_workday

class TestIsWeekend:
    def test_weekends(self):
        assert Weekday.SAT.is_weekend
        assert Weekday.SUN.is_weekend
    
    def test_workdays(self):
        assert not Weekday.MON.is_weekend
        assert not Weekday.TUE.is_weekend
        assert not Weekday.WED.is_weekend
        assert not Weekday.THU.is_weekend
        assert not Weekday.FRI.is_weekend
