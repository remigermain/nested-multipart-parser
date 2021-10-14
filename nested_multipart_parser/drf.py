from .parser import NestedParser as NestPars
from rest_framework.parsers import MultiPartParser
from django.http.multipartparser import MultiPartParserError
from django.http import QueryDict


class NestedParser(NestPars):

    @property
    def validate_data(self):
        dtc = QueryDict(mutable=True)
        dtc.update(super().validate_data)
        dtc.mutable = False
        return dtc


class DrfNestedParser(MultiPartParser):

    def parse(self, stream, media_type=None, parser_context=None):
        parsed = super().parse(stream, media_type, parser_context)

        copy = parsed.data.copy()
        if parsed.files:
            copy.update(parsed.files)
        parser = NestedParser(copy)
        if parser.is_valid():
            return parser.validate_data
        if parser.errors:
            raise MultiPartParserError(parser.errors)
        return parsed
