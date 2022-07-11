from django.urls import path

from user import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change-pass/', views.ChangePassView.as_view(), name='change_password'),
    path('profile/', views.ProfileDetailView.as_view(), name='profile'),
    path('edit-profile/', views.UpdateProfileView.as_view(), name='edit_profile'),
]
