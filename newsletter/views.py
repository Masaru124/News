from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden  
from .models import Article, Category, Comment
from .forms import ArticleForm  
from django.contrib.auth.models import User  # Import User model

def welcome(request):
    # Render the welcome page
    return render(request, 'newsletter/welcome.html')

def home(request, slug=None):
    # Render the home page with articles
    if slug:
        category = get_object_or_404(Category, slug=slug)
        articles = Article.objects.filter(is_approved=True, category=category)  # Only show approved articles in the category
    else:
        articles = Article.objects.filter(is_approved=True)  # Only show approved articles
    categories = Category.objects.all()  # Get all categories
    return render(request, 'newsletter/index.html', {'articles': articles, 'categories': categories})

def submit_article(request):
    # Handle article submission
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.is_approved = False  # Set article as not approved
            
            # Check if the article is new or old
            if request.user.is_authenticated:
                article.author = request.user  # Set the author to the logged-in user
            else:
                # If the article is old and has no author, set it to admin
                if not article.author_id:  # Assuming author_id is None for old articles
                    admin_user = User.objects.get(username='admin')  # Fetch the admin user
                    article.author = admin_user
            
            article.save()  # Save the article
            return render(request, 'newsletter/success.html', {
                'message': 'Your article has been submitted successfully and is pending approval.'
            })
    else:
        form = ArticleForm()  # Create a new article form
    return render(request, 'newsletter/submit_article.html', {'form': form})

def render_static_html(request):
    # Render a static HTML page
    return render(request, 'newsletter/submit_article.html') 

def approve_article(request, article_id):
    # Approve an article
    article = get_object_or_404(Article, id=article_id)
    article.is_approved = True  # Approve the article
    article.save()  # Save the changes
    return redirect('admin_article_list')  # Redirect to admin list after approval

def admin_article_list(request):
    # Render the admin article list
    if not request.user.is_staff:
        return redirect('home')  # Redirect to home if not staff
    articles = Article.objects.filter(is_approved=False).select_related('category', 'author')  # Get unapproved articles
    return render(request, 'newsletter/admin_articles.html', {'articles': articles})

def article_detail(request, article_id):
    # Render the article detail page
    article = get_object_or_404(Article, id=article_id)  # Retrieve the article by ID
    return render(request, 'newsletter/article_detail.html', {'article': article})  # Render the article detail template

def submit_comment(request, article_id):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to submit a comment.")

    article = get_object_or_404(Article, id=article_id)  # Get the article by ID
    if request.method == 'POST':
        content = request.POST.get('content')  # Get the comment content from the form
        comment = Comment(article=article, author=request.user, content=content)  # Create a new comment
        comment.save()  # Save the comment
        return redirect('article_detail', article_id=article.id)  # Redirect back to the article detail page

def like_article(request, article_id):
    # Handle the like action for an article
    article = get_object_or_404(Article, id=article_id)  # Retrieve the article by ID
    article.likes_count += 1  # Increment the likes count
    article.save()  # Save the changes
    return redirect('article_detail', article_id=article.id)  # Redirect back to the article detail page
