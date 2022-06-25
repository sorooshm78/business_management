from django.urls import path

from repository import views

urlpatterns = [
    path('', views.RepositoryView.as_view(), name='list_repository'),
    path('del-repo/<repo_id>', views.del_repository, name='del_repository'),
    path('new-repo/', views.NewRepositoryView.as_view(), name='new_repository'),
    path('repo/<repo_id>', views.DetailRepositoryView.as_view(), name='detail_repository'),
]
