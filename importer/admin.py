from import_export.admin import ImportExportModelAdmin
from .resources import *
from django.contrib import admin
from .models import *


#admin.site.register(PagofacilFile)
#admin.site.register(SalesforceFile)


class CampaingAdmin(ImportExportModelAdmin):
    resource_class = Campaing_Resourse
    list_display = ['campaing_id', 'campaing_code', 'valid_from', 'valid_to', 'loyalty_card','description']
    search_fields = ['campaing_code', 'valid_from', 'valid_to']
    list_filter = ['description', 'valid_from', 'valid_to']
    ordering = ('id',)  # The negative sign indicate descendent order


class SF_idsAdmin(ImportExportModelAdmin):
    resource_class = Sf_ids_Resource
    list_display = ['sf_partner_id', 'partner_id']
    search_fields = ['partner_id']


class SFAdmin(ImportExportModelAdmin):
    resource_class = Sf_Resource
    filter_vertical = ()
    list_display = ['campaign_code_old', 'campaign_code', 'campaign_description', 'description']
    date_hierarchy = 'created_date'
    list_filter = ['description', 'campaign_code_old', 'created_date']

admin.site.register(Campaing, CampaingAdmin)
admin.site.register(Sf_Ids, SF_idsAdmin)
admin.site.register(SalesforceFile, SFAdmin)
# Register your models here.
