from .parser import NestedParser as NestPars
from rest_framework.parsers import MultiPartParser, DataAndFiles
from rest_framework.exceptions import ParseError
from django.http import QueryDict
from django.conf import settings


class NestedParser(NestPars):

    def __init__(self, data):
        super().__init__(data, getattr(settings, "DRF_NESTED_MULTIPART_PARSER", {}))

    def convert_value(self, data, key):
        # all value in querydict as set in list
        value = data[key]
        if isinstance(value, list):
            return value[0]
        return value

    @property
    def validate_data(self):
        dtc = QueryDict(mutable=True)
        dtc.update(super().validate_data)
        dtc.mutable = False
        return dtc


class DrfNestedParser(MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        clsDataAndFile = super().parse(stream, media_type, parser_context)

        parser = NestedParser(clsDataAndFile.data.dict())
        if parser.is_valid():
            return DataAndFiles(parser.validate_data, clsDataAndFile.files)
        raise ParseError(parser.errors)
