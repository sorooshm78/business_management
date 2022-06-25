from django.urls import path

from category import views

urlpatterns = [
    path('<repo_id>', views.CategoryListView.as_view(), name='list_categories'),
    path('del-category/<category_id>', views.del_category, name='del_category'),
    path('add-category/<repo_id>', views.CreateCategory.as_view(), name='add_category'),
    path('get-cat-list/', views.get_category_list, name='get_category_list'),
    path('get-cat-id/<record_id>', views.get_cat_dis_id, name='get_cat_dis_id'),
]
