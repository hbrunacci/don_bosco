# Generated by Django 2.1 on 2018-08-27 06:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('importer', '0011_auto_20180826_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sf_Ids',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('update_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('export_date', models.DateTimeField(blank=True, null=True)),
                ('sf_partner_id', models.CharField(max_length=100)),
                ('partner_id', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name_plural': 'Socios Salesforce',
                'verbose_name': 'Socio Salesforce',
            },
        ),
    ]
