from django.urls import path

from report.api.views import (
    ReportsView,
    ReportCreateView,
    ReportDestroyView,
)


urlpatterns = [
    path("reports/", ReportsView.as_view()),
    path("reports/<int:pk>/create/", ReportCreateView.as_view()),
    path("reports/<int:pk>/delete/", ReportDestroyView.as_view()),
]
