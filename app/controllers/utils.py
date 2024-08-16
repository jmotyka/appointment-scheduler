import datetime


def round_time(time: datetime.datetime) -> datetime.datetime:
    "Round timestampe to nearest 15 minute mark."
    rounded_minute = round(time.minute // 15) * 15
    rounded_time = time.replace(minute=rounded_minute, second=0, microsecond=0)

    if time.minute % 15 >= 7.5:
        rounded_time += datetime.timedelta(minutes=15)

    return rounded_time
