# Generated by Django 3.2.9 on 2021-11-18 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('introduce', '0003_alter_member_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='pic',
            field=models.URLField(blank=True, max_length=100, null=True),
        ),
    ]