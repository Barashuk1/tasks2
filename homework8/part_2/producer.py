import pika
from mongoengine import connect
from faker import Faker
from models import Contact

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


channel.queue_declare(queue='email_queue')

connect(host="mongodb+srv://<username>:<password>@cluster0.1rsrwmq.mongodb.net/homework8.2",
        ssl=True  
)

def generate_fake_contacts(num_contacts):
    fake = Faker()
    contacts = []
    for _ in range(num_contacts):
        name = fake.name()
        email = fake.email()
        contact = Contact(name=name, email=email)
        contact.save()
        contacts.append(contact)
    return contacts

def send_contacts_to_queue(contacts):
    for contact in contacts:
        channel.basic_publish(
            exchange='',
            routing_key='email_queue',
            body=str(contact.id)
        )
        print(f"Contact {contact.id} sent to queue")

if __name__ == "__main__":
    num_contacts = 10
    fake_contacts = generate_fake_contacts(num_contacts)
    send_contacts_to_queue(fake_contacts)

    connection.close()
