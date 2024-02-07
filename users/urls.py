from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('change_password/<token>', views.change_password, name='change_password'),
    path('', views.user_page, name='user_page'),
    path('request_friendship/', views.request_friendship, name='request_friendship'),
    path('answer_friendship/<int:id>/<status>', views.answer_friendship, name='answer_friendship'),
]
