# Generated by Django 2.2.5 on 2019-11-12 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20191101_1318'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ('date_created',)},
        ),
    ]
