import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden  
from .models import Article, Category, Comment
from .forms import ArticleForm  
from django.contrib.auth.models import User  # Import User model

# Configure logging
logger = logging.getLogger(__name__)

def welcome(request):
    logger.info(f"GET request to welcome page")
    return render(request, 'newsletter/welcome.html')

def home(request, slug=None):
    logger.info(f"GET request to home page with slug: {slug}")
    if slug:
        category = get_object_or_404(Category, slug=slug)
        articles = Article.objects.filter(is_approved=True, category=category)
    else:
        articles = Article.objects.filter(is_approved=True)
    categories = Category.objects.all()
    return render(request, 'newsletter/index.html', {'articles': articles, 'categories': categories})

def submit_article(request):
    logger.info(f"Request to submit article: {request.method}")
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.is_approved = False
            
            if request.user.is_authenticated:
                article.author = request.user
            else:
                if not article.author_id:
                    admin_user = User.objects.get(username='admin')
                    article.author = admin_user
            
            article.save()
            logger.info(f"Article submitted: {article.title}")
            return render(request, 'newsletter/success.html', {
                'message': 'Your article has been submitted successfully and is pending approval.'
            })
    else:
        form = ArticleForm()
    return render(request, 'newsletter/submit_article.html', {'form': form})

def render_static_html(request):
    logger.info(f"GET request to render static HTML")
    return render(request, 'newsletter/submit_article.html') 

def approve_article(request, article_id):
    logger.info(f"Request to approve article with ID: {article_id}")
    article = get_object_or_404(Article, id=article_id)
    article.is_approved = True
    article.save()
    return redirect('admin_article_list')

def admin_article_list(request):
    logger.info(f"GET request to admin article list")
    if not request.user.is_staff:
        return redirect('home')
    articles = Article.objects.filter(is_approved=False).select_related('category', 'author')
    return render(request, 'newsletter/admin_articles.html', {'articles': articles})

def article_detail(request, article_id):
    logger.info(f"GET request for article detail with ID: {article_id}")
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'newsletter/article_detail.html', {'article': article})

def submit_comment(request, article_id):
    logger.info(f"Request to submit comment for article ID: {article_id}")
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to submit a comment.")

    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        comment = Comment(article=article, author=request.user, content=content)
        comment.save()
        logger.info(f"Comment submitted for article ID: {article_id}")
        return redirect('article_detail', article_id=article.id)

def like_article(request, article_id):
    logger.info(f"Request to like article with ID: {article_id}")
    article = get_object_or_404(Article, id=article_id)
    article.likes_count += 1
    article.save()
    return redirect('article_detail', article_id=article.id)
