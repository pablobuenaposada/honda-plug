from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from part.models import Image, Part, Stock


class PartAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    model = Part
    readonly_fields = ("created", "modified")
    list_display = ("reference", "source", "modified")
    search_fields = ["reference"]


class ImageInlineAdmin(admin.TabularInline):
    model = Image


class StockAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    model = Stock
    readonly_fields = ("created", "modified")
    list_display = (
        "part",
        "title",
        "source",
        "price",
        "available",
        "discontinued",
        "modified",
    )
    search_fields = ["part__reference", "title"]
    list_filter = ["source", "available", "discontinued"]
    inlines = [ImageInlineAdmin]


class ImageAdmin(admin.ModelAdmin):
    model = Image
    list_display = ("id", "url", "stock")


admin.site.register(Part, PartAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Image, ImageAdmin)
