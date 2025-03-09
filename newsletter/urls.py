from django.urls import path
from .views import article_detail, delete_comment, submit_comment, like_article, home,submit_article, home, approve_article, admin_article_list, render_static_html, article_detail, welcome, submit_comment, like_article
urlpatterns = [ 
    path('', welcome, name='welcome'),  # Welcome page
    path('index/', home, name='index'),  # Home page with articles
    path('submit/', submit_article, name='submit_article'),  # Submit article page
    path('article/<int:article_id>/', article_detail, name='article_detail'),  # Article detail page
    path('article/<int:article_id>/approve/', approve_article, name='approve_article'),  # Approve article
    path('article/<int:article_id>/like/', like_article, name='like_article'),  # Like article
    path('admin/articles/', admin_article_list, name='admin_article_list'),  # Admin article list
    path('submit_comment/<int:article_id>/', submit_comment, name='submit_comment'),  # Submit comment for an article
    path('article/<int:article_id>/', article_detail, name='article_detail'),
    path('article/comment/delete/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('article/comment/submit/<int:article_id>/', submit_comment, name='submit_comment'),
    path('article/like/<int:article_id>/', like_article, name='like_article'),
]
