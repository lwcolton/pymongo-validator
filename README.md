# mongo_validator

A class-based Python 3 ORM for MongoDB.
Document class subclasses UserDict for ultimate compatibility with extrnal libraries.

Example:

```python
from pymongo.mongo_client import MongoClient

from mongo_validator.document import Document
from mongo_validator import fields

class Pet(Document):
    name = fields.StringField(required=True, empty=False)
    type = fields.StringField(required=True, allowed=["cat", "dog"]
    notes = fields.StringField()

scratch = Pet(name="scratch")

try:
    scratch.validate()
except Exception as validation_error:
    print(validation_error.errors)

scratch["type"] = "cat"
scratch.validate()

mongo_client = MongoClient("localhost")

scratch.save(mongo_client.petstore.pets)
```


