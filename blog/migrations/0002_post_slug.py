# Generated by Django 4.1.7 on 2023-03-02 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.CharField(default='', max_length=130),
            preserve_default=False,
        ),
    ]
