from django.urls import path

from report import views

urlpatterns = [
    path('<repo_id>', views.report_view, name='report'),
    path('detail/<repo_id>', views.record_report_view, name='record_report'),
    path('cat-detail/<repo_id>', views.category_report_view, name='category_report'),
]
