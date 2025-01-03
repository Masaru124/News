from django.urls import path
from .views import submit_article, home, approve_article, admin_article_list, render_static_html, article_detail, welcome

urlpatterns = [
    path('', welcome, name='welcome'),  # Welcome page
    path('index/', home, name='index'),  # Main page
    path('index/submit/', submit_article, name='submit_article'),
    path('index/admin/', admin_article_list, name='admin_article_list'),
    path('admin/articles/approve/<int:article_id>/', approve_article, name='approve_article'),
    path('article/<int:article_id>/', article_detail, name='article_detail'),
    path('category/<slug:slug>/', home, name='category_articles'),
]
