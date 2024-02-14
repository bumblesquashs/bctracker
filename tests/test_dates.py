
import calendar
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
    
    def test_not_equal_year(self):
        date1 = Date(2000, 1, 1, timezone)
        date2 = Date(2001, 1, 1, timezone)
        
        assert date1 != date2
    
    def test_not_equal_month(self):
        date1 = Date(2000, 1, 1, timezone)
        date2 = Date(2000, 2, 1, timezone)
        
        assert date1 != date2
    
    def test_not_equal_day(self):
        date1 = Date(2000, 1, 1, timezone)
        date2 = Date(2000, 1, 2, timezone)
        
        assert date1 != date2
    
    def test_not_equal_timezone(self):
        date1 = Date(2000, 1, 1, timezone)
        timezone2 = pytz.timezone('America/Edmonton')
        date2 = Date(2000, 1, 1, timezone2)
        
        assert date1 != date2

class TestLessThan:
    def test_equal(self):
        date1 = Date(2000, 1, 1, timezone)
        date2 = Date(2000, 1, 1, timezone)
        
        assert not (date1 < date2)
        assert not (date2 < date1)
    
    def test_year(self):
        date1 = Date(2000, 1, 1, timezone)
        date2 = Date(2001, 1, 1, timezone)
        
        assert date1 < date2
        assert not (date2 < date1)
    
    def test_month(self):
        date1 = Date(2000, 1, 1, timezone)
        date2 = Date(2000, 2, 1, timezone)
        
        assert date1 < date2
        assert not (date2 < date1)
    
    def test_day(self):
        date1 = Date(2000, 1, 1, timezone)
        date2 = Date(2000, 1, 2, timezone)
        
        assert date1 < date2
        assert not (date2 < date1)
    
    def test_year_priority(self):
        date1 = Date(2000, 2, 2, timezone)
        date2 = Date(2001, 1, 1, timezone)
        
        assert date1 < date2
        assert not (date2 < date1)
    
    def test_month_priority(self):
        date1 = Date(2000, 1, 2, timezone)
        date2 = Date(2000, 2, 1, timezone)
        
        assert date1 < date2
        assert not (date2 < date1)

class TestGreaterThan:
    def test_equal(self):
        date1 = Date(2000, 1, 1, timezone)
        date2 = Date(2000, 1, 1, timezone)
        
        assert not (date1 > date2)
        assert not (date2 > date1)
    
    def test_year(self):
        date1 = Date(2001, 1, 1, timezone)
        date2 = Date(2000, 1, 1, timezone)
        
        assert date1 > date2
        assert not (date2 > date1)
    
    def test_month(self):
        date1 = Date(2000, 2, 1, timezone)
        date2 = Date(2000, 1, 1, timezone)
        
        assert date1 > date2
        assert not (date2 > date1)
    
    def test_day(self):
        date1 = Date(2000, 1, 2, timezone)
        date2 = Date(2000, 1, 1, timezone)
        
        assert date1 > date2
        assert not (date2 > date1)
    
    def test_year_priority(self):
        date1 = Date(2001, 1, 1, timezone)
        date2 = Date(2000, 2, 2, timezone)
        
        assert date1 > date2
        assert not (date2 > date1)
    
    def test_month_priority(self):
        date1 = Date(2000, 2, 1, timezone)
        date2 = Date(2000, 1, 2, timezone)
        
        assert date1 > date2
        assert not (date2 > date1)

class TestLessThanOrEqual:
    def test_equal(self):
        date1 = Date(2000, 1, 1, timezone)
        date2 = Date(2000, 1, 1, timezone)
        
        assert date1 <= date2
        assert date2 <= date1
    
    def test_year(self):
        date1 = Date(2000, 1, 1, timezone)
        date2 = Date(2001, 1, 1, timezone)
        
        assert date1 <= date2
        assert not (date2 <= date1)
    
    def test_month(self):
        date1 = Date(2000, 1, 1, timezone)
        date2 = Date(2000, 2, 1, timezone)
        
        assert date1 <= date2
        assert not (date2 <= date1)
    
    def test_day(self):
        date1 = Date(2000, 1, 1, timezone)
        date2 = Date(2000, 1, 2, timezone)
        
        assert date1 <= date2
        assert not (date2 <= date1)
    
    def test_year_priority(self):
        date1 = Date(2000, 2, 2, timezone)
        date2 = Date(2001, 1, 1, timezone)
        
        assert date1 <= date2
        assert not (date2 <= date1)
    
    def test_month_priority(self):
        date1 = Date(2000, 1, 2, timezone)
        date2 = Date(2000, 2, 1, timezone)
        
        assert date1 <= date2
        assert not (date2 <= date1)

