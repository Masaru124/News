from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    # Represents a category for articles
    name = models.CharField(max_length=100)  # Name of the category
    slug = models.SlugField(unique=True)  # Unique slug for the category
    description = models.TextField(blank=True)  # Optional description of the category
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the category was created

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"  # Plural name for the admin interface


class Article(models.Model):
    # Represents a news article
    title = models.CharField(max_length=200)  # Title of the article
    department = models.CharField(
        max_length=50,
        choices=[
            ('general', 'General'),
            ('cse', 'CSE'),
            ('aiml', 'AIML'),
            ('cs-ds', 'CS-DS'),
        ],
        default='general',
    )  # Department of the article
    departments = models.CharField(
        max_length=50,
        choices=[
            ('general', 'General'),
            ('cse', 'CSE'),
            ('aiml', 'AIML'),
            ('cs-ds', 'CS-DS'),
        ],
        default='general',
    )  # New departments field
    slug = models.SlugField(unique=True, null=True, blank=True)  # Unique slug for the article
    content = models.TextField()  # Content of the article
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the article was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the article was last updated
    is_approved = models.BooleanField(default=False)  # Approval status of the article
    is_published = models.BooleanField(default=False)  # Publication status of the article
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', default=1)  # Author of the article
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')  # Category of the article
    views_count = models.IntegerField(default=0)  # Number of views for the article
    likes_count = models.IntegerField(default=0)  # Number of likes for the article
    featured_image = models.ImageField(upload_to='articles/', null=True, blank=True)  # Optional featured image

    def save(self, *args, **kwargs):
        # Override save method to create a unique slug
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            num = 1
            while Article.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']  # Order articles by creation date


class Comment(models.Model):
    # Represents a comment on an article
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')  # Article the comment belongs to
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  # Author of the comment
    content = models.TextField()  # Content of the comment
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the comment was created
    is_approved = models.BooleanField(default=True)  # Approval status of the comment
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')  # Parent comment for threaded replies

    def __str__(self):
        return f'Comment by {self.author.username} on {self.article.title}'

    class Meta:
        ordering = ['created_at']  # Order comments by creation date
