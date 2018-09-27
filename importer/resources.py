from import_export import resources
from .models import *

class Sf_Resource(resources.ModelResource):
    class Meta:
        model = SalesforceFile


class Pf_Resource(resources.ModelResource):
    class Meta:
        model = PagofacilFile


class Sf_ids_Resource(resources.ModelResource):

    class Meta:
        model = Sf_Ids
        fields = ('sf_partner_id', 'partner_id')
        import_id_fields = ['partner_id']

    def before_export(self, queryset, *args, **kwargs):
        new_qs = queryset.filter(partner_id='-1')
        queryset = new_qs




class Campaing_Resourse(resources.ModelResource):
    class Meta:
        model = Campaing
        fields = ('campaing_id', 'campaing_code',)
        import_id_fields = ['campaing_id']

    def before_save_instance(self, instance, using_transactions, dry_run):
        if instance.campaing_code == '':
            self.skip_row(instance)
        if instance.campaing_id == '':
            self.skip_row(instance)
