from mongoengine import connect
from part_1.models import Authors, Quotes
import json

connect(host="mongodb+srv://<username>:<password>@cluster0.1rsrwmq.mongodb.net/homework8.1",
        ssl=True  
)


with open('authors.json', 'r') as f:
    authors_data = json.load(f)

for author_data in authors_data:
    author = Authors(
    fullname=author_data['fullname'],
    born_date=author_data['born_date'],
    born_location=author_data['born_location'],
    description=author_data['description']
    )
    author.save()
    

with open('quotes.json', 'r') as f:
    quotes_data = json.load(f)

    for quote_data in quotes_data:
        author_name = quote_data['author']
        author = Authors.objects(fullname=author_name).first()
        if author:
            quote = Quotes(
                quote=quote_data['quote'],
                tags=quote_data['tags'],
                author=author
            )
            quote.save()
        else:
            print(f"Author '{author_name}' not found in the database. Quote skipped.")

