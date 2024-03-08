import json
from mongoengine import connect
from moduls import Author, Quote

# Підключення до MongoDB Atlas
connect('DB', host='mongodb+srv://zhytnikov:1234@db.bkiropa.mongodb.net/DB')

# Завантаження даних про авторів
with open('authors.json', 'r') as file:
    authors_data = json.load(file)
    for author_data in authors_data:
        author = Author(**author_data)
        author.save()
        
# Завантаження цитат
with open('quotes.json', 'r') as file:
    quotes_data = json.load(file)
    for quote_data in quotes_data:
        author_name = quote_data['author']
        author = Author.objects(fullname=author_name).first()
        if author:
            quote_data['author'] = author
            quote = Quote(**quote_data)
            quote.save()