from django.test import TestCase
from .models import Article

class ArticleModelTest(TestCase):

    def test_string_representation(self):
        article = Article(title="Sample Article")
        self.assertEqual(str(article), article.title)