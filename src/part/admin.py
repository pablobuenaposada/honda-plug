import pycountry
from django.contrib import admin
from django.db import models
from django.db.models import Count
from django.forms import TextInput
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from simple_history.admin import SimpleHistoryAdmin

from part.models import Image, Part, Stock


class StockInlineAdmin(admin.TabularInline):
    model = Stock
    can_delete = False
    extra = 0
    show_change_link = True

    def get_readonly_fields(self, request, obj=None):
        fields = [f.name for f in self.model._meta.fields] + [
            "get_num_of_updates",
            "get_country_flag",
        ]
        fields.remove("country")
        return fields

    def has_add_permission(self, request, obj=None):
        return False

    def get_country_flag(self, obj):
        return pycountry.countries.get(alpha_2=obj.country.code).flag

    get_country_flag.short_description = "Country"

    def get_num_of_updates(self, obj):
        return obj.history.count() - 1

    get_num_of_updates.short_description = "Times updated"


class PartAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    model = Part
    readonly_fields = ("created", "modified", "last_time_delivered", "link")
    list_display = (
        "reference",
        "source",
        "stock_found",
        "modified",
        "get_num_of_stock_updates",
        "last_time_delivered",
    )
    search_fields = ["reference"]
    list_filter = ["source", "modified"]
    inlines = [StockInlineAdmin]

    def get_queryset(self, request):
        """just to be able to order by column stock found"""
        qs = super().get_queryset(request)
        qs = qs.annotate(stock_count=Count("stock"))
        return qs

    def stock_found(self, obj):
        return obj.stock_set.count()

    stock_found.admin_order_field = "stock_count"

    def get_num_of_stock_updates(self, obj):
        updates = 0
        for stock in obj.stock_set.all():
            updates += stock.history.count() - 1
        return updates

    def link(self, obj):
        return format_html(
            '<a href="https://hondaplug.com/part/{}">https://hondaplug.com/part/{}</a>',
            obj.reference,
            obj.reference,
        )

    get_num_of_stock_updates.short_description = "Times updated"


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
        "get_num_of_updates",
    )
    search_fields = ["part__reference", "title"]
    list_filter = ["source", "available", "discontinued"]
    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "100"})},
    }

    def get_country_flag(self, obj):
        return pycountry.countries.get(alpha_2=obj.country.code).flag

    get_country_flag.short_description = "Country"

    def get_num_of_updates(self, obj):
        return obj.history.count() - 1

    get_num_of_updates.short_description = "Times updated"


class ImageAdmin(admin.ModelAdmin):
    model = Image
    list_display = ("id", "url", "get_stock_ids", "image")
    search_fields = ["url", "id"]
    readonly_fields = ["image", "stocks"]
    fields = ["stocks", "url", "image"]

    def image(self, obj):
        return mark_safe(f'<img src="{obj.url}" style="height: 200px"/>')

    def get_stock_ids(self, obj):
        return ", ".join([str(stock.id) for stock in obj.stocks.all()])

    get_stock_ids.short_description = "Stocks"


admin.site.register(Part, PartAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Image, ImageAdmin)
