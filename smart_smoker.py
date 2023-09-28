# Courtney Pigford 9-21-2023

import pika 
import sys 
import csv
import time 
import webbrowser

host = "localhost"
csv_file = "smoker-temps.csv"
smokertemp_queue = "01-smoker"
food1_queue = "02-food-1"
food2_queue = "03-food-2"
show_offer = True 

def offer_rabbitmq_admin_site(show_offer):
    if show_offer == True: 
        """Offer to open the RabbitMQ Admin website"""
        ans = input("Would you like to monitor RabbitMQ queue? y or n")
        print()
        if ans.lower() == "y":
            webbrowser.open_new("http://localhost:15672/#/queues")
            print()

def delete_queue(host: str, queue_name: str):
    conn = pika.BlockingConnection(pika.ConnectionParameters(host))
    ch = conn.channel()
    ch.queue_delete(queue=queue_name)
    
def publish_message_to_queue(host: str, queue_name: str, message: str):
    """Parameters : 
        host (str): the host name or IP address of the RabbitMQ server
        queue_name (str): the name of the queue
        message (str): the message to be sent to the queue"""
    try: 
        conn = pika.BlockingConnection(pika.ConnectionParameters(host))
        ch = conn.channel()
        ch.queue_declare(queue=queue_name, durable=True)
        ch.basic_publish(exchange="", routing_key=queue_name, body=message)
        print(f" [x] Sent {message} to {queue_name}")
    except pika.exceptions.AMQPConnectionError as e:
       print(f"Error: Connection to RabbitMQ server failed: {e}")
       sys.exit(1)
    finally: 
        conn.close()

def get_message_from_csv(input_file):
     input_file = open(csv_file, "r")
     reader = csv.reader(input_file, delimiter=',')
     
     next(reader)
    
for row in reader: 
        input_string_row1 = row[1]
        input_string_row2 = row[2]
        input_string_row3 = row[3]
        
        to_convert_column1 = input_string_row1.replace('', '0')
        to_convert_column2 = input_string_row2.replace('', '0')
        to_convert_column3 = input_string_row3.replace('', '0') 
        
        float_row1 = float(to_convert_column1)
        float_row2 = float(to_convert_column2)
        float_row3 = float(to_convert_column3)
        
        fstring_time = f"{row[0]}"
        fstring_channel1 = f"{row[1]}"
        fstring_channel2 = f"{row[2]}"
        fstring_channel3 = f"{row[3]}"
        
        fstring_message_smokertemp = f"[{fstring_time}, {fstring_channel1}]"
        fstring_message_food1 = f"[{fstring_time}, {fstring_channel2}]"
        fstring_message_food2 = f"[{fstring_time}, {fstring_message_food2}]"
        
        message_smokertemp = fstring_message_smokertemp.encode()
        message_food1 = fstring_message_food1.encode()
        message_food2 = fstring_message_food2.encode()
        
        if float_row1 > 0: publish_message_to_queue(host, smokertemp_queue, message_smokertemp)
        if float_row2 > 0: publish_message_to_queue(host, food1_queue, message_food1)
        if float_row3 > 0: publish_message_to_queue(host, food2_queue, message_food2)
        
        time.sleep(30)
        
if __import__ == "__main__":
    offer_rabbitmq_admin_site(show_offer)
    delete_queue(host, smokertemp_queue)
    delete_queue(host, food1_queue)
    delete_queue(host, food2_queue)
    get_message_from_csv(csv_file)
        
        
        