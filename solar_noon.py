import datetime
from solartime import SolarTime


lat = 38.291969
lon = 21.788156


today = datetime.date.today()

date = datetime.date(2021, 9, 15)

sun = SolarTime()
solar_noon = sun.solar_noon_utc(date, lon)
