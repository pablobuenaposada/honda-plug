import pycountry
from django.contrib import admin
from django.db import models
from django.db.models import Count
from django.forms import TextInput
from django.utils.safestring import mark_safe
from simple_history.admin import SimpleHistoryAdmin

from part.models import Image, Part, Stock
from part.tasks import enqueue_queryset


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


class ImageInlineAdmin(admin.TabularInline):
    model = Image
    readonly_fields = ("image",)
    fields = ("url", "image")

    def image(self, obj):
        return mark_safe(f'<img src="{obj.url}" style="height: 200px"/>')


class PartAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    model = Part
    readonly_fields = ("created", "modified", "last_time_delivered")
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
    actions = ["search_stocks"]

    def get_queryset(self, request):
        """just to be able to order by column stock found"""
        qs = super().get_queryset(request)
        qs = qs.annotate(stock_count=Count("stock"))
        return qs

    def stock_found(self, obj):
        return obj.stock_set.count()

    stock_found.admin_order_field = "stock_count"

    def search_stocks(self, request, queryset):
        enqueue_queryset.delay(queryset, at_front=True)

    def get_num_of_stock_updates(self, obj):
        updates = 0
        for stock in obj.stock_set.all():
            updates += stock.history.count() - 1
        return updates

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
    inlines = [ImageInlineAdmin]
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
    list_display = ("id", "url", "stock", "image")
    search_fields = ["url", "id", "stock__part__reference"]
    readonly_fields = ["image", "stock"]
    fields = ["stock", "url", "image"]

    def image(self, obj):
        return mark_safe(f'<img src="{obj.url}" style="height: 200px"/>')


admin.site.register(Part, PartAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Image, ImageAdmin)
