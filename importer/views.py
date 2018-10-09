from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib import messages
import json
import csv
from django.shortcuts import render
from django.http import HttpResponse
from .resources import Sf_Resource
from .forms import SalesforceFileForm, UnidentifiedForm # El formulario que creaste

from .function import *

import logging


def base(request):
    data = {}
    if "GET" == request.method:
        return render(request, "Importer/base.html", data)


def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "Importer/import.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        response = process_file(csv_file)
        if response:
            messages.add_message(request, messages.INFO, 'Archivo procesado correctamente')
            return HttpResponseRedirect(reverse("importer:upload_csv"))
        else:
            messages.add_message(request, messages.INFO, 'Algunos donantes no pudieron se identificados, '
                                                         'Se deben colocar en la pestaña de identificación')
            return HttpResponseRedirect(reverse("importer:upload_csv"))

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"No se pudo procesar el archivo "+repr(e))
        return HttpResponseRedirect(reverse("importer:upload_csv"))

def check_sf_code(sf_id):
    if len(sf_id) == 15:
        if sf_id[0:5] == '00361':
            return True
    return False


def identificar(request):

    unidentified = Sf_Ids.objects.filter(sf_partner_id__in=[0, -1]).order_by('sf_partner_id', 'partner_id')
    if request.method == 'POST':
        for sf_id in request.POST:
            if sf_id != 'csrfmiddlewaretoken':
                if request.POST[sf_id]:
                    updated_sf_id = Sf_Ids.objects.get(id=sf_id)
                    if check_sf_code(request.POST[sf_id]):
                        updated_sf_id.sf_partner_id = request.POST[sf_id]
                        updated_sf_id.save()
                    else:
                        messages.add_message(request, messages.INFO,
                                             'El dato ingresado para %s no corresponde con un codigo '
                                             'Salesforce valido' % updated_sf_id.partner_id)

                    #print(updated_sf_id)
    else:
        form = UnidentifiedForm()
    return render(request, 'Importer/identificar.html', {'unidentified': unidentified})

def exportar_csv(request):
    form = SalesforceFileForm()
    if request.method == 'POST':
        form = SalesforceFileForm(request.POST)
        if form.is_valid():
            # Obtener los objetos que deseas exportar e iterar
            # filtrado por los campos del formulario
            range = form.cleaned_data.get('date_range_with_format')
            exporteds = form.cleaned_data.get('is_exported')
            for_update = SalesforceFile.objects.filter(contact_id__in=[0, -1])
            if for_update:
                for item in for_update:
                    try:
                        sf_id = Sf_Ids.objects.get(partner_id=item.partner_id)
                        if check_sf_code(sf_id.sf_partner_id):
                            item.contact_id = sf_id.sf_partner_id
                            item.save()
                        else:
                            item.contact_id = -1
                            item.save()
                            if not sf_id.sf_partner_id in ['-1','0']:
                                messages.add_message(request, messages.INFO,
                                                     'El dato ingresado para %s no corresponde con un codigo '
                                                     'Salesforce valido' % sf_id.partner_id)

                    except Exception as e:
                        pass
            if exporteds:
                objetos = SalesforceFile.objects.filter(agreement_date__range=range).exclude(contact_id__in=[0, -1])
            else:
                objetos = SalesforceFile.objects.filter(agreement_date__range=range, export_date__isnull=True)\
                    .exclude(contact_id__in=[0, -1])

            objects_total = objetos.count()
            filename = 'SF_%s_%s (%i).csv' %(range[0], range[1], objects_total)
            csv.register_dialect("dbosco", delimiter=",")

            # Crear el objeto HttpResponse con sus cabeceras
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=' + filename

            # Se usa el response como un "archivo" destino
            writer = csv.writer(response, dialect="dbosco")
            # encabezado del archivo
            header = ('Donante', 'Banco', 'Canal de Ingreso', 'Tratamiento', 'CBU', 'Descripción', 'Estado',
                      'Fecha de compromiso', 'Fecha de fin de compromiso', 'Fecha para realizar primer  cobranza',
                      'Forma de Pago', 'Frecuencia', 'Moneda','Monto en pesos', 'Monto en otra moneda',
                      'Número de Sobre', 'Tipo de compromiso', 'Donó tarjeta donante', 'Campaña')
            row = header
            writer.writerow(row)
            for objeto in objetos:
                row = [
                    objeto.contact_id,  # Donante
                    objeto.bank,   # Banco
                    objeto.source,   # Canal de Ingreso
                    objeto.process,   # Tratamiento
                    '',   # CBU
                    '', #Descirpcion
                    objeto.state,   # Estado
                    objeto.agreement_date.strftime("%d/%m/%Y"),   # Fecha de compromiso
                    objeto.agreement_end_date.strftime("%d/%m/%Y"),   # Fecha de fin de compromiso
                    objeto.first_payment_date.strftime("%d/%m/%Y"),   # Fecha para realizar primer cobranza
                    objeto.description,  # Descripción Forma de Pago
                    # objeto.payment_method,   # Forma de Pago
                    objeto.frequency,   # Frecuencia
                    objeto.currency,   # Moneda
                    objeto.amount,   # Monto en pesos
                    '',   # Monto en otra moneda
                    int(objeto.id) + 20000,  # Número de Sobre
                    objeto.agreement_type,   # Tipo de compromiso
                    objeto.use_loyalty_card,   # Donó tarjeta donante
                    objeto.campaign_code,   # Campaña
                    ]
                objeto.export()
                writer.writerow(row)
            return response
    return render(request, 'Importer/export.html', {'form': form})

# Create your views here.
