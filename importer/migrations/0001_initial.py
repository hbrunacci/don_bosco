# Generated by Django 2.1 on 2018-08-23 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Salesforce_file',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner_id', models.IntegerField()),
                ('contact_id', models.CharField(max_length=200)),
                ('bank', models.CharField(default='', max_length=20)),
                ('source', models.CharField(default='Otro', max_length=20)),
                ('Tratamiento', models.CharField(default='', max_length=10)),
                ('description', models.CharField(max_length=10)),
                ('state', models.CharField(default='completo', max_length=10)),
                ('agreement_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('agreement_end_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('first_payment_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('payment_method', models.CharField(max_length=200)),
                ('frecuency', models.CharField(default='Esporadica', max_length=200)),
                ('currency', models.CharField(default='Pesos Argentinos', max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('agreement_type', models.CharField(max_length=200)),
                ('use_loyalty_card', models.BooleanField()),
                ('campaign', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('export_date', models.DateTimeField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
