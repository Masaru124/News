from django.db import models
from django.contrib.auth.models import User

User.add_to_class('bio', models.TextField(blank=True, null=True))
