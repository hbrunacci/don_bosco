# Generated by Django 2.1 on 2018-08-26 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0007_auto_20180826_1241'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='campaing',
            options={'verbose_name': 'Campaña', 'verbose_name_plural': 'Campañas'},
        ),
        migrations.AlterModelOptions(
            name='pagofacilfile',
            options={'verbose_name': 'Dato Pago Facil', 'verbose_name_plural': 'Datos Pago Facil'},
        ),
        migrations.AlterModelOptions(
            name='salesforcefile',
            options={'verbose_name': 'Dato SalesForce', 'verbose_name_plural': 'Datos SalesForce'},
        ),
    ]
