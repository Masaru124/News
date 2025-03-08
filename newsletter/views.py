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

def home(request):
    department = request.GET.get('department')
    search_query = request.GET.get('search')
    selected_category_slug = request.GET.get('category_slug')  # Added category slug filter
    
    logger.info(f"GET request to home page with department: {department}, search: {search_query}, category: {selected_category_slug}")

    # Start with all approved articles
    articles = Article.objects.filter(is_approved=True)

    # Apply department filter if selected
    if department:
        articles = articles.filter(department=department)

    # Apply category filter if selected
    if selected_category_slug:
        category = get_object_or_404(Category, slug=selected_category_slug)
        articles = articles.filter(category=category)

    # Apply search filter
    if search_query:
        articles = articles.filter(title__icontains=search_query) | articles.filter(content__icontains=search_query)

    # Get all categories for the dropdown in the template
    categories = Category.objects.all()

    # Render the home page with the filtered articles and categories
    return render(request, 'newsletter/index.html', {
        'articles': articles,
        'categories': categories,
        'selected_department': department,
        'selected_category': selected_category_slug,
    })

def submit_article(request):
    logger.info(f"Request to submit article: {request.method}")
    
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.is_approved = False  # Article is not approved initially
            
            # Assign the current user as the article author if authenticated
            if request.user.is_authenticated:
                article.author = request.user
            else:
                # If not authenticated, assign an admin user as the author
                admin_user = User.objects.get(username='admin')
                article.author = admin_user
            
            article.save()  # Save the article to the database
            logger.info(f"Article submitted: {article.title}")

            # Display success message
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
    article.is_approved = True  # Approve the article
    article.save()
    return redirect('admin_article_list')

def admin_article_list(request):
    logger.info(f"GET request to admin article list")
    
    # Only allow staff users to access this view
    if not request.user.is_staff:
        return redirect('home')
    
    # Fetch all unapproved articles
    articles = Article.objects.filter(is_approved=False).select_related('category', 'author')
    return render(request, 'newsletter/admin_articles.html', {'articles': articles})

def article_detail(request, article_id):
    logger.info(f"GET request for article detail with ID: {article_id}")
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'newsletter/article_detail.html', {'article': article})

def submit_comment(request, article_id):
    logger.info(f"Request to submit comment for article ID: {article_id}")

    # Ensure the user is logged in before allowing comment submission
    if not request.user.is_authenticated:
        return HttpResponseForbidden("You must be logged in to submit a comment.")

    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        
        # Create and save the comment
        comment = Comment(article=article, author=request.user, content=content)
        comment.save()
        logger.info(f"Comment submitted for article ID: {article_id}")
        
        return redirect('article_detail', article_id=article.id)

def like_article(request, article_id):
    logger.info(f"Request to like article with ID: {article_id}")
    article = get_object_or_404(Article, id=article_id)
    
    # Increment the likes count
    article.likes_count += 1
    article.save()
    
    return redirect('article_detail', article_id=article.id)

# Optional: Add more views if needed (e.g., for pagination, article approval, etc.)
