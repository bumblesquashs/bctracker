
import pytest
import pytz

from datetime import datetime, timedelta

from models.date import Date
from models.weekday import Weekday

timezone = pytz.timezone('America/Vancouver')

class TestParse:
    def test_defaults(self):
        date = Date.parse('2000-01-01')
        
        assert date.year == 2000
        assert date.month == 1
        assert date.day == 1
        assert date.timezone == timezone
    
    def test_custom_timezone(self):
        timezone = pytz.timezone('America/Edmonton')
        date = Date.parse('2000-01-01', timezone=timezone)
        
        assert date.year == 2000
        assert date.month == 1
        assert date.day == 1
        assert date.timezone == timezone
    
    def test_custom_format(self):
        date = Date.parse('20000101', format='%Y%m%d')
        
        assert date.year == 2000
        assert date.month == 1
        assert date.day == 1
        assert date.timezone == timezone
    
    def test_custom_format_invalid(self):
        with pytest.raises(ValueError):
            Date.parse('2000-01-01', format='%Y%m%d')

class TestToday:
    def test_defaults(self):
        now = datetime.now(timezone)
        if now.hour < 4:
            now = now - timedelta(days=1)
        date = Date.today()
        
        assert date.year == now.year
        assert date.month == now.month
        assert date.day == now.day
        assert date.timezone == timezone
    
    def test_custom_timezone(self):
        timezone = pytz.timezone('America/Edmonton')
        now = datetime.now(timezone)
        if now.hour < 4:
            now = now - timedelta(days=1)
        date = Date.today(timezone)
        
        assert date.year == now.year
        assert date.month == now.month
        assert date.day == now.day
        assert date.timezone == timezone

class TestIsEarlier:
    def test_earlier(self):
        date = Date.today() - timedelta(days=1)
        
        assert date.is_earlier
    
    def test_later(self):
        date = Date.today() + timedelta(days=1)
        
        assert not date.is_earlier

class TestIsToday:
    def test_today(self):
        date = Date.today()
        
        assert date.is_today
    
    def test_not_today(self):
        date = Date.today() + timedelta(days=1)
        
        assert not date.is_today

class TestIsLater:
    def test_later(self):
        date = Date.today() + timedelta(days=1)
        
        assert date.is_later
    
    def test_earlier(self):
        date = Date.today() - timedelta(days=1)
        
        assert not date.is_later

class TestDatetime:
    def test(self):
        date = Date.today()
        datetime = date.datetime
        
        assert datetime.year == date.year
        assert datetime.month == date.month
        assert datetime.day == date.day

class TestTimezoneName:
    def test_default(self):
        date = Date.today()
        
        assert (date.timezone_name == 'PST' or date.timezone_name == 'PDT')
    
    def test_custom(self):
        timezone = pytz.timezone('America/Edmonton')
        date = Date.today(timezone)
        
        assert (date.timezone_name == 'MST' or date.timezone_name == 'MDT')

class TestWeekday:
    def test_default(self):
        date = Date.today()
        now = datetime.now()
        weekday = Weekday(now.weekday())
        
        assert date.weekday == weekday
    
    def test_custom(self):
        date = Date(2000, 1, 1, timezone)
        
        assert date.weekday == Weekday.SAT

class TestStr:
    def test(self):
        date = Date(2000, 1, 1, timezone)
        
        assert str(date) == 'January 1, 2000'

class TestEqual:
    def test_equal(self):
        date1 = Date(2000, 1, 1, timezone)
        date2 = Date(2000, 1, 1, timezone)
        
        assert date1 == date2
