from django import forms
from .models import Article, Comment, Category, User  # Import User model

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User  # Specify the User model to use
        fields = ['bio']  # Only include the bio field

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article  # Specify the model to use
        fields = ['title', 'content', 'category', 'departments']  # Include the new department field

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # Specify the model to use
        fields = ['content']  # Fields for the comment form
