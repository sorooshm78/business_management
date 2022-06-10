from django.urls import path

from business import views

urlpatterns = [
    path('', views.RepositoryView.as_view(), name='list_repository'),
    path('del-repo/<repo_id>', views.del_repository, name='del_repository'),
    path('del-record/<record_id>', views.del_record, name='del_record'),
    path('new-repo/', views.NewRepositoryView.as_view(), name='new_repository'),
    path('repo/<repo_id>', views.DetailRepositoryView.as_view(), name='detail_repository'),
    path('add-record/<repo_id>', views.CreateRecordView.as_view(), name='add_record'),
    path('get-cat-list/', views.get_category_list, name='get_category_list'),
    path('update-record/<record_id>', views.UpdateRecordView.as_view(), name='update_record'),
    path('get-cat-id/<record_id>', views.get_cat_dis_id, name='get_cat_dis_id')
]
