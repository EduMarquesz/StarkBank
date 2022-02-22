import starkbank
import schedule
from time import sleep
from datetime import date, datetime, timedelta
from faker import Faker

private_key_content = """
Sua Private Key

"""

project = starkbank.Project(
environment="sandbox",
id="5515337999056896",
private_key=private_key_content,)

organization = starkbank.Organization(
environment="sandbox",
id="5631986051842048",
private_key=private_key_content,
workspace_id=None)

balance = starkbank.balance.get(user=project)

starkbank.user = project  # or organization

balance = starkbank.balance.get()

starkbank.language = "pt-BR"

def generate_random_invoice_data():
    faker = Faker()
    factory = Faker('pt_BR')
    data = {
        'tax_id':factory.cpf(),
        'name':factory.name(),
        'amount':faker.random_int(1000, 9000),
        'due':datetime.utcnow() + timedelta(hours=1),
        'expiration':timedelta(hours=2).total_seconds(),
        'tags':["immediate"],
        }
    return data


def generate_random_invoice(invoice_quantity):
    random_invoice_list = []
    for i in range(0,invoice_quantity):
        random_data = generate_random_invoice_data()
        invoice = starkbank.Invoice(**random_data)
        random_invoice_list.append(invoice)

    return random_invoice_list

def get_invoices():
    invoice_list = generate_random_invoice(12)
    return invoice_list


def send_invoices(invoices_list):
    "Envia a invoice"
    invoices = starkbank.invoice.create(invoices_list)
    for invoice in invoices_list:
        print(f"Invoice enviado para sandbox TaxId: {invoice.tax_id} | Amount: {invoice.amount}")

    return [invoice.id for invoice in invoices]
def query_invoices(start_date,end_date,invoices_ids,status):

    invoices = starkbank.invoice.query(
    after=start_date,
    before=end_date,
    ids=invoices_ids,
    status = status)

    return invoices

def verify_invoice(invoice):
    "Verifica se a invoice é valida para transferencia"
    status = invoice.status

    if status == "paid":
        return True
    else:
        return False


def send_transfer(bank_code,branch_code,account_number,tax_id,name,amount):
    
    """Envia uma transferencia"""
    for transfer_template in get_invoices():
        try:
            transfer_template = [
            starkbank.Transfer(
            amount=amount,
            bank_code=bank_code,
            branch_code=branch_code,
            account_number=account_number,
            tax_id=tax_id,
            name=name,
            tags=["payment"]
            )]
            transfer = starkbank.transfer.create(transfer_template)
            return True
        except Exception as q:
            print(q)
            return False

def get_bank_account_infos():
    """Pega as informações bancarias de amostra"""
    bank_code="20018183"
    branch_code="0001"
    account_number="6341320293482496"
    tax_id="20.018.183/0001-80"
    name="Stark Bank S.A."
    return {
            'bank_code':bank_code,
            'branch_code':branch_code,
            'account_number':account_number,
            'tax_id':tax_id,
            'name':name}

def send_local_invoices():
    """Envia as invoices criadas para sandbox"""
    local_invoices = get_invoices()

    print('enviando invoices')
    invoices_ids = send_invoices(local_invoices)
    return invoices_ids



def schedule_invoices():
    """Cria invoices a cada 3 horas"""

    schedule.every(3).hours.do(send_local_invoices)
    start_date = datetime.today()
    start_date = start_date - timedelta(days = 1)
    start_date = start_date.date()
    start_day = start_date.day
    while True:
        run = schedule.run_pending()

        current_day = datetime.today().day
        if start_day != current_day:
            send_transfer_by_filters(start_date = start_date,end_date = datetime.today().date(),invoices_ids = None,status = 'paid')

        sleep(timedelta(hours=1).seconds)



def send_transfer_by_filters(start_date,end_date,status,invoices_ids = None):

    query_invoices_ = query_invoices(start_date = start_date,end_date = end_date,invoices_ids = invoices_ids, status = status)
    bank_account_info = get_bank_account_infos()

    for invoice in query_invoices_:
        id_ = invoice.id
        status = invoice.status
        amount = invoice.amount
        fee = invoice.fee

        bank_account_info['amount'] = amount

        verify = verify_invoice(invoice)
    
        if verify:
            transfer_status = send_transfer(**bank_account_info)
            print(f"Status feita com sucesso:{transfer_status} | invoiceID:{id_}")
        else:
            print(f"Status invalido | {status} | invoiceID : {id_}")

if __name__ == '__main__':

    #schedule_invoices()

    t = schedule_invoices()
