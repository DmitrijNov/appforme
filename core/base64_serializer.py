import six
import uuid
import base64
import imghdr
from django.utils.translation import ugettext_lazy as _
from django.core.files.base import ContentFile

from rest_framework import (
    serializers
)
from drf_extra_fields.fields import Base64FileField, Base64FieldMixin
from mimetypes import guess_extension


class CustomBase64FileField(Base64FileField):
    ALLOWED_TYPES = (
        "jpeg",
        "jpg",
        "png",
        "gif",
        "pdf",
        "doc",
        "docx",
        "xlsx"
    )
    INVALID_FILE_MESSAGE = _("Please upload a valid file.")
    INVALID_TYPE_MESSAGE = _("The type of the file couldn't be determined.")

    def get_file_extension(self, filename, decoded_file):
        extension = imghdr.what(filename, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension

    def to_internal_value(self, data):
        file_extension = None
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
                file_extension = guess_extension(header.split(':')[-1])[1:]
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')
            file_name = str(uuid.uuid4())[:12]
            if not file_extension:
                file_extension = self.get_file_extension(
                    file_name, decoded_file
                )
            if file_extension not in self.ALLOWED_TYPES:
                raise serializers.ValidationError(self.INVALID_TYPE_MESSAGE)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)
        result = super(Base64FieldMixin, self).to_internal_value(data)
        return result

    def to_representation(self, value):
        url = None
        try:
            if not getattr(value, 'url', None):
                return None
            url = value.url
        except Exception:
            pass
        return url


class Base64ImageField(serializers.ImageField):

    def __init__(self, *args, **kwargs):
        self.return_extension = kwargs.get('return_extension')
        if self.return_extension:
            kwargs.pop('return_extension')
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        file_extension = None
        if isinstance(data, str) and data.startswith('media'):
            return data.split('/')[-1]
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)
        result = super(Base64ImageField, self).to_internal_value(data)
        if self.return_extension and file_extension:
            result = {
                'data': result,
                'extension': file_extension
            }
        return result

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension

    def to_representation(self, value):
        url = None
        try:
            if not getattr(value, 'url', None):
                return None
            url = value.url
        except Exception:
            pass
        return url
