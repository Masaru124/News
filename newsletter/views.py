from django.shortcuts import render, redirect, get_object_or_404
from .models import Article, Category
from .forms import ArticleForm  

def welcome(request):
      return render(request, 'newsletter/welcome.html')

def home(request, slug=None):
    if slug:
        category = get_object_or_404(Category, slug=slug)
        articles = Article.objects.filter(is_approved=True, category=category)  # Only show approved articles in the category
    else:
        articles = Article.objects.filter(is_approved=True)  # Only show approved articles
    categories = Category.objects.all()
    return render(request, 'newsletter/index.html', {'articles': articles, 'categories': categories})

def submit_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.is_approved = False
            if request.user.is_authenticated:
                article.author = request.user
            article.save()
            return render(request, 'newsletter/success.html', {
                'message': 'Your article has been submitted successfully and is pending approval.'
            })
    else:
        form = ArticleForm()
    return render(request, 'newsletter/submit_article.html', {'form': form})

def render_static_html(request):
    return render(request, 'newsletter/submit_article.html') 

def approve_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.is_approved = True  # Approve the article
    article.save()
    return redirect('admin_article_list')  # Redirect to admin list after approval

def admin_article_list(request):
    if not request.user.is_staff:
        return redirect('home')
    articles = Article.objects.filter(is_approved=False).select_related('category', 'author')
    return render(request, 'newsletter/admin_articles.html', {'articles': articles})

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)  # Retrieve the article by ID
    return render(request, 'newsletter/article_detail.html', {'article': article})  # Render the article detail template
