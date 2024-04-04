from mongoengine import connect
from models import Authors, Quotes

connect(host="mongodb+srv://<username>:<password>@cluster0.1rsrwmq.mongodb.net/homework9",
        ssl=True  
)

while True:
    command = input('>>> ')
    
    if command.strip().startswith("exit"):
        break
    
    try:
        command, value = command.split(':')

        if command == "name":
            quotes = Quotes.objects(author=Authors.objects(name=value).first()).all()
        elif command == "tag":
            quotes = Quotes.objects(tags=value).all()
        elif command == "tags":
            tags = value.split(",")
            quotes = Quotes.objects(tags__in=tags).all()
        else:
            print("incorrect input")

        if quotes:
            for i, quote in enumerate(quotes):
                print(f'{i + 1}){quote.quote}')
        else:
            print('quotes not found')
    except ValueError:
            print("incorrect input")