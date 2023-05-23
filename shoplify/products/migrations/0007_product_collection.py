# Generated by Django 4.1.6 on 2023-02-10 10:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_collection'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_collection', to='products.collection'),
        ),
    ]