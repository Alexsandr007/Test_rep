import datetime


def default_datetime():
  date = datetime.datetime.now()
  new_year = int(date.year) + 2
  date_end = datetime.date(new_year, date.month, date.day)
  return date_end

