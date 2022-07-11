from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail

from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from .utils import MyMixin


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Пользователь успешно создан.')
            return redirect('home')
        else:
            messages.error(request, 'Данные введены неверно.')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Пользователь авторизован.')
            return redirect('home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def test_mail(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'], 'simakovich.ea@yandex.ru', ['evgeny.simakovich@gmail.com'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено.')
                return redirect('home')
            else:
                messages.error(request, 'Ошибка при отправке письма.')
    else:
        form = ContactForm()
    return render(request, 'news/mail.html', {'form': form})


# Примеры работы с шаблонами с помощью классов
class HomeNews(MyMixin, ListView):
    paginate_by = 2
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    mixin_prop = 'hello world'
    # extra_context = {'title': '123'} - только статичные данные

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        context['title'] = 'Новости'
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsByCategory, self).get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category=self.kwargs['category_id'], is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News
    template_name = 'news/view_news.html'
    context_object_name = 'news_item'


class CreateNews(LoginRequiredMixin, CreateView):
    login_url = '/admin'
    form_class = NewsForm
    template_name = 'news/add_news.html'
    # success_url = reverse_lazy('home')



# Примеры работы с шаблонами с помощью методов
# -------------------------------------------------------------------------------------------
# def index(request: object) -> object:
#     news = News.objects.all()
#     data = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, 'news/index.html', data)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     data = {
#         'news': news,
#         'category': category,
#     }
#     return render(request, 'news/category.html', data)


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     data = {
#         'news_item': news_item,
#     }
#     return render(request, 'news/view_news.html', data)

# # Пример работы с формой, связанной с моделью
# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})


'''
# Пример работы с формой, не связанной с моделью
def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = News.objects.create(**form.cleaned_data)
            return redirect(str(news.get_absolute_url()))
    else:
        form = NewsForm()
    return render(request, 'news/add_news.html', {'form': form})
'''
