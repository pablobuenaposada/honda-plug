from api.parts.serializers import PartOutputSerializer, SearchOutputSerializer
from part.models import Part
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView


class PartsView(RetrieveAPIView):
    serializer_class = PartOutputSerializer
    queryset = Part.objects.all()
    lookup_field = "reference"

    def get_object(self):
        if "reference" in self.kwargs:
            # we expect the url to contain always the reference in lower case so to match it we need it in upper case
            self.kwargs["reference"] = self.kwargs["reference"].upper()
        return super().get_object()


class SearchView(ListAPIView):
    queryset = Part.objects.all()
    serializer_class = SearchOutputSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["reference", "stock__title"]
