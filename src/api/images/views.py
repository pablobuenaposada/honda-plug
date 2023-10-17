from api.images.serializers import ImageSerializer
from rest_framework.generics import CreateAPIView


class ImagesCreateView(CreateAPIView):
    """Creates new Images entries for given Stock"""

    serializer_class = ImageSerializer
