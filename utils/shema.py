# myapp/schema.py
from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

class MySchemaGenerator(SchemaGenerator):
    def get_request_serializer(self, path, method, view):
        serializer = super().get_request_serializer(path, method, view)
        if serializer is not None:
            serializer.field = OpenApiParameter(
                name='data',
                type=OpenApiTypes.OBJECT,
                location=OpenApiParameter.QUERY,
                description='Request body format: application/x-www-form-urlencoded',
            )
        return serializer

generator_class = MySchemaGenerator
