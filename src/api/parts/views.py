from copy import deepcopy
from datetime import datetime, timedelta

from api.parts.permissions import HasScrapPermission
from api.parts.serializers import PartOutputSerializer, SearchOutputSerializer
from django.http import Http404
from django.utils import timezone
from elasticsearch_dsl import Q, Search
from main.parts_to_sneak import PartsToSneak
from part.documents import PART_INDEX_NAME
from part.models import Part
from rest_framework.generics import ListAPIView, RetrieveAPIView


class PartsView(RetrieveAPIView):
    permission_classes = []
    serializer_class = PartOutputSerializer
    lookup_field = "reference"

    def get_queryset(self):
        return Part.objects.search_reference(self.kwargs["reference"])

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = queryset.get()
        except Part.DoesNotExist as e:
            raise Http404 from e
        self.check_object_permissions(self.request, obj)
        if (
            obj.last_time_delivered
            and obj.last_time_delivered <= timezone.now() - timedelta(days=1)
        ):
            PartsToSneak.add(obj.reference)

        return obj


class PartsToScrapView(RetrieveAPIView):
    """
    Returns a part that needs to be scrapped and marks last_time_delivered to current time
    """

    permission_classes = [HasScrapPermission]
    serializer_class = PartOutputSerializer

    def get_object(self):
        if reference := PartsToSneak.pop():
            # if there's any urgent part to scrap we will return those
            obj = Part.objects.get(reference=reference)
        else:
            queryset = self.filter_queryset(Part.objects.parts_to_scrap())
            obj = queryset.first()
        self.check_object_permissions(self.request, obj)
        obj_copy = deepcopy(obj)
        obj.last_time_delivered = datetime.now()
        obj.save(update_fields=["last_time_delivered"])

        return obj_copy


class SearchView(ListAPIView):
    permission_classes = []
    serializer_class = SearchOutputSerializer

    def get_queryset(self):
        query_param = self.request.GET.get("query", "")
        es_search = Search(index=PART_INDEX_NAME).query(
            Q("multi_match", query=query_param, fields=["title", "part.reference"])
        )
        response = es_search.execute()

        unique_references = {hit.part.reference for hit in response.hits}
        references = [
            {"reference": reference, "title": hit.title}
            for hit, reference in zip(response.hits, unique_references, strict=False)
        ]

        return references
