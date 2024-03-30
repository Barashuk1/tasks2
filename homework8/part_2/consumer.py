import pika
from mongoengine import connect
from bson import ObjectId
from time import sleep
from models import Contact


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


channel.queue_declare(queue='email_queue')

connect(host="mongodb+srv://<username>:<password>@cluster0.1rsrwmq.mongodb.net/homework8.2",
        ssl=True  
)

def callback(ch, method, properties, body):
    contact_id = ObjectId(body.decode())
    contact = Contact.objects(id=contact_id).first()
    if contact:
        print(f"Sending email to {contact.email}")
        sleep(2)
        contact.email_sent = True
        contact.save()
        print(f"Email sent to {contact.email}, status updated")
    else:
        print("Contact not found")

channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
