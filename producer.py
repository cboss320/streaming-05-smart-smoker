import pika
import sys
import webbrowser
import csv
import time


def open_rabbitmq_admin_site():
    show_offer = True
    if show_offer == True:
        ans = input("Would you like to monitor RabbitMQ queues? y or n ")
        print()
        if ans.lower() == "y":
            webbrowser.open_new("http://localhost:15672/#/queues")
            print()

def send_message(host: str, queue_name: str, message: str):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(exchange="", routing_key=queue_name, body=message)
        print(f" [x] Sent {message}")
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Error: Connection to RabbitMQ server failed: {e}")
        sys.exit(1)
    finally:
        connection.close()

if __name__ == "__main__":
    open_rabbitmq_admin_site()
    with open("smoker-temps.csv", "r") as input_file:
        tasks = (input_file)

        reader = csv.reader(tasks, delimiter=",")

        for row in reader:
            
            time, smoker, food1, food2 = row
            
            message1 = " ".join(sys.argv[1:]) or f"[{time}, {smoker}]"
            message2 = " ".join(sys.agrv[1:]) or f"[{Time}, {food1}]"
            message3 = " ".join(sys.argv[1:]) or f"[{time}, {food2}]"
            
            send_message("localhost","temp1",message1)
            send_message("localhost","temp2",message2)
            send_message("localhost","temp3",message3)
            
            print(f" [x] Sent {message1}")
            print(f" [x] Sent {message2}")
            print(f" [x] Sent {message3}")

            time.sleep(30)