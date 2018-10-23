from django.db import models
from django.utils import timezone
# Create your models here

class BaseTable(models.Model):

    id = models.AutoField(primary_key=True)
    created_date = models.DateTimeField(
        default=timezone.now)
    update_date = models.DateTimeField(
        default=timezone.now)
    export_date = models.DateTimeField(
        blank=True, null=True)

    class Meta:
        abstract = True

class Sf_Ids(BaseTable):
    sf_partner_id = models.CharField(max_length=100, null=False)
    partner_id = models.CharField(max_length=10, null=False)

    class Admin:
        list_display = ('sf_partner_id', 'partner_id')
        list_filter = ('sf_partner_id', 'partner_id')
        ordering = ('-partner_id',)
        search_fields = ('partner_id',)

    class Meta:
        verbose_name = 'Socio Salesforce'
        verbose_name_plural = 'Socios Salesforce'


class Campaing(BaseTable):
    campaing_id = models.CharField(
        max_length=10,default='')
    campaing_code = models.CharField(
        max_length=50, default='')

    class Meta:
        verbose_name = 'Campaña'
        verbose_name_plural = 'Campañas'


class SalesforceFile(BaseTable):

    partner_id = models.IntegerField()
    contact_id = models.CharField(max_length=200)
    bank = models.CharField(
           max_length=20, default='')
    source = models.CharField(
            max_length=20, default='Otro')
    process = models.CharField(
        max_length=10, default='')
    description = models.CharField(max_length=10)
    state = models.CharField(
        max_length=10, default='completo')
    agreement_date = models.DateTimeField(
            default=timezone.now)
    agreement_end_date = models.DateTimeField(
            default=timezone.now)
    first_payment_date = models.DateTimeField(
            default=timezone.now)
    payment_method = models.CharField(max_length=200)
    frequency = models.CharField(max_length=200, default='Esporadica')
    currency = models.CharField(
            max_length=200, default='Pesos Argentinos')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    agreement_type = models.CharField(max_length=200)
    use_loyalty_card = models.BooleanField()
    campaign_code = models.CharField(max_length=50, default='')
    terminal_id = models.CharField(max_length=10,default='')
    order_nro = models.CharField(max_length=10, default='')
    identificated = models.BooleanField()

    class Meta:
        verbose_name = 'Dato SalesForce'
        verbose_name_plural = 'Datos SalesForce'

    def export(self):
        self.export_date = timezone.now()
        self.save()

    def __str__(self):
        return self.description



class PagofacilFile(BaseTable):

    file_line = models.IntegerField(default=0)
    file_name = models.CharField(max_length=100,default='')
    data = models.CharField(max_length=128, default='')

    class Meta:
        verbose_name = 'Dato Pago Facil'
        verbose_name_plural = 'Datos Pago Facil'
