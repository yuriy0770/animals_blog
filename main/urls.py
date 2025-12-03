from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.TemplateMain.as_view(), name='index'),
    path('category/', views.CategoriesList.as_view(), name='category'),
    path('category/<slug:slug>/', views.CategoryDetail.as_view(), name='category_detail'),
    path('post/<path:slug>/', views.DetailPost.as_view(), name='detail'),
    path('about/', views.AboutProject.as_view(), name='about'),
    path('created/', views.CreatePost.as_view(), name='create_post'),
    path('updated/<slug:slug>/', views.UpdatePost.as_view(), name='updated'),

]