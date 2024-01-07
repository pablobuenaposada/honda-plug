from django.contrib import admin

from review.models import ReviewPart


class ReviewPartAdmin(admin.ModelAdmin):
    model = ReviewPart
    list_display = ("reference",)


admin.site.register(ReviewPart, ReviewPartAdmin)
