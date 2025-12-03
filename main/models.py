from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100,verbose_name='Название категории')
    description = models.TextField(max_length=500,verbose_name='Описание категории')
    slug = models.SlugField(max_length=100,unique=True,verbose_name='URL-адрес')
    image_category = models.ImageField(upload_to='category/',blank=True,verbose_name='Изображение категории')
    background_image = models.ImageField(upload_to='category_backgrounds/',blank=True,null=True,verbose_name='Фон категории')
    publish = models.DateTimeField(default=timezone.now,verbose_name='Дата публикации')
    created = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True,verbose_name='Дата обновления')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]


class Tag(models.Model):
    name = models.CharField(max_length=50,unique=True,verbose_name='Название тега')
    slug = models.SlugField(max_length=50,unique=True,verbose_name='URL-адрес тега')
    created = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']


class Post(models.Model):
    name_animal = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=250,verbose_name='Заголовок поста')
    slug = models.SlugField(max_length=250,unique=True,verbose_name='URL-адрес поста')
    body = models.TextField(verbose_name='Текст поста')
    short_description = models.CharField(max_length=300,blank=True,verbose_name='Краткое описание')
    publish = models.DateTimeField(default=timezone.now,verbose_name='Дата публикации')
    created = models.DateTimeField(auto_now_add=True,verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True,verbose_name='Дата обновления')
    image = models.ImageField(upload_to='post/',verbose_name='Главное изображение')
    cat = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='posts',verbose_name='Категория')
    tags = models.ManyToManyField(Tag,blank=True,related_name='posts',verbose_name='Теги')
    is_published = models.BooleanField(default=True,verbose_name='Опубликовано')
    views = models.PositiveIntegerField(default=0,verbose_name='Количество просмотров')
    author = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE,related_name='posts',verbose_name='Автор',null=True,blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == '':
            if self.title:
                self.slug = slugify(self.title, allow_unicode=False)
            else:
                self.slug = f"post-{self.id if self.id else 'new'}"
        if not self.slug or self.slug.strip() == '':
            self.slug = f"post-{self.id if self.id else 'new'}"
        if not self.short_description:
            self.short_description = self.body[:297] + '...' if len(self.body) > 300 else self.body
        super().save(*args, **kwargs)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
            models.Index(fields=['-views']),
        ]
