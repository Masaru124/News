from django.db import models
from django.contrib.auth.models import User

# Extend the User model to include a bio field
User.add_to_class('bio', models.TextField(blank=True, null=True))
