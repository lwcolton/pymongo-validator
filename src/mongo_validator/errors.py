class DocumentValidationError(Exception):
    def __init__(self, errors_dict, *args):
        super().__init__(*args)
        self.errors = errors_dict
