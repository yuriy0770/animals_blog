from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from main.models import Category, Post
from .forms import FormPost



class TemplateMain(TemplateView):
    template_name = 'main/index.html'

class CategoriesList(ListView):
    model = Category
    context_object_name = "categories"
    template_name = 'main/category_list.html'

class DetailPost(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'main/post_detail.html'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.increase_views()
        return obj

class CategoryDetail(DetailView):
    model = Category
    template_name = 'main/category_detail.html'
    context_object_name = 'category'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(cat=self.object, is_published=True)
        return context

class AboutProject(TemplateView):
    template_name = 'main/about.html'


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = FormPost
    template_name = 'main/post_form.html'
    success_url = reverse_lazy('main:index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class UpdatePost(UpdateView):
    model = Post
    form_class = FormPost
    success_url = reverse_lazy('main:index')
    slug_url_kwarg = 'slug'



