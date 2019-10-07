import pika
import time
import json
from datetime import timedelta
from math import sqrt, pi, e

# Peak x value (mean) is at 2 PM (in seconds)
mean = 14 * 60 * 60
# Standard deviation is 3 hours (in seconds)
std_deviation = 3 * 60 * 60
# Max PV value (in watts)
max_pv = 3500
# The y value when x == mean
val_at_mean = 1/(std_deviation * sqrt(2 * pi))
# The multiplier to convert that probability to wattage
multiplier = max_pv/val_at_mean


def get_pv_value(time):
    return (multiplier/(std_deviation * sqrt(2 * pi))) * e**(-0.5 * ((time - mean)/std_deviation)**2)

def callback(ch, method, properties, body):
    # Acknowledge the message was received
    ch.basic_ack(delivery_tag=method.delivery_tag)

    # Parse the values
    msg_body = json.loads(body)
    msg_time = int(msg_body["time"])
    msg_datetime = timedelta(seconds=msg_time)
    msg_meter_value = float(msg_body["meter_value"])

    pv_value = get_pv_value(msg_time)
    net_usage = pv_value - msg_meter_value

    with open('results.txt', 'a') as results:
        results.write(str(msg_datetime) + ' - Meter (Watts): ' + str(msg_meter_value)
                                        + ', PV (Watts): ' + str(pv_value)
                                        + ', Total Usage (Watts): ' + str(net_usage) + '\n')

def simulate_pv_output():
    # Clear the results file
    with open('results.txt','w'): pass

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='meter_value_queue', durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='meter_value_queue', on_message_callback=callback)

    channel.start_consuming()

if __name__ == '__main__':
  simulate_pv_output()
