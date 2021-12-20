from django.urls import path

from . import views

urlpatterns = [
    path('sign_up', views.sign_up),
    path('sign_in', views.sign_in),
    path('refresh', views.refresh),
    path('update_details', views.update_details),
]
