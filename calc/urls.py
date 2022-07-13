from django.urls import path
from . import views

app_name = 'calc'
urlpatterns = [
    path('', views.CalcView, name='calculator'),
    path('results/', views.ResultsView, name='results'),
    path('error/', views.ErrorView, name='error'),
]
