from mongoengine import connect
from models import Authors, Quotes
import json
# <username>:<password>
connect(host="mongodb+srv://<username>:<password>@cluster0.1rsrwmq.mongodb.net/homework9",
        ssl=True  
)

with open('authors.json', 'r') as f:
    authors_data = json.load(f)

for author_data in authors_data:
    author = Authors(name=author_data['name'])
    author.save()
    

with open('quotes.json', 'r') as f:
    quotes_data = json.load(f)

    for quote_data in quotes_data:
        author_name = quote_data['author']
        author = Authors.objects(name=author_name).first()
        if author:
            quote = Quotes(
                quote=quote_data['quote'],
                tags=quote_data['tags'],
                author=author
            )
            quote.save()
        else:
            print(f"Author '{author_name}' not found in the database. Quote skipped.")

