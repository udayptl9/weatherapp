from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='weather'),
    path('delete/<cityId>', views.delete, name='delete'),
]
