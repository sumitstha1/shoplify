# Generated by Django 4.1.6 on 2023-02-11 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_wishlistitems_wish'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='profile',
            new_name='user',
        ),
    ]
