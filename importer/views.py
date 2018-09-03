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
            objetos = SalesforceFile.objects.filter(
                agreement_date=form.cleaned_data.get('agreement_date'),
            )

            # Crear el objeto HttpResponse con sus cabeceras
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="SaleForce.csv"'

            # Se usa el response como un "archivo" destino
            writer = csv.writer(response)

            for objeto in objetos:
                row = [
                    objeto.agreement_date,
                    objeto.order_nro,
                    objeto.partner_id,
                ]
                writer.writerow(row)
            return response
    return render(request, 'Importer/export.html', {'form': form})

# Create your views here.
