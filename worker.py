import time 

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.base_ack(delivery_tag = methid.delivery_tag)
channel.basic_consume(queue='hello', on_message_callback=callback)
    