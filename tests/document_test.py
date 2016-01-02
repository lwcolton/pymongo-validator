import unittest

from mongo_validator.errors import DocumentValidationError
from mongo_validator.document import Document

class FakeDocument(Document):
    schema = {
        "test_field":{"type":"string", "required":True}
    }

class TestDocument(unittest.TestCase):
    def setUp(self):
        self.doc = FakeDocument()

    def test_validation_error(self):
        with self.assertRaises(DocumentValidationError):
            self.doc.validate()

    def test_validation_success(self):
        self.doc["test_field"] = "a string"
        self.assertTrue(self.doc.validate())
