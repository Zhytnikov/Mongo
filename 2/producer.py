import pika
from faker import Faker
from mongoengine import connect
from model import Contact

# Підключення до MongoDB
connect('DB2', host='mongodb+srv://zhytnikov:1234@cluster0.wn1tspq.mongodb.net/DB2')

# Підключення до RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='contacts_queue')

# Генерація фейкових контактів та надсилання їх до черги
fake = Faker()

for _ in range(10):  # Генеруємо 10 фейкових контактів
    full_name = fake.name()
    email = fake.email()
    contact = Contact(full_name=full_name, email=email)
    contact.save()
    
    # Надсилаємо ідентифікатор контакту у чергу RabbitMQ
    channel.basic_publish(exchange='',
                          routing_key='contacts_queue',
                          body=str(contact.id))
    print(f"Sent {contact.id}")

connection.close()
