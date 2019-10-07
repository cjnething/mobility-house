import sys
import pika
import random
import json

# How often a sample is taken (in seconds)
time_interval = 2
max_wattage = 9000
# Min period length is same as the time interval (in seconds)
min_period_length = time_interval
# Max period length is 4 hours (in seconds)
max_period_length = 4 * 60 * 60


def get_period_length():
    return random.randint(min_period_length, max_period_length)

def simulate_meter():
    params = pika.ConnectionParameters(host='localhost')
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='meter_value_queue', durable=True)

    # Midnight to midnight of day (in seconds)
    start_time = 0
    end_time = 24 * 60 * 60
    curr_time = start_time

    # Create meter values in steps (periods) to make it more realistic
    meter_value = random.uniform(0, max_wattage)
    period_end = curr_time + get_period_length()

    while curr_time < end_time:
        message = {
            'time': curr_time,
            'meter_value': meter_value,
        }

        channel.basic_publish(
            exchange='',
            routing_key='meter_value_queue',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))

        # If the period has ended, create a new period
        if period_end <= curr_time:
            meter_value = random.uniform(0, max_wattage)
            period_end = curr_time + get_period_length()

        # Increase time
        curr_time += time_interval


    connection.close()

if __name__ == '__main__':
  simulate_meter()
