import pycountry
from django.contrib import admin
from django.db import models
from django.forms import TextInput
from simple_history.admin import SimpleHistoryAdmin

from part.models import Image, Part, Stock


class PartAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    model = Part
    readonly_fields = ("created", "modified")
    list_display = ("reference", "source", "modified")
    search_fields = ["reference"]
    list_filter = ["source", "modified"]


class ImageInlineAdmin(admin.TabularInline):
    model = Image


class StockAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    model = Stock
    readonly_fields = ("created", "modified", "part")
    fields = (
        "part",
        "title",
        "source",
        "url",
        "quantity",
        "available",
        "discontinued",
        "price",
        "country",
        "created",
        "modified",
    )
    list_display = (
        "part",
        "title",
        "source",
        "price",
        "available",
        "discontinued",
        "get_country_flag",
        "modified",
    )
    search_fields = ["part__reference", "title"]
    list_filter = ["source", "available", "discontinued"]
    inlines = [ImageInlineAdmin]
    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "100"})},
    }

    def get_country_flag(self, obj):
        return pycountry.countries.get(alpha_2=obj.country.code).flag

    get_country_flag.short_description = "Country"


class ImageAdmin(admin.ModelAdmin):
    model = Image
    list_display = ("id", "url", "stock")


admin.site.register(Part, PartAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Image, ImageAdmin)
