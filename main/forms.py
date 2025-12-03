from django import forms
from main.models import Post

class FormPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'name_animal',
            'title',
            'body',
            'short_description',
            'image',
            'cat',
            'tags',
            'is_published'
        ]
        widgets = {
            'name_animal': forms.TextInput(attrs={
                'class': 'form-control custom-input',
                'placeholder': 'Введите название животного'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control custom-input',
                'placeholder': 'Введите заголовок поста'
            }),
            'body': forms.Textarea(attrs={
                'class': 'form-control custom-textarea',
                'placeholder': 'Введите текст поста',
                'rows': 6
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control custom-textarea',
                'placeholder': 'Введите краткое описание',
                'rows': 3
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control custom-file-input',
                'accept': 'image/*'
            }),
            'cat': forms.Select(attrs={
                'class': 'form-select custom-select'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-select custom-select',
                'size': 5
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'form-check-input custom-checkbox'
            }),
        }
        labels = {
            'name_animal': 'Название животного',
            'title': 'Заголовок поста',
            'body': 'Текст поста',
            'short_description': 'Краткое описание',
            'image': 'Изображение',
            'cat': 'Категория',
            'tags': 'Теги',
            'is_published': 'Опубликовать сразу',
        }
        help_texts = {
            'short_description': 'Краткое описание, которое будет отображаться в карточке поста',
            'tags': 'Выберите один или несколько тегов (зажмите Ctrl для выбора нескольких)',
        }