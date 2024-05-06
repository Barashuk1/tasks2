import pymongo
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes_project.settings')
django.setup()

from quotes.models import Author, Quote, Tag

mongo_uri = "mongodb+srv://Barashuk:*****@cluster0.1rsrwmq.mongodb.net/homework9"
mongo_client = pymongo.MongoClient(mongo_uri)
mongo_db = mongo_client.homework9
authors_collection = mongo_db.authors
quotes_collection = mongo_db.quotes

author_list = []

for author_doc in authors_collection.find():
    author_name = author_doc["name"]
    author_list.append(author_name)
    author_instance, created = Author.objects.get_or_create(name=author_name)

for i, quote_doc in enumerate(quotes_collection.find()):
    quote_text = quote_doc["quote"]
    author_name = author_list[i]
    tags = quote_doc["tags"]

    author_instance, created = Author.objects.get_or_create(name=author_name)
    
    quote_instance = Quote.objects.create(author=author_instance, text=quote_text)
    
    for tag_name in tags:
        tag_instance, created = Tag.objects.get_or_create(name=tag_name)
        quote_instance.tags.add(tag_instance)

mongo_client.close()
