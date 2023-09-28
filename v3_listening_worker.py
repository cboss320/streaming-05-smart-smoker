import pika 
import sys 
import time 

def callback(channel, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(body.count(b"."))
    print (" [x] Done.")
    channel.basic_ack(delivery_tag=method.delivery_tag)
    
def main(hn: str = "localhost", qn: str = "task_queue"):
    
    try: connection = pika.BlockingConnection(pika.ConnectionParameters(host=hn))
    
    except Exception as e: 
        print()
        print("ERROR: connection to RabbitMQ server failed.")
        print(f"Verify the server is running on host={hn}.")
        print(f"The error says : {e}")
        print ()
        sys.exit(1)
        
    try:
        channel = connection.channel()
        channel.queue_declare(queue=qn, durable=True)
        channel.basic_qos(prefetch_count=1)
        print("[*] Ready to work. To exit press CTRL+C")
        channel.start_consuming()
        
    except Exception as e: 
       print()
       print("ERROR: something went wrong.")
       print(f"The error says : {e}")
       print ()
       sys.exit(1)
       
    except KeyboardInterrupt:
        print()
        print(" User interruptered continuius listening process.")
        sys.exit(0)
        
    finally: 
        print("\nclosing connection. Goodbye. \n")
        connection.close()     

if __name__ == "__main__":
    main("localhost", "FirstQueue")   