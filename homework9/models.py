from mongoengine import Document
from mongoengine.fields import ReferenceField, ListField, StringField


class Authors(Document):
    name = StringField(required=True)

class Quotes(Document):
    tags = ListField(StringField())
    author = ReferenceField(Authors)
    quote = StringField(required=True)