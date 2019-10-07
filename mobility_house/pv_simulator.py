import pika
import time
import json
import pandas as pd
from datetime import timedelta, datetime, date, time
from math import sqrt, pi, e
import plotly.express as px
from mobility_house.meter import end_time, time_interval

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

# Data structures for the charts
data_time = []
data_watts = []
data_type = []


def plot_values():
    df = pd.DataFrame({
        'Time': data_time,
        'Watts': data_watts,
        'Type': data_type,
        })

    df['Time'] = pd.to_datetime(df['Time'])

    figure = px.line(df, x='Time', y='Watts', color='Type', title='PV Simulation')
    figure.layout.images = [dict(
        source="https://www.mobilityhouse.com/media/logo/default/tmh_logo.png",
        xref="paper", yref="paper",
        x=0.5, y=1.08,
        sizex=0.3, sizey=0.3,
        xanchor="center", yanchor="middle"
    )]
    figure.show()

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
    total_usage = pv_value - msg_meter_value

    # Store data for charts
    chart_time = datetime.combine(date.today(), time.min) + msg_datetime
    # Meter
    data_time.append(chart_time)
    data_watts.append(msg_meter_value)
    data_type.append('Meter')
    # PV
    data_time.append(chart_time)
    data_watts.append(pv_value)
    data_type.append('PV')
    # Total
    data_time.append(chart_time)
    data_watts.append(total_usage)
    data_type.append('Total')

    with open('results.txt', 'a') as results:
        results.write(str(msg_datetime) + ' - Meter (Watts): ' + str(msg_meter_value)
                                        + ', PV (Watts): ' + str(pv_value)
                                        + ', Total Usage (Watts): ' + str(total_usage) + '\n')

    # The end of the messages
    if msg_time + time_interval >= end_time:
        plot_values()


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
