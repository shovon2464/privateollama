from django.urls import path
from .views import IsActiveView

urlpatterns = [
    path('isactive/', IsActiveView.as_view(), name='is-active'),
]