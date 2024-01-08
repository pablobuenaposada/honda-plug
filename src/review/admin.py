from django.contrib import admin
from part.constants import SOURCE_UNKNOWN
from part.models import Part

from review.models import ReviewPart


class ReviewPartAdmin(admin.ModelAdmin):
    model = ReviewPart
    list_display = ("reference",)
    actions = ["add_as_part"]

    def add_as_part(self, request, queryset):
        references = list(queryset.values_list("reference", flat=True))
        Part.objects.bulk_create(
            [
                Part(reference=reference, source=SOURCE_UNKNOWN)
                for reference in references
            ]
        )
        queryset.delete()


admin.site.register(ReviewPart, ReviewPartAdmin)
