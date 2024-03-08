import pika
from model import Contact
from mongoengine import connect

# Підключення до MongoDB
connect('DB2', host='mongodb+srv://zhytnikov:1234@cluster0.wn1tspq.mongodb.net/DB2')

# Підключення до RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='email')

def send_email_stub(contact_id):
    # Функція-заглушка для надсилання електронної пошти
    # Можна додати реальну логіку надсилання пошти тут
    print(f" [x] Sent email to contact {contact_id}")
    contact = Contact.objects.get(id=contact_id)
    contact.message_sent = True
    contact.save()

def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    send_email_stub(contact_id)

channel.basic_consume(queue='email', on_message_callback=callback, auto_ack=True)

print('Waiting for messages.')
channel.start_consuming()
