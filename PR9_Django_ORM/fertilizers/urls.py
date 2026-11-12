from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('fertilizer/<int:fertilizer_id>/', views.detail, name='detail'),
]
