from django.urls import path

from . import views

urlpatterns = [
    path('sign-up', views.sign_up),
    path('sign-in', views.sign_in),
    path('refresh', views.refresh),
    path('update-account', views.update_account),
    path('delete-account', views.delete_account)
]
