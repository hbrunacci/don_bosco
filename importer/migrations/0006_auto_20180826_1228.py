# Generated by Django 2.1 on 2018-08-26 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0005_auto_20180826_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesforcefile',
            name='campaign_code',
            field=models.CharField(default='', max_length=50),
        ),
    ]
