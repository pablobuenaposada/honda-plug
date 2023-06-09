from api.parts.serializers import PartOutputSerializer
from part.models import Part
from rest_framework.generics import RetrieveAPIView


class PartsView(RetrieveAPIView):
    serializer_class = PartOutputSerializer
    queryset = Part.objects.all()
    lookup_field = "reference"

    def get_object(self):
        if "reference" in self.kwargs:
            # we expect the url to contain always the reference in lower case so to match it we need it in upper case
            self.kwargs["reference"] = self.kwargs["reference"].upper()
        return super().get_object()
