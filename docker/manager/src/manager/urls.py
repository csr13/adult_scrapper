from django.urls import path, re_path

from manager import views

app_name = "manager"


urlpatterns = [
    path(
        "single-scrape-admin-action/<uid>",
        view=views.ManualSingleScrapeAdminAction.as_view(),
        name="single-scrape-admin-action"
    )
]
