from django.urls import path
from .views import setting

urlpatterns = [
	path('', setting, name='blog-home'),
]
