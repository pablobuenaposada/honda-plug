import pycountry
from django.contrib import admin
from django.db import models
from django.forms import TextInput
from django.utils.safestring import mark_safe
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
    readonly_fields = ("image",)
    fields = ("url", "image")

    def image(self, obj):
        return mark_safe(f'<img src="{obj.url}" style="height: 200px"/>')


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
        "quantity",
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
    readonly_fields = ["image", "stock"]
    fields = ["stock", "url", "image"]

    def image(self, obj):
        return mark_safe(f'<img src="{obj.url}" style="height: 200px"/>')


admin.site.register(Part, PartAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Image, ImageAdmin)
