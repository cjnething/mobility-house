import pika
import time
import json
from datetime import datetime

def get_pv_value(msg_datetime):
    return 1

def callback(ch, method, properties, body):
    # Acknowledge the message was received
    ch.basic_ack(delivery_tag=method.delivery_tag)

    # Parse the values
    msg_body = json.loads(body)
    msg_time = int(msg_body["time"])
    msg_datetime = datetime.fromtimestamp(msg_time)
    msg_meter_value = float(msg_body["meter_value"])

    pv_value = get_pv_value(msg_datetime)
    net_usage = pv_value - msg_meter_value

    with open('results.txt', 'a') as results:
        results.write(str(msg_datetime) + ' - Meter: ' + str(msg_meter_value)
                                        + ', PV: ' + str(pv_value)
                                        + ', Net Usage: ' + str(net_usage) + '\n')

def main():
    # Clear the results file
    with open('results.txt','w'): pass

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    channel.start_consuming()

if __name__ == '__main__':
  main()