class TestGreaterThanOrEqual:
    def test_equal(self):
        date1 = Date(2000, 1, 1, timezone)
        date2 = Date(2000, 1, 1, timezone)
        
        assert date1 >= date2
        assert date2 >= date1
    
    def test_year(self):
        date1 = Date(2001, 1, 1, timezone)
        date2 = Date(2000, 1, 1, timezone)
        
        assert date1 >= date2
        assert not (date2 >= date1)
    
    def test_month(self):
        date1 = Date(2000, 2, 1, timezone)
        date2 = Date(2000, 1, 1, timezone)
        
        assert date1 >= date2
        assert not (date2 >= date1)
    
    def test_day(self):
        date1 = Date(2000, 1, 2, timezone)
        date2 = Date(2000, 1, 1, timezone)
        
        assert date1 >= date2
        assert not (date2 >= date1)
    
    def test_year_priority(self):
        date1 = Date(2001, 1, 1, timezone)
        date2 = Date(2000, 2, 2, timezone)
        
        assert date1 >= date2
        assert not (date2 >= date1)
    
    def test_month_priority(self):
        date1 = Date(2000, 2, 1, timezone)
        date2 = Date(2000, 1, 2, timezone)
        
        assert date1 >= date2
        assert not (date2 >= date1)

class TestAdd:
    def test_year(self):
        date1 = Date(2000, 1, 1, timezone) + timedelta(days=366) # 2000 was a leap year!
        date2 = Date(2001, 1, 1, timezone)
        
        assert date1 == date2
    
    def test_month(self):
        date1 = Date(2000, 1, 1, timezone) + timedelta(days=31)
        date2 = Date(2000, 2, 1, timezone)
        
        assert date1 == date2
    
    def test_day(self):
        date1 = Date(2000, 1, 1, timezone) + timedelta(days=1)
        date2 = Date(2000, 1, 2, timezone)
        
        assert date1 == date2
    
    def test_all(self):
        date1 = Date(2000, 1, 1, timezone) + timedelta(days=398) # 2000 was a leap year!
        date2 = Date(2001, 2, 2, timezone)
        
        assert date1 == date2

class TestSubtract:
    def test_year(self):
        date1 = Date(2001, 1, 1, timezone) - timedelta(days=366) # 2000 was a leap year!
        date2 = Date(2000, 1, 1, timezone)
        
        assert date1 == date2
    
    def test_month(self):
        date1 = Date(2000, 2, 1, timezone) - timedelta(days=31)
        date2 = Date(2000, 1, 1, timezone)
        
        assert date1 == date2
    
    def test_day(self):
        date1 = Date(2000, 1, 2, timezone) - timedelta(days=1)
        date2 = Date(2000, 1, 1, timezone)
        
        assert date1 == date2
    
    def test_all(self):
        date1 = Date(2001, 2, 2, timezone) - timedelta(days=398) # 2000 was a leap year!
        date2 = Date(2000, 1, 1, timezone)
        
        assert date1 == date2

class TestFormatDB:
    def test(self):
        date = Date(2000, 1, 1, timezone)
        
        assert date.format_db() == '2000-01-01'

class TestFormatLong:
    def test_other_year(self):
        date = Date(2000, 1, 1, timezone)
        
        assert date.format_long() == 'January 1, 2000'
    
    def test_current_year(self):
        now = datetime.now()
        date = Date(now.year, 1, 1, timezone)
        
        assert date.format_long() == 'January 1'

class TestFormatShort:
    def test_other_year(self):
        date = Date(2000, 1, 1, timezone)
        
        assert date.format_short() == 'Jan 1, 2000'
    
    def test_current_year(self):
        now = datetime.now()
        date = Date(now.year, 1, 1, timezone)
        
        assert date.format_short() == 'Jan 1'

