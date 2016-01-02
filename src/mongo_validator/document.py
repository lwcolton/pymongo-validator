import collections

import cerberus

from .errors import DocumentValidationError

class Document(collections.UserDict):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self._schema_dict = self._get_schema_dict()

	def validate(self):
		validator = cerberus.Validator(self._schema_dict)
		if validator.validate(self.data):
			return True
		else:
			raise DocumentValidationError(validator.errors)

	def _get_schema_dict(self):
		if hasattr(self, "schema"):
			schema = getattr(self, "schema")
			if isinstance(schema, collections.Mapping):
				return schema
			elif issubclass(schema, Schema):
				return self._get_schema_dict_from_class(schema)
			else:
				return ValueError(
					"Unknown type for schema attribute: {0}".format(type(schema))
				)

	@classmethod
	def _get_schema_dict_from_class(cls, schema_class):
		"""Retrieves a cerberus schema dict from a Schema class"""
		schema_class = self.schema
		schema_dict = {}
		for schema_attr_name in dir(schema_class):
			if schema_attr_name.startswith("_"):
				continue
			schema_attr = getattr(schema_class, schema_attr_name)
			if isinstance(schema_attr, collections.Mapping):
				schema_dict[schema_attr_name] = schema_attr
			elif hasattr(schema_attr, '__call__'):
				schema_dict[schema_attr_name] = schema_attr()
			else:
				raise ValueError("Unknown type for field {0}: {1}".format(
						schema_attr_name, type(schema_attr)
					)
				)
		return schema_dict
