from rest_framework import serializers
from main.models import Post, Category, Tag
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'post_count']

    def get_post_count(self, obj):
        # Используем 'posts' вместо 'post_set'
        return obj.posts.count()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class PostListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка постов (короткий)"""
    cat = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    word_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'name_animal',
            'short_description', 'image', 'cat', 'tags',
            'author', 'views', 'created', 'word_count'  # ← created вместо created_at!
        ]

    def get_word_count(self, obj):
        return len(obj.body.split()) if obj.body else 0


class PostDetailSerializer(serializers.ModelSerializer):
    cat = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    related_posts = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_related_posts(self, obj):
        related = Post.objects.filter(
            cat=obj.cat,
            is_published=True
        ).exclude(id=obj.id)[:3]
        return PostListSerializer(related, many=True).data


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title', 'name_animal', 'body', 'short_description',
            'image', 'cat', 'tags', 'is_published'
        ]

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)