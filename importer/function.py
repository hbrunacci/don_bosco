from .models import SalesforceFile
from .models import Sf_Ids
from datetime import datetime

def process_file(csv_file):
    file_data = csv_file.read().decode("utf-8")

    lines = file_data.split("\r\n")
    # loop over the lines and save them in db. If error , store as string and then display
    line_count = len(lines)
    line_pos = 1
    for line in lines:
        if len(line) > 0:
            if line[0] == '1':
                # datos de encabezado
                description = line[9:22]

            if line[0] == '8':
                # datos de resumen del batch
                pass
            if line[0] == '9':
                # datos de resumen del archivo
                pass
            if line[0] == '5':
                #datos de cobro
                terminal_id = get_terminal_id(line)
                order_nro = get_order_nro(line)
                new_item = SalesforceFile.objects.filter(terminal_id=terminal_id, order_nro=order_nro).first()
                if not new_item:
                    new_item = SalesforceFile()
                new_item.order_nro = order_nro
                new_item.terminal_id = terminal_id
                new_item.description = description
                new_item.partner_id = get_partner_id(line)
                new_item.partner_nro = get_partner_nro(line)
                new_item.agreement_date = get_agreement_date(line)
                new_item.agreement_end_date = get_agreement_end_date(line)
                new_item.agreement_type =get_agreement_type(line)
                new_item.amount = get_amount(line)
                new_item.bank = get_bank(line)
                new_item.contact_id = get_contact_id(line)
                new_item.first_payment_date = get_first_payment_date(line)
                new_item.currency = get_currency(line)
                new_item.payment_method = get_payment_method(line)
                new_item.frequency = get_frequency(line)
                new_item.source = get_source(line)
                new_item.process = get_process(line)
                new_item.state = get_state(line)
                new_item.use_loyalty_card = get_use_loyalty_card(line)
                new_item.campaign_code = get_campaign_code(line)
                if int(line[1:6]) > 65:
                    print(line[1:6])
            if line[0] == '6':
                #datos de codigo de barras
                pass
            if line[0] == '7':
                #resumen de cobro cliente
                new_item.save()
            line_pos += 1

    return True


def get_description(line):
    return ''


def get_terminal_id(line):
    data = line[58:64]
    return data


def get_order_nro(line):
    data = line[76:80]
    return data


def get_campaign_code(line):
    data = line[24:27]
    return data


def get_partner_id(line):
    data = line[27:45]
    return data


def get_partner_nro(line):
    data = line[27:45]
    return data


def get_contact_id(line):
    partner_nro = int(get_partner_nro(line))
    SF_contac = Sf_Ids.objects.get(partner_id=partner_nro)
    return SF_contac.sf_partner_id


def get_agreement_date(line):
    date = datetime.strptime(line[16:24], '%Y%m%d').date()
    return date


def get_agreement_end_date(line):
    date = datetime.strptime(line[16:24], '%Y%m%d').date()
    return date


def get_agreement_type(line):
    return 'Eventual'


def get_amount(line):
    amount = line[48:58]
    amount = float(amount)/100
    return amount


def get_bank(line):
    return ''


def get_first_payment_date(line):
    date = datetime.strptime(line[16:24], '%Y%m%d').date()
    return date


def get_payment_method(line):
    return 'Efectivo'


def get_currency(line):
    if line[45:48] == 'PES':
        data = 'Pesos'
    else:
        data = 'Otra'
    return data


def get_frequency(line):
    return 'Esporadica'


def get_source(line):
    return 'Otro'


def get_process(line):
    return ''


def get_state(line):
    return 'Completo'


def get_use_loyalty_card(line):
    return True
