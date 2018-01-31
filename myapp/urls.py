from django.urls import path

from . import views


urlpatterns = [
    # ex: /myapp/
    path('', views.index, name='index'),
    path('/', views.index, name='index'),

    # ex: /myapp/5/
    path('<int:bot_response_id>/', views.bot_response, name='bot_response'),
    # ex: /myapp/5/results/
    path('<int:bot_response_id>/get/', views.bot_response, name='bot_response_get'),


]