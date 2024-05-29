from django.urls import path
from .views import IsActiveView,ClassifyNaturesView

urlpatterns = [
    path('isactive/', IsActiveView.as_view(), name='is-active'),
    path('classifynatures/', ClassifyNaturesView.as_view(), name='classify-natures'),
]