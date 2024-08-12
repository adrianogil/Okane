from dateutil.parser import parse as dtparse


def get_date(date_str):
    try:
        datetime_value = dtparse(date_str)
        # print(datetime_value)
        return datetime_value
    except:
        from dategpt import dategpt
        datetime_value = dategpt.parse_date(date_str)
        datetime_value = datetime_value["date"]
        return datetime_value
