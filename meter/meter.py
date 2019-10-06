import sys
import pika
import random
from datetime import date, datetime, time, timedelta
import json

def main():
    # cred = pika.PlainCredentials('guest', 'guest')
    params = pika.ConnectionParameters(
        host='host.docker.internal',
        port=5672,
        virtual_host='/',
        # credentials=cred
    )
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    # Midnight to midnight of current day
    start_time = datetime.combine(date.today(), time.min).timestamp()
    end_time = datetime.combine(date.today(), time.max).timestamp()
    curr_time = start_time
    print("-------")

    while curr_time <= end_time:
        # Floating values
        meter_value = random.uniform(0, 9000)
        print(curr_time)
        message = {
            'time': curr_time,
            'meter_value': meter_value,
        }

        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))

        # Increase by two seconds
        curr_time += 2


    connection.close()

if __name__ == '__main__':
  main()
