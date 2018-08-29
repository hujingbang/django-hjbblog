from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('details/c_id/<int:c_id>/a_id/<int:id>', views.details)
]