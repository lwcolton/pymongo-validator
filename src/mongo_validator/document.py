import collections

import cerberus

from .errors import DocumentValidationError
from . import fields

class Document(collections.UserDict):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._schema_dict = self._get_schema_dict()

	def validate(self):
		validator = cerberus.Validator(self._schema_dict)
		if validator.validate(self.data):
			return True
		else:
			raise DocumentValidationError(validator.errors)

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
