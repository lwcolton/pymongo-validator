import collections

import cerberus

class Document(collections.UserDict):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self._schema_dict = {}
		schema_class = self.schema
		for schema_attr_name in dir(schema_class):
			if schema_attr_name.startswith("_"):
				continue
			if schema_attr_name in ignore_attrs:
				continue
			schema_attr = getattr(schema_attr_name, schema_class)
			if isinstance(schema_attr, collections.Mapping):
				self._schema_dict.update(schema_attr)
			if hasattr(schema_attr, '__call__'):
				self._schema_dict.update(schema_attr())
			else:
				raise ValueError("Unknown type for field {0}: {1}".format(
						schema_attr_name, type(schema_attr)
					)
				)

	def validate(self):
		validator = cerberus.Validator(self._schema_dict)
		if validator.validate(self.data):
			return True
		else:
			return validator.errors



		



