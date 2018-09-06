from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib import messages
import csv
from django.shortcuts import render
from django.http import HttpResponse
from .resources import Sf_Resource
from .forms import SalesforceFileForm # El formulario que creaste

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

        if process_file(csv_file):
            return HttpResponseRedirect(reverse("importer:upload_csv"))
            pass

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request,"Unable to upload file. "+repr(e))

    return HttpResponseRedirect(reverse("importer:upload_csv"))


def export(request):
    person_resource = Sf_Resource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="persons.csv"'
    return response


def exportar_csv(request):
    form = SalesforceFileForm()
    if request.method == 'POST':
        form = SalesforceFileForm(request.POST)
        if form.is_valid():
            # Obtener los objetos que deseas exportar e iterar
            # filtrado por los campos del formulario
            range = form.cleaned_data.get('date_range_with_format')
            objetos = SalesforceFile.objects.filter(
                agreement_date__range=range)
            objects_total = objetos.count()
            filename = 'SF_%s_%s (%i).csv' %(range[0], range[1], objects_total)


            # Crear el objeto HttpResponse con sus cabeceras
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=' + filename

            # Se usa el response como un "archivo" destino
            writer = csv.writer(response, delimiter=';')
            # encabezado del archivo
            row = ['Donante;Banco;Canal de Ingreso; Tratamiento; CBU; Descripción; Estado; Fecha de compromiso; Fecha'
                   ' de fin de compromiso; Fecha para realizar primer  cobranza; Forma de Pago; Frecuencia; Moneda; M'
                   'onto en pesos;Monto en otra moneda; Número de Sobre; Tipo de compromiso; Donó tarjeta donante; '
                   'Campaña']
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
                writer.writerow(row)
            return response
    return render(request, 'Importer/export.html', {'form': form})

# Create your views here.
