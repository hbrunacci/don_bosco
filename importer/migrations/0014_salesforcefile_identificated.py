# Generated by Django 2.1 on 2018-09-26 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0013_auto_20180827_0700'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesforcefile',
            name='identificated',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
