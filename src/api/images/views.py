from api.images.serializers import ImageInputSerializer, ImageOutputSerializer
from part.models import Image, Stock
from rest_framework import status
from rest_framework.exceptions import ErrorDetail, ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response


class ImagesCreateView(CreateAPIView):
    """Creates new Images entries for given Stock"""

    serializer_class = ImageOutputSerializer

    def create(self, request, *args, **kwargs):
        serializer_class = ImageInputSerializer
        serializer = serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            if e.args == (
                {
                    "url": [
                        ErrorDetail(
                            string="image with this url already exists.", code="unique"
                        )
                    ]
                },
            ):
                # this validation error is a special case where the image already exists,
                # so it's just about finding the instance and updating it
                image = Image.objects.get(url=request.data["url"])
                image.stocks.add(Stock.objects.get(id=request.data["stock"]))
                serializer = self.get_serializer(image)
                headers = self.get_success_headers(serializer.data)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED, headers=headers
                )
            else:
                raise e
        serializer = self.get_serializer(
            data={
                "stocks": [serializer.validated_data["stock"].id],
                "url": serializer.validated_data["url"],
            }
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            self.get_serializer(serializer.instance).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )
