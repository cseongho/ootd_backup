from django.urls import path, include
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
	path('register/', views.register, name='register'),
	path('login/', views.login_page, name='login'),
	path('logout/', views.logout_page, name='logout'),
	path('profile/', views.profile, name='profile'),
]