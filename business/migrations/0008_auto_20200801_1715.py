# Generated by Django 3.0.7 on 2020-08-01 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0007_auto_20200801_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='url_category',
            field=models.URLField(max_length=500, unique=True, verbose_name='Url de la categorie'),
        ),
    ]