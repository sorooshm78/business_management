from django.urls import path

from report import views

urlpatterns = [
    path('<repo_id>', views.report_view, name='report'),
    path('detail/<repo_id>', views.detail_report_view, name='detail_report'),
]
