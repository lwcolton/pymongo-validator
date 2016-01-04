import collections

import cerberus

from .errors import DocumentValidationError
from . import fields

class DocumentWrapperCursor(object):
    def __init__(self, pymongo_cursor, document_class):
    	self.pymongo_cursor = pymongo_cursor
    	self.document_class = document_class
    def __iter__(self):
        return self.pymongo_cursor
    def next(self):
        return self.document_class.new(values=self.pymongo_cursor.next())
    def __getattr__(self, name):
        return getattr(self.pymongo_cursor, name)

class Document(collections.UserDict):
	def __init__(self, **kwargs):
		self._new(values=kwargs)

	@classmethod
	def new(cls, **kwargs):
		new_instance = cls()
		cls._new(**kwargs)

	def _new(self, values=None, rename_id_field=True):
		if values is None:
			values = {}
		if rename_id_field and "_id" in values:
			values["id"] = str(values["_id"])
			del values["_id"]
		self.data = values

		self._schema_dict = self._get_schema_dict()

	@classmethod
	def find(cls, collection, *args, **kwargs):
		cursor = collection.find(*args, **kwargs)
		if cursor is None:
			return []
		return DocumentWrapperCursor(cursor, cls)

	def validate(self):
		validator = cerberus.Validator(self._schema_dict)
		if validator.validate(self.data):
			return True
		else:
			message = "Error validating fields: {0}".format(
				list(validator.errors.keys())
			)
			raise DocumentValidationError(validator.errors, message)

	def _get_schema_dict(self):
		"""Retrieves a cerberus schema dict from field attributes"""
		schema_dict = {}
		for schema_attr_name in dir(self):
			if schema_attr_name.startswith("_"):
				continue
			schema_attr = getattr(self, schema_attr_name)
			if isinstance(schema_attr, fields.BaseField):
				schema_dict[schema_attr_name] = schema_attr
		return schema_dict
