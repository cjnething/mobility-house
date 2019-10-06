from datetime import date, datetime, time, timedelta
import random


start_time = datetime.combine(date.today(), time.min)
end_time = datetime.combine(date.today(), time.max)
curr_time = start_time

print("HELLO")
print(start_time)
print(start_time.timestamp())
print(end_time)
print(end_time.timestamp())

# while curr_time <= end_time:
#     rand = random.randint(0, 9000)
#     if rand >= 8990:
#         print(rand)
#     curr_time += timedelta(0, 2)

