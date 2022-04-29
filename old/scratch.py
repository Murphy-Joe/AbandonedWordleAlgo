import pytz
from datetime import datetime
utc_current_datetime = datetime.now(pytz.timezone("EST"))
print(utc_current_datetime.hour)

