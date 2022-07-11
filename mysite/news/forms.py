from django import forms
from .models import News

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class ContactForm(forms.Form):
    subject = forms.CharField(label='Тема письма', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# Пример создания формы, связанной с моделью
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        # fields = '__all__'
        fields = ['title', 'content', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if title[0].isdigit():
            raise ValidationError('Название не должно начинаться с цифры')
        return title

"""
# Пример создания формы, не связанной с моделью
class NewsForm(forms.Form):
    title = forms.CharField(max_length=100, label='Название ', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст ', required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    is_published = forms.BooleanField(label='Опубликовано ', initial=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория ', empty_label='Выберите категорию', widget=forms.Select(attrs={'class': 'form-control'}))
"""
