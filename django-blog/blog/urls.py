from django.urls import path, include
from . import views
from django.urls import reverse_lazy
from .views import PostListView, PostDetailView, PostCreateView, PostDeleteView, PostUpdateView, PostCategoryView, CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView, SearchListView

urlpatterns = [
	path('', views.home, name='home'),
	path('feedback/', PostListView.as_view(), name='feedback'),
	path('market/', views.market, name='market'),
	path('ranking/', views.ranking, name='ranking'),
	path('create/', PostCreateView.as_view(), name='post_create'),
	path('category/create/', CategoryCreateView.as_view(), name='category_create'),
	path('category/list/', CategoryListView.as_view(), name='category_list'),
	path('category/<slug:slug>/update/', CategoryUpdateView.as_view(), name='category_update'),
	path('category/<slug:slug>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
	path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
	path('<slug:slug>/update/', PostUpdateView.as_view(), name='post_update'),
	path('<slug:slug>/delete/', PostDeleteView.as_view(), name='post_delete'),
	path('category/<slug:slug>/', PostCategoryView.as_view(), name='post_by_category'),
	path('search/', SearchListView.as_view(), name='search'),
	path('tinymce/', include('tinymce.urls')),
]
