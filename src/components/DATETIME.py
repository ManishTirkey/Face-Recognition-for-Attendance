from datetime import datetime
from public.file_config import *

import calendar


def Date() -> str:
    current_datetime = datetime.now()
    return f"{current_datetime.strftime('%Y-%m-%d')}"


def Time() -> str:
    current_datetime = datetime.now()
    return f"{current_datetime.strftime('%I:%M:%S %p')}"


def Current_month_date_list():
    # Get the current year and month
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Get the number of days in the current month
    num_days = calendar.monthrange(current_year, current_month)[1]

    # Generate a list of dates for the current month
    dates_of_month = [datetime(current_year, current_month, day).strftime("%Y-%m-%d") for day in range(1, num_days + 1)]

    return dates_of_month


if __name__ == '__main__':
    Current_month_date_list()
