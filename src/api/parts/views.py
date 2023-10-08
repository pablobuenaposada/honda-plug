from copy import deepcopy
from datetime import datetime

from api.parts.permissions import HasScrapPermission
from api.parts.serializers import PartOutputSerializer, SearchOutputSerializer
from django.db.models import Value
from django.db.models.functions import Replace
from part.models import Part
from rest_framework import filters
from rest_framework.generics import ListAPIView, RetrieveAPIView


class PartsView(RetrieveAPIView):
    permission_classes = []
    serializer_class = PartOutputSerializer
    queryset = Part.objects.all()
    lookup_field = "reference"

    def get_object(self):
        if "reference" in self.kwargs:
            # we expect the url to contain always the reference in lower case so to match it we need it in upper case
            self.kwargs["reference"] = self.kwargs["reference"].upper()
        return super().get_object()


class PartsToScrapView(RetrieveAPIView):
    """
    Returns a part that needs to be scrapped and marks last_time_delivered to current time
    """

    permission_classes = [HasScrapPermission]
    serializer_class = PartOutputSerializer
    queryset = Part.objects.parts_to_scrap()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.first()
        self.check_object_permissions(self.request, obj)
        obj_copy = deepcopy(obj)
        obj.last_time_delivered = datetime.now()
        obj.save(update_fields=["last_time_delivered"])

        return obj_copy


class SearchView(ListAPIView):
    permission_classes = []
    queryset = Part.objects.annotate(
        cleaned_reference=Replace("reference", Value("-"), Value(""))
    )
    serializer_class = SearchOutputSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["cleaned_reference", "stock__title"]