class TestFormatSince:
    def test_today(self):
        date = Date.today(timezone)
        
        assert date.format_since() == 'Today'
    
    def test_one_day(self):
        date = self.today_diff(days=1)
        
        assert date.format_since() == '1 day ago'
    
    def test_multiple_days(self):
        date = self.today_diff(days=2)
        
        assert date.format_since() == '2 days ago'
    
    def test_one_month(self):
        date = self.today_diff(months=1)
        
        assert date.format_since() == '1 month ago'
    
    def test_multiple_months(self):
        date = self.today_diff(months=2)
        
        assert date.format_since() == '2 months ago'
    
    def test_one_year(self):
        date = self.today_diff(years=1)
        
        assert date.format_since() == '1 year ago'
    
    def test_multiple_years(self):
        date = self.today_diff(years=2)
        
        assert date.format_since() == '2 years ago'
    
    def test_one_month_one_day(self):
        date = self.today_diff(months=1, days=1)
        
        assert date.format_since() == '1 month, 1 day ago'
    
    def test_one_month_multiple_days(self):
        date = self.today_diff(months=1, days=2)
        
        assert date.format_since() == '1 month, 2 days ago'
    
    def test_multiple_months_one_day(self):
        date = self.today_diff(months=2, days=1)
        
        assert date.format_since() == '2 months, 1 day ago'
    
    def test_multiple_months_multiple_days(self):
        date = self.today_diff(months=2, days=2)
        
        assert date.format_since() == '2 months, 2 days ago'
    
    def test_one_year_one_day(self):
        date = self.today_diff(years=1, days=1)
        
        assert date.format_since() == '1 year, 1 day ago'
    
    def test_one_year_multiple_days(self):
        date = self.today_diff(years=1, days=2)
        
        assert date.format_since() == '1 year, 2 days ago'
    
    def test_multiple_years_one_day(self):
        date = self.today_diff(years=2, days=1)
        
        assert date.format_since() == '2 years, 1 day ago'
    
    def test_multiple_years_multiple_days(self):
        date = self.today_diff(years=2, days=2)
        
        assert date.format_since() == '2 years, 2 days ago'
    
    def test_one_year_one_month(self):
        date = self.today_diff(years=1, months=1)
        
        assert date.format_since() == '1 year, 1 month ago'
    
    def test_one_year_multiple_months(self):
        date = self.today_diff(years=1, months=2)
        
        assert date.format_since() == '1 year, 2 months ago'
    
    def test_multiple_years_one_month(self):
        date = self.today_diff(years=2, months=1)
        
        assert date.format_since() == '2 years, 1 month ago'
    
    def test_multiple_years_multiple_months(self):
        date = self.today_diff(years=2, months=2)
        
        assert date.format_since() == '2 years, 2 months ago'
    
    def test_one_all(self):
        date = self.today_diff(years=1, months=1, days=1)
        
        assert date.format_since() == '1 year, 1 month, 1 day ago'
    
    def test_multiple_all(self):
        date = self.today_diff(years=2, months=2, days=2)
        
        assert date.format_since() == '2 years, 2 months, 2 days ago'

    def today_diff(self, years=0, months=0, days=0):
        today = Date.today(timezone)
        year = today.year - years
        month = today.month - months
        day = today.day - days
        while day <= 0:
            month -= 1
            if month <= 0:
                year -= 1
                month += 12
            day += calendar.monthrange(year, month)[1]
        while month <= 0:
            year -= 1
            month += 12
        return Date(year, month, day, timezone)

class TestNext:
    def test_day(self):
        date1 = Date(2000, 1, 1, timezone).next()
        date2 = Date(2000, 1, 2, timezone)
        
        assert date1 == date2
    
    def test_month(self):
        date1 = Date(2000, 1, 31, timezone).next()
        date2 = Date(2000, 2, 1, timezone)
        
        assert date1 == date2
    
    def test_year(self):
        date1 = Date(2000, 12, 31, timezone).next()
        date2 = Date(2001, 1, 1, timezone)
        
        assert date1 == date2

class TestPrevious:
    def test_day(self):
        date1 = Date(2000, 1, 2, timezone).previous()
        date2 = Date(2000, 1, 1, timezone)
        
        assert date1 == date2
    
    def test_month(self):
        date1 = Date(2000, 2, 1, timezone).previous()
        date2 = Date(2000, 1, 31, timezone)
        
        assert date1 == date2
    
    def test_year(self):
        date1 = Date(2001, 1, 1, timezone).previous()
        date2 = Date(2000, 12, 31, timezone)
        
        assert date1 == date2
