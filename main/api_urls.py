# main/api_urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    PostListView, PostDetailView, PostCreateView,
    CategoryListView, CategoryDetailView,
    TagListView, TagDetailView,
    RecentPostsView, PopularPostsView,
    StatisticsView, PostViewSet
)

router = DefaultRouter()
router.register(r'admin/posts', PostViewSet)

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/<slug:slug>/', TagDetailView.as_view(), name='tag-detail'),
    path('recent/', RecentPostsView.as_view(), name='recent-posts'),
    path('popular/', PopularPostsView.as_view(), name='popular-posts'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
    path('', include(router.urls)),
]