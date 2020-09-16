# Generated by Django 3.1.1 on 2020-09-16 07:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subreddit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover', models.ImageField(default='default.jpg', upload_to='subreddit_pics')),
                ('avatar', models.ImageField(default='default.jpg', upload_to='subreddit_pics')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subreddit_creator_of', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='subreddit_member_of', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
