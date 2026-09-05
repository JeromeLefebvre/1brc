import datetime
import random

def memoize_increment(station, initial_starttime):
    current_time = initial_starttime
    def wrapper():
        nonlocal current_time
        current_time += datetime.timedelta(seconds=100)
        return f"{station};{current_time};{random.randint(1,100)}"
    return wrapper

tags = [memoize_increment(station=chr(97 + index), initial_starttime=datetime.datetime.now()) for index in range(5)]
for _ in range(5):
    for tag in random.choices(tags,k=2):
        result = tag()
        print(result)
    print('-'*10)
