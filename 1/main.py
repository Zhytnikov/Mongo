from moduls import Quote, Author
from mongoengine import connect

# Підключення до MongoDB Atlas
connect('DB', host='mongodb+srv://zhytnikov:1234@db.bkiropa.mongodb.net/DB')

def search_quotes(command):
    if command.startswith('name:'):
        author_name = command.split(':')[1].strip()
        author = Author.objects(fullname=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            for quote in quotes:
                print(f"{quote.author.fullname}: {quote.quote}")
        else:
            print(f"For author '{author_name}' quotes not found .")
    elif command.startswith('tag:'):
        tag = command.split(':')[1].strip()
        quotes = Quote.objects(tags=tag)
        for quote in quotes:
            print(f"{quote.author.fullname}: {quote.quote}")
    elif command.startswith('tags:'):
        tags = command.split(':')[1].strip().split(',')
        quotes = Quote.objects(tags__in=tags)
        for quote in quotes:
            print(f"{quote.author.fullname}: {quote.quote}")
    else:
        print("Invalid command!")


if __name__ == "__main__":
    while True:
        command = input("Choose your command (For exemple: name: Steve Martin, tag: humor, tags: humor,simile, exit for ending): ").strip()
        if command.lower() == 'exit':
            break
        search_quotes(command)