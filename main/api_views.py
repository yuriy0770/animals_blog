from rest_framework import generics, viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.db.models import Count
from django.shortcuts import get_object_or_404

from main.models import Post, Category, Tag
from .serializers import (
    PostListSerializer, PostDetailSerializer,
    PostCreateSerializer, CategorySerializer,
    TagSerializer
)


class PostListView(generics.ListAPIView):
    """API для списка постов с фильтрацией"""
    serializer_class = PostListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'name_animal', 'body', 'short_description']
    ordering_fields = ['created', 'views', 'title']  # ← created вместо created_at!
    ordering = ['-created']  # ← created вместо created_at!

    def get_queryset(self):
        queryset = Post.objects.filter(is_published=True)

        # Фильтрация по категории
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(cat__slug=category_slug)

        # Фильтрация по тегу
        tag_slug = self.request.query_params.get('tag')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        return queryset.select_related('cat', 'author').prefetch_related('tags')


class PostDetailView(generics.RetrieveAPIView):
    """API для детального просмотра поста"""
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs.get('slug')
        post = get_object_or_404(Post, slug=slug, is_published=True)

        # Увеличиваем счетчик просмотров
        post.views += 1
        post.save(update_fields=['views'])

        return post


class PostCreateView(generics.CreateAPIView):
    """API для создания нового поста (требует аутентификации)"""
    serializer_class = PostCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryListView(generics.ListAPIView):
    """API для списка категорий с количеством постов"""
    queryset = Category.objects.annotate(post_count=Count('posts'))  # ← posts!
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveAPIView):
    """API для детальной информации о категории"""
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Category, slug=slug)


class TagListView(generics.ListAPIView):
    """API для списка тегов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetailView(generics.RetrieveAPIView):
    """API для постов определенного тега"""
    serializer_class = PostListSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        tag = get_object_or_404(Tag, slug=slug)
        return Post.objects.filter(tags=tag, is_published=True)


class RecentPostsView(generics.ListAPIView):
    """API для последних постов"""
    serializer_class = PostListSerializer

    def get_queryset(self):
        count = self.request.query_params.get('limit', 5)
        return Post.objects.filter(
            is_published=True
        ).order_by('-created')[:int(count)]


class PopularPostsView(generics.ListAPIView):
    """API для самых популярных постов"""
    serializer_class = PostListSerializer

    def get_queryset(self):
        count = self.request.query_params.get('limit', 5)
        return Post.objects.filter(
            is_published=True
        ).order_by('-views')[:int(count)]


class StatisticsView(APIView):
    """API для статистики сайта"""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        total_posts = Post.objects.filter(is_published=True).count()
        total_categories = Category.objects.count()
        total_tags = Tag.objects.count()
        total_views = Post.objects.filter(is_published=True).aggregate(
            total=Count('views')
        )['total']

        # Получаем самую популярную категорию
        popular_category = Category.objects.annotate(
            post_count=Count('posts')  # ← posts!
        ).order_by('-post_count').first()

        return Response({
            'total_posts': total_posts,
            'total_categories': total_categories,
            'total_tags': total_tags,
            'total_views': total_views,
            'most_popular_category': popular_category.name if popular_category else 'Нет данных',
        })


# ViewSet для административных операций
class PostViewSet(viewsets.ModelViewSet):
    """ViewSet для полного CRUD постов (для админки)"""
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        elif self.action == 'create':
            return PostCreateSerializer
        return PostDetailSerializer

    @action(detail=True, methods=['post'])
    def increment_views(self, request, pk=None):
        """Увеличить счетчик просмотров"""
        post = self.get_object()
        post.views += 1
        post.save(update_fields=['views'])
        return Response({'views': post.views})