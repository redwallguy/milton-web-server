import magic
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

@deconstructible
class FileTypeValidator:

    def __init__(self, allowed_extensions=None):
        if allowed_extensions is not None:
            self.allowed_extensions = allowed_extensions
        else:
            self.allowed_extensions = []

    def get_filetype(self, f):
        sample = f.read(2048)
        f.seek(0)
        return magic.from_buffer(sample, mime=True)

    def __call__(self, f):
        if len(self.allowed_extensions) != 0:
            if self.get_filetype(f) not in self.allowed_extensions:
                raise ValidationError("Not an allowed filetype")