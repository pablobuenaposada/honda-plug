from django.urls import include, re_path

app_name = "api"


urlpatterns = [
    re_path("parts/", include("api.parts.urls")),
]
