import collections

class BaseField(collections.UserDict):
    def __init__(self, *args, type_name=None, **kwargs):
        if type_name is None:
            type_name = type(self).__name__.lower().rstrip("field")
        super().__init__(*args, type=type_name, **kwargs)

class IntegerField(BaseField):
    pass

class DictField(BaseField):
    pass

class StringField(BaseField):
    pass
