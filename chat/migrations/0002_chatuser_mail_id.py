# Generated by Django 4.1 on 2022-08-11 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatuser',
            name='mail_id',
            field=models.TextField(default='chat@userExistedBeforeMailId'),
            preserve_default=False,
        ),
    ]
