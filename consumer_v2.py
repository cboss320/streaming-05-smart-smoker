
import pika
import sys
import time
import csv

output_file = open("food1.csv", "w")
writer = csv.writer(output_file, delimiter = ",")

def food1_callback(ch, method, properties, body):
    
    message = body.decode()
    message2 = str(message)[1:-1]
    message3 = message2.split(',')
    
    message2 = message.lower()
    print(f"[x] Received {message}")
    writer.writerrow(message3)
    writer.writerow([message, message2])
    print("[x] Done.")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main(hn: str = "localhost", qn: str = "temp2"):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))
        
    except Exception as e:
        print()
        print("ERROR: connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={hn}.")
        print(f"The error says: {e}")
        print()
        sys.exit(1)
    try:
        channel = connection.channel()
        channel.queue_declare(queue=qn, durable=True) 
        channel.basic_qos(prefetch_count=1) 
        channel.basic_consume( queue=qn, on_message_callback=food1_callback)
        print(" [*] Ready for work. To exit press CTRL+C")
        channel.start_consuming()

    except Exception as e:
        print()
        print("ERROR: something went wrong.")
        print(f"The error says: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print()
        print(" User interrupted continuous listening process.")
        sys.exit(0)
    finally:
        print("\nClosing connection. Goodbye.\n")
        connection.close()
        
if __name__ == "__main__":
    main("localhost", "temp2")