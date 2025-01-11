from django import forms
from .models import Article, Comment, Category

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article  # Specify the model to use
        fields = ['title', 'slug', 'content', 'category', 'featured_image']  # Fields to include in the form
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),  # Textarea for content
            'title': forms.TextInput(attrs={'class': 'form-control'}),  # Input for title
            'slug': forms.TextInput(attrs={'class': 'form-control'}),  # Input for slug
            'category': forms.Select(attrs={'class': 'form-control'}),  # Dropdown for category
        }

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()  # Set queryset for category field

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # Specify the model to use
        fields = ['content']  # Fields to include in the form
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),  # Textarea for comment content
        }
