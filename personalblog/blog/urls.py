from django.urls import path
from .views import (
  ArticleListView,
  ArticleDetailView,
  dashboard,
  article_create,
  article_update,
  article_delete,
  user_login,
  user_logout,
  unauthorized,
)

urlpatterns = [
  path('', ArticleListView.as_view(), name='home'),
  path('article/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
  path('dashboard/', dashboard, name='dashboard'),
  path('article/new/', article_create, name='article-create'),
  path('article/<int:pk>/update/', article_update, name='article-update'),
  path('article/<int:pk>/delete/', article_delete, name='article-delete'),
  path('login/', user_login, name='login'),
  path('logout/', user_logout, name='logout'),
  path('unauthorized/', unauthorized, name='unauthorized'),
]