# Generated by Django 2.1 on 2019-04-12 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0018_auto_20190412_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaing',
            name='valid_from',
            field=models.DateField(default='01-01-2019', verbose_name='Valida desde'),
        ),
        migrations.AlterField(
            model_name='campaing',
            name='valid_to',
            field=models.DateField(default='01-01-2019', verbose_name='Valida hasta'),
        ),
    ]
