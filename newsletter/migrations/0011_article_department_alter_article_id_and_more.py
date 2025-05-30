# Generated by Django 5.1.5 on 2025-03-07 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0010_article_likes_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='department',
            field=models.CharField(choices=[('general', 'General'), ('cse', 'CSE'), ('aiml', 'AIML'), ('cs-ds', 'CS-DS')], default='general', max_length=50),
        ),
        migrations.AlterField(
            model_name='article',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
