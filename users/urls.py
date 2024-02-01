from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('change_password/<token>', views.change_password, name='change_password'),
    path('<username>/', views.user_page, name='user_page'),
]
