from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    # path('crawler/', views.cookcrawler),
    path('bot/' , views.bot),

]