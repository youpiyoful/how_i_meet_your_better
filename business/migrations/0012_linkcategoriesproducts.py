# Generated by Django 3.0.7 on 2020-08-05 02:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0011_auto_20200804_2135'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkCategoriesProducts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hyerarchie_score', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.Category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.Product')),
            ],
        ),
    ]