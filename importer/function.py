from .models import SalesforceFile
from .models import Sf_Ids, Campaing
from datetime import datetime


def process_file(csv_file):
    file_data = csv_file.read().decode("utf-8")
    lines = file_data.split("\r\n")
    if lines[0][9:22].strip() == 'PAGO FACIL':
        error = process_data(lines, 'PF')
    if lines[0][8:22].strip() == 'COBRO EXPRESS':
        error = process_data(lines, 'CE')
    if lines[0][0:8].strip() == '04003345':
        error = process_data(lines, 'PMC')
    if error:
        return False
    else:
        return True


def process_data(lines, file_type):
    # loop over the lines and save them in db. If error , store as string and then display
    line_pos = 1
    description = ''
    error = False
    for line in lines:
        if len(line) > 0:
            print(line_pos)
            if line_pos == 1:
                # datos de encabezado
                description = str(get_description(line, file_type))

            if line[0] == '8':
                # datos de resumen del batch
                pass
            if line[0] == '9':
                # datos de resumen del archivo
                pass
            data_block = False
            if file_type == 'PF' and line[0] == '5':
                data_block = True
            if file_type == 'CE' and line[0] == '2':
                data_block = True
            if file_type == 'PMC' and line[0] == '5':
                data_block = True

            if data_block:
                # datos de cobro
                terminal_id = get_terminal_id(line, file_type)
                order_nro = get_order_nro(line, file_type)
                new_item = SalesforceFile.objects.filter(terminal_id=terminal_id, order_nro=order_nro).first()
                if not new_item:
                    new_item = SalesforceFile()
                new_item.order_nro = order_nro
                new_item.terminal_id = terminal_id
                new_item.description = description.strip()
                new_item.partner_id = get_partner_id(line, file_type)
                new_item.partner_nro = get_partner_nro(line, file_type)
                new_item.agreement_date = get_agreement_date(line, file_type)
                new_item.agreement_end_date = get_agreement_end_date(line, file_type)
                new_item.agreement_type = get_agreement_type(line, file_type)
                new_item.amount = get_amount(line, file_type)
                new_item.bank = get_bank(line, file_type)
                new_item.contact_id, new_item.identificated = get_contact_id(line, file_type)
                new_item.first_payment_date = get_first_payment_date(line, file_type)
                new_item.currency = get_currency(line, file_type)
                new_item.payment_method = get_payment_method(line, file_type)
                new_item.frequency = get_frequency(line, file_type)
                new_item.source = get_source(line, file_type)
                new_item.process = get_process(line, file_type)
                new_item.state = get_state(line, file_type)
                new_item.use_loyalty_card = get_use_loyalty_card(line, file_type)
                new_item.campaign_code = get_campaign_code(line, file_type)
                if not new_item.identificated:
                    error = True
                new_item.save()
            line_pos += 1
    return error


def get_description(line, file_type):
    if file_type == 'PF':
        data = 'Pago Fácil'
    if file_type == 'CE':
        data = 'Cobro Express'
    if file_type == 'PMC':
        data = 'Pago Mis Cuentas'
    return data


def get_terminal_id(line, file_type):
    if file_type == 'PF':
        data = int(line[59:64])
    if file_type == 'CE':
        data = int(line[0:7])
    if file_type == 'PMC':
        data = int(line[69:77])
    return data


def get_order_nro(line, file_type):
    if file_type == 'PF':
        data = line[76:80]
    if file_type == 'CE':
        data = int(line[31:41])
    if file_type == 'PMC':
        data = line[77:83]
    return data


def get_campaign_code(line, file_type):
    if file_type == 'PF':
        campaing_nro = int(line[24:27])
    if file_type == 'CE':
        campaing_nro = int(line[27:30])
    if file_type == 'PMC':
        campaing_nro = 0

    pay_date = get_agreement_date(line,file_type)

    if campaing_nro in (0, 50, 20, 500):
        campaing_nro = 245 + pay_date.month + ((2018 - pay_date.year) * 12)
    try:
        sf_campaing = Campaing.objects.get(campaing_id=campaing_nro)
    except:
        return 0
    return sf_campaing.campaing_code


def get_partner_id(line, file_type):
    if file_type == 'PF':
        data = get_partner_nro(line, file_type)
    if file_type == 'CE':
        data = get_partner_nro(line, file_type)
    if file_type == 'PMC':
        data = get_partner_nro(line, file_type)
    return data


def get_partner_nro(line, file_type):
    if file_type == 'PF':
        data = int(line[27:45])
    if file_type == 'CE':
        data = int(line[30:35])
    if file_type == 'PMC':
        data = int(line[1:9])
    return data


def get_contact_id(line, file_type, error={}):
    partner_nro = int(get_partner_nro(line, file_type))
    # TODO: Mejorar usando get_or_created para identificar el socio o crear uno con -1 si no existe
    try:
        SF_contact = Sf_Ids.objects.get(partner_id=partner_nro)
    except:
        new_sf_id = Sf_Ids()
        new_sf_id.partner_id = partner_nro
        new_sf_id.sf_partner_id = -1
        new_sf_id.save()
        return 0, False
    if SF_contact.partner_id == '-1':
        return 0, False
    return SF_contact.sf_partner_id, True


def get_agreement_date(line, file_type):
    if file_type == 'PF':
        date = datetime.strptime(line[16:24], '%Y%m%d').date()
    if file_type == 'CE':
        date = datetime.strptime(line[0:8], '%Y%m%d').date()
    if file_type == 'PMC':
        date = datetime.strptime(line[69:77], '%Y%m%d').date()
    return date


def get_agreement_end_date(line, file_type):
    if file_type == 'PF':
        date = datetime.strptime(line[16:24], '%Y%m%d').date()
    if file_type == 'CE':
        date = datetime.strptime(line[0:8], '%Y%m%d').date()
    if file_type == 'PMC':
        date = datetime.strptime(line[69:77], '%Y%m%d').date()
    return date


def get_amount(line, file_type):
    if file_type == 'PF':
        amount = line[48:58]
    if file_type == 'CE':
        amount = line[14:22]
    if file_type == 'PMC':
        amount = line[58:68]
    amount = float(amount)/100
    return amount


def get_first_payment_date(line, file_type):
    if file_type == 'PF':
        date = datetime.strptime(line[16:24], '%Y%m%d').date()
    if file_type == 'CE':
        date = datetime.strptime(line[0:8], '%Y%m%d').date()
    if file_type == 'PMC':
        date = datetime.strptime(line[69:77], '%Y%m%d').date()
    return date


def get_use_loyalty_card(line, file_type):
    if file_type == 'PF':
        campaing_nro = int(line[24:27])
    if file_type == 'CE':
        campaing_nro = int(line[28:30])
    if file_type == 'PMC':
        campaing_nro = 0
    if campaing_nro in (0, 50, 20, 500):
        return False
    return True


def get_payment_method(line, file_type):
    return 'Efectivo'


def get_bank(line, file_type):
    return ''

def get_currency(line, file_type):
    data = 'Pesos Argentinos'
    return data


def get_frequency(line, file_type):
    return 'Esporádica'


def get_source(line, file_type):
    return 'Otro'


def get_process(line, file_type):
    return ''


def get_state(line, file_type):
    return 'Completo'


def get_agreement_type(line, file_type):
    return 'Eventual'
