# Generated by Django 2.2.5 on 2019-09-12 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cma',
            field=models.BigIntegerField(),
        ),
    ]
