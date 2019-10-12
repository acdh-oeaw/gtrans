from datetime import date
from datetime import timezone
from datetime import datetime


def date_to_utc(some_date):
    """takes a date object and returns a utc times
        :param some_date: a date object
        :return: A unix time stamp as integer
    """
    my_time = datetime.min.time()
    my_datetime = datetime.combine(some_date, my_time)
    return int(my_datetime.replace(tzinfo=timezone.utc).timestamp())


def vis_date_utc(model, field_name):
    vis_date = getattr(model, field_name, None)
    if vis_date is not None:
        try:
            as_utc = date_to_utc(vis_date)
        except Exception as e:
            print(e)
            as_utc = None
        return as_utc
    else:
        return None
