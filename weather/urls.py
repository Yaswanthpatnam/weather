from django.urls import path
from. import views

urlpatterns = [
    path('',views.index, name='index'),
    path('weather/',views.get_weather, name='get_weather')
]
