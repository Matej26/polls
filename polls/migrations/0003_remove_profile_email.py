# Generated by Django 3.2.3 on 2021-05-23 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_rename_author_question_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
    ]
