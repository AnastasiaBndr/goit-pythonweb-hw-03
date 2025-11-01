from datetime import datetime

def str_to_datetime(value, fmt='%Y-%m-%d %H:%M:%S'):
    try:
        dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
        return dt.strftime(fmt)
    except Exception as e:
        return print(f'Error while converting into datetime format! {e}')