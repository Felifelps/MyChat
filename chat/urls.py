from django.urls import path
from . import views

urlpatterns = [
    path('<int:friendship_id>', views.index, name="index")
]
