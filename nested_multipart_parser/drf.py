from .parser import NestedParser as NestPars
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import ParseError
from django.http import QueryDict
from django.conf import settings

DRF_OPTIONS = {"querydict": True}


class NestedParser(NestPars):
    def __init__(self, data):
        # merge django settings to default DRF_OPTIONS ( special parser options in on parser)
        options = {
            **DRF_OPTIONS,
            **getattr(settings, "DRF_NESTED_MULTIPART_PARSER", {}),
        }
        super().__init__(data, options)

    def convert_value(self, value):
        if isinstance(value, list) and len(value) > 0:
            return value[0]
        return value

    @property
    def validate_data(self):
        data = super().validate_data

        # return dict ( not conver to querydict)
        if not self._options["querydict"]:
            return data

        dtc = QueryDict(mutable=True)
        dtc.update(data)
        dtc.mutable = False
        return dtc


class DrfNestedParser(MultiPartParser):
    def parse(self, stream, media_type=None, parser_context=None):
        clsDataAndFile = super().parse(stream, media_type, parser_context)

        data = clsDataAndFile.data.dict()
        data.update(clsDataAndFile.files.dict())  # add files to data

        parser = NestedParser(data)
        if parser.is_valid():
            return parser.validate_data
        raise ParseError(parser.errors)
