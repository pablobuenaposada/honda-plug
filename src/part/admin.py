from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from part.models import Image, Part, Stock


class PartAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    model = Part
    readonly_fields = ("created", "modified")
    list_display = ("reference", "source", "modified")


class ImageInlineAdmin(admin.TabularInline):
    model = Image


class StockAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    model = Stock
    readonly_fields = ("created", "modified")
    list_display = ("part", "source", "title", "price", "modified")
    inlines = [ImageInlineAdmin]


class ImageAdmin(admin.ModelAdmin):
    model = Image
    list_display = ("id", "url", "stock")


admin.site.register(Part, PartAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Image, ImageAdmin)
