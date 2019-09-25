from django.urls import path
from rank import views

urlpatterns = [
    path('', views.index, name='index'),
    path('refresh/', views.refresh, name='refresh')
]
