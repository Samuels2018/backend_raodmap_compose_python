from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from .models import Article
from .forms import ArticleForm, LoginForm

def home(request):
  articles = Article.objects.all().order_by('-date_posted')
  return render(request, 'blog/home.html', {'articles': articles})

class ArticleListView(ListView):
  model = Article
  template_name = 'blog/home.html'
  context_object_name = 'articles'
  ordering = ['-date_posted']
  paginate_by = 5

class ArticleDetailView(DetailView):
  model = Article
  template_name = 'blog/article_detail.html'

@login_required
def dashboard(request):
  articles = Article.objects.filter(author=request.user).order_by('-date_posted')
  return render(request, 'blog/dashboard.html', {'articles': articles})

@login_required
def article_create(request):
  if request.method == 'POST':
    form = ArticleForm(request.POST)
    if form.is_valid():
      article = form.save(commit=False)
      article.author = request.user
      article.save()
      return redirect('dashboard')
  else:
    form = ArticleForm()
  return render(request, 'blog/article_form.html', {'form': form, 'title': 'New Article'})

@login_required
def article_update(request, pk):
  article = get_object_or_404(Article, pk=pk, author=request.user)
  if request.method == 'POST':
    form = ArticleForm(request.POST, instance=article)
    if form.is_valid():
      form.save()
      return redirect('dashboard')
  else:
    form = ArticleForm(instance=article)
  return render(request, 'blog/article_form.html', {'form': form, 'title': 'Update Article'})

@login_required
def article_delete(request, pk):
  article = get_object_or_404(Article, pk=pk, author=request.user)
  if request.method == 'POST':
    article.delete()
    return redirect('dashboard')
  return render(request, 'blog/article_confirm_delete.html', {'article': article})

def user_login(request):
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data['username']
      password = form.cleaned_data['password']
      user = authenticate(request, username=username, password=password)
      if user is not None:
        login(request, user)
        return redirect('dashboard')
      else:
        form.add_error(None, 'Invalid username or password')
  else:
    form = LoginForm()
  return render(request, 'blog/login.html', {'form': form})

def user_logout(request):
  logout(request)
  return redirect('home')

def unauthorized(request):
  return render(request, 'blog/unauthorized.html')