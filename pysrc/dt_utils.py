from datetime import datetime, timedelta


def get_formatted_offset_date(days_offset):
    '''Get formatted date some days in future or past.
    
    Used to get date range parameters (startTime, endTime)
    in apple ad data query.

    Use a positive number for a day in the future,
    use a negative number to get day in the past.
    '''
    # Using current time
    ini_time_for_now = datetime.now()
    print ("initial_date", str(ini_time_for_now))
    offset_date = ini_time_for_now + timedelta(days = days_offset)
    print('offset_date:', str(offset_date))
    formatted_date = str(offset_date.strftime("%Y-%m-%d"))
    print('offset_date formatted:', formatted_date)
    return formatted_date